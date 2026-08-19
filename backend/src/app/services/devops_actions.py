from app.schemas.devops_action import AvailableAction


class DevOpsActionCatalog:
    _actions = {
        "Docker": [
            AvailableAction(
                action="docker_restart",
                name="Restart Docker Container",
                description="Restart a selected Docker container.",
                target_type="container",
                enabled=True,
            )
        ],
        "Kubernetes": [
            AvailableAction(
                action="kubernetes_restart_deployment",
                name="Restart Kubernetes Deployment",
                description="Restart a selected Kubernetes deployment.",
                target_type="deployment",
                enabled=True,
            )
        ],
        "Terraform": [],
        "PostgreSQL": [],
    }

    @classmethod
    def get_actions(
        cls,
        component: str,
    ) -> list[AvailableAction]:
        return cls._actions.get(component, [])
