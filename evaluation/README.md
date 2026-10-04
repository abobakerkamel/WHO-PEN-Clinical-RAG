# Evaluation

## Gold-100

The included Gold-100 set is a **source-grounded development / silver dataset**.

It is useful for:
- retrieval regression,
- failure analysis,
- ablation testing,
- evidence-pack coverage.

It must **not** be represented as a pristine held-out clinical test set because it has already been used for:
- relevance-label repair,
- retrieval analysis,
- candidate tuning / ablation decisions.

## Final clinical acceptance

Create a fresh held-out set after architecture freeze. Recommended:
- 30–50 questions minimum,
- stratified by module,
- numeric / threshold questions,
- table questions,
- recommendation questions,
- emergency / safety-sensitive questions,
- ideally clinician-reviewed,
- no tuning against this set.

## RAGAS

The notebook implements:
- Context Precision
- Context Recall
- Faithfulness

The RAGAS runner checkpoints after each question and treats provider 429/quota errors as a **blocked/pending** state rather than a pass.

Current final RAGAS provider-quota run is pending completion.
