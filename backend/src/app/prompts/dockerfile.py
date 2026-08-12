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

def build_structured_dockerfile_analysis_prompt(dockerfile: str) -> str:
    return f"""
You are an experienced DevOps and Docker Engineer.

Analyze the following Dockerfile and return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
  "severity": "low | medium | high | critical",
  "component": "Docker",
  "summary": "short summary of the overall Dockerfile assessment",
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
- component must be exactly "Docker".
- findings must contain concrete observations from the Dockerfile.
- recommended_actions must contain practical DevOps recommendations.
- Focus on image size, security, dependency management, caching, maintainability, and production readiness.
- Do not invent configuration that is not present in the Dockerfile.

Dockerfile:

{dockerfile}
"""
