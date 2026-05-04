"""
Type-2 Neutrosophic Sets — Evidencia empírica desde LLM evaluations.

Reanaliza los 1,830 evals de Paper 1 para cuantificar:
  - Respuestas que REQUIEREN representación Type-2 (fuera de [0,1] en algún componente)
  - Distribución por protocolo, vendor y fenómeno
  - Witness más extremo por categoría Type-2

Resultado: sección empírica del paper Type-k Neutrosophic Sets.
"""
import pandas as pd
import numpy as np

DATA = "C:/Users/HP/Documents/BreakingChains_v3_Empirical/data/v3_multivendor_results.csv"
OUT  = "C:/Users/HP/Documents/BreakingChains_v3_Empirical/results/"

df = pd.read_csv(DATA)

# ── Clasificación Type-2 ──────────────────────────────────────────
# Un triplete requiere Type-2 si algún componente está fuera de [0,1]
df["T2_T_neg"]   = df["T"] < 0                  # T negativo (anti-verdad)
df["T2_I_over"]  = df["I"] > 1                  # I > 1 (hiper-indeterminación)
df["T2_F_over"]  = df["F"] > 1                  # F > 1 (hiper-falsedad)
df["T2_T_over"]  = df["T"] > 1                  # T > 1 (hiper-verdad)
df["is_type2"]   = df["T2_T_neg"] | df["T2_I_over"] | df["T2_F_over"] | df["T2_T_over"]

# ── Resumen global ────────────────────────────────────────────────
total = len(df)
n_type2 = df["is_type2"].sum()
pct_type2 = 100 * n_type2 / total

print("=" * 60)
print("TYPE-2 NEUTROSOPHIC SETS — EVIDENCIA EMPÍRICA")
print("=" * 60)
print(f"Total evaluaciones: {total}")
print(f"Requieren Type-2:   {n_type2} ({pct_type2:.1f}%)")
print(f"Type-1 suficiente:  {total - n_type2} ({100 - pct_type2:.1f}%)")
print()

# ── Por subtipo ───────────────────────────────────────────────────
print("Subtipo Type-2:")
for col, label in [
    ("T2_T_neg",  "T < 0  (anti-verdad)"),
    ("T2_T_over", "T > 1  (hiper-verdad)"),
    ("T2_I_over", "I > 1  (hiper-indeterminación)"),
    ("T2_F_over", "F > 1  (hiper-falsedad)"),
]:
    n = df[col].sum()
    print(f"  {label}: {n} ({100*n/total:.1f}%)")
print()

# ── Por protocolo ─────────────────────────────────────────────────
print("Type-2 por protocolo:")
by_protocol = (
    df.groupby("protocol")["is_type2"]
    .agg(["sum", "count"])
    .assign(pct=lambda x: 100 * x["sum"] / x["count"])
    .rename(columns={"sum": "n_type2", "count": "n_total"})
    .sort_values("pct", ascending=False)
)
print(by_protocol.to_string())
print()

# ── Por vendor ────────────────────────────────────────────────────
print("Type-2 por vendor:")
by_vendor = (
    df.groupby("vendor")["is_type2"]
    .agg(["sum", "count"])
    .assign(pct=lambda x: 100 * x["sum"] / x["count"])
    .rename(columns={"sum": "n_type2", "count": "n_total"})
    .sort_values("pct", ascending=False)
)
print(by_vendor.to_string())
print()

# ── Witnesses extremos ────────────────────────────────────────────
print("Witnesses más extremos (los que más necesitan Type-2):")
extremes = df[df["is_type2"]].copy()
extremes["extremity"] = (
    abs(df["T"].clip(upper=0)) +          # magnitud de T negativo
    (df["T"] - 1).clip(lower=0) +         # exceso T sobre 1
    (df["I"] - 1).clip(lower=0) +         # exceso I sobre 1
    (df["F"] - 1).clip(lower=0)           # exceso F sobre 1
)
top = extremes.nlargest(5, "extremity")[
    ["vendor", "protocol", "phenomenon", "T", "I", "F", "extremity"]
]
print(top.to_string(index=False))
print()

# ── Tabla para paper ──────────────────────────────────────────────
table = by_protocol[["n_type2", "n_total", "pct"]].copy()
table.columns = ["n_Type2", "n_total", "pct_Type2"]
table.to_csv(OUT + "table_type2_by_protocol.csv")

by_vendor_out = by_vendor.copy()
by_vendor_out.columns = ["n_Type2", "n_total", "pct_Type2"]
by_vendor_out.to_csv(OUT + "table_type2_by_vendor.csv")

# ── Conclusión interpretativa ─────────────────────────────────────
print("=" * 60)
print("INTERPRETACIÓN PARA EL PAPER:")
print("=" * 60)

# Protocolos S4-O (offset/overset) vs S1/S4 (standard)
standard = df[df["protocol"].isin(["S1","S4","S4-N"])]["is_type2"].mean() * 100
extended = df[df["protocol"].isin(["S4-O.A","S4-O.C"])]["is_type2"].mean() * 100

print(f"Protocolos estándar (S1, S4, S4-N): {standard:.1f}% requieren Type-2")
print(f"Protocolos extendidos (S4-O):        {extended:.1f}% requieren Type-2")
print()
print("Argumento central:")
print(f"  Los modelos producen espontáneamente valores Type-2 cuando el")
print(f"  protocolo abre el espacio [0,1]. Esto demuestra que la restricción")
print(f"  Type-1 es una limitación del protocolo, no del fenómeno epistémico.")
print(f"  La construcción formal de Smarandache (Type-k) provee el framework")
print(f"  que hace estas representaciones matemáticamente legítimas.")
