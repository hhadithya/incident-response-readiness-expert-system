# Knowledge Engineering Process

This project follows the knowledge engineering sequence below.

```
Domain Selection -> Domain Study -> Knowledge Acquisition -> Knowledge Representation
   -> Facts and Rules -> Inference -> Testing -> Explanation
```

| Step | Where it lives |
|---|---|
| Domain selection | Scope statement in [README.md](../README.md) |
| Domain study | Analysis of NIST SP 800-61r3 |
| Knowledge acquisition | [rule_source_mapping.md](rule_source_mapping.md) |
| Knowledge representation | CLIPS templates in [`src/rules.clp`](../src/rules.clp) |
| Facts and rules | [`src/questions.clp`](../src/questions.clp), [`src/rules.clp`](../src/rules.clp) |
| Inference | The CLIPS forward chaining engine, driven from [`src/main.clp`](../src/main.clp) |
| Explanation | [`src/explanations.clp`](../src/explanations.clp) |
| Testing | [`tests/test_scenarios.clp`](../tests/test_scenarios.clp), [test_results.md](test_results.md) |

## Knowledge acquisition method

No domain expert was interviewed. Interviewing an expert is not mandatory for this assignment provided all domain knowledge is grounded in a valid external source.

Knowledge was acquired by document analysis of the publication listed in [sources.md](sources.md). Each rule is traced back to a specific location in that document before it is implemented, and the trace is carried in the rule itself so the running system can cite it.

## Inference

The system does not implement its own inference engine. Answers become facts in CLIPS working memory, the CLIPS pattern matcher tests them against the rule conditions, matching rules enter the agenda and fire, and the findings they assert can in turn satisfy further rules. That is the native forward chaining the CLIPS shell provides.
