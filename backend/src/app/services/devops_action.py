import docker
from docker.errors import DockerException, NotFound
from kubernetes.client.exceptions import ApiException

from app.repositories.devops_action import DevOpsActionRepository
from app.services.kubernetes import KubernetesService

class DevOpsActionService:
    def __init__(
        self,
        repository: DevOpsActionRepository | None = None,
    ):
        self.client = docker.from_env()
        self.kubernetes = KubernetesService()
        self.repository = repository

    def list_docker_containers(self) -> list[dict]:
        containers = self.client.containers.list()

        return [
            {
                "name": container.name,
                "status": container.status,
                "image": (
                    container.image.tags[0]
                    if container.image.tags
                    else container.image.short_id
                ),
            }
            for container in containers
        ]

    async def restart_docker_container(
        self,
        *,
        user_id,
        analysis_id: int,
        container_name: str,
    ) -> dict:
        action = "docker_restart"

        try:
            container = self.client.containers.get(
                container_name
            )

            container.restart()

            status = "completed"
            message = "Container restarted successfully"

        except NotFound:
            status = "failed"
            message = "Container not found"

        except DockerException as exc:
            status = "failed"
            message = f"Docker action failed: {exc}"

        if self.repository is not None:
            await self.repository.create(
                user_id=user_id,
                analysis_id=analysis_id,
                action=action,
                target=container_name,
                status=status,
                message=message,
            )

        return {
            "action": action,
            "target": container_name,
            "status": status,
            "message": message,
        }

    async def restart_kubernetes_deployment(
        self,
        *,
        user_id,
        analysis_id: int,
        namespace: str,
        deployment_name: str,
    ) -> dict:
        action = "kubernetes_restart_deployment"
        target = f"{namespace}/{deployment_name}"

        try:
            self.kubernetes.restart_deployment(
                namespace=namespace,
                deployment_name=deployment_name,
            )

            status = "completed"
            message = "Kubernetes deployment restarted successfully"

        except ApiException as exc:
            status = "failed"
            message = f"Kubernetes action failed: {exc.reason}"

        except Exception as exc:
            status = "failed"
            message = f"Kubernetes action failed: {exc}"

        if self.repository is not None:
            await self.repository.create(
                user_id=user_id,
                analysis_id=analysis_id,
                action=action,
                target=target,
                status=status,
                message=message,
            )

        return {
            "action": action,
            "target": target,
            "status": status,
            "message": message,
        }
