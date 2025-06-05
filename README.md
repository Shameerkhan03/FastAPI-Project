# FastAPI Social Media Backend

A fully functional RESTful API backend for a social media-like application built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. This backend system allows users to sign up, log in, create and manage posts, and interact by liking posts — with secure authentication and scalable architecture suitable for production.

## Features

- User registration and login with JWT authentication
- Secure password hashing
- CRUD operations on social media posts
- Ability to like and unlike other users' posts
- PostgreSQL database integration using SQLAlchemy ORM
- Route modularization using FastAPI routers and tags
- Automatic interactive API documentation with Swagger UI
- Environment variable support for secure configuration
- The app is deployed on Render and can be accessed [here](https://fastapi-project-k5rp.onrender.com/docs).

## Tech Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT (OAuth2 with Password Flow)
- **Schema Validation**: Pydantic
- **Deployment**: Render (can be extended to other platforms)
- **Others**: Alembic (for migrations), Passlib (for hashing), Python-dotenv


