<!-- Styled README for AI Ethics Assignment -->
# AI Ethics Assignment — Designing Responsible and Fair AI Systems

Concise write-up covering theoretical concepts, case-study analyses, ethical reflection, and healthcare AI guidelines.

## Table of Contents
- [Part 1 — Theoretical Understanding](#part-1---theoretical-understanding)
- [Part 2 — Case Study Analysis](#part-2---case-study-analysis)
- [Part 3 — (If applicable)](#part-3---if-applicable)
- [Part 4 — Ethical Reflection](#part-4---ethical-reflection)
- [Bonus — Healthcare AI Guidelines](#bonus---healthcare-ai-guidelines)

---

## Part 1 — Theoretical Understanding (30%)

### 1. Key Concepts

- **Algorithmic bias** — systematic errors in models that produce unfair outcomes for particular groups (often due to biased training data or proxy features).
	- Examples: credit-scoring models using zip codes; healthcare allocation models reflecting historical disparities.

- **Transparency vs Explainability**
	- *Transparency*: openness about system design, data sources, capabilities, and limits.
	- *Explainability*: the ability to explain individual decisions or predictions.
	- Both protect users, enable accountability, and support regulatory compliance.

- **GDPR implications for AI**
	- Right to explanation, data minimization, purpose limitation, rectification, privacy-by-design, and impact assessments for high-risk systems.

### 2. Ethical Principles Matching

- **Non-maleficence**: avoid harm.
- **Autonomy**: respect user control over data and decisions.
- **Sustainability**: consider environmental impact.
- **Justice**: ensure fair distribution of benefits and burdens.

---

## Part 2 — Case Study Analysis (40%)

### Case 1: Biased Hiring Tool (Amazon)

**Source of bias**
- Historical resumes over-represented male applicants; model learned undesirable correlations (e.g., penalizing resumes mentioning women-specific terms).

**Proposed fixes**
- Data: augment and balance datasets, remove proxy features, use synthetic examples when needed.
- Algorithms: incorporate fairness constraints, adversarial debiasing, and post-processing to equalize outcomes.
- Process: human-in-the-loop for final decisions, diverse development teams, regular bias audits.

**Suggested fairness metrics**: demographic parity difference, equalized odds difference, disparate impact (0.8–1.25 target), per-group precision/recall parity.

### Case 2: Facial Recognition in Policing

**Ethical risks**
- Wrongful arrests from higher false positives for minorities.
- Privacy erosion and mission creep.

**Policy recommendations**
- Independent, third-party accuracy testing across demographic groups.
- Human verification required for matches; prohibition of sole reliance on algorithmic output for arrests.
- Oversight: civilian review boards, public reporting, and sunset clauses for deployments.

---

## Part 4 — Ethical Reflection (5%)

In future projects (e.g., a healthcare diagnostic tool), adopt a comprehensive ethics-first approach:

- Collect diverse, multi-site data and document limitations.
- Integrate fairness constraints and regular audits (e.g., using AIF360).
- Provide explainability for clinicians and keep humans in the decision loop for critical outcomes.
- Enforce strong consent and governance protocols; continuously monitor subgroup performance and address disparities.

---

## Bonus — Healthcare AI Guidelines

### 1) Patient Consent Protocols
- Explicit informed consent, clear communication about AI role and limits, opt-out options, and re-consent when algorithms change.

### 2) Bias Mitigation Strategies
- Multi-site, demographically diverse datasets; adversarial debiasing; automated monitoring with alerts for significant (>5%) subgroup disparities.

### 3) Transparency Requirements
- Explainable outputs, public documentation of training data demographics, and regular reporting of model performance.

### 4) Implementation Safeguards
- Mandatory clinician review for AI diagnoses, robust validation before deployment, emergency overrides, and staff training.

---

## Notes

- This README preserves the original analysis and proposals while improving structure and readability.
- If you want, I can add a short abstract, link references, or export this into a PDF for submission.

**Author**: Einstein Dipondo — Week 7 Software Assignment
