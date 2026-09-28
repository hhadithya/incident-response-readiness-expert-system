# Incident Response Readiness Expert System

A rule based expert system that assesses whether an IT organization has key cybersecurity incident response practices in place, identifies readiness gaps, and recommends improvements. For every conclusion it reports the rule that fired, the facts that triggered it, and the authoritative source the rule was derived from.

## Purpose

You answer a short questionnaire about your organization's incident response practices. The system then:

1. identifies readiness gaps,
2. infers relevant recommendations,
3. shows the reasoning and rules behind each conclusion,
4. cites the authoritative source behind each rule.

## Domain and scope

In scope: organizational preparedness, detection, response, and recovery practices for cybersecurity incidents, as covered by the knowledge source below.

Out of scope: full cybersecurity risk assessment, ISO/IEC 27001 or SOC 2 compliance assessment, general IT risk management, technical vulnerability scanning.

This is an educational expert system built for a university assignment. It is not an official NIST assessment tool, not a certification or compliance tool, not a guarantee of compliance with any standard, not a complete cybersecurity risk assessment, and not professional security or legal advice.

## Knowledge source

All domain knowledge is derived from:

> National Institute of Standards and Technology (2025). *NIST Special Publication 800-61 Revision 3: Incident Response Recommendations and Considerations for Cybersecurity Risk Management, A CSF 2.0 Community Profile.* April 2025.

A copy is kept at [`references/NIST.SP.800-61r3.pdf`](references/NIST.SP.800-61r3.pdf) so that every citation can be checked against the exact document used.

No domain expert was interviewed. Each rule is instead traced to a specific location in the source document. The full trace is recorded in [`docs/rule_source_mapping.md`](docs/rule_source_mapping.md) and repeated inside the executable rule definitions, so the running system can cite it. See [`docs/sources.md`](docs/sources.md) for the source policy.

## Technology

Python 3, standard library only. Command line interface. No third party runtime dependencies.

## Repository structure

```
incident-response-readiness-expert-system/
├── README.md
├── requirements.txt
├── references/
│   └── NIST.SP.800-61r3.pdf
├── docs/
│   ├── sources.md
│   ├── knowledge_engineering_process.md
│   ├── rule_source_mapping.md
│   └── test_cases.md
├── src/
│   ├── facts.py
│   ├── knowledge_base.py
│   ├── inference_engine.py
│   ├── explanation.py
│   └── main.py
├── tests/
│   ├── scenarios/
│   └── test_cases.py
└── report/
    └── screenshots/
```

| Path | Role |
|---|---|
| `references/` | The authoritative source document |
| `docs/sources.md` | Source register and the rules governing source use |
| `docs/rule_source_mapping.md` | Traceability from source text to each executable rule |
| `src/facts.py` | Fact and question model |
| `src/knowledge_base.py` | The rules, each carrying its source citation |
| `src/inference_engine.py` | Forward and backward reasoning |
| `src/explanation.py` | Reasoning trace and citation output |
| `src/main.py` | Command line interface |
| `tests/scenarios/` | Scenario fact sets used by the test cases |

## Requirements

Python 3.10 or newer. Nothing else.

## Installation

```bash
git clone https://github.com/hhadithya/incident-response-readiness-expert-system.git
cd incident-response-readiness-expert-system
pip install -r requirements.txt
```

`requirements.txt` lists no packages, since the system uses only the standard library. The step is harmless and keeps the instructions uniform across machines.

## Acknowledgement

Domain knowledge in this project is derived from NIST SP 800-61r3, a publication of the U.S. National Institute of Standards and Technology. This project is not affiliated with, endorsed by, or reviewed by NIST.
