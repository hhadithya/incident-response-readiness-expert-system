"""Structural checks on the knowledge base."""

import re
import unittest
from pathlib import Path

from src import knowledge_base as kb
from src.models import Answer, AnswerIs, Derived

MAPPING = Path(__file__).resolve().parents[1] / "docs" / "rule_source_mapping.md"


class TestKnowledgeBase(unittest.TestCase):

    def test_validates_cleanly(self):
        self.assertEqual(kb.validate(), [])

    def test_has_at_least_twenty_rules(self):
        self.assertGreaterEqual(len(kb.RULES), 20)

    def test_rule_ids_are_unique(self):
        ids = [r.rule_id for r in kb.RULES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_conclusions_are_unique(self):
        conclusions = [r.conclusion for r in kb.RULES]
        self.assertEqual(len(conclusions), len(set(conclusions)))

    def test_every_rule_cites_a_source(self):
        for r in kb.RULES:
            with self.subTest(rule=r.rule_id):
                self.assertTrue(r.source.element)
                self.assertTrue(r.source.knowledge)
                self.assertIn(r.source.priority, ("High", "Medium", "Low"))
                self.assertIn("NIST SP 800-61r3", r.source.citation())

    def test_every_rule_recommends_something(self):
        for r in kb.RULES:
            with self.subTest(rule=r.rule_id):
                self.assertTrue(r.recommendation.strip())

    def test_every_question_feeds_a_rule(self):
        read = {c.fact for r in kb.RULES for c in r.conditions
                if isinstance(c, AnswerIs)}
        self.assertEqual({q.fact for q in kb.QUESTIONS}, read)

    def test_derived_conditions_resolve_to_rules(self):
        conclusions = {r.conclusion for r in kb.RULES}
        for r in kb.RULES:
            for c in r.conditions:
                if isinstance(c, Derived):
                    with self.subTest(rule=r.rule_id, needs=c.fact):
                        self.assertIn(c.fact, conclusions)

    def test_no_rule_depends_on_itself(self):
        for r in kb.RULES:
            for c in r.conditions:
                if isinstance(c, Derived):
                    self.assertNotEqual(c.fact, r.conclusion, r.rule_id)

    def test_questions_allow_yes_and_no(self):
        for q in kb.QUESTIONS:
            with self.subTest(question=q.fact_id):
                self.assertIn(Answer.YES, q.allowed)
                self.assertIn(Answer.NO, q.allowed)

    def test_only_the_third_party_question_allows_not_applicable(self):
        allowing = [q.fact_id for q in kb.QUESTIONS
                    if Answer.NOT_APPLICABLE in q.allowed]
        self.assertEqual(allowing, ["F07"])

    def test_lookup_helpers(self):
        self.assertEqual(kb.rule("R01").conclusion, "gap_ir_policy_missing")
        self.assertEqual(kb.question_for("ir_policy_exists").fact_id, "F01")
        self.assertEqual([r.rule_id for r in
                          kb.rules_concluding("gap_ir_policy_missing")], ["R01"])
        with self.assertRaises(KeyError):
            kb.rule("R99")


class TestMatchesDocumentation(unittest.TestCase):
    """The implemented rules must match docs/rule_source_mapping.md."""

    @classmethod
    def setUpClass(cls):
        cls.text = MAPPING.read_text(encoding="utf-8")

    def test_rule_ids_match(self):
        documented = set(re.findall(r"^\*\*(R\d\d)\.", self.text, re.M))
        self.assertEqual({r.rule_id for r in kb.RULES}, documented)

    def test_primitive_conditions_match(self):
        documented = dict((f, c) for f, c in re.findall(
            r"\*Rule:\* if `([a-z_]+)` = no, then `([a-z_]+)`", self.text))
        implemented = {}
        for r in kb.RULES:
            if not r.is_derived:
                implemented[r.conditions[0].fact] = r.conclusion
        self.assertEqual(implemented, documented)

    def test_every_rule_id_appears_in_the_mapping(self):
        for r in kb.RULES:
            with self.subTest(rule=r.rule_id):
                self.assertIn(f"**{r.rule_id}.", self.text)


class TestAnswerParsing(unittest.TestCase):

    def test_accepts_common_spellings(self):
        for text, expected in [("yes", Answer.YES), ("YES", Answer.YES),
                               ("y", Answer.YES), ("no", Answer.NO),
                               ("N", Answer.NO), ("unknown", Answer.UNKNOWN),
                               ("u", Answer.UNKNOWN),
                               ("not applicable", Answer.NOT_APPLICABLE),
                               ("not-applicable", Answer.NOT_APPLICABLE),
                               ("na", Answer.NOT_APPLICABLE)]:
            with self.subTest(text=text):
                self.assertIs(Answer.parse(text), expected)

    def test_rejects_anything_else(self):
        for text in ("maybe", "", "1"):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    Answer.parse(text)


class TestFactBase(unittest.TestCase):

    def test_records_and_reports_answers(self):
        base = kb.fact_base_from({"ir_policy_exists": "no",
                                  "ir_plan_exists": Answer.UNKNOWN})
        self.assertIs(base.answer_for("ir_policy_exists"), Answer.NO)
        self.assertIs(base.answer_for("ir_plan_exists"), Answer.UNKNOWN)
        self.assertIsNone(base.answer_for("network_monitoring"))
        self.assertEqual(base.unknowns(), ["ir_plan_exists"])

    def test_reports_unanswered_questions(self):
        base = kb.fact_base_from({"ir_policy_exists": "yes"})
        missing = base.unanswered(kb.QUESTIONS)
        self.assertEqual(len(missing), len(kb.QUESTIONS) - 1)
        self.assertNotIn("ir_policy_exists", [q.fact for q in missing])

    def test_records_conclusions(self):
        base = kb.fact_base_from({})
        self.assertFalse(base.knows("gap_ir_policy_missing"))
        base.conclude("gap_ir_policy_missing", "R01")
        self.assertTrue(base.knows("gap_ir_policy_missing"))
        self.assertEqual(base.derived["gap_ir_policy_missing"], "R01")


if __name__ == "__main__":
    unittest.main()
