"""Inference over the knowledge base."""

from dataclasses import dataclass

from .knowledge_base import RULES
from .models import Answer, AnswerIs, Derived

MAX_CYCLES = 100


@dataclass(frozen=True)
class Evidence:
    """One condition that helped fire a rule, and what satisfied it."""

    fact: str
    answer: Answer = None
    concluded_by: str = None

    def describe(self):
        if self.answer is not None:
            return f"{self.fact} = {self.answer.value}"
        return f"{self.fact} (concluded by {self.concluded_by})"


@dataclass(frozen=True)
class Firing:
    rule: object
    evidence: tuple
    cycle: int

    @property
    def rule_id(self):
        return self.rule.rule_id

    @property
    def conclusion(self):
        return self.rule.conclusion

    @property
    def recommendation(self):
        return self.rule.recommendation

    @property
    def source(self):
        return self.rule.source


@dataclass(frozen=True)
class ForwardResult:
    facts: object
    firings: tuple
    cycles: int
    not_assessed: tuple
    unanswered: tuple

    def fired(self, rule_id):
        return any(f.rule_id == rule_id for f in self.firings)

    def rule_ids(self):
        return [f.rule_id for f in self.firings]

    def conclusions(self):
        return [f.conclusion for f in self.firings]

    def by_group(self):
        grouped = {}
        for f in self.firings:
            grouped.setdefault(f.rule.group, []).append(f)
        return grouped

    def recommendations(self):
        seen = set()
        out = []
        for f in self.firings:
            if f.recommendation not in seen:
                seen.add(f.recommendation)
                out.append(f)
        return out


def evaluate(rule, facts):
    """Return the evidence satisfying `rule`, or None if it does not fire.

    An unknown answer satisfies nothing, so a rule never fires on one.
    """
    satisfied = []
    for condition in rule.conditions:
        if isinstance(condition, AnswerIs):
            answer = facts.answer_for(condition.fact)
            if answer is condition.value:
                satisfied.append(Evidence(condition.fact, answer=answer))
            elif rule.match == "all":
                return None
        elif isinstance(condition, Derived):
            if facts.knows(condition.fact):
                satisfied.append(Evidence(condition.fact,
                                          concluded_by=facts.derived[condition.fact]))
            elif rule.match == "all":
                return None
        else:
            raise TypeError(f"{rule.rule_id}: unsupported condition {condition!r}")

    if rule.match == "any" and not satisfied:
        return None
    return tuple(satisfied)


def forward_chain(facts, rules=RULES):
    """Fire every rule whose conditions hold, until no further rule can fire.

    Each pass collects the rules that match against the facts known at the
    start of that pass, then records their conclusions together, so the result
    does not depend on the order rules are listed in.

    A rule fires only if its conclusion is not already known, so re-running
    over a fact base that has already been through the engine adds nothing.
    """
    firings = []
    fired = set()
    cycle = 0

    while True:
        if cycle >= MAX_CYCLES:
            raise RuntimeError(f"inference did not settle within {MAX_CYCLES} cycles")
        cycle += 1

        matched = []
        for rule in rules:
            if rule.rule_id in fired or facts.knows(rule.conclusion):
                continue
            evidence = evaluate(rule, facts)
            if evidence is not None:
                matched.append((rule, evidence))

        if not matched:
            cycle -= 1
            break

        for rule, evidence in matched:
            facts.conclude(rule.conclusion, rule.rule_id)
            fired.add(rule.rule_id)
            firings.append(Firing(rule=rule, evidence=evidence, cycle=cycle))

    not_assessed = []
    for rule in rules:
        for condition in rule.conditions:
            if isinstance(condition, AnswerIs):
                if facts.answer_for(condition.fact) is Answer.UNKNOWN:
                    not_assessed.append((condition.fact, rule.rule_id))

    unanswered = []
    for rule in rules:
        for condition in rule.conditions:
            if isinstance(condition, AnswerIs) and condition.fact not in facts.answers:
                unanswered.append((condition.fact, rule.rule_id))

    return ForwardResult(facts=facts, firings=tuple(firings), cycles=cycle,
                         not_assessed=tuple(not_assessed),
                         unanswered=tuple(unanswered))
