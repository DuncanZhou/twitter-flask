# -*- coding:utf-8 -*-

from app import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)