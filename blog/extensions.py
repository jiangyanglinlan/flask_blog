from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()