from project.config import DevelopmentConfig
from project.dao.models.genre import Genre
from project.dao.models.director import Director
from project.dao.models.movie import Movie
from project.dao.models.users import User
from project.server import create_app, db

app = create_app(DevelopmentConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
        "Director": Director,
        "Movie": Movie,
        "User": User,
    }
