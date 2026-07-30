from app.models.project import Project
from app.models.user import User
from app.models.role import UserRole
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(
        self,
        data: ProjectCreate,
        current_user: User,
    ) -> Project:
        project = Project(
            name=data.name,
            description=data.description,
            owner_id=current_user.id,
        )

        return await self.repository.create(project)

    async def list_projects(
        self,
        current_user: User,
    ) -> list[Project]:
        return await self.repository.list_by_owner(current_user.id)

    async def get_project(
        self,
        project_id: int,
        current_user: User,
    ) -> Project | None:

        project = await self.repository.get_by_id(project_id)

        if project is None:
            return None

        if (
            project.owner_id != current_user.id
            and current_user.role != UserRole.ADMIN
        ):
            raise PermissionError("Access denied")

        return project

    async def update_project(
        self,
        project: Project,
        data: ProjectUpdate,
    ) -> Project:

        if data.name is not None:
            project.name = data.name

        if data.description is not None:
            project.description = data.description

        return await self.repository.update(project)

    async def delete_project(
        self,
        project: Project,
    ) -> None:

        await self.repository.delete(project)
