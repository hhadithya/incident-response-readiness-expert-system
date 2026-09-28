# Test Results

Nine scenarios covering the four areas of the questionnaire, the chaining between rules, the handling of unknown answers, and the source information a finding carries.

Expected rule lists were worked out from [rule_source_mapping.md](rule_source_mapping.md) before the scenarios were run, not copied from program output.

## Running them

From the repository root, in the CLIPS shell:

```
(batch* "src/main.clp")
(load "tests/test_scenarios.clp")
(run-tests)
```

Each scenario resets working memory, sets all 23 answers, runs the engine, and compares the rules that fired against the rules expected. A scenario fails if an expected rule did not fire or an unexpected one did.

## Results

**9 scenarios, 9 passed, 0 failed.**

| Test | Scenario | Answers | Expected | Actual | Result |
|---|---|---|---|---|---|
| T01 | Broadly prepared organization | all 23 yes | none | none | Pass |
| T02 | Preparation and governance weak | F01 to F06 no, rest yes | R01 R02 R03 R04 R05 R06 | same | Pass |
| T03 | Detection weak | F07 to F12 no, rest yes | R07 R08 R09 R10 R11 R12 R24 | same | Pass |
| T04 | Response weak | F13 to F17 no, rest yes | R13 R14 R15 R16 R17 R25 | same | Pass |
| T05 | Recovery weak | F18 to F23 no, rest yes | R18 R19 R20 R21 R22 R23 R26 | same | Pass |
| T06 | Nothing known | all 23 unknown | none | none | Pass |
| T07 | One gap beside two unknowns | F08 no, F07 and F09 unknown, rest yes | R08 R24 | same | Pass |
| T08 | Rollup names all its support | F18 and F20 no, rest yes | R26 supported by R18 and R20 | same | Pass |
| T09 | Findings carry their source | all 23 no | R01 GV.PO.R1, R09 DE.CM-09.R1 to R5, R18 PR.DS-11, R23 RC.RP-06.R1 | same | Pass |

Unexpected rules fired: none. Missing expected rules: none.

## What each test establishes

**T01** No gap is reported for an organization that has the practices in place. A system that always finds problems would be useless, so this is worth asserting.

**T02 to T05** Each area of the questionnaire reaches the rules it should, and only those. Because the comparison rejects unexpected rules as well as missing ones, these also confirm that weakness in one area does not produce findings in another.

**T03, T04, T05** also exercise the three rules that read other rules' findings. R24, R25 and R26 appear only in the area whose gaps feed them, which is the second round of forward chaining working as intended.

**T06** Twenty three unknown answers produce nothing. If unknown were being treated as no, this scenario would fire all 26 rules. It is the sharpest test of that distinction.

**T07** Mixes a definite gap with two unknowns in the same area. R08 fires on the definite no. R24 fires because R08's finding exists. The two unknowns produce nothing, and no rule is invented for them.

**T08** Looks inside the R26 finding and checks that every gap it rests on resolves to a finding that actually exists, and that both R18 and R20 are named. This is what the earlier explanation defect would have failed: R26 previously reported only the first gap it matched.

**T09** Reads the source slot of four findings from three different CSF Functions and compares it against the citation in the rule mapping, so a finding cannot drift away from the rule it came from.

## Harness check

The comparison was verified to fail when it should, by running a scenario with a deliberately wrong expectation:

```
TX  deliberately wrong expectation
     expected : R01 R99
     actual   : R01
     result   : FAIL
     missing  : R99
```

A passing suite is only meaningful if the harness can fail.
