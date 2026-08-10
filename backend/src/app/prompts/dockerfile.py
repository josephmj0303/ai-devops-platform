def build_dockerfile_review_prompt(dockerfile: str) -> str:
    return f"""
You are an experienced DevOps Engineer.

Review the following Dockerfile.

Focus on:

- Security
- Image size
- Best practices
- Performance
- Production readiness

Provide practical recommendations.

Dockerfile:

{dockerfile}
"""
