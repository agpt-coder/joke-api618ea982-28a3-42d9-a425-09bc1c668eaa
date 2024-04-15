import random

import prisma
import prisma.models
from pydantic import BaseModel


class RandomJoke(BaseModel):
    """
    The response model for the 'get_random_tech_joke' endpoint providing a single random tech joke to the requester. This model will encompass the essential details of a joke such as its content, ensuring the joke is delivered in a format that is both consumable and compliant with the expectations of tech-savvy users.
    """

    id: str
    content: str
    createdAt: str
    updatedAt: str


async def get_random_tech_joke() -> RandomJoke:
    """
    Returns a random tech joke from the database

    This function fetches a list of non-deleted jokes from the database,
    selects one at random, and maps the selected joke to the RandomJoke model.

    Args:
        None

    Returns:
        RandomJoke: The response model for the 'get_random_tech_joke' endpoint providing
        a single random tech joke to the requester. This model will encompass the essential
        details of a joke such as its content, ensuring the joke is delivered in a format that is
        both consumable and compliant with the expectations of tech-savvy users.

    Example:
        get_random_tech_joke()
        > RandomJoke(id="123", content="Why do programmers prefer dark mode? Because light attracts bugs.",
                     createdAt="2022-01-01T12:00:00", updatedAt="2022-01-01T12:00:00")
    """
    jokes = await prisma.models.Joke.prisma().find_many(where={"deleted": False})
    if jokes:
        random_joke = random.choice(jokes)
        return RandomJoke(
            id=random_joke.id,
            content=random_joke.content,
            createdAt=random_joke.createdAt.isoformat(),
            updatedAt=random_joke.updatedAt.isoformat(),
        )
    else:
        return RandomJoke(
            id="0",
            content="No jokes available.",
            createdAt="1970-01-01T00:00:00",
            updatedAt="1970-01-01T00:00:00",
        )
