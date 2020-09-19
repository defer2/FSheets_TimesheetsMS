import datetime
from database import db
from models import Timesheets, TimesheetsSchema, Slots, SlotsSchema, Subslots, SubslotsSchema, TimesheetsSlotsSchema


def hello_world():
    return 'Hello World!'


def create_timesheet(date):
    date_datetime = datetime.datetime.strptime(date, '%Y-%m-%d')
    one_timesheet = Timesheets(date=date_datetime)
    db.session.add(one_timesheet)
    db.session.commit()

    db.session.refresh(one_timesheet)

    __create_timesheet_slots(one_timesheet.id, date)

    return TimesheetsSchema(many=True).dump(db.session.query(Timesheets)
                                            .filter(Timesheets.id == one_timesheet.id))


def get_timesheets():
    return TimesheetsSchema(many=True).dump(Timesheets.query.all())


def get_timesheets_by_date(date):
    return TimesheetsSchema(many=True).dump(db.session.query(Timesheets)
                                            .filter(Timesheets.date == date))


def get_timesheets_by_dates(start_date, end_date):
    return TimesheetsSchema(many=True).dump(db.session.query(Timesheets)
                                            .filter(Timesheets.date <= end_date)
                                            .filter(Timesheets.date >= start_date))


def get_timesheet(timesheet_id):
    timesheet = db.session.query(Timesheets).filter(timesheet_id == Timesheets.id).all()
    return TimesheetsSchema(many=True).dump(timesheet)


def delete_timesheet(timesheet_id):
    one_timesheet = db.session.query(Timesheets).filter_by(id=timesheet_id).one()
    db.session.delete(one_timesheet)
    db.session.commit()
    return TimesheetsSchema(many=True).dump(Timesheets.query.all())


def __create_timesheet_slots(timesheet_id, date):
    date_datetime = datetime.datetime.strptime(date, '%Y-%m-%d')
    for hour in range(0, 24):
        hour = date_datetime.replace(hour=hour, minute=0)
        create_slot(timesheet_id, hour)

    return SlotsSchema(many=True).dump(db.session.query(Slots)
                                       .filter(Slots.timesheet_id == timesheet_id).all())


# SLOTS
def create_slot(timesheet_id, slot_hour):
    slot_hour_datetime = datetime.datetime.strptime(slot_hour, '%Y-%m-%d %H:%M:%S')

    db.session.add(Slots(hour=slot_hour_datetime, status=1, timesheet_id=timesheet_id))
    db.session.commit()
    return SlotsSchema(many=True).dump(Slots.query.all())


def get_slots(timesheet_id):
    return SlotsSchema(many=True).dump(db.session.query(Slots).filter(Slots.timesheet_id == timesheet_id))


def get_slot(slot_id):
    return SlotsSchema(many=True).dump(db.session.query(Slots).filter(Slots.id == slot_id))


def get_slot_by_hour(timesheet_id, slot_hour):
    slot_hour_datetime = datetime.datetime.strptime(slot_hour, '%Y-%m-%d %H:%M:%S')

    return SlotsSchema(many=True).dump(db.session.query(Slots)
                                       .filter_by(hour=slot_hour_datetime, timesheet_id=timesheet_id))


def update_slot(slot_id, slot_status):
    one_slot = db.session.query(Slots).filter_by(id=slot_id).one()
    one_slot.status = slot_status or one_slot.status
    db.session.add(one_slot)
    db.session.commit()
    return SlotsSchema(many=True).dump(db.session.query(Slots)
                                       .filter_by(id=one_slot.id))


def update_slot_by_hour(timesheet_id, slot_hour, slot_status):
    slot_hour_datetime = datetime.datetime.strptime(slot_hour, '%Y-%m-%d %H:%M:%S')

    one_slot = db.session.query(Slots).filter_by(timesheet_id=timesheet_id, hour=slot_hour_datetime).one()
    return update_slot(one_slot.slot_id, slot_status)


# SUBSLOTS
def create_subslot(slot_id, start_date, end_date, task_id):
    start_date_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    db.session.add(
        Subslots(slot_id=slot_id, start_date=start_date_datetime, end_date=end_date_datetime, task_id=task_id))
    db.session.commit()
    return SubslotsSchema(many=True).dump(Subslots.query.all())


def create_quick_subslot(slot_id, task_id, task_name):
    one_slot = get_slot(slot_id)[0]
    new_date = datetime.datetime.strptime(one_slot['hour'], '%Y-%m-%dT%H:%M:%S')

    db.session.add(
        Subslots(slot_id=slot_id, task_id=task_id, start_date=new_date, end_date=new_date, task_name=task_name))
    db.session.commit()

    __calculate_subslots_dates(slot_id)

    return SubslotsSchema(many=True).dump(Subslots.query.all())


def create_subslot_by_hour(timesheet_id, slot_hour, start_date, end_date, task_id):
    start_date_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    one_slot = get_slot_by_hour(timesheet_id, slot_hour)
    return create_subslot(one_slot.id, start_date_datetime, end_date_datetime, task_id)


def get_subslots(slot_id):
    return SubslotsSchema(many=True).dump(db.session.query(Subslots)
                                          .filter(Subslots.slot_id == slot_id))


def get_subslots_by_hour(timesheet_id, slot_hour):
    one_slot = get_slot_by_hour(timesheet_id, slot_hour)
    return get_subslots(one_slot.slot_id)


def get_subslot(subslot_id):
    return SubslotsSchema(many=True).dump(db.session.query(Subslots)
                                          .filter(Subslots.id == subslot_id))


def delete_subslot(subslot_id):
    one_subslot = db.session.query(Subslots).filter_by(id=subslot_id).one()
    db.session.delete(one_subslot)
    db.session.commit()
    return SubslotsSchema(many=True).dump(Subslots.query.all())


def update_subslot_change_dates(subslot_id, subslot_start_date, subslot_end_date):
    one_subslot = db.session.query(Subslots).filter_by(id=subslot_id).one()
    try:
        subslot_start_date = datetime.datetime.strptime(subslot_start_date, '%Y-%m-%dT%H:%M:%S')
        subslot_end_date = datetime.datetime.strptime(subslot_end_date, '%Y-%m-%dT%H:%M:%S')
    except:
        pass

    one_subslot.start_date = subslot_start_date or one_subslot.start_date
    one_subslot.end_date = subslot_end_date or one_subslot.end_date
    db.session.add(one_subslot)
    db.session.commit()
    return SubslotsSchema(many=True).dump(db.session.query(Subslots)
                                          .filter(Subslots.id == subslot_id))


# private
def update_subslot_change_slot(subslot_id, new_slot_id):
    one_subslot = db.session.query(Subslots).filter_by(id=subslot_id).one()
    prev_slot_id = str(one_subslot.slot_id)
    one_subslot.slot_id = new_slot_id or one_subslot.slot_id
    db.session.add(one_subslot)
    db.session.commit()

    __calculate_subslots_dates(new_slot_id)
    __calculate_subslots_dates(int(prev_slot_id))

    return SubslotsSchema(many=True).dump(db.session.query(Subslots)
                                          .filter(Subslots.id == subslot_id))


# private
def __calculate_subslots_dates(slot_id):
    one_slot = db.session.query(Slots).filter_by(id=slot_id).one()
    slot_start_hour = one_slot.hour.hour
    all_subslots = __get_subslots_as_objects(slot_id)
    number_of_subslots = __count_subslots(slot_id)
    minutes_for_each_subslot = round(60 / number_of_subslots)
    calculated_minutes = 0
    count_loops = 0
    for one_subslot in all_subslots:
        subslot_start_date = one_subslot.start_date.replace(hour=slot_start_hour, minute=calculated_minutes, second=0)
        one_subslot.start_date = subslot_start_date
        calculated_minutes += minutes_for_each_subslot
        if count_loops == number_of_subslots - 1:
            subslot_end_date = one_subslot.end_date.replace(hour=slot_start_hour, minute=59, second=59)
            one_subslot.end_date = subslot_end_date
        else:
            subslot_end_date = one_subslot.end_date.replace(hour=slot_start_hour, minute=calculated_minutes)
            one_subslot.end_date = subslot_end_date
        db.session.commit()
        count_loops += 1


# private
def __get_subslots_as_objects(slot_id):
    return db.session.query(Subslots).filter(Subslots.slot_id == slot_id)


# private
def __get_slot_as_object(slot_id):
    return db.session.query(Slots).filter(Slots.id == slot_id)


# private
def __count_subslots(slot_id):
    return db.session.query(Subslots).filter(Subslots.slot_id == slot_id).count()
