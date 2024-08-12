from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from sqlalchemy import MetaData
from config import Config
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

# Instantiate REST API
api = Api(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5174"}})

from app import models, routes
