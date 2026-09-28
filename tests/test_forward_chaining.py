"""Forward chaining behaviour."""

import unittest

from src import knowledge_base as kb
from src.inference_engine import forward_chain
from src.models import Answer

ALL_FACTS = [q.fact for q in kb.QUESTIONS]


def answers(**overrides):
    """Every question answered yes, except the ones named."""
    base = {fact: "yes" for fact in ALL_FACTS}
    base.update(overrides)
    return kb.fact_base_from(base)


class TestFiring(unittest.TestCase):

    def test_nothing_fires_when_everything_is_in_place(self):
        result = forward_chain(answers())
        self.assertEqual(result.firings, ())
        self.assertEqual(result.cycles, 0)

    def test_one_rule_fires(self):
        result = forward_chain(answers(ir_policy_exists="no"))
        self.assertEqual(result.rule_ids(), ["R01"])
        self.assertEqual(result.conclusions(), ["gap_ir_policy_missing"])

    def test_several_independent_rules_fire(self):
        result = forward_chain(answers(ir_policy_exists="no",
                                       ir_roles_documented="no",
                                       role_based_ir_training="no"))
        self.assertEqual(sorted(result.rule_ids()), ["R01", "R02", "R06"])

    def test_unrelated_rules_stay_quiet(self):
        result = forward_chain(answers(ir_policy_exists="no"))
        for rule_id in ("R02", "R09", "R14", "R19", "R25", "R26", "R27"):
            with self.subTest(rule=rule_id):
                self.assertFalse(result.fired(rule_id))

    def test_each_rule_fires_on_its_own_fact(self):
        for rule in kb.RULES:
            if rule.is_derived:
                continue
            fact = rule.conditions[0].fact
            with self.subTest(rule=rule.rule_id):
                result = forward_chain(answers(**{fact: "no"}))
                self.assertIn(rule.rule_id, result.rule_ids())

    def test_a_rule_fires_at_most_once(self):
        result = forward_chain(answers(ir_policy_exists="no", ir_plan_exists="no"))
        self.assertEqual(len(result.rule_ids()), len(set(result.rule_ids())))

    def test_recommendations_are_not_repeated(self):
        result = forward_chain(answers(**{f: "no" for f in ALL_FACTS}))
        texts = [f.recommendation for f in result.recommendations()]
        self.assertEqual(len(texts), len(set(texts)))


class TestUnknownAnswers(unittest.TestCase):

    def test_unknown_does_not_fire_a_rule(self):
        result = forward_chain(answers(ir_policy_exists="unknown"))
        self.assertEqual(result.firings, ())

    def test_unknown_is_reported_as_not_assessed(self):
        result = forward_chain(answers(ir_policy_exists="unknown"))
        self.assertIn(("ir_policy_exists", "R01"), result.not_assessed)

    def test_unknown_does_not_reach_a_derived_rule(self):
        result = forward_chain(answers(logs_generated_and_available="unknown",
                                       network_monitoring="unknown",
                                       endpoint_and_service_monitoring="unknown"))
        self.assertFalse(result.fired("R25"))

    def test_not_applicable_does_not_fire_a_rule(self):
        result = forward_chain(answers(third_parties_in_ir_planning="not_applicable"))
        self.assertFalse(result.fired("R07"))

    def test_missing_answers_are_reported(self):
        result = forward_chain(kb.fact_base_from({"ir_policy_exists": "no"}))
        missing = {fact for fact, _ in result.unanswered}
        self.assertNotIn("ir_policy_exists", missing)
        self.assertIn("network_monitoring", missing)


class TestChaining(unittest.TestCase):

    def test_a_derived_rule_fires_after_the_rule_it_depends_on(self):
        result = forward_chain(answers(network_monitoring="no"))
        self.assertEqual(result.rule_ids(), ["R09", "R25"])
        self.assertEqual([f.cycle for f in result.firings], [1, 2])
        self.assertEqual(result.cycles, 2)

    def test_the_derived_rule_records_what_triggered_it(self):
        result = forward_chain(answers(network_monitoring="no"))
        rollup = next(f for f in result.firings if f.rule_id == "R25")
        self.assertEqual([e.fact for e in rollup.evidence], ["gap_no_network_monitoring"])
        self.assertEqual(rollup.evidence[0].concluded_by, "R09")

    def test_any_one_input_is_enough_for_a_derived_rule(self):
        for fact in ("logs_generated_and_available", "network_monitoring",
                     "endpoint_and_service_monitoring"):
            with self.subTest(fact=fact):
                result = forward_chain(answers(**{fact: "no"}))
                self.assertTrue(result.fired("R25"))

    def test_a_derived_rule_reports_every_input_that_held(self):
        result = forward_chain(answers(network_monitoring="no",
                                       endpoint_and_service_monitoring="no"))
        rollup = next(f for f in result.firings if f.rule_id == "R25")
        self.assertEqual(sorted(e.fact for e in rollup.evidence),
                         ["gap_no_endpoint_monitoring", "gap_no_network_monitoring"])

    def test_recovery_preparedness_chains_from_backups(self):
        result = forward_chain(answers(backups_created_and_tested="no"))
        self.assertEqual(result.rule_ids(), ["R19", "R27"])

    def test_derived_rules_do_not_fire_without_their_inputs(self):
        result = forward_chain(answers(ir_policy_exists="no"))
        for rule_id in ("R25", "R26", "R27"):
            self.assertFalse(result.fired(rule_id))


class TestSettling(unittest.TestCase):

    def test_everything_missing_fires_every_rule(self):
        result = forward_chain(answers(**{f: "no" for f in ALL_FACTS}))
        self.assertEqual(sorted(result.rule_ids()),
                         sorted(r.rule_id for r in kb.RULES))
        self.assertEqual(result.cycles, 2)

    def test_running_again_adds_nothing(self):
        facts = answers(network_monitoring="no")
        first = forward_chain(facts)
        second = forward_chain(first.facts)
        self.assertEqual(second.firings, ())

    def test_conclusions_are_recorded_against_the_rule_that_made_them(self):
        result = forward_chain(answers(network_monitoring="no"))
        self.assertEqual(result.facts.derived["gap_no_network_monitoring"], "R09")
        self.assertEqual(result.facts.derived["detection_capability_incomplete"], "R25")


class TestEvidence(unittest.TestCase):

    def test_a_primitive_firing_records_the_answer_given(self):
        result = forward_chain(answers(ir_policy_exists="no"))
        evidence = result.firings[0].evidence
        self.assertEqual(len(evidence), 1)
        self.assertEqual(evidence[0].fact, "ir_policy_exists")
        self.assertIs(evidence[0].answer, Answer.NO)
        self.assertEqual(evidence[0].describe(), "ir_policy_exists = no")

    def test_a_firing_carries_its_source(self):
        result = forward_chain(answers(ir_policy_exists="no"))
        source = result.firings[0].source
        self.assertEqual(source.element, "GV.PO.R1")
        self.assertEqual(source.priority, "High")
        self.assertIn("NIST SP 800-61r3", source.citation())


if __name__ == "__main__":
    unittest.main()
