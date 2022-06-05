from project.config import DevelopmentConfig
from project.dao.models.director import Director  # noqa F401, F403
from project.dao.models.genre import Genre  # noqa F401, F403
from project.dao.models.movie import Movie  # noqa F401, F403
from project.dao.models.users import User  # noqa F401, F403
from project.server import create_app
from project.setup_db import db

app = create_app(DevelopmentConfig)

with app.app_context():
    db.drop_all()
    db.create_all()
