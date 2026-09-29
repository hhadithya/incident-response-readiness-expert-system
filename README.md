# Incident Response Readiness Expert System

A rule based expert system that assesses whether an IT organization has key cybersecurity incident response practices in place, identifies readiness gaps, and recommends improvements. For every finding it reports the rule that fired, the answers that triggered it, and the authoritative source the rule was derived from.

## What it does

You answer 23 questions about your organization's incident response practices. The system then:

1. identifies readiness gaps,
2. gives a recommendation for each,
3. shows the rule and the facts behind each finding,
4. cites the NIST location the rule came from.

It reports gaps, not a score. NIST defines no readiness scale in the source document, so the system does not invent one.

## Domain and scope

In scope: organizational preparedness, detection, response, and recovery practices for cybersecurity incidents, as covered by the knowledge source below.

Out of scope: full cybersecurity risk assessment, ISO/IEC 27001 or SOC 2 compliance, general IT risk management, penetration testing, vulnerability scanning.

This is an educational system built for a university assignment. It is not an official NIST assessment tool, not a certification or compliance tool, and not professional security advice.

## Knowledge source

All domain knowledge comes from:

> National Institute of Standards and Technology (2025). *NIST Special Publication 800-61 Revision 3: Incident Response Recommendations and Considerations for Cybersecurity Risk Management, A CSF 2.0 Community Profile.* April 2025. https://doi.org/10.6028/NIST.SP.800-61r3

A copy is kept at [`references/NIST.SP.800-61r3.pdf`](references/NIST.SP.800-61r3.pdf) so every citation can be checked against the exact document used.

No domain expert was interviewed. Each of the 26 rules is traced to a specific CSF element, item identifier and page in that document. The trace is recorded in [`docs/rule_source_mapping.md`](docs/rule_source_mapping.md) and carried inside the rule itself, so the running system can cite it.

## Technology stack

| Layer | Technology |
|---|---|
| Expert system shell | CLIPS 6.4.2 |
| Inference | CLIPS forward chaining |
| Knowledge base | CLIPS production rules, `src/rules.clp` |
| Desktop interface | Python 3, Tkinter |
| Integration | CLIPSpy |
| Knowledge source | NIST SP 800-61 Revision 3 |

## Where the reasoning happens

**CLIPS holds the knowledge and does the inference.** The rules live in `src/rules.clp` as CLIPS production rules, and CLIPS' own forward chaining engine decides what fires.

```
answers  ->  answer facts in CLIPS working memory
         ->  CLIPS pattern matcher tests them against rule conditions
         ->  matching rules enter the agenda and fire
         ->  finding facts are asserted
         ->  those findings satisfy further rules, which fire in turn
```

Three rules (R24, R25, R26) match on findings asserted by other rules rather than on answers, so a second round of chaining follows the first.

There are two interfaces onto the same knowledge base, and only one set of rules:

```
        CLIPS terminal  ─┐
                         ├─►  src/rules.clp  +  src/questions.clp
   Tkinter desktop app  ─┘
```

The desktop application is written in Python, but **Python performs no reasoning**. It collects answers, asserts them as the same CLIPS facts the terminal asserts, calls `env.run()`, and displays the findings CLIPS produced. Every finding, recommendation, priority and citation is read out of CLIPS.

## Requirements

| | |
|---|---|
| CLIPS 6.4.2 | For the terminal interface. https://www.clipsrules.net |
| Python 3.10 or newer | For the desktop interface only |
| clipspy | `pip install -r requirements.txt` |
| Tkinter | Bundled with Python on Windows and macOS. On Debian or Ubuntu: `sudo apt install python3-tk` |

The terminal interface needs CLIPS alone. The desktop interface needs Python, clipspy and Tkinter.

## Installation

```bash
git clone https://github.com/hhadithya/incident-response-readiness-expert-system.git
cd incident-response-readiness-expert-system
pip install -r requirements.txt
```

For the CLIPS terminal interface, install CLIPS 6.4.2 from https://www.clipsrules.net as well. The desktop application does not need it, because clipspy bundles the engine.

## Running the desktop application (recommended)

```bash
python app/desktop_app.py
```

On Windows, use `py` in place of `python` if `python` opens the Microsoft Store.

Answer each question Yes, No or Unknown, then click **Run Assessment**. Findings appear grouped by area, each with its rule, recommendation and source. **View Explanation** on any finding shows what triggered it.

Leaving a question blank is allowed. You are asked to confirm, and it is recorded as Unknown, never as No.

## Running in the CLIPS terminal (alternative)

Open CLIPS with the repository root as the working directory, then:

```
(batch* "src/main.clp")
(start)
```

If you opened CLIPS some other way, set the directory first:

```
(chdir "/path/to/incident-response-readiness-expert-system")
```

`batch*` rather than `load`, because CLIPS will not nest a `load` inside a `load`, and the star suppresses the echo.

Answer each question with `yes`, `no` or `unknown`. `y`, `n` and `u` work too. Anything else re-prompts.

After the questionnaire, the findings are printed. Then:

```
(explain R18)      the reasoning behind one finding
(explain-all)      every finding in full
```

## How findings are shown

Each finding names the rule that produced it, what that rule concluded, a recommendation, and the NIST location the rule came from:

```
  [R18] Backups   (NIST priority: High)
      Finding        : Backups of data are not created, protected, maintained and tested.
      Recommendation : Create, protect, maintain and test backups of data.
      Source         : NIST SP 800-61r3, PR.DS-11, PDF p. 30 (doc p. 22)
```

Asking for the explanation adds what made the rule fire. For a rule that read an answer, that is the question and the answer given. For R24, R25 and R26, which match on other rules' findings, it is those findings:

```
  Triggered because
      These findings, already established by other rules:
      [R18] Backups
      [R20] Restoration asset integrity
```

The NIST priority is the source's own judgement of how central that outcome is to incident response. It is not a severity rating for your organization.

## How answers are treated

| Answer | Effect |
|---|---|
| `yes` | The practice is in place. No rule fires. |
| `no` | The practice is missing. The rule for that question fires. |
| `unknown` | Nothing is concluded. Reported separately as not assessed. |

`unknown` is never treated as `no`. Reporting a gap an organization may not have would be as wrong as missing one it does.

## Running the tests

CLIPS scenarios, in the CLIPS terminal:

```
(batch* "src/main.clp")
(load "tests/test_scenarios.clp")
(run-tests)
```

Python integration tests, from the repository root:

```bash
python -m unittest discover -s tests -p "test_adapter.py"
```

The nine CLIPS scenarios and the Python tests check the same expected rule sets, which is how the two interfaces are shown to agree. Results are in [`docs/test_results.md`](docs/test_results.md).

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
│   ├── fact_questionnaire_mapping.md
│   ├── test_results.md
│   ├── architecture_spec.md
│   └── user_manual.md
├── src/
│   ├── rules.clp
│   ├── questions.clp
│   ├── explanations.clp
│   └── main.clp
├── app/
│   ├── clips_adapter.py
│   └── desktop_app.py
├── tests/
│   ├── test_scenarios.clp
│   └── test_adapter.py
└── report/
    └── screenshots/
```

| Path | Role |
|---|---|
| `src/rules.clp` | The 26 rules and the two templates, each rule carrying its source citation |
| `src/questions.clp` | The 23 questions |
| `src/explanations.clp` | Findings and explanation output for the terminal |
| `src/main.clp` | Loads the system and runs the terminal questionnaire |
| `app/clips_adapter.py` | Loads the CLIPS files from Python, asserts answers, reads findings |
| `app/desktop_app.py` | The Tkinter window |

## Limitations

- **Coverage is partial by design.** NIST lists five asset classes for continuous monitoring in `DE.CM.R1`; this system assesses three. The physical environment (`DE.CM-02`) and external service provider activities (`DE.CM-06`) are not assessed, and both are rated High.
- **Self assessment.** Findings reflect what the respondent reports, and nothing is verified.
- **Rules cover 26 of the CSF outcomes** in the source Profile, not all of them. Outcomes NIST rates Low, and areas it places outside the Profile's scope such as risk assessment, are excluded. See the end of `docs/rule_source_mapping.md`.
- **The wording "incomplete" and "inadequate"** in the conclusions of R24 to R26 is this project's, not NIST's. The claims underneath are source backed.
- Closing the desktop application may print `[ENVRNMNT8] Environment data not fully deallocated`. That comes from inside clipspy and affects nothing.

## References

National Institute of Standards and Technology (2025). *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile.* NIST SP 800-61r3. https://doi.org/10.6028/NIST.SP.800-61r3

Giarratano, J. *CLIPS Rule Based Programming Language*, version 6.4.2. https://www.clipsrules.net

## Acknowledgement

Domain knowledge in this project is derived from NIST SP 800-61r3, a publication of the U.S. National Institute of Standards and Technology. This project is not affiliated with, endorsed by, or reviewed by NIST.
