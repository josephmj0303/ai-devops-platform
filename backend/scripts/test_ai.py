import asyncio
import sys
from pathlib import Path

# Add backend/src to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app.services.ai import AIService


async def main():
    service = AIService()

    response = await service.generate(
        prompt="Explain Kubernetes in one short paragraph."
    )

    print("\nAI Response:\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
