<!-- Styled Fairness Audit Report -->
# COMPAS Fairness Audit — Executive Summary

This audit summarizes key fairness findings from an analysis of the COMPAS recidivism risk model, highlights measured disparities across racial groups, and proposes prioritized remediation and monitoring actions.

## Key Findings

- **False Positive Rate (FPR)**: African-American defendants — **45%**; Caucasian defendants — **23%**. This large gap indicates African-American individuals were substantially more likely to be incorrectly labeled high-risk.
- **True Positive Rate (TPR)**: African-American — **59%**; Caucasian — **51%**. Higher TPR for one group does not negate disparate harms caused by elevated FPR.
- **Disparate Impact Ratio**: **0.68** (below the 0.8 benchmark) — indicates adverse impact against the protected group.
- **Statistical Parity Difference**: **-0.13** — systematic disadvantage for minority groups in high-risk assignments.

## Interpretation

The pattern of high FPR combined with a low disparate impact ratio demonstrates that the model produces unequal error burdens across groups. Some observed TPR differences likely reflect data collection and labeling bias rather than fairer model performance.

## Remediation Recommendations (prioritized)

1. Pre-processing: reweight or resample training data to reduce historical imbalances and mitigate proxy correlations with race.
2. In-processing: incorporate fairness-aware objectives (e.g., equality of odds constraints) and adversarial debiasing during model training.
3. Post-processing: apply calibrated score adjustments or thresholding to equalize error rates where appropriate and lawful.
4. Feature engineering: enrich models with contextual, non-protected features (e.g., community resources, case complexity) while carefully avoiding proxies for race.
5. Human oversight: require human-in-the-loop review for high-risk classifications and ensure diverse review panels.
6. Continuous monitoring: deploy automated fairness checks and alerting (e.g., monitor FPR/TPR by subgroup monthly).

## Metrics & Targets

- Aim for a disparate impact ratio within **0.8–1.25** where feasible.
- Target maximum subgroup FPR gap of **<= 5 percentage points** after remediation.
- Document and publish per-group metrics and evaluation methodology for transparency.

## Methods & Data

- Dataset: historical COMPAS predictions and observed recidivism outcomes (as used in the audit).
- Evaluation: confusion-matrix-derived metrics (FPR, TPR), statistical parity, and disparate impact ratio computed per demographic group.
- Limitations: label bias in observed recidivism and unobserved confounders may influence results; mitigation techniques should account for these limitations.

## Reproducibility

Run the audit script used in this project (example):

```powershell
cd Practical
python compas_fairness_audit.py
```

Ensure dependencies in the project environment are installed (see `requirements.txt` or project README).

## Conclusions

The audit identifies clear, actionable disparities in COMPAS outputs that warrant remediation before any high-stakes deployment. Combining data-level fixes with fairness-aware training, post-processing, and enforced human oversight will reduce harms and improve accountability.

## Next Steps

- Implement one remediation strategy in a controlled experiment and measure metric improvement.
- Set up automated monitoring dashboards and periodic external audits.
- Engage stakeholders (community representatives, legal experts, domain clinicians) for policy alignment.

---

*Prepared as part of Week 7 practical assignment.*
