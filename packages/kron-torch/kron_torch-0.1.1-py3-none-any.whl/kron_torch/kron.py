import torch
import opt_einsum


def precond_update_prob_schedule(
    max_prob=1.0, min_prob=0.03, decay=0.001, flat_start=200
):
    """Anneal preconditioner update probability during beginning of training.

    PSGD benefits from more preconditioner updates at the beginning of training,
    but once the preconditioner is learned the update probability can drop low.

    This schedule is an exponential anneal with a flat start. Default settings keep
    update probability at 1.0 for 200 steps then exponentially anneal down to
    `min_prob` by 4000 steps. Default settings work very well for most models and
    training regimes.
    """

    def _schedule(n):
        """Exponential anneal with flat start."""
        n = torch.tensor(n, dtype=torch.float32)
        prob = torch.minimum(
            torch.maximum(
                max_prob * torch.exp(-decay * (n - flat_start)), torch.tensor(min_prob)
            ),
            torch.tensor(max_prob),
        )
        return prob.item()

    return _schedule


class Kron(torch.optim.Optimizer):
    def __init__(
        self,
        params,
        lr=0.001,
        b1=0.9,
        weight_decay=0.0,
        preconditioner_update_probability=None,
        max_size_triangular=8192,
        max_skew_triangular=10,
        mu_dtype=None,
        precond_dtype=None,
    ):
        if not 0.0 <= lr:
            raise ValueError(f"Invalid learning rate: {lr}")
        if not 0.0 <= b1 < 1.0:
            raise ValueError(f"Invalid beta parameter: {b1}")
        if not 0.0 <= weight_decay:
            raise ValueError(f"Invalid weight_decay value: {weight_decay}")

        if preconditioner_update_probability is None:
            preconditioner_update_probability = precond_update_prob_schedule()

        defaults = dict(
            lr=lr,
            b1=b1,
            weight_decay=weight_decay,
            preconditioner_update_probability=preconditioner_update_probability,
            max_size_triangular=max_size_triangular,
            max_skew_triangular=max_skew_triangular,
            precond_lr=0.1,  # precond lr hardcoded to 0.1
            mu_dtype=mu_dtype,
            precond_dtype=precond_dtype,
        )
        super(Kron, self).__init__(params, defaults)

        self._params_with_grad = []
        total_params = 0
        for group in self.param_groups:
            for p in group["params"]:
                if p.requires_grad:
                    self._params_with_grad.append(p)
                    total_params += p.numel()

        self._global_clip_norm = total_params**0.5
        self._element_wise_clip = 1.0
        self._tiny = 1e-30
        self._Qs_exprs = None

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            if "step" not in group:
                group["step"] = 0
            group["step"] += 1

            if "momentum_buffer" not in group:
                group["momentum_buffer"] = [
                    torch.zeros_like(
                        p,
                        dtype=(
                            group["mu_dtype"]
                            if group["mu_dtype"] is not None
                            else p.dtype
                        ),
                    )
                    for p in group["params"]
                ]

            for i, (p, m) in enumerate(zip(group["params"], group["momentum_buffer"])):
                if p.grad is None:
                    continue

                g = p.grad.to(dtype=m.dtype)
                m.mul_(group["b1"]).add_(g, alpha=1 - group["b1"])
                bias_correction = 1 - group["b1"] ** group["step"]
                mu_hat = m / bias_correction
                group["momentum_buffer"][i] = mu_hat

            # Update preconditioner (whitening type)
            update_prob = group["preconditioner_update_probability"]
            if callable(update_prob):
                update_prob = update_prob(group["step"])

            if (torch.rand([]) < update_prob) or (self._Qs_exprs is None):
                if self._Qs_exprs is None:
                    self._Qs_exprs = [
                        init_Q_exprs(
                            mu,
                            1.0,  # init scale hardcoded to 1.0
                            group["max_size_triangular"],
                            group["max_skew_triangular"],
                            dtype=(
                                group["precond_dtype"]
                                if group["precond_dtype"] is not None
                                else p.dtype
                            ),
                        )
                        for mu, p in zip(group["momentum_buffer"], group["params"])
                    ]

                for Q_exprs, mu, p in zip(
                    self._Qs_exprs, group["momentum_buffer"], group["params"]
                ):
                    precond_dtype = (
                        group["precond_dtype"]
                        if group["precond_dtype"] is not None
                        else p.dtype
                    )
                    update_precond_kron_math_(
                        *Q_exprs,
                        torch.randn_like(mu, dtype=precond_dtype),
                        mu.to(dtype=precond_dtype),
                        group["precond_lr"],
                        "2nd",  # step_normalizer (fixed to "2nd")
                        self._tiny,
                    )

            # Preconditioned gradients
            pre_grads = [
                precond_grad_kron_math(*Q_exprs, mu)
                for Q_exprs, mu in zip(self._Qs_exprs, group["momentum_buffer"])
            ]

            # Global gradient clipping
            torch.nn.utils.clip_grad_norm_(pre_grads, self._global_clip_norm)

            # Element-wise gradient clipping
            for g in pre_grads:
                g.clamp_(-self._element_wise_clip, self._element_wise_clip)

            # Apply weight decay
            if group["weight_decay"] != 0:
                for p, g in zip(group["params"], pre_grads):
                    if p.dim() >= 2:
                        g.add_(p.to(dtype=g.dtype), alpha=group["weight_decay"])

            # Update parameters
            for param, g in zip(group["params"], pre_grads):
                param.add_(g.to(dtype=param.dtype), alpha=-group["lr"])

        return loss


def norm_lower_bound(A):
    """
    Returns a cheap lower bound for the spectral norm of A.
    Numerical results on random matrices with a wide range of distributions and sizes suggest,
        norm(A) <= sqrt(2) * norm_lower_bound(A)
    Looks to be a very tight lower bound.
    """
    max_abs = torch.max(
        torch.abs(A)
    )  # used to normalize A to avoid numerically under- or over-flow
    if max_abs > 0:
        A = A / max_abs
        aa = torch.real(A * A.conj())
        value0, i = torch.max(torch.sum(aa, dim=0), 0)
        value1, j = torch.max(torch.sum(aa, dim=1), 0)
        if value0 > value1:
            x = A[:, i].conj() @ A
            # We must have norm(x) > 0 since norm(x) >= value0 > value1 >= 0
            # Also, avoid expression norm(x*A^H)/norm(x) as x*A^H could under/over flow
            return max_abs * torch.linalg.vector_norm(
                (x / torch.linalg.vector_norm(x)) @ A.H
            )
        else:
            x = A @ A[j].conj()
            # normx = torch.linalg.vector_norm(x)
            # if normx > 0:
            #     # Again, avoid expression norm(A^H*x)/norm(x) as A^H*x could under/over flow
            #     return max_abs * torch.linalg.vector_norm(A.H @ (x / normx))
            # else:  # A = 0
            #     return normx
            return max_abs * torch.linalg.vector_norm(
                A.H @ (x / torch.linalg.vector_norm(x))
            )
    else:  # must have A=0
        return max_abs


def init_Q_exprs(t, scale, max_size, max_skew, dtype=None):
    """
    For a scalar or tensor t, we initialize its preconditioner Q and reusable contraction expressions for updating Q and preconditioning gradient.
    """
    dtype = dtype if dtype is not None else t.dtype
    shape = t.shape
    if len(shape) == 0:  # scalar
        Q = [scale * torch.ones_like(t, dtype=dtype)]
        exprA = opt_einsum.contract_expression(",->", Q[0].shape, t.shape)
        exprP = opt_einsum.contract_expression(",,->", Q[0].shape, Q[0].shape, t.shape)
        exprGs = [opt_einsum.contract_expression(",->", t.shape, t.shape)]
    else:  # tensor
        if len(shape) > 26:
            raise ValueError(
                f"Got tensor with dim {len(t.shape)}; Einstein runs out of letters; Replace 26 with larger numbers!"
            )

        scale = scale ** (1 / len(shape))
        if len(shape) == 1:
            beta_size = 1  # 2nd largest size
        else:
            beta_size = sorted(list(shape))[-2]

        Q = []
        exprGs = []
        piece1A, piece2A, piece3A = (
            [],
            "",
            "",
        )  # used for getting the subscripts for exprA
        piece1P, piece2P, piece3P, piece4P = (
            [],
            [],
            "",
            "",
        )  # used for getting the subscripts for exprP
        for i, size in enumerate(shape):
            if size == 1 or size > max_size or size > max_skew * beta_size:
                # use diagonal matrix as preconditioner for this dim
                Q.append(scale * torch.ones(size, dtype=dtype, device=t.device))

                piece1A.append(opt_einsum.get_symbol(i))
                piece2A = piece2A + opt_einsum.get_symbol(i)
                piece3A = piece3A + opt_einsum.get_symbol(i)

                piece1P.append(opt_einsum.get_symbol(i + 26))
                piece2P.append(opt_einsum.get_symbol(i + 26))
                piece3P = piece3P + opt_einsum.get_symbol(i + 26)
                piece4P = piece4P + opt_einsum.get_symbol(i + 26)

                piece1 = "".join(
                    [
                        (
                            opt_einsum.get_symbol(i + 26)
                            if j == i
                            else opt_einsum.get_symbol(j)
                        )
                        for j in range(len(shape))
                    ]
                )
                subscripts = (
                    piece1 + "," + piece1 + "->" + opt_einsum.get_symbol(i + 26)
                )
                exprGs.append(
                    opt_einsum.contract_expression(subscripts, t.shape, t.shape)
                )
            else:
                # use triangular matrix as preconditioner for this dim
                Q.append(scale * torch.eye(size, dtype=dtype, device=t.device))

                piece1A.append(opt_einsum.get_symbol(i) + opt_einsum.get_symbol(i + 26))
                piece2A = piece2A + opt_einsum.get_symbol(i + 26)
                piece3A = piece3A + opt_einsum.get_symbol(i)

                a, b, c = (
                    opt_einsum.get_symbol(i),
                    opt_einsum.get_symbol(i + 26),
                    opt_einsum.get_symbol(i + 805),
                )
                piece1P.append(a + b)
                piece2P.append(a + c)
                piece3P = piece3P + c
                piece4P = piece4P + b

                piece1 = "".join(
                    [
                        (
                            opt_einsum.get_symbol(i + 26)
                            if j == i
                            else opt_einsum.get_symbol(j)
                        )
                        for j in range(len(shape))
                    ]
                )
                piece2 = "".join(
                    [
                        (
                            opt_einsum.get_symbol(i + 805)
                            if j == i
                            else opt_einsum.get_symbol(j)
                        )
                        for j in range(len(shape))
                    ]
                )
                subscripts = (
                    piece1
                    + ","
                    + piece2
                    + "->"
                    + opt_einsum.get_symbol(i + 26)
                    + opt_einsum.get_symbol(i + 805)
                )
                exprGs.append(
                    opt_einsum.contract_expression(subscripts, t.shape, t.shape)
                )

        subscripts = ",".join(piece1A) + "," + piece2A + "->" + piece3A
        exprA = opt_einsum.contract_expression(
            subscripts, *[q.shape for q in Q], t.shape
        )

        subscripts = (
            ",".join(piece1P) + "," + ",".join(piece2P) + "," + piece3P + "->" + piece4P
        )
        exprP = opt_einsum.contract_expression(
            subscripts, *[q.shape for q in Q], *[q.shape for q in Q], t.shape
        )

    exprGs = tuple(exprGs)
    return [Q, (exprA, exprGs, exprP)]


def update_precond_kron_math_(Q, exprs, V, G, step, step_normalizer, tiny):
    """
    Update Kronecker product preconditioner Q with (vector, hess-vector-product) pair (V, G).
    V is optional, and we can set it to None if it is integrated out (NOT recommend).
    """

    def triangular_inv(A):
        # return inv(A); used only when V is None, i.e., integrating out V; NOT recommend.
        I = torch.eye(A.shape[0], dtype=A.dtype, device=A.device)
        return torch.linalg.solve_triangular(A, I, upper=True)

    def solve_triangular_right(X, A):
        # return X @ inv(A)
        if X.dim() > 1:
            return torch.linalg.solve_triangular(A, X, upper=True, left=False)
        else:  # torch.linalg.solve_triangular complains if X.dim() < 2! So insert None
            return torch.linalg.solve_triangular(A, X[None, :], upper=True, left=False)[
                0
            ]

    order = G.dim()  # order of tensor
    if order > 1 and torch.rand([]) < 0.01:
        # balance the dynamic range of Q if there are more than one factors
        norms = [torch.max(torch.abs(q)) for q in Q]
        gmean = (torch.cumprod(torch.stack(norms), dim=0)[-1]) ** (
            1 / order
        )  # geometric mean
        for i, q in enumerate(Q):
            q.mul_(gmean / norms[i])

    exprA, exprGs, _ = exprs

    A = exprA(*Q, G)
    if V is not None:
        invQhinvQ, trace_invQhinvQ = None, None
        p = list(range(order))
        conjB = torch.permute(
            V.conj(), p[1:] + p[:1]
        )  # permute dims like [0,1,2,3,4] -> [1,2,3,4,0]
        for i, q in enumerate(Q):
            conjB = conjB / q if q.dim() < 2 else solve_triangular_right(conjB, q)
            if (
                i < order - 1
            ):  # transpose dims like [1,2,3,4,0]->[0,2,3,4,1]->[0,1,3,4,2]->[0,1,2,4,3]->[0,1,2,3,4]
                conjB = torch.transpose(conjB, i, order - 1)
    else:  # V is integrated out, and no need to form conjB
        conjB = None
        invQ = [1 / q if q.dim() < 2 else triangular_inv(q) for q in Q]
        invQhinvQ = [q.conj() * q if q.dim() < 2 else q.H @ q for q in invQ]
        trace_invQhinvQ = [
            torch.sum(q) if q.dim() < 2 else torch.trace(q) for q in invQhinvQ
        ]

    for i, q in enumerate(Q):
        term1 = exprGs[i](A, A.conj())
        if conjB is not None:
            term2 = exprGs[i](conjB.conj(), conjB)
        else:  # V is integrated out
            term2 = 1.0
            for j, trace in enumerate(trace_invQhinvQ):
                term2 = term2 * (trace if i != j else invQhinvQ[i])

        if step_normalizer == "2nd":
            if q.dim() < 2:  # q is a diagonal matrix or scalar
                q.sub_(
                    step
                    / (torch.max(torch.abs(term1 + term2)) + tiny)
                    * (term1 - term2)
                    * q
                )
            else:
                q.sub_(
                    step
                    / (norm_lower_bound(term1 + term2) + tiny)
                    * torch.triu(term1 - term2)
                    @ q
                )
        else:  # only use gradient for step size normalization
            if q.dim() < 2:  # q is a diagonal matrix or scalar
                q.sub_(
                    step
                    / (torch.max(torch.abs(term1 - term2)) + tiny)
                    * (term1 - term2)
                    * q
                )
            else:
                q.sub_(
                    step
                    / (norm_lower_bound(term1 - term2) + tiny)
                    * torch.triu(term1 - term2)
                    @ q
                )


def precond_grad_kron_math(Q, exprs, G):
    """
    Precondition gradient G with preconditioner Q.
    """
    return exprs[-1](*[q.conj() for q in Q], *Q, G)  # the last expr is exprP
