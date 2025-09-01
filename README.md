
# 📘 CheckPoint 4 — Programação Dinâmica (COP30 — Belém)

Este pacote implementa os dois desafios do **Checkpoint 4** com foco em **Programação Dinâmica** e comparação com **Brute Force** e **Divide & Conquer**. O código está modularizado em `.py` e orquestrado por um **notebook Jupyter** com figuras, métricas e conclusões.

---

## 👥 Composição do Grupo
- Guilherme Lunghini Teixeira – RM 555892
- Luan Ramos Garcia de Souza – RM 558537
- Marchel Augusto Ribeiro de Matos – RM 99856
- Matheus Ricciotti – RM 556930
- Matheus Bortolotto – RM 555189


---

## 📂 Arquivos
- `checkpoint4.ipynb` — Notebook principal (execução, gráficos, métricas e conclusões).
- `knapsack.py` — **Desafio 1**: Mochila 0/1 (Brute Force, Meet‑in‑the‑Middle, DP bottom‑up).
- `maxsubarray.py` — **Desafio 2**: Máxima Soma Contígua (Brute Force, Divide & Conquer, Kadane).
- `README.md` — Este documento.

---

## 🧩 Desafio 1 — Seleção de Projetos (Mochila 0/1)
**Objetivo:** maximizar benefício (tCO₂ evitadas) respeitando o orçamento (R$ mi).  
**Entradas:** lista de pares `(custo, benefício)` e `budget` inteiro.  
**Algoritmos:** Brute Force (`2^n`), Meet‑in‑the‑Middle (`~2^(n/2)`), **DP bottom‑up** (`O(n·C)`).  
**Figuras:** dispersão custo×benefício com itens selecionados; gráfico de desempenho (ms×n).  
**Métricas:** decorator `@quality_metrics` coleta tempo e pico de memória.

## 🧩 Desafio 2 — Janela de Qualidade do Ar (Máx. Soma)
**Objetivo:** encontrar a janela contígua com soma máxima em série de inteiros ±.  
**Entradas:** lista de inteiros (p.ex. `[-3, 5, -1, ...]`).  
**Algoritmos:** Brute Force (`O(n²)`), Divide & Conquer (`O(n log n)`), **Kadane** (`O(n)`).  
**Figuras:** série temporal com janela ótima sombreada; gráfico de desempenho (ms×n).  
**Métricas:** decorator `@quality_metrics` coleta tempo e pico de memória.

---

## 📖 Explicações e Conexões (resumo)
- **Brute Force**: baseline de corretude; inviável em larga escala.  
- **Divide & Conquer**: reduz custo versus BF, mas ainda abaixo da melhor eficiência.  
- **Programação Dinâmica**: abordagem prática e escalável (DP bottom‑up para Mochila; Kadane para Máx. Soma).

---

## ✅ Conclusões
- **DP domina quando aplicável**:  
  - Mochila: DP bottom‑up encontra solução ótima em `O(n·C)` (adequado para orçamentos moderados).  
  - Máx. Soma: **Kadane** resolve em `O(n)` e é padrão prático.  
- **Brute Force** apenas como baseline (instâncias pequenas).  
- **Validação**: `assert` confirma a consistência entre métodos em instâncias pequenas.  
- **Gráficos**: evidenciam a diferença entre exponencial e (quase) linear/polinomial.

---

## ▶️ Como Executar
1. Abra `checkpoint4.ipynb` (Jupyter/Colab).  
2. Preencha a **Composição do Grupo**.  
3. Execute as células em ordem.  
4. Os benchmarks estão na versão **“aderência ao enunciado”** (n=10..25 e 200..1600). Se precisar reduzir, ajuste os ranges.

---

## 📝 Avaliação (rubrica)
- **Read‑Me (3 pts)** — este documento + organização.  
- **Explicação & conexão com a matéria (5 pts)** — docstrings, comentários e seções no notebook.  
- **Conclusões (2 pts)** — gráficos + análise final.

---

## ⚠️ Observação
Para evitar travamentos, o Brute Force possui limite interno:  
- Mochila: `n ≤ 22`.  
- Máx. Soma: `n ≤ 600`.  
Acima disso, ele é marcado como `NaN` nos gráficos (mantendo a comparação sem custo excessivo).
