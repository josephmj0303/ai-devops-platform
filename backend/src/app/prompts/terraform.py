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
