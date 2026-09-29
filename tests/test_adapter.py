"""Check that Python driving CLIPS gives the same answers as the CLIPS CLI.

The expected rule sets here are the ones documented in docs/test_results.md
and asserted by tests/test_scenarios.clp. If the adapter agrees with them, it
agrees with the CLI, because both are measured against the same expectations.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.clips_adapter import ExpertSystem, KnowledgeBaseError

PREPARATION = ["ir-policy-exists", "ir-roles-documented", "ir-authority-designated",
               "ir-plan-exists", "ir-plan-reviewed-periodically", "role-based-ir-training"]
DETECTION = ["logs-generated-and-available", "network-monitoring",
             "endpoint-and-service-monitoring", "event-correlation",
             "alerts-reach-responders", "incident-declaration-criteria"]
RESPONSE = ["incident-triage-performed", "incidents-categorized-and-prioritized",
            "incident-status-tracked", "notification-procedures-defined",
            "containment-eradication-criteria"]
RECOVERY = ["backups-created-and-tested", "recovery-initiation-criteria",
            "backup-integrity-verified", "restored-assets-verified",
            "root-cause-analysis", "after-action-report"]


_SYSTEM = None


def shared_system():
    """One environment for the whole run, reused the way the GUI reuses it."""
    global _SYSTEM
    if _SYSTEM is None:
        _SYSTEM = ExpertSystem()
    return _SYSTEM


class AdapterTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.system = shared_system()
        cls.names = [q["name"] for q in cls.system.questions()]

    def answers(self, default="yes", **overrides):
        answers = {name: default for name in self.names}
        for name, value in overrides.items():
            answers[name.replace("_", "-")] = value
        return answers

    def rules_for(self, answers):
        return [f["rule_id"] for f in self.system.assess(answers)]

    def set_to(self, value, names, default="yes"):
        answers = {name: default for name in self.names}
        for name in names:
            answers[name] = value
        return answers


class TestQuestionnaire(AdapterTestCase):

    def test_reads_the_questionnaire_from_clips(self):
        questions = self.system.questions()
        self.assertEqual(len(questions), 23)
        self.assertEqual(questions[0]["id"], "F01")
        self.assertEqual(questions[0]["name"], "ir-policy-exists")
        self.assertTrue(questions[0]["text"].endswith("?"))

    def test_questions_keep_their_declared_order_and_areas(self):
        areas = [q["area"] for q in self.system.questions()]
        self.assertEqual(areas[:6], ["preparation"] * 6)
        self.assertEqual(areas[6:12], ["detection"] * 6)
        self.assertEqual(areas[12:17], ["response"] * 5)
        self.assertEqual(areas[17:], ["recovery"] * 6)


class TestScenariosMatchTheCli(AdapterTestCase):
    """The same scenarios as tests/test_scenarios.clp, run through Python."""

    def test_T01_broadly_prepared(self):
        self.assertEqual(self.rules_for(self.answers("yes")), [])

    def test_T02_preparation_weak(self):
        self.assertEqual(self.rules_for(self.set_to("no", PREPARATION)),
                         ["R01", "R02", "R03", "R04", "R05", "R06"])

    def test_T03_detection_weak(self):
        self.assertEqual(self.rules_for(self.set_to("no", DETECTION)),
                         ["R07", "R08", "R09", "R10", "R11", "R12", "R24"])

    def test_T04_response_weak(self):
        self.assertEqual(self.rules_for(self.set_to("no", RESPONSE)),
                         ["R13", "R14", "R15", "R16", "R17", "R25"])

    def test_T05_recovery_weak(self):
        self.assertEqual(self.rules_for(self.set_to("no", RECOVERY)),
                         ["R18", "R19", "R20", "R21", "R22", "R23", "R26"])

    def test_T06_everything_unknown(self):
        self.assertEqual(self.rules_for(self.answers("unknown")), [])

    def test_T07_one_gap_beside_two_unknowns(self):
        answers = self.answers("yes")
        answers["network-monitoring"] = "no"
        answers["logs-generated-and-available"] = "unknown"
        answers["endpoint-and-service-monitoring"] = "unknown"
        self.assertEqual(self.rules_for(answers), ["R08", "R24"])

    def test_everything_missing_fires_every_rule(self):
        self.assertEqual(len(self.rules_for(self.answers("no"))), 26)


class TestFindingsCarryTheirSource(AdapterTestCase):

    def test_source_matches_the_rule_mapping(self):
        findings = {f["rule_id"]: f for f in
                    self.system.assess(self.answers("no"))}
        for rule_id, source, page in (
                ("R01", "GV.PO.R1", "PDF p. 21 (doc p. 13)"),
                ("R09", "DE.CM-09.R1 to R5", "PDF p. 32 (doc p. 24)"),
                ("R18", "PR.DS-11", "PDF p. 30 (doc p. 22)"),
                ("R23", "RC.RP-06.R1", "PDF p. 42 (doc p. 34)")):
            with self.subTest(rule=rule_id):
                self.assertEqual(findings[rule_id]["source"], source)
                self.assertEqual(findings[rule_id]["page"], page)

    def test_a_finding_carries_everything_the_display_needs(self):
        finding = self.system.assess(self.set_to("no", ["backups-created-and-tested"]))[0]
        for field in ("rule_id", "area", "title", "finding", "recommendation",
                      "source", "page", "priority", "conclusion"):
            self.assertTrue(finding[field], field)
        self.assertEqual(finding["rule_id"], "R18")
        self.assertEqual(finding["asked"], "backups-created-and-tested")


class TestChaining(AdapterTestCase):

    def test_rollup_reports_every_finding_it_rests_on(self):
        findings = self.system.assess(
            self.set_to("no", ["backups-created-and-tested", "backup-integrity-verified"]))
        rollup = next(f for f in findings if f["rule_id"] == "R26")
        supporting = self.system.supporting_findings(rollup, findings)
        self.assertEqual([f["rule_id"] for f in supporting], ["R18", "R20"])

    def test_a_rollup_has_no_asked_fact_of_its_own(self):
        findings = self.system.assess(self.set_to("no", ["network-monitoring"]))
        rollup = next(f for f in findings if f["rule_id"] == "R24")
        self.assertIsNone(rollup["asked"])


class TestRepeatedUse(AdapterTestCase):

    def test_a_second_assessment_does_not_inherit_the_first(self):
        first = self.rules_for(self.set_to("no", PREPARATION))
        second = self.rules_for(self.answers("yes"))
        third = self.rules_for(self.set_to("no", RECOVERY))
        self.assertEqual(first, ["R01", "R02", "R03", "R04", "R05", "R06"])
        self.assertEqual(second, [])
        self.assertEqual(third, ["R18", "R19", "R20", "R21", "R22", "R23", "R26"])

    def test_running_the_same_answers_twice_gives_the_same_result(self):
        answers = self.set_to("no", DETECTION)
        self.assertEqual(self.rules_for(answers), self.rules_for(answers))


class TestRejectsBadInput(AdapterTestCase):

    def test_rejects_a_value_that_is_not_yes_no_or_unknown(self):
        answers = self.answers("yes")
        answers["ir-plan-exists"] = "maybe"
        with self.assertRaises(ValueError):
            self.system.assess(answers)

    def test_rejects_a_question_that_does_not_exist(self):
        answers = self.answers("yes")
        answers["invented-practice"] = "no"
        with self.assertRaises(ValueError):
            self.system.assess(answers)

    def test_reports_a_missing_knowledge_base_clearly(self):
        with self.assertRaises(KnowledgeBaseError):
            ExpertSystem(src=Path(__file__).resolve().parent / "nonexistent")


if __name__ == "__main__":
    unittest.main(verbosity=2)
