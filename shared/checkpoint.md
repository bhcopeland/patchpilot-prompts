ANALYSIS CHECKPOINT — Do not produce your verdict yet.

Re-read the Bypassed Validation and Explanation Quality sections from your instructions. Verify you have checked every new code path against the existing validation below it. Make additional tool calls if needed.

{questions}

WARNINGS FILTER — Before emitting warnings, discard any that are:
- Operational advice (verify URLs, update CI, rebuild caches, update documentation)
- Process suggestions (run tests, check compatibility, plan for future conflicts)
- Obvious context (submodule URLs point to well-known upstream projects)
- Style or naming preferences

Only emit warnings about concrete code issues you can prove with evidence: bugs, regressions, bypassed validation, security problems, or missing error handling on reachable paths.

Then produce your final JSON verdict. Your explanation must prove each issue to someone who has not read the code — quote the bypassed check, walk through a concrete failure with specific values, and state the correct behaviour.
