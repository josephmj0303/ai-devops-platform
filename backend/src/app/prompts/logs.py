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
You are an experienced DevOps Engineer analyzing application logs.

Analyze the logs and return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
  "severity": "low | medium | high | critical",
  "component": "single concise component name, such as PostgreSQL, Redis, Docker, Kubernetes, FastAPI, or Nginx",  "summary": "short summary of the incident",
  "likely_cause": "most likely root cause",
  "impact": "likely impact on the application or infrastructure",
  "recommended_actions": [
    "action 1",
    "action 2",
    "action 3"
  ]
}}

Rules:

- Do not use Markdown.
- Do not wrap the JSON in ```json or ``` blocks.
- severity must be one of: low, medium, high, critical.
- recommended_actions must be a JSON array of practical troubleshooting or remediation actions.
- Base the analysis on the provided logs.
- Do not invent specific infrastructure details that are not supported by the logs.
- component must contain only one concise component name.
- Do not return multiple names separated by commas.

Application Logs:

{logs}
"""
