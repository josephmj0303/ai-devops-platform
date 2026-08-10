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
