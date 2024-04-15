from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateJokeResponse(BaseModel):
    """
    Response model confirming the successful update of a joke, including the updated joke information or error messages in case of failure.
    """

    success: bool
    message: Optional[str] = None
    updated_joke: prisma.models.Joke


class Joke:
    """
    The joke object representing the structure of a joke as stored in the database.
    """

    def __init__(
        self, id: str, content: str, createdAt: str, updatedAt: str, deleted: bool
    ):
        self.id = id
        self.content = content
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.deleted = deleted


async def update_joke(jokeId: str, content: str) -> UpdateJokeResponse:
    """
    Enables joke details updating by administrators.

    Args:
        jokeId (str): The unique identifier for the joke to be updated. This is a path parameter.
        content (str): The updated content of the joke.

    Returns:
        UpdateJokeResponse: Response model confirming the successful update of a joke, including the updated joke information or error messages in case of failure.
    """
    try:
        joke = await prisma.models.Joke.prisma().find_unique(where={"id": jokeId})
        if joke is None:
            return UpdateJokeResponse(
                success=False,
                message="prisma.models.Joke not found.",
                updated_joke=None,
            )
        await prisma.models.Joke.prisma().update(
            where={"id": jokeId}, data={"content": content}
        )
        updated_joke = await prisma.models.Joke.prisma().find_unique(
            where={"id": jokeId}
        )
        return UpdateJokeResponse(
            success=True,
            message="prisma.models.Joke updated successfully.",
            updated_joke=prisma.models.Joke(
                id=updated_joke.id,
                content=updated_joke.content,
                createdAt=str(updated_joke.createdAt),
                updatedAt=str(updated_joke.updatedAt),
                deleted=updated_joke.deleted,
            ),
        )
    except Exception as e:
        return UpdateJokeResponse(
            success=False,
            message=f"Failed to update joke due to an error: {str(e)}",
            updated_joke=None,
        )
