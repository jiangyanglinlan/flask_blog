from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_mail import Mail


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
mail = Mail()