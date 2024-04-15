from datetime import datetime

import prisma
import prisma.models
from pydantic import BaseModel


class CreateJokeResponse(BaseModel):
    """
    Response after successfully adding a joke. Includes the joke's identifier and content for confirmation.
    """

    id: str
    content: str
    created_at: datetime


async def create_joke(content: str) -> CreateJokeResponse:
    """
    Allows administrators to add a new joke to the database

    Args:
        content (str): The text content of the joke to be added to the database.

    Returns:
        CreateJokeResponse: Response after successfully adding a joke. Includes the joke's identifier and content for confirmation.
    """
    new_joke = await prisma.models.Joke.prisma().create(data={"content": content})
    return CreateJokeResponse(
        id=new_joke.id, content=new_joke.content, created_at=new_joke.createdAt
    )
