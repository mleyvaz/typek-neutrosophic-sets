"""
Genera el .docx del paper Type-k Neutrosophic Sets.
Florentin Smarandache (1ro) & Maikel Leyva-Vázquez (2do)
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Márgenes ──────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)

# ── Estilos base ──────────────────────────────────────────────────
normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(11)

def heading(text, level=1, bold=True, size=13, space_before=12, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    return p

def body(text, italic=False, space_after=6, indent=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.left_indent  = Cm(indent)
    run = p.add_run(text)
    run.italic = italic
    run.font.size = Pt(11)
    run.font.name = 'Times New Roman'
    return p

def add_table(headers, rows, caption=""):
    if caption:
        cp = doc.add_paragraph(caption)
        cp.runs[0].bold = True
        cp.runs[0].font.size = Pt(10)
        cp.paragraph_format.space_before = Pt(10)
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    # header row
    hrow = t.rows[0]
    for i, h in enumerate(headers):
        c = hrow.cells[i]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.size = Pt(10)
        c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            c = t.rows[ri+1].cells[ci]
            c.text = str(val)
            c.paragraphs[0].runs[0].font.size = Pt(10)
    doc.add_paragraph()

# ════════════════════════════════════════════════════════════════
# TÍTULO Y AUTORES
# ════════════════════════════════════════════════════════════════
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(12)
r = p_title.add_run(
    "Type-k Neutrosophic Sets: Recursive Triadic Structures\n"
    "and Their Empirical Realization in Large Language Models"
)
r.bold = True
r.font.size = Pt(16)
r.font.name = 'Times New Roman'

p_auth = doc.add_paragraph()
p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_auth.paragraph_format.space_after = Pt(4)
r2 = p_auth.add_run(
    "Florentin Smarandache¹   ·   Maikel Leyva-Vázquez²"
)
r2.font.size = Pt(12)
r2.font.name = 'Times New Roman'

p_aff = doc.add_paragraph()
p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_aff.paragraph_format.space_after = Pt(14)
r3 = p_aff.add_run(
    "¹ Department of Mathematics, University of New Mexico, "
    "Gallup, NM 87301, USA. smarand@unm.edu\n"
    "² Facultad de Ciencias Matemáticas y Físicas, Universidad de Guayaquil, Ecuador.\n"
    "³ Universidad Bolivariana del Ecuador, Durán, Ecuador.\n"
    "⁴ Universidad Bernardo O'Higgins, Santiago, Chile.\n"
    "maikel.leyvavazquez@ug.edu.ec"
)
r3.font.size = Pt(9)
r3.italic = True
r3.font.name = 'Times New Roman'

doc.add_paragraph("―" * 80).paragraph_format.space_after = Pt(4)

# ════════════════════════════════════════════════════════════════
# ABSTRACT
# ════════════════════════════════════════════════════════════════
heading("Abstract", size=11, bold=True, space_before=6, space_after=4)
body(
    "We introduce Type-k Neutrosophic Sets, a recursive extension of neutrosophic "
    "logic in which each epistemic component (T, I, F) is itself characterised by a "
    "full neutrosophic triplet, yielding 3ᵏ scalars per element at recursion depth k. "
    "We prove a strict expressive hierarchy Type-1 ⊊ Type-2 ⊊ ⋯ ⊊ Type-k "
    "and define a canonical embedding and a recursive aggregation operator that reduces "
    "to the standard Single-Valued Neutrosophic Weighted Average (SVNWA) at k = 1. "
    "Empirically, we demonstrate that large language models (LLMs) implicitly compute "
    "Type-2 values when evaluation protocols permit components outside [0,1]: across "
    "2,419 evaluations of six foundation models under five epistemic protocols, 24.7% "
    "of all responses require Type-2 representation, rising to 97.3% under the overset "
    "protocol S4-O.A. The restriction to Type-1 is a protocol artefact, not an epistemic "
    "limit. Type-k Neutrosophic Sets provide the first formal framework that makes these "
    "LLM behaviours mathematically legitimate.",
    space_after=6
)
p_kw = doc.add_paragraph()
p_kw.paragraph_format.space_after = Pt(10)
r_kw = p_kw.add_run("Keywords: ")
r_kw.bold = True
r_kw.font.size = Pt(10)
p_kw.add_run(
    "neutrosophic sets; type-2 neutrosophic; recursive neutrosophic; "
    "large language models; epistemic uncertainty; foundation models."
).font.size = Pt(10)

doc.add_paragraph("―" * 80).paragraph_format.space_after = Pt(6)

# ════════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ════════════════════════════════════════════════════════════════
heading("1. Introduction")
body(
    "Smarandache’s neutrosophic logic [1] represents propositions as triplets (T, I, F) "
    "where T is the degree of truth, I the degree of indeterminacy, and F the degree of "
    "falsity, with T, I, F ∈ [0,1] independently (no sum constraint). This Type-1 "
    "representation has found application in multi-criteria decision making [2], image "
    "processing, and, more recently, in the epistemic evaluation of large language models "
    "(LLMs) [3, 4]."
)
body(
    "A fundamental question arises naturally: if T is the degree to which a proposition "
    "is true, to what degree is T itself true, indeterminate, or false? In type-2 fuzzy "
    "logic [5], membership degrees are themselves fuzzy sets, enabling a second layer of "
    "uncertainty. The neutrosophic analogue has not been formally defined."
)
body(
    "In this paper we fill that gap. We introduce Type-k Neutrosophic Sets, where each "
    "component of a Type-(k-1) representation is replaced by a full neutrosophic triplet. "
    "The resulting structure has 3ᵏ scalars per element at depth k and subsumes "
    "Type-1 as the base case."
)
body(
    "Our motivation is both theoretical and empirical. On the theoretical side, the "
    "construction is the most natural extension of neutrosophic logic to nested uncertainty. "
    "On the empirical side, we show that state-of-the-art LLMs already compute Type-2 "
    "values when evaluation protocols open the range beyond [0,1]: negative T values "
    "(‘anti-truth’), I > 1 (‘hyper-indeterminacy’), and F > 1 "
    "(‘hyper-falsity’) appear across all vendors under the appropriate protocol."
)

# ════════════════════════════════════════════════════════════════
# 2. BACKGROUND
# ════════════════════════════════════════════════════════════════
heading("2. Background")
heading("2.1 Type-1 Neutrosophic Sets", level=2, size=11, bold=True,
        space_before=6, space_after=4)
body(
    "Definition 1 (Type-1 Neutrosophic Set [1]). Let U be a universe of discourse. "
    "A neutrosophic set A⁽¹⁾ on U assigns to each element x ∈ U a triplet "
    "μ⁽¹⁾(x) = (T, I, F), with T, I, F ∈ [0,1] independently. "
    "There is no constraint T + I + F = 1."
)
heading("2.2 Existing extensions", level=2, size=11, bold=True,
        space_before=6, space_after=4)
body(
    "Interval-valued neutrosophic sets [2] allow T, I, F to be closed intervals in [0,1]. "
    "Refined neutrosophic logic [6] splits each component into sub-components "
    "T → (T₁,…,Tₚ), I → (I₁,…,Iᵣ), "
    "F → (F₁,…,Fₛ) — remaining scalars at each level. "
    "Neutrosophic overset/offset [7] allows components outside [0,1]. "
    "Plithogenic sets [8] assign contradiction degrees between attribute values. "
    "None assigns a full neutrosophic triplet to each component — "
    "the defining feature of Type-k Neutrosophic Sets."
)

# ════════════════════════════════════════════════════════════════
# 3. TYPE-K NEUTROSOPHIC SETS
# ════════════════════════════════════════════════════════════════
heading("3. Type-k Neutrosophic Sets")
heading("3.1 Definitions", level=2, size=11, bold=True, space_before=6, space_after=4)

body(
    "Definition 2 (Type-2 Neutrosophic Set). A Type-2 Neutrosophic Set A⁽²⁾ "
    "on U assigns to each x ∈ U nine scalars organised as three nested triplets:",
    space_after=2
)
body(
    "    T : (T_T, I_T, F_T)  — to what degree is T itself true / indeterminate / false\n"
    "    I : (T_I, I_I, F_I)  — to what degree is I itself true / indeterminate / false\n"
    "    F : (T_F, I_F, F_F)  — to what degree is F itself true / indeterminate / false",
    indent=1, space_after=6
)
body(
    "where all nine scalars are in [0,1] independently. "
    "This is the construction proposed by Smarandache (personal communication, 2026-05-04): "
    "‘we may set a triplet T, I, F for each type of uncertainty, contradiction, "
    "indeterminacy, etc.’"
)
body(
    "Definition 3 (Type-3 Neutrosophic Set). Each of the nine scalars of a Type-2 "
    "representation is itself replaced by a neutrosophic triplet, yielding 27 scalars. "
    "For the T component: T → ( T_T(T_TT, I_TT, F_TT), I_T(T_IT, I_IT, F_IT), "
    "F_T(T_FT, I_FT, F_FT) ), and analogously for I and F."
)
body(
    "Definition 4 (Type-k Neutrosophic Set). A Type-k Neutrosophic Set is defined "
    "recursively: (i) base case k = 1 is the standard neutrosophic set; (ii) for k ≥ 2, "
    "each scalar component of a Type-(k−1) element is replaced by a full neutrosophic "
    "triplet. Each element x ∈ U is characterised by 3ᵏ scalars. "
    "The set of Type-k neutrosophic sets over U is denoted NS⁽ᵏ⁾(U)."
)
body(
    "Remark (Subset generalisation). More generally, T, I, F may be neutrosophic sets "
    "rather than scalars, yielding an infinite-dimensional construction that subsumes all "
    "finite Type-k as projections. We leave the formal development of this case to future work.",
    italic=True
)

heading("3.2 Canonical embedding and hierarchy", level=2, size=11, bold=True,
        space_before=6, space_after=4)
body(
    "Definition 5 (Embedding φ). The canonical embedding "
    "φ: NS⁽ᵏ⁻¹⁾(U) → NS⁽ᵏ⁾(U) "
    "maps each scalar s to the triplet (s, 0, 1−s)."
)
body(
    "Theorem 1 (Strict hierarchy). "
    "NS⁽¹⁾(U) ⊊ NS⁽²⁾(U) ⊊ ⋯ ⊊ NS⁽ᵏ⁾(U).",
    italic=False
)
p_proof = doc.add_paragraph()
p_proof.paragraph_format.left_indent = Cm(0.5)
p_proof.paragraph_format.space_after = Pt(6)
r_proof = p_proof.add_run(
    "Proof. Inclusion ⊆ follows from the embedding φ. "
    "Strictness ⊊ (witness for k = 2): consider a response with T = −0.2 "
    "(anti-truth). In Type-1, T ∈ [0,1] is required, so T = −0.2 is inadmissible. "
    "In Type-2 it is represented as (T_T = 0.0, I_T = 0.2, F_T = 0.8) — a well-formed "
    "triplet. Empirically, 65 such responses were observed (2.7% of evaluations). "
    "The witness (T = 1.7, I = 1.8, F = 1.6) is inadmissible in any Type-1 framework "
    "but fully representable in Type-2. ■"
)
r_proof.font.size = Pt(10)
r_proof.font.name = 'Times New Roman'

# ════════════════════════════════════════════════════════════════
# 4. RECURSIVE AGGREGATION
# ════════════════════════════════════════════════════════════════
heading("4. Recursive Aggregation Operator")
body(
    "The standard SVNWA [2] at Type-1 is: "
    "SVNWA(μ₁,…,μn; w) = (1−∏(1−T_i)^w_i, "
    "∏I_i^w_i, ∏F_i^w_i)."
)
body(
    "Definition 6 (Type-k SVNWA). The Type-k SVNWA applies the SVNWA operator "
    "recursively to each sub-triplet independently at every level. For Type-2:"
)
body(
    "    SVNWA⁽²⁾(μ⁽²⁾₁,…,μ⁽²⁾n; w) = "
    "( SVNWA(T₁,…,Tn; w),  SVNWA(I₁,…,In; w),  SVNWA(F₁,…,Fn; w) )",
    indent=1, space_after=6
)
body(
    "Proposition 1 (Reduction). SVNWA⁽ᵏ⁾ reduces to standard SVNWA when all "
    "elements are images under φ (i.e., all sub-triplets have I = 0 and F = 1−T)."
)

# ════════════════════════════════════════════════════════════════
# 5. EMPIRICAL EVIDENCE
# ════════════════════════════════════════════════════════════════
heading("5. Empirical Evidence: LLMs as Implicit Type-2 Computers")
heading("5.1 Experimental design", level=2, size=11, bold=True,
        space_before=6, space_after=4)
body(
    "We reanalysed 2,419 evaluations from a multi-vendor empirical study [3]. "
    "Six foundation models (Alibaba Qwen-3-235B, Anthropic Claude Sonnet 4, DeepSeek Chat, "
    "Meta Llama-4-Maverick, Mistral Medium-3.1, OpenAI GPT-4o) were evaluated on five "
    "epistemic phenomena under five protocols: S1 (classical scalar), S4 (Mason [4] "
    "three-component frame), S4-N (per-attribute neutrosophic), S4-O.A (overset T,I,F ∈ "
    "[0,2]), S4-O.C (offset T,I,F ∈ [−1,2]). "
    "A response requires Type-2 if any component falls outside [0,1]. "
    "Data and code: github.com/mleyvaz/typek-neutrosophic-sets"
)
heading("5.2 Results", level=2, size=11, bold=True, space_before=6, space_after=4)

add_table(
    headers=["Protocol", "n", "Type-2 required", "%"],
    rows=[
        ["S4-O.A",  "300",   "292", "97.3"],
        ["S4-O.C",  "889",   "305", "34.3"],
        ["S4-N",    "300",   "0",   "0.0"],
        ["S4",      "300",   "0",   "0.0"],
        ["S1",      "300",   "0",   "0.0"],
        ["S1-taut", "90",    "0",   "0.0"],
        ["Total",   "2,419", "597", "24.7"],
    ],
    caption="Table 1. Type-2 requirement by protocol."
)
add_table(
    headers=["Vendor", "n", "Type-2 required", "%"],
    rows=[
        ["Mistral (Medium-3.1)",        "435", "130", "29.9"],
        ["OpenAI (GPT-4o)",             "377", "100", "26.5"],
        ["Anthropic (Claude Sonnet 4)", "408", "108", "26.5"],
        ["Meta (Llama-4-Maverick)",     "355", "81",  "22.8"],
        ["DeepSeek Chat",               "431", "97",  "22.5"],
        ["Alibaba (Qwen-3-235B)",       "413", "81",  "19.6"],
    ],
    caption="Table 2. Type-2 requirement by vendor (S4-O protocols)."
)
add_table(
    headers=["Type-2 subtype", "n", "% of total"],
    rows=[
        ["I > 1  (hyper-indeterminacy)", "507", "21.0"],
        ["T > 1  (hyper-truth)",         "129",  "5.3"],
        ["F > 1  (hyper-falsity)",        "91",  "3.8"],
        ["T < 0  (anti-truth)",           "65",  "2.7"],
    ],
    caption="Table 3. Type-2 subtypes across all evaluations."
)
add_table(
    headers=["Vendor", "Protocol", "Phenomenon", "T", "I", "F"],
    rows=[
        ["Mistral", "S4-O.A", "Contradiction (Ethical)", "1.7", "1.8", "1.6"],
        ["Mistral", "S4-O.A", "Contradiction (Ethical)", "1.7", "1.8", "1.6"],
        ["OpenAI",  "S4-O.A", "Paradox (Logical)",       "0.0", "2.0", "2.0"],
        ["OpenAI",  "S4-O.A", "Paradox (Logical)",       "0.0", "2.0", "2.0"],
        ["OpenAI",  "S4-O.A", "Paradox (Logical)",       "0.0", "2.0", "2.0"],
    ],
    caption="Table 4. Five most extreme Type-2 witnesses."
)
heading("5.3 Interpretation", level=2, size=11, bold=True, space_before=6, space_after=4)
body(
    "Three observations are central. First, the zero vs. high dichotomy: standard protocols "
    "produce 0% Type-2 responses because the format enforces [0,1]; extended protocols yield "
    "97.3% Type-2. The restriction is a protocol artefact. Second, cross-vendor consistency: "
    "19.6%–29.9% across all six independent vendors rules out a single-model idiosyncrasy. "
    "Third, the witness (T = 1.7, I = 1.8, F = 1.6) maps to Type-2 as: "
    "T → (T_T=1.0, I_T=0.7, F_T=0.0), I → (T_I=1.0, I_I=0.8, F_I=0.0), "
    "F → (T_F=1.0, I_F=0.6, F_F=0.0) — a coherent epistemic state that Type-1 cannot represent."
)

# ════════════════════════════════════════════════════════════════
# 6. CONNECTIONS
# ════════════════════════════════════════════════════════════════
heading("6. Connections to Existing Neutrosophic Frameworks")
body(
    "Refined neutrosophic logic [6] increases cardinality at a single level "
    "(T → T₁,…,Tₚ). Type-k increases recursion depth. They are orthogonal. "
    "Plithogenic tensors [3] assign Type-1 triplets per attribute — a Type-2 structure "
    "along the attribute dimension. SVN Tensors [9] are Type-1 structures across tensor modes; "
    "Type-k Tensors (combining both) are natural future work. "
    "The Absorption Problem [3] — where I → 1 under standard protocols — "
    "is now formally characterised as forced Type-2 → Type-1 projection: the sub-structure "
    "of I (genuine ignorance vs. source conflict) is lost in the collapse."
)

# ════════════════════════════════════════════════════════════════
# 7. CONCLUSION
# ════════════════════════════════════════════════════════════════
heading("7. Conclusion")
body(
    "We have introduced Type-k Neutrosophic Sets, proved a strict expressive hierarchy, "
    "and demonstrated that LLMs already compute Type-2 values when the protocol allows it. "
    "Three directions for future work: (1) Type-3 for meta-uncertainty, where the evaluator "
    "characterises its own indeterminacy; (2) subset generalisation beyond finite depth k; "
    "(3) Type-k distance and clustering of LLMs by depth of epistemic expression."
)

# ════════════════════════════════════════════════════════════════
# REFERENCES
# ════════════════════════════════════════════════════════════════
heading("References", size=11)
refs = [
    "[1] Smarandache, F. (1998). Neutrosophy: Neutrosophic Probability, Set, and Logic. American Research Press.",
    "[2] Wang, H., Smarandache, F., Zhang, Y.Q., & Sunderraman, R. (2010). Single valued neutrosophic sets. Multispace & Multistructure, 4, 410-413.",
    "[3] Leyva-Vázquez, M., & Smarandache, F. (2026). Plithogenic tensor neutrosophic logic: A formal foundation for declared-loss evaluation in LLMs. Manuscript submitted.",
    "[4] Mason, T. (2026). From scalars to tensors: Declared losses recover epistemic distinctions that neutrosophic scalars cannot express. arXiv:2604.09602.",
    "[5] Mendel, J.M., & John, R.I. (2002). Type-2 fuzzy sets made simple. IEEE Transactions on Fuzzy Systems, 10(2), 117-127.",
    "[6] Smarandache, F. (2013). n-Valued refined neutrosophic logic and its applications to physics. Progress in Physics, 4, 143-146.",
    "[7] Smarandache, F. (2016). Neutrosophic overset, neutrosophic underset, and neutrosophic offset. Pons Editions.",
    "[8] Smarandache, F. (2018). Plithogeny, plithogenic set, logic, probability, and statistics. Pons Publishing House.",
    "[9] Leyva-Vázquez, M., & Smarandache, F. (2026). Single-valued neutrosophic tensors. arXiv preprint (in preparation).",
    "[10] Ye, J. (2014). A multicriteria decision-making method using aggregation operators for simplified neutrosophic sets. JIFS, 26(5), 2459-2466.",
    "[11] Atanassov, K.T. (1986). Intuitionistic fuzzy sets. Fuzzy Sets and Systems, 20(1), 87-96.",
]
for ref in refs:
    p = doc.add_paragraph(ref)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    p.runs[0].font.size = Pt(10)
    p.runs[0].font.name = 'Times New Roman'

# ════════════════════════════════════════════════════════════════
# GUARDAR
# ════════════════════════════════════════════════════════════════
out = "C:/Users/HP/Documents/TypeK_Neutrosophic_Paper/Smarandache_LeyvaVazquez_2026_TypeK_NS_v01.docx"
doc.save(out)
print(f"Guardado: {out}")
