def build_kubernetes_review_prompt(manifest: str) -> str:
    return f"""
You are an experienced Kubernetes and DevOps Engineer.

Review the following Kubernetes manifest.

Focus on:

- Image tags
- Resource requests and limits
- Liveness and readiness probes
- Security
- Production readiness

Provide practical recommendations.

Kubernetes Manifest:

{manifest}
"""

def build_structured_kubernetes_analysis_prompt(manifest: str) -> str:
    return f"""
You are an experienced Kubernetes and DevOps Engineer.

Analyze the following Kubernetes manifest and return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
  "severity": "low | medium | high | critical",
  "component": "Kubernetes",
  "summary": "short summary of the overall Kubernetes manifest assessment",
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
- component must be exactly "Kubernetes".
- findings must contain concrete observations from the provided manifest.
- recommended_actions must contain practical Kubernetes recommendations.
- Focus on:
  - image tags
  - resource requests and limits
  - liveness and readiness probes
  - security context
  - privileged containers
  - configuration and secrets
  - replicas and availability
  - production readiness
- Do not invent configuration that is not present in the manifest.

Kubernetes Manifest:

{manifest}
"""
