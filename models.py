from flask_marshmallow import Schema
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import db


class Timesheets(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    Slots = relationship("Slots", backref="timesheet")
    ppm_synced = db.Column(db.Integer)
    ppm_last_sync = db.Column(db.Date)


class Slots(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hour = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)
    timesheet_id = db.Column(db.Integer, ForeignKey('timesheets.id'))
    Subslots = relationship("Subslots", backref="subslot")
    Timesheet = relationship('Timesheets', foreign_keys='Slots.timesheet_id')


class Subslots(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slot_id = db.Column(db.Integer, ForeignKey('slots.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    task_id = db.Column(db.Integer)
    task_name = db.Column(db.String)


class SubslotsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subslots
        include_relationships = True
        load_instance = True
        include_fk = True


class SlotsSchema(SQLAlchemyAutoSchema):
    Subslots = Nested(SubslotsSchema, many=True)

    class Meta:
        model = Slots


class TimesheetsSchema(SQLAlchemyAutoSchema):
    Slots = Nested(SlotsSchema, many=True)

    class Meta:
        model = Timesheets


class TimesheetsSlotsSchema(SQLAlchemyAutoSchema):
    slots = Nested(SlotsSchema, many=True)

    class Meta:
        model = Timesheets

