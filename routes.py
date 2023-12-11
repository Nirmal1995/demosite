from application import app, db
from flask import render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integr, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
import re

class Userstore(db.Model):
    __tablename__ = 'userstore'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    password = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Patients(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer)
    pname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)