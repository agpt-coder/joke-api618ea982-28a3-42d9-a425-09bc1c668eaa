import prisma
import prisma.models
from pydantic import BaseModel


class DeleteJokeResponse(BaseModel):
    """
    This response model communicates the result of a delete joke operation, including confirmation of deletion or any errors encountered, such as non-existent jokeId or insufficient permissions.
    """

    message: str


async def delete_joke(jokeId: str) -> DeleteJokeResponse:
    """
    Allows for deletion of a joke entry by administrators.

    Args:
    jokeId (str): The unique identifier of the joke to be deleted.

    Returns:
    DeleteJokeResponse: This response model communicates the result of a delete joke operation, including confirmation of deletion or any errors encountered, such as non-existent jokeId or insufficient permissions.
    """
    joke = await prisma.models.Joke.prisma().find_unique(where={"id": jokeId})
    if joke is None:
        return DeleteJokeResponse(message=f"Joke with ID {jokeId} does not exist.")
    elif joke.deleted:
        return DeleteJokeResponse(
            message=f"Joke with ID {jokeId} has already been deleted."
        )
    else:
        await prisma.models.Joke.prisma().update(
            where={"id": jokeId}, data={"deleted": True}
        )
        return DeleteJokeResponse(message="Joke successfully deleted.")
