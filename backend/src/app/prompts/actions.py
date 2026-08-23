def build_action_intent_prompt(prompt: str) -> str:
    return f"""
You are an AI assistant for a DevOps platform.

Determine whether the user's request requires an executable DevOps action.

Currently supported actions:

1. docker_restart
   - Restart a Docker container.
   - target should be the container name.

2. kubernetes_restart_deployment
   - Restart a Kubernetes deployment.
   - target should be the deployment name.
   - namespace should contain the Kubernetes namespace.

If the request does not clearly match one of the supported actions,
return is_action=false.

Return ONLY valid JSON using exactly this structure:

{{
  "is_action": true,
  "action": "docker_restart | kubernetes_restart_deployment | null",
  "target": "target name or null",
  "namespace": "namespace or null",
  "parameters": {{}},
  "reason": "short explanation"
}}

Rules:

- Return JSON only.
- Do not use Markdown.
- Do not wrap the JSON in code fences.
- is_action must be true only when the user clearly requests an executable action.
- action must be one of the supported actions or null.
- target must contain the requested target when it is clearly identifiable.
- namespace is required for Kubernetes actions when provided or identifiable.
- Do not invent target names.
- Do not invent namespaces.
- If the target is unclear, return is_action=false.
- parameters must always be a JSON object.
- reason must briefly explain the decision.

User request:

{prompt}
"""
