def build_terraform_review_prompt(terraform: str) -> str:
    return f"""
You are an experienced DevOps Engineer.

Review the following Terraform configuration.

Focus on:

- Security
- Best practices
- Resource organization
- Naming
- Production readiness

Provide practical recommendations.

Terraform Configuration:

{terraform}
"""

def build_structured_terraform_analysis_prompt(terraform: str) -> str:
    return f"""
You are an experienced Terraform and DevOps Engineer.

Analyze the following Terraform configuration and return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
  "severity": "low | medium | high | critical",
  "component": "Terraform",
  "summary": "short summary of the overall Terraform configuration assessment",
  "findings": [
    "specific finding 1",
    "specific finding 2"
  ],
  "recommended_actions": [
    "practical recommendation 1",
    "practical recommendation 2"
  ]
}}

Rules:

- Do not use Markdown.
- Do not wrap the JSON in ```json or ``` blocks.
- severity must be one of: low, medium, high, critical.
- component must be exactly "Terraform".
- findings must contain concrete observations from the provided configuration.
- recommended_actions must contain practical Terraform and DevOps recommendations.
- Focus on:
  - security
  - IAM and access
  - hardcoded credentials
  - resource configuration
  - naming
  - organization
  - state management
  - variables
  - outputs
  - production readiness
- Do not invent configuration that is not present.

Terraform Configuration:

{terraform}
"""
