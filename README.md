---
date: 2024-04-15T18:12:17.959234
author: AutoGPT <info@agpt.co>
---

# joke-api

To develop a single API that returns one tech joke, the recommended tech stack includes Python as the programming language due to its simplicity and extensive library support. FastAPI is chosen for the API framework for its performance benefits, ease of use for creating RESTful APIs, and built-in support for data validation and serialization. PostgreSQL will serve as the database, renowned for its reliability, capability to handle complex queries, scalability, and strong community support. Prisma is the preferred ORM for this project, considering its modern approach to database management, type safety features, and straightforward syntax which aligns well with Python and FastAPI. This setup will efficiently handle the delivery of tech jokes, ensuring a robust, scalable, and maintainable architecture. The API will return a single tech joke, catering specifically to users with a preference for tech-focused humor, thereby making the content both educational and entertaining for a tech-savvy audience.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'joke-api'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
