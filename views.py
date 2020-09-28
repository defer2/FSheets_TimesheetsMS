from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

import controllers

view_blueprint = Blueprint('view_blueprint', __name__)


@view_blueprint.route('/', methods=['GET'])
@cross_origin()
def hello_world():
    return controllers.hello_world()


@view_blueprint.route('/timesheets', methods=['POST'])
@cross_origin()
def create_timesheet():
    timesheet_date = request.args.get("date")
    return jsonify(controllers.create_timesheet(timesheet_date))


@view_blueprint.route('/timesheets', methods=['GET'])
@cross_origin()
def get_timesheets():
    return jsonify(controllers.get_timesheets())


@view_blueprint.route('/timesheets/<int:timesheet_id>', methods=['GET'])
@cross_origin()
def get_timesheet(timesheet_id):
    return jsonify(controllers.get_timesheet(timesheet_id))


@view_blueprint.route('/timesheets/dates', methods=['GET'])
@cross_origin()
def get_timesheet_by_date_or_dates():
    timesheet_date = request.args.get("date")
    timesheet_start_date = request.args.get("start_date")
    timesheet_end_date = request.args.get("end_date")
    if timesheet_date:
        return jsonify(controllers.get_timesheets_by_date(timesheet_date))
    else:
        return jsonify(controllers.get_timesheets_by_dates(timesheet_start_date, timesheet_end_date))


@view_blueprint.route('/timesheets/<int:timesheet_id>', methods=['DELETE'])
@cross_origin()
def delete_timesheet(timesheet_id):
    return jsonify(controllers.delete_timesheet(timesheet_id))


@view_blueprint.route('/timesheets/<int:timesheet_id>', methods=['PUT'])
@cross_origin()
def update_timesheet_last_sync(timesheet_id):
    operation = request.args.get("operation")
    if operation == 'update_ppm_sync':
        sync_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        return jsonify(controllers.update_timesheet_last_sync(timesheet_id, True, sync_date))
    else:
        return jsonify({})


# SLOTS
@view_blueprint.route('/slots', methods=['POST'])
@cross_origin()
def create_slot():
    timesheet_id = request.args.get("timesheet_id")
    slot_hour = request.args.get("hour")
    return jsonify(controllers.create_slot(timesheet_id, slot_hour))


@view_blueprint.route('/slots', methods=['GET'])
@cross_origin()
def get_slots():
    timesheet_id = request.args.get("timesheet_id")
    return jsonify(controllers.get_slots(timesheet_id))


@view_blueprint.route('/slots/<int:slot_id>', methods=['GET'])
@cross_origin()
def get_slot(slot_id):
    return jsonify(controllers.get_slot(slot_id))


@view_blueprint.route('/slots/hour', methods=['GET'])
@cross_origin()
def get_slot_by_hour():
    timesheet_id = request.args.get("timesheet_id")
    slot_hour = request.args.get("slot_hour")
    return jsonify(controllers.get_slot_by_hour(timesheet_id, slot_hour))


@view_blueprint.route('/slots/<int:slot_id>', methods=['PUT'])
@cross_origin()
def update_slot(slot_id):
    slot_status = request.args.get("status")
    return jsonify(controllers.update_slot(slot_id, slot_status))


@view_blueprint.route('/slots/hour', methods=['PUT'])
@cross_origin()
def update_slot_by_hour():
    timesheet_id = request.args.get("timesheet_id")
    slot_hour = request.args.get("slot_hour")
    slot_status = request.args.get("status")
    return jsonify(controllers.update_slot_by_hour(timesheet_id, slot_hour, slot_status))


# SUBSLOTS
@view_blueprint.route('/subslots', methods=['POST'])
@cross_origin()
def create_subslot():
    slot_id = request.args.get("slot_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    task_id = request.args.get("task_id")
    return jsonify(controllers.create_subslot(slot_id, start_date, end_date, task_id))


@view_blueprint.route('/subslots/quick', methods=['POST'])
@cross_origin()
def create_quick_subslot():
    slot_id = request.args.get("slot_id")
    task_id = request.args.get("task_id")
    task_name = request.args.get("task_name")
    return jsonify(controllers.create_quick_subslot(slot_id, task_id, task_name))


@view_blueprint.route('/subslots/hour', methods=['POST'])
@cross_origin()
def create_subslot_by_hour():
    timesheet_id = request.args.get("timesheet_id")
    slot_hour = request.args.get("slot_hour")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    task_id = request.args.get("task_id")
    return jsonify(controllers.create_subslot_by_hour(timesheet_id, slot_hour, start_date, end_date, task_id))


@view_blueprint.route('/subslots', methods=['GET'])
@cross_origin()
def get_subslots_by_hour():
    timesheet_id = request.args.get("timesheet_id")
    slot_hour = request.args.get("slot_hour")
    return jsonify(controllers.get_subslots_by_hour(timesheet_id, slot_hour))


@view_blueprint.route('/subslots/slot/<int:slot_id>', methods=['GET'])
@cross_origin()
def get_subslots(slot_id):
    return jsonify(controllers.get_subslots(slot_id))


@view_blueprint.route('/subslots/<int:subslot_id>', methods=['GET'])
@cross_origin()
def get_subslot(subslot_id):
    return jsonify(controllers.get_subslot(subslot_id))


@view_blueprint.route('/subslots/<int:subslot_id>', methods=['PUT'])
@cross_origin()
def update_subslot(subslot_id):
    operation = request.args.get("operation")
    slot_id = request.args.get("slot_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if operation == 'change_slot':
        return update_subslot_change_slot(subslot_id, slot_id)
    elif operation == 'change_dates':
        return update_subslot_change_dates(subslot_id, start_date, end_date)
    else:
        return None


def update_subslot_change_slot(subslot_id, new_slot_id):
    return jsonify(controllers.update_subslot_change_slot(subslot_id, new_slot_id))


def update_subslot_change_dates(subslot_id, subslot_start_date, subslot_end_date):
    return jsonify(controllers.update_subslot_change_dates(subslot_id, subslot_start_date, subslot_end_date))


@view_blueprint.route('/subslots/<int:subslot_id>', methods=['DELETE'])
@cross_origin()
def delete_subslot(subslot_id):
    return jsonify(controllers.delete_subslot(subslot_id))
