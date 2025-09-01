
"""
maxsubarray.py — Desafio 2 (Máxima Soma Contígua)

Abordagens:
1) Brute Force (O(n^2)) — baseline (n pequeno).
2) Divide & Conquer (O(n log n)) — considera janela que cruza o meio.
3) Kadane (O(n)) — DP linear.

Extras:
- gen_days: gerador de séries inteiras ±.
- @quality_metrics: tempo, pico de memória, validação simples.

Limite para Brute Force:
- BRUTE_FORCE_MAX_N = 600
"""
from typing import List, Tuple
import time, tracemalloc
import random

BRUTE_FORCE_MAX_N = 600
QUALITY_REGISTRY = []

def quality_metrics(label: str):
    """Decorator que registra tempo, pico de memória e validação simples de entrada."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            valid_input = True
            if len(args) > 0 and isinstance(args[0], list):
                arr = args[0]
                if not all(isinstance(x, int) for x in arr):
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

def gen_days(n: int, vmin: int = -10, vmax: int = 10, seed: int = 123) -> List[int]:
    """Gera série de tamanho n com inteiros entre vmin e vmax (inclusivos)."""
    rng = random.Random(seed)
    return [rng.randint(vmin, vmax) for _ in range(n)]

@quality_metrics("maxsub_bruteforce")
def maxsub_bruteforce(arr: List[int]) -> Tuple[int, int, int]:
    """Brute Force O(n^2): retorna (melhor_soma, i, j)."""
    n = len(arr)
    if n > BRUTE_FORCE_MAX_N:
        raise ValueError(f"Brute Force desabilitado para n={n} > {BRUTE_FORCE_MAX_N}.")
    best = arr[0]
    best_i = best_j = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += arr[j]
            if s > best:
                best = s
                best_i, best_j = i, j
    return best, best_i, best_j

def _max_cross(arr, l, m, r):
    """Melhor subarray cruzando o meio m."""
    left_sum = -10**18
    s = 0
    max_l = m
    for i in range(m, l-1, -1):
        s += arr[i]
        if s > left_sum:
            left_sum = s
            max_l = i
    right_sum = -10**18
    s = 0
    max_r = m+1
    for j in range(m+1, r+1):
        s += arr[j]
        if s > right_sum:
            right_sum = s
            max_r = j
    return left_sum + right_sum, max_l, max_r

def _dac(arr, l, r):
    if l == r:
        return arr[l], l, r
    m = (l + r) // 2
    left_val, li, lj = _dac(arr, l, m)
    right_val, ri, rj = _dac(arr, m+1, r)
    cross_val, ci, cj = _max_cross(arr, l, m, r)
    if left_val >= right_val and left_val >= cross_val:
        return left_val, li, lj
    if right_val >= left_val and right_val >= cross_val:
        return right_val, ri, rj
    return cross_val, ci, cj

@quality_metrics("maxsub_divide_conquer")
def maxsub_divide_conquer(arr: List[int]) -> Tuple[int, int, int]:
    """Interface pública do Divide & Conquer."""
    return _dac(arr, 0, len(arr)-1)

@quality_metrics("maxsub_kadane")
def kadane(arr: List[int]) -> Tuple[int, int, int]:
    """Kadane O(n) com reconstrução de índices (início/fim)."""
    best = arr[0]
    cur = arr[0]
    start = 0
    best_i = best_j = 0
    for i in range(1, len(arr)):
        if cur + arr[i] < arr[i]:
            cur = arr[i]
            start = i
        else:
            cur += arr[i]
        if cur > best:
            best = cur
            best_i = start
            best_j = i
    return best, best_i, best_j
