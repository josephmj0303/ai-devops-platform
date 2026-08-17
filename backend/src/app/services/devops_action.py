import docker
from docker.errors import DockerException, NotFound


class DevOpsActionService:
    def __init__(self):
        self.client = docker.from_env()

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

    def restart_docker_container(
        self,
        container_name: str,
    ) -> dict:
        try:
            container = self.client.containers.get(container_name)
            container.restart()

            return {
                "action": "docker_restart",
                "target": container_name,
                "status": "completed",
                "message": "Container restarted successfully",
            }

        except NotFound:
            return {
                "action": "docker_restart",
                "target": container_name,
                "status": "failed",
                "message": "Container not found",
            }

        except DockerException as exc:
            return {
                "action": "docker_restart",
                "target": container_name,
                "status": "failed",
                "message": f"Docker action failed: {exc}",
            }
