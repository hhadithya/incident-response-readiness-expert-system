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
| Knowledge representation | Rule and fact schemas in [`src/knowledge_base.py`](../src/knowledge_base.py) and [`src/facts.py`](../src/facts.py) |
| Facts and rules | [`src/facts.py`](../src/facts.py), [`src/knowledge_base.py`](../src/knowledge_base.py) |
| Inference | [`src/inference_engine.py`](../src/inference_engine.py) |
| Explanation | [`src/explanation.py`](../src/explanation.py) |
| Interface | [`src/main.py`](../src/main.py) |
| Testing | [`tests/`](../tests), [test_cases.md](test_cases.md) |

## Knowledge acquisition method

No domain expert was interviewed. Interviewing an expert is not mandatory for this assignment, provided all domain knowledge is grounded in a valid external source.

Knowledge is therefore acquired by document analysis of the publication listed in [sources.md](sources.md). Each candidate rule is traced back to a specific location in that document before it is implemented, and the trace is preserved in the executable rule definition so that the running system can cite it.
