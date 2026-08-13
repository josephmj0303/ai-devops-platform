import json

from app.providers import get_provider


class AIService:

    def __init__(self):
        self.provider = get_provider()

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        response_format: str | None = None,
    ) -> str:
        return await self.provider.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            response_format=response_format,
        )

    async def analyze_logs(
        self,
        prompt: str,
    ) -> dict:
        response = await self.generate(
            prompt=prompt,
            response_format="json",
        )

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        return json.loads(response)

    async def analyze_dockerfile(
        self,
        prompt: str,
    ) -> dict:
        response = await self.generate(
            prompt=prompt,
            response_format="json",
        )

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        return json.loads(response)

    async def analyze_kubernetes(
        self,
        prompt: str,
    ) -> dict:
        response = await self.generate(
            prompt=prompt,
            response_format="json",
        )

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        return json.loads(response)

    async def analyze_terraform(
        self,
        prompt: str,
    ) -> dict:
        response = await self.generate(
            prompt=prompt,
            response_format="json",
        )

        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        return json.loads(response)
