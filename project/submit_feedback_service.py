from typing import Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class FeedbackSubmissionResponse(BaseModel):
    """
    A simple confirmation that the user's feedback has been received and processed. Optionally, it might include updated feedback statistics for the joke.
    """

    success: bool
    message: str
    updatedLikes: Optional[int] = None
    updatedDislikes: Optional[int] = None


async def submit_feedback(
    jokeId: str, feedbackText: Optional[str], feedbackType: str
) -> FeedbackSubmissionResponse:
    """
    Endpoint for users to submit feedback on a joke.

    Args:
    jokeId (str): The unique identifier of the joke for which feedback is being submitted. This is captured from the URL path.
    feedbackText (Optional[str]): The textual feedback provided by the user. This is optional as a user might only want to leave a like or dislike.
    feedbackType (str): The type of feedback being submitted. This can be 'like', 'dislike', or 'text' for textual feedback.

    Returns:
    FeedbackSubmissionResponse: A simple confirmation that the user's feedback has been received and processed. Optionally, it might include updated feedback statistics for the joke.

    Raises:
    HTTPException: If the joke does not exist or feedback type is invalid.
    """
    joke = await prisma.models.Joke.prisma().find_unique(where={"id": jokeId})
    if not joke:
        return FeedbackSubmissionResponse(success=False, message="Joke not found.")
    if feedbackType not in ["like", "dislike", "text"]:
        return FeedbackSubmissionResponse(
            success=False, message="Invalid feedback type."
        )
    await prisma.models.Feedback.prisma().create(
        data={
            "jokeId": jokeId,
            "userId": "user-placeholder-id",
            "content": feedbackText if feedbackText else "",
        }
    )
    updated_likes = await prisma.models.Feedback.prisma().count(
        where={"jokeId": jokeId, "content": "like"}
    )
    updated_dislikes = await prisma.models.Feedback.prisma().count(
        where={"jokeId": jokeId, "content": "dislike"}
    )
    return FeedbackSubmissionResponse(
        success=True,
        message="Feedback submitted successfully.",
        updatedLikes=updated_likes,
        updatedDislikes=updated_dislikes,
    )
