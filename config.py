import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate

with open('database.yaml', 'r') as file:
    config = yaml.safe_load(file)

class Config:
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{config['database']['user']}:{config['database']['password']}"
                               f"@{config['database']['host']}:{config['database']['port']}/{config['database']['dbname']}")
app = Flask(__name__)
app.config.from_object(Config)
Session(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

student_categorys={
    11:'本科生',
    13:'本科交换生',
    18:'本科留学生',
    31:'学术研究生',
    32:'专业研究生',
    33:'研究生交换生',
    38:'研究生留学生',
}
