"""Core data structures for the expert system."""

from dataclasses import dataclass, field
from enum import Enum


class Answer(str, Enum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"
    NOT_APPLICABLE = "not_applicable"

    @classmethod
    def parse(cls, text):
        key = text.strip().lower().replace(" ", "_").replace("-", "_")
        aliases = {"y": cls.YES, "n": cls.NO, "u": cls.UNKNOWN, "na": cls.NOT_APPLICABLE,
                   "n_a": cls.NOT_APPLICABLE, "not_applicable": cls.NOT_APPLICABLE}
        if key in aliases:
            return aliases[key]
        return cls(key)


class Group(str, Enum):
    PREPARATION = "Preparation and governance"
    DETECTION = "Detection"
    RESPONSE = "Response"
    RECOVERY = "Recovery and improvement"


@dataclass(frozen=True)
class SourceReference:
    """A location in NIST SP 800-61r3, with the knowledge taken from it."""

    element: str
    table: str
    pdf_page: str
    doc_page: str
    priority: str
    knowledge: str
    document: str = "NIST SP 800-61r3"

    def citation(self):
        return (f"{self.document}, {self.element}, {self.table}, "
                f"PDF p. {self.pdf_page} (doc p. {self.doc_page})")


@dataclass(frozen=True)
class AnswerIs:
    """Satisfied when the user gave `value` for `fact`."""

    fact: str
    value: Answer

    def describe(self):
        return f"{self.fact} = {self.value.value}"


@dataclass(frozen=True)
class Derived:
    """Satisfied when another rule has concluded `fact`."""

    fact: str

    def describe(self):
        return f"{self.fact} was concluded"


@dataclass(frozen=True)
class Rule:
    rule_id: str
    name: str
    group: Group
    conditions: tuple
    conclusion: str
    recommendation: str
    source: SourceReference
    match: str = "all"

    def __post_init__(self):
        if self.match not in ("all", "any"):
            raise ValueError(f"{self.rule_id}: match must be 'all' or 'any'")
        if not self.conditions:
            raise ValueError(f"{self.rule_id}: no conditions")

    @property
    def is_derived(self):
        return any(isinstance(c, Derived) for c in self.conditions)

    def describe_condition(self):
        parts = [c.describe() for c in self.conditions]
        if len(parts) == 1:
            return parts[0]
        joiner = " and " if self.match == "all" else " or "
        return joiner.join(parts)


@dataclass(frozen=True)
class Question:
    fact_id: str
    fact: str
    text: str
    group: Group
    allowed: tuple = (Answer.YES, Answer.NO, Answer.UNKNOWN)


@dataclass
class FactBase:
    """Working memory: the answers given, and the facts rules have concluded."""

    answers: dict = field(default_factory=dict)
    derived: dict = field(default_factory=dict)

    def record(self, fact, answer):
        self.answers[fact] = answer

    def answer_for(self, fact):
        return self.answers.get(fact)

    def conclude(self, fact, rule_id):
        self.derived[fact] = rule_id

    def knows(self, fact):
        return fact in self.derived

    def unanswered(self, questions):
        return [q for q in questions if q.fact not in self.answers]

    def unknowns(self):
        return [f for f, a in self.answers.items() if a is Answer.UNKNOWN]
