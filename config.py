from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bicqwucdvbgpau:94a09da7ef0a9c9e512130cd5efc0ab9170d55d48fc594160a76dd3c9738e303@ec2-54-225-97-112.compute-1.amazonaws.com:5432/df8l77hauvn3gt'

app.config['SECRET_KEY'] = '7"#~L?y78hWq%~NV'


