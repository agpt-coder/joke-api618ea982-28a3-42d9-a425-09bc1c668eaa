import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.create_joke_service
import project.delete_joke_service
import project.get_random_tech_joke_service
import project.submit_feedback_service
import project.update_joke_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="joke-api",
    lifespan=lifespan,
    description="To develop a single API that returns one tech joke, the recommended tech stack includes Python as the programming language due to its simplicity and extensive library support. FastAPI is chosen for the API framework for its performance benefits, ease of use for creating RESTful APIs, and built-in support for data validation and serialization. PostgreSQL will serve as the database, renowned for its reliability, capability to handle complex queries, scalability, and strong community support. Prisma is the preferred ORM for this project, considering its modern approach to database management, type safety features, and straightforward syntax which aligns well with Python and FastAPI. This setup will efficiently handle the delivery of tech jokes, ensuring a robust, scalable, and maintainable architecture. The API will return a single tech joke, catering specifically to users with a preference for tech-focused humor, thereby making the content both educational and entertaining for a tech-savvy audience.",
)


@app.post("/admin/jokes", response_model=project.create_joke_service.CreateJokeResponse)
async def api_post_create_joke(
    content: str,
) -> project.create_joke_service.CreateJokeResponse | Response:
    """
    Allows administrators to add a new joke to the database
    """
    try:
        res = await project.create_joke_service.create_joke(content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/feedback/jokes/{jokeId}",
    response_model=project.submit_feedback_service.FeedbackSubmissionResponse,
)
async def api_post_submit_feedback(
    jokeId: str, feedbackText: Optional[str], feedbackType: str
) -> project.submit_feedback_service.FeedbackSubmissionResponse | Response:
    """
    Endpoint for users to submit feedback on a joke
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            jokeId, feedbackText, feedbackType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/jokes/random", response_model=project.get_random_tech_joke_service.RandomJoke
)
async def api_get_get_random_tech_joke() -> project.get_random_tech_joke_service.RandomJoke | Response:
    """
    Returns a random tech joke from the database
    """
    try:
        res = await project.get_random_tech_joke_service.get_random_tech_joke()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/admin/jokes/{jokeId}",
    response_model=project.delete_joke_service.DeleteJokeResponse,
)
async def api_delete_delete_joke(
    jokeId: str,
) -> project.delete_joke_service.DeleteJokeResponse | Response:
    """
    Allows for deletion of a joke entry by administrators
    """
    try:
        res = await project.delete_joke_service.delete_joke(jokeId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/admin/jokes/{jokeId}",
    response_model=project.update_joke_service.UpdateJokeResponse,
)
async def api_put_update_joke(
    jokeId: str, content: str
) -> project.update_joke_service.UpdateJokeResponse | Response:
    """
    Enables joke details updating by administrators
    """
    try:
        res = await project.update_joke_service.update_joke(jokeId, content)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
