from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import db


class Timesheets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    Slots = relationship("Slots", back_populates="Timesheets")


class Slots(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hour = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)
    timesheet_id = db.Column(db.Integer, ForeignKey('timesheets.id'))
    Timesheets = relationship("Timesheets", back_populates="Slots")
    Subslots = relationship("Subslots", back_populates="Slots")


class Subslots(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slot_id = db.Column(db.Integer, ForeignKey('slots.id'))
    Slots = relationship("Slots", back_populates="Subslots")
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    task_id = db.Column(db.Integer)


class TimesheetsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Timesheets
        include_relationships = True
        load_instance = True


class SlotsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Slots
        include_relationships = True
        load_instance = True


class SubslotsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subslots
        include_relationships = True
        load_instance = True
