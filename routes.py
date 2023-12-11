from application import app, db
from flask import render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integr, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
import re
