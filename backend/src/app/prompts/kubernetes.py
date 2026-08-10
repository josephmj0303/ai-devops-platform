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
