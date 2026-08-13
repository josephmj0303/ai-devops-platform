def build_log_analysis_prompt(logs: str) -> str:
    return f"""
You are an experienced DevOps Engineer.

Analyze the following application logs.

Provide a practical and concise analysis with these sections:

1. Likely Cause
2. Troubleshooting Steps
3. Possible Fixes

Focus on actionable DevOps recommendations.

Application Logs:

{logs}
"""


def build_structured_log_analysis_prompt(logs: str) -> str:
    return f"""
You are an experienced DevOps Engineer.

Analyze the application logs below.

Return ONLY ONE JSON OBJECT.

The JSON object MUST contain these six fields:

- severity
- component
- summary
- likely_cause
- impact
- recommended_actions

Use this exact JSON structure:

{{
  "severity": "critical",
  "component": "PostgreSQL",
  "summary": "Connection to PostgreSQL failed",
  "likely_cause": "PostgreSQL connection was refused",
  "impact": "Application cannot access the database",
  "recommended_actions": [
    "Verify PostgreSQL is running",
    "Check connectivity between the application and PostgreSQL",
    "Verify the database connection configuration"
  ]
}}

STRICT RULES:

1. Return JSON only.
2. Do not return Markdown.
3. Do not return ```json.
4. Do not add any text before or after the JSON object.
5. The "severity" field MUST contain exactly one of:
   "low", "medium", "high", "critical".
6. The "component" field MUST be one concise component name.
7. The "summary" field MUST be a short description of the problem.
8. The "likely_cause" field MUST contain the most likely cause.
9. The "impact" field MUST describe the effect on the application or infrastructure.
10. The "recommended_actions" field MUST be a JSON array containing practical actions.
11. Do not omit any field.
12. Do not use null for any field.
13. Do not use empty strings.
14. Base the analysis only on the provided logs.
15. Do not invent infrastructure details that are not supported by the logs.

Application Logs:

{logs}
"""
