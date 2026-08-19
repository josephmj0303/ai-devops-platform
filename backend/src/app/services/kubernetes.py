from kubernetes import client, config

from app.core.settings.loader import get_settings


class KubernetesService:

    def __init__(self):
        settings = get_settings()

        self.enabled = settings.kubernetes.ENABLED

        if not self.enabled:
            self.core_api = None
            self.apps_api = None
            return

        config.load_kube_config(
            config_file=settings.kubernetes.KUBECONFIG
        )

        self.core_api = client.CoreV1Api()
        self.apps_api = client.AppsV1Api()

    def get_nodes(self) -> list[dict]:
        nodes = self.core_api.list_node()

        return [
            {
                "name": node.metadata.name,
                "status": self._node_status(node),
                "roles": self._node_roles(node),
                "internal_ip": self._node_internal_ip(node),
            }
            for node in nodes.items
        ]

    def get_pods(self) -> list[dict]:
        pods = self.core_api.list_pod_for_all_namespaces()

        return [
            {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "restart_count": sum(
                    container.restart_count or 0
                    for container in (pod.status.container_statuses or [])
                ),
            }
            for pod in pods.items
        ]

    def get_deployments(self) -> list[dict]:
        deployments = self.apps_api.list_deployment_for_all_namespaces()

        return [
            {
                "name": deployment.metadata.name,
                "namespace": deployment.metadata.namespace,
                "desired_replicas": deployment.spec.replicas or 0,
                "ready_replicas": deployment.status.ready_replicas or 0,
                "available_replicas": (
                    deployment.status.available_replicas or 0
                ),
            }
            for deployment in deployments.items
        ]

    def restart_deployment(
        self,
        *,
        namespace: str,
        deployment_name: str,
    ) -> dict:
        if not self.enabled:
            raise RuntimeError("Kubernetes integration is disabled")

        deployment = self.apps_api.read_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
        )

        annotations = (
            deployment.spec.template.metadata.annotations
            or {}
        )

        from datetime import datetime, timezone

        annotations["ai-devops-platform/restarted-at"] = (
            datetime.now(timezone.utc).isoformat()
        )

        deployment.spec.template.metadata.annotations = annotations

        self.apps_api.patch_namespaced_deployment(
            name=deployment_name,
            namespace=namespace,
            body=deployment,
        )

        return {
            "name": deployment_name,
            "namespace": namespace,
            "status": "restarted",
        }

    def get_cluster_summary(self) -> dict:
        nodes = self.get_nodes()
        pods = self.get_pods()
        deployments = self.get_deployments()

        pod_status_counts = {}

        for pod in pods:
            status = pod["status"]
            pod_status_counts[status] = (
                pod_status_counts.get(status, 0) + 1
            )

        return {
            "nodes": {
                "total": len(nodes),
                "ready": sum(
                    node["status"] == "Ready"
                    for node in nodes
                ),
            },
            "pods": {
                "total": len(pods),
                "status": pod_status_counts,
            },
            "deployments": {
                "total": len(deployments),
            },
        }

    @staticmethod
    def _node_status(node) -> str:
        for condition in node.status.conditions or []:
            if condition.type == "Ready":
                return "Ready" if condition.status == "True" else "NotReady"

        return "Unknown"

    @staticmethod
    def _node_roles(node) -> list[str]:
        labels = node.metadata.labels or {}
        roles = []

        for key in labels:
            if key.startswith("node-role.kubernetes.io/"):
                role = key.split("/", 1)[1]
                roles.append(role)

        return roles

    @staticmethod
    def _node_internal_ip(node) -> str | None:
        for address in node.status.addresses or []:
            if address.type == "InternalIP":
                return address.address

        return None
