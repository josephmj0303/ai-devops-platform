from pydantic import BaseModel


class KubernetesNode(BaseModel):
    name: str
    status: str
    roles: list[str]
    internal_ip: str | None


class KubernetesPodStatus(BaseModel):
    total: int
    status: dict[str, int]


class KubernetesDeploymentSummary(BaseModel):
    total: int


class KubernetesDeployment(BaseModel):
    name: str
    namespace: str
    desired_replicas: int
    ready_replicas: int
    available_replicas: int


class KubernetesNodeSummary(BaseModel):
    total: int
    ready: int


class KubernetesClusterSummary(BaseModel):
    nodes: KubernetesNodeSummary
    pods: KubernetesPodStatus
    deployments: KubernetesDeploymentSummary
