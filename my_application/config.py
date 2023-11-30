import pathlib
import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta



basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)


app = connex_app.app
app.secret_key= "dhajnfapokèfg"
app.permanent_session_lifetime = timedelta(seconds= 10)

#configurazione DataBase 
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'data_website.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)