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
        "Kubernetes": [],
        "Terraform": [],
        "PostgreSQL": [],
    }

    @classmethod
    def get_actions(
        cls,
        component: str,
    ) -> list[AvailableAction]:
        return cls._actions.get(component, [])
