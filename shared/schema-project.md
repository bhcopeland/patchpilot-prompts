{
    "verdict": "proceed|warn|replan|reject",
    "confidence": 5,
    "warnings": [{"text": "actionable phrase",
                  "category": "coverage|informational"}],
    "explanation": "Markdown text. Use:
        - a one-line summary, then a blank line
        - a numbered list (1. 2. 3.) for distinct issues, with one issue per item
        - **bold** for issue titles inside a list item
        - `inline code` for symbols, paths, and literal values
        - fenced ```c code blocks for relevant snippets
        For each issue, give a concrete triggering scenario with specific
        values (addresses, sizes, indices). Avoid emitting one continuous
        paragraph — every distinct issue or scenario is its own list item.",
    "issues_found": 0,
    "issue_severity": "none|low|medium|high|urgent",
    "hotspots": ["path/to/file.c:function_name"]
}
