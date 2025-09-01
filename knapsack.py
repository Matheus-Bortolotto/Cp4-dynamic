
"""
knapsack.py — Desafio 1 (Mochila 0/1 / Seleção de Projetos)

Abordagens:
1) Brute Force (2^n) — baseline (n pequeno).
2) Meet-in-the-Middle (~2^(n/2)) — divide em duas metades e combina com busca binária.
3) DP bottom-up (O(n·C)) — programação dinâmica por capacidade, com reconstrução.

Extras:
- gen_projects: gerador de instâncias (custos/benefícios inteiros).
- @quality_metrics: decorator que mede tempo, pico de memória e validação simples.

Limites para evitar travamentos:
- BRUTE_FORCE_MAX_N = 22
"""
from typing import List, Tuple
import tracemalloc
import time

BRUTE_FORCE_MAX_N = 22
QUALITY_REGISTRY = []

def quality_metrics(label: str):
    """Decorator que registra tempo, pico de memória e validação simples de entrada."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Validação simples: lista de tuplas (int,int) + budget int
            valid_input = True
            if len(args) > 0 and isinstance(args[0], list):
                items = args[0]
                for it in items:
                    if (not isinstance(it, tuple)) or len(it) != 2:
                        valid_input = False
                        break
                    c, b = it
                    if not (isinstance(c, int) and isinstance(b, int)):
                        valid_input = False
                        break
            if len(args) > 1 and not isinstance(args[1], int):
                valid_input = False

            tracemalloc.start()
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                ok = True
            except Exception as e:
                ok = False
                result = e
            elapsed = time.perf_counter() - start
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            QUALITY_REGISTRY.append({
                "label": label,
                "function": func.__name__,
                "ok": ok,
                "valid_input": valid_input,
                "time_sec": elapsed,
                "peak_mem_mib": peak / (1024*1024),
            })
            if not ok:
                raise result
            return result
        return wrapper
    return decorator

def gen_projects(n: int, cost_min: int = 2, cost_max: int = 20,
                 benefit_min: int = 10, benefit_max: int = 120, seed: int = 42) -> List[Tuple[int,int]]:
    """Gera `n` projetos (custo, benefício), inteiros, controlados por semente."""
    import random
    rng = random.Random(seed)
    return [(rng.randint(cost_min, cost_max), rng.randint(benefit_min, benefit_max)) for _ in range(n)]

@quality_metrics("knapsack_bruteforce")
def knapsack_bruteforce(projects: List[Tuple[int,int]], budget: int):
    """
    Brute Force: testa todos os subconjuntos (2^n).
    Retorna (benefício_ótimo, indices_selecionados).
    """
    n = len(projects)
    if n > BRUTE_FORCE_MAX_N:
        raise ValueError(f"Brute Force desabilitado para n={n} > {BRUTE_FORCE_MAX_N}.")
    best_benefit = -1
    best_set = []
    for mask in range(1 << n):
        total_cost = 0
        total_benefit = 0
        chosen = []
        for i in range(n):
            if mask & (1 << i):
                c, b = projects[i]
                total_cost += c
                total_benefit += b
                chosen.append(i)
        if total_cost <= budget and total_benefit > best_benefit:
            best_benefit = total_benefit
            best_set = chosen
    return best_benefit, best_set

def _enumerate_half(items: List[Tuple[int,int]]):
    """Enumera todos os subconjuntos de uma metade, retornando (custo, benefício, mask)."""
    n = len(items)
    out = []
    for mask in range(1 << n):
        cost = 0
        ben = 0
        for i in range(n):
            if mask & (1 << i):
                c, b = items[i]
                cost += c
                ben += b
        out.append((cost, ben, mask))
    return out

@quality_metrics("knapsack_mitm")
def knapsack_meet_in_the_middle(projects: List[Tuple[int,int]], budget: int):
    """
    Divide o conjunto em duas metades.
    Enumera todas as combinações em cada metade.
    Ordena/filtra a metade direita para remover dominados.
    Combina por busca binária maximizando o benefício sem ultrapassar o orçamento.
    """
    n = len(projects)
    mid = n // 2
    left = projects[:mid]
    right = projects[mid:]

    L = _enumerate_half(left)
    R = _enumerate_half(right)

    # Ordena por custo e filtra dominância
    R.sort(key=lambda x: x[0])
    filtered = []
    max_b = -1
    for c, b, m in R:
        if b > max_b:
            filtered.append((c, b, m))
            max_b = b
    R = filtered

    import bisect
    costs_R = [c for c,_,_ in R]
    best_benefit = -1
    best_masks = (0,0)
    for cL, bL, mL in L:
        if cL > budget:
            continue
        remain = budget - cL
        idx = bisect.bisect_right(costs_R, remain) - 1
        if idx >= 0:
            cR, bR, mR = R[idx]
            total = bL + bR
            if total > best_benefit:
                best_benefit = total
                best_masks = (mL, mR)

    left_sel = [i for i in range(len(left)) if (best_masks[0] & (1 << i))]
    right_sel = [i + len(left) for i in range(len(right)) if (best_masks[1] & (1 << i))]
    return best_benefit, left_sel + right_sel

@quality_metrics("knapsack_dp_bottomup")
def knapsack_dp(projects: List[Tuple[int,int]], budget: int):
    """DP 1D por capacidade; retorna (benefício_ótimo, indices_selecionados)."""
    n = len(projects)
    dp = [0]*(budget+1)
    pick = [[False]*(budget+1) for _ in range(n)]

    for i, (cost, ben) in enumerate(projects):
        if cost > budget:
            continue
        for c in range(budget, cost-1, -1):
            if dp[c-cost] + ben > dp[c]:
                dp[c] = dp[c-cost] + ben
                pick[i][c] = True

    selected = []
    c = budget
    for i in range(n-1, -1, -1):
        if pick[i][c]:
            selected.append(i)
            c -= projects[i][0]
    selected.reverse()
    return dp[budget], selected
