import yaml
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

with open('database.yaml', 'r') as file:
    config = yaml.safe_load(file)

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = (f"postgresql://{config['database']['user']}:{config['database']['password']}"
                               f"@{config['database']['host']}:{config['database']['port']}/{config['database']['dbname']}")
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
