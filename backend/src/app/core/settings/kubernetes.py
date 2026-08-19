from pydantic_settings import BaseSettings, SettingsConfigDict


class KubernetesSettings(BaseSettings):
    ENABLED: bool = True

    KUBECONFIG: str = "/home/vagrant/.kube/ai-devops-platform.config"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="KUBERNETES_",
        case_sensitive=True,
        extra="ignore",
    )
