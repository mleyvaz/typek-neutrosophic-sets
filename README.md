# Type-k Neutrosophic Sets
## Smarandache & Leyva-Vázquez (2026)

Companion repository for the paper:

> **Type-k Neutrosophic Sets: Recursive Triadic Structures and Their
> Empirical Realization in Large Language Models**
> Florentin Smarandache · Maikel Leyva-Vázquez
> *Neutrosophic Sets and Systems* (under review)

---

## Repository structure

```
main.tex                       LaTeX source (compile with pdflatex)
main.pdf                       Compiled paper (6 pages)
data/
  v3_multivendor_results.csv   2,419 LLM evaluations (6 vendors × 5 protocols)
experiments/
  type2_evidence.py            Reproduces all tables and findings in Section 5
results/
  table_type2_by_protocol.csv  Table 1 — Type-2 requirement by protocol
  table_type2_by_vendor.csv    Table 2 — Type-2 requirement by vendor
```

---

## Data description

`v3_multivendor_results.csv` — 2,419 epistemic evaluations.

| Column | Description |
|---|---|
| `vendor` | Foundation model provider (alibaba, anthropic, deepseek, meta, mistral, openai) |
| `model` | Model identifier |
| `phenomenon` | Epistemic phenomenon (Paradox, Ignorance, Vagueness, Contradiction, Contingency) |
| `protocol` | Evaluation protocol (S1, S4, S4-N, S4-O.A, S4-O.C) |
| `T` | Truth component |
| `I` | Indeterminacy component |
| `F` | Falsity component |
| `rep` | Repetition index (10 reps per cell) |

A response **requires Type-2 representation** if any component falls outside [0,1]:
`T < 0`, `T > 1`, `I > 1`, or `F > 1`.

---

## Reproduce the results

```bash
pip install pandas numpy
python experiments/type2_evidence.py
```

Expected output matches Tables 1–4 in Section 5 of the paper:
- 24.7% of all evaluations require Type-2 (597 / 2,419)
- S4-O.A: 97.3% | S4-O.C: 34.3% | S1/S4/S4-N: 0.0%
- Consistent across all 6 vendors (19%–30%)

No API keys required. No additional cost. Runtime < 5 seconds.

---

## Compile the paper

```bash
pdflatex main.tex
pdflatex main.tex   # second pass for cross-references
```

---

## Citation

```bibtex
@article{smarandache2026typek,
  author  = {Smarandache, Florentin and Leyva-V{\'a}zquez, Maikel},
  title   = {Type-$k$ Neutrosophic Sets: Recursive Triadic Structures
             and Their Empirical Realization in Large Language Models},
  journal = {Neutrosophic Sets and Systems},
  year    = {2026},
  note    = {Under review. Preprint: arXiv (forthcoming)}
}
```

---

## License

Data and code: MIT License.
Paper text: © The Authors. Submitted to Neutrosophic Sets and Systems.
