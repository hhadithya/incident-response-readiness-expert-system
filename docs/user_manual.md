# User Manual

How to install and run the Incident Response Readiness Expert System on another machine.

There are two interfaces onto the same CLIPS knowledge base. The desktop application is easier; the CLIPS terminal needs no Python.

## Required software

| Interface | Needs |
|---|---|
| Desktop application | Python 3.10+, clipspy, Tkinter |
| CLIPS terminal | CLIPS 6.4.2 |

Neither needs the other. Installing both lets you run the same assessment either way.

## Installing CLIPS

Download CLIPS 6.4.2 from https://www.clipsrules.net, which links to the SourceForge releases at https://sourceforge.net/projects/clipsrules/files/CLIPS/6.4.2/

| Platform | File |
|---|---|
| Windows 64 bit | `clips_windows_64_bit_installer_642.msi` |
| macOS | `clips_macos_executable_642.dmg` |
| Source | `clips_core_source_642.zip` |

On Windows the installer provides two programs. `CLIPSDOS.exe` is the command line shell used below. `CLIPSIDE.exe` is a windowed editor that works the same way.

## Installing the desktop application

```bash
git clone https://github.com/hhadithya/incident-response-readiness-expert-system.git
cd incident-response-readiness-expert-system
pip install -r requirements.txt
```

That installs `clipspy`, which bundles its own copy of the CLIPS engine. You do not need CLIPS separately for the desktop application.

Tkinter is part of the standard library on Windows and macOS. On Debian or Ubuntu:

```bash
sudo apt install python3-tk
```

## Running the desktop application

On Windows, if `python` opens the Microsoft Store instead of running, use the `py` launcher in place of `python` in every command below.

From the repository root:

```bash
python app/desktop_app.py
```

A window opens with 23 questions in four sections: Preparation and governance, Detection, Response, Recovery and improvement. The list scrolls.

1. Choose **Yes**, **No** or **Unknown** for each question.
2. Click **Run Assessment**.
3. Findings appear grouped by area. Each shows the rule, the finding, a recommendation and the NIST source.
4. Click **View Explanation** on any finding to see what triggered it.
5. **New Assessment** clears everything. **Back to Answers** returns with your answers intact. **Exit** closes the application.

If you leave questions blank, you are asked whether to record them as Unknown. Nothing is ever recorded as No unless you chose No.

## Running in the CLIPS terminal

Start CLIPS with the repository root as the working directory. If you opened it another way, set the directory first:

```
(chdir "/path/to/incident-response-readiness-expert-system")
```

Then load and start:

```
(batch* "src/main.clp")
(start)
```

You should see `Loaded. Run (start) to begin an assessment.` after the first command.

Answer each question with `yes`, `no` or `unknown`. Single letters `y`, `n`, `u` work, and case does not matter. An unrecognised answer re-prompts rather than being guessed.

After the last question the assessment runs and the findings print. Then:

```
(explain R18)      one finding in full
(explain-all)      every finding in full
```

Use `(start)` again for a new assessment.

## Reading the output

A finding looks like this:

```
  [R18] Backups   (NIST priority: High)
      Finding        : Backups of data are not created, protected, maintained and tested.
      Recommendation : Create, protect, maintain and test backups of data.
      Source         : NIST SP 800-61r3, PR.DS-11, PDF p. 30 (doc p. 22)
```

| Part | Meaning |
|---|---|
| `R18` | The rule that fired. Look it up in `docs/rule_source_mapping.md`. |
| NIST priority | How central NIST considers this outcome to incident response. It is not a severity rating for your organization. |
| Source | The CSF element and the page in the source PDF. |

An explanation adds what triggered the rule:

```
  Triggered because
      Question F18: Are backups of data created, protected, maintained and tested?
      You answered: no
```

For R24, R25 and R26 the trigger is other findings rather than an answer, because those rules match on what earlier rules concluded:

```
  Triggered because
      These findings, already established by other rules:
      [R18] Backups
      [R20] Restoration asset integrity
```

Questions answered Unknown appear under **Not assessed**. They produce no finding, because an unknown answer is not evidence of a gap.

There is no overall score. The source defines no readiness scale, so the system reports gaps rather than inventing one.

## Example

Answer every question **Yes** except:

| Question | Answer |
|---|---|
| F18 backups created and tested | No |
| F20 restoration asset integrity verified | No |
| F22 root cause analysis | Unknown |
| F23 after action report | No |

Four findings result, all under Recovery and improvement: **R18**, **R20**, **R23** and **R26**. F22 appears under Not assessed.

R26 is worth looking at. No question maps to it. It fired because R18 and R20 asserted findings and a further rule matched on those, which is the second round of forward chaining.

## Running the tests

CLIPS scenarios, in the CLIPS terminal:

```
(batch* "src/main.clp")
(load "tests/test_scenarios.clp")
(run-tests)
```

Expected: `9 tests, 9 passed, 0 failed`.

Python integration tests, from the repository root:

```bash
python -m unittest discover -s tests -p "test_adapter.py"
```

Expected: `Ran 19 tests` and `OK`.

## If something goes wrong

| Problem | Cause |
|---|---|
| `Unable to find file src/rules.clp` in CLIPS | Working directory is not the repository root. Use `(chdir ...)`. |
| `Unable to find deftemplate` when loading | `src/main.clp` was opened with `load` instead of `batch*`. CLIPS will not nest a load inside a load. |
| `ModuleNotFoundError: No module named 'clips'` | `pip install -r requirements.txt` has not been run. |
| `ModuleNotFoundError: No module named 'tkinter'` | On Linux, install `python3-tk`. |
| `python` opens the Microsoft Store | Windows alias for an uninstalled Python. Use `py` instead. |
| Desktop app reports it cannot start | The `.clp` files in `src/` are missing or unreadable. |
| `[ENVRNMNT8] Environment data not fully deallocated` | A diagnostic from inside clipspy when the application closes. Harmless. |
