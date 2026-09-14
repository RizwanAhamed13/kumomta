# Review disposition

Artifact repair responds to the hosted high-confidence keyword false positive and Auto Review attachment `b10e34ee-7ff8-4972-9740-7dcd642b4fb0`.

| Finding | Classification | Disposition |
|---|---|---|
| Keyword accepted by broad identifier predicate and panics during isolation | Prompt-stated regression and hosted FP | Added a reused `self` request to the existing non-identifier/unsupported-role scenario. Exact Orion fails; reference and preserved genuine Nova pass. |
| Unsupported roles after nested forwarding | Prompt-stated route composition | Added nested mixed type/pattern/binding/record assertions to the existing unsupported-role scenario. |
| Unsupported roles below an enclosing attribute | Prompt-stated route composition | Added an attribute-wrapped mixed-role assertion to the existing attribute scenario. |
| Bare tokenless request | Prompt-stated eligibility boundary | Added historical-first-site preservation to the existing non-identifier helper. |
| Internal synthetic-marker caveat | Description-quality issue | Removed the implementation-facing caveat. |

No behavioral requirement or existing assertion was removed. The description now defines a non-keyword identifier and gives route-independent mixed-role examples so future solvers can distinguish eligibility and filtering without repository function names.

## Exact Cloud matrix

- Reference new: 29/29 pass.
- Preserved genuine Nova new: 29/29 pass.
- Exact Orion FP new: 28/29; keyword request panics in `ast::make::ident`.
- Untouched plus test patch new: 29/29 fail.
- Reference base: 747/747 pass.
- Preserved genuine Nova base: 753/753 pass.
