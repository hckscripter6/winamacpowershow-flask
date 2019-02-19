from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wjkuybwrjllzoi:b241032ce098ab7709929f39be0ab3ea831693657bfc573e5c982df15720a306@ec2-75-101-138-26.compute-1.amazonaws.com:5432/d2t3epaqj8anqe'

app.config['SECRET_KEY'] = '7"#~L?y78hWq%~NV'


