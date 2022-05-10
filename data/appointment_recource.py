from datetime import datetime

from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.appointments import Appointments
from data.reqparse_appointment import parser


def abort_if_appointment_not_found(appointment_id):
    session = db_session.create_session()
    appointment = session.query(Appointments).get(appointment_id)
    if not appointment:
        abort(404, message=f"Appointment {appointment_id} not found")


class AppointmentResource(Resource):
    def get(self, appointment_id):
        abort_if_appointment_not_found(appointment_id)
        session = db_session.create_session()
        appointment = session.query(Appointments).get(appointment_id)

        return jsonify({'appointment': appointment.to_dict(
            only=('vacancy_id', 'message', 'datetime', 'platform', 'link', 'hr', 'finder', 'is_actual'))})

    def delete(self, appointment_id):
        abort_if_appointment_not_found(appointment_id)
        session = db_session.create_session()
        appointment = session.query(Appointments).get(appointment_id)
        session.delete(appointment)
        session.commit()
        return jsonify({'success': 'OK'})


class AppointmentListResource(Resource):
    def get(self):
        session = db_session.create_session()
        appointments = session.query(Appointments).all()
        return jsonify({'appointments': [
            item.to_dict(only=('vacancy_id', 'message', 'datetime', 'platform', 'link', 'hr', 'finder', 'is_actual'))
            for item in appointments]})

    def post(self):
        format_d = "%Y-%m-%d %H:%M"
        args = parser.parse_args()
        session = db_session.create_session()
        appointment = Appointments()
        appointment.message = args["message"]
        appointment.datetime = datetime.strptime(args["date"] + " " + args["time"], format_d)
        appointment.platform = args["platform"]
        appointment.link = args["link"]
        appointment.hr = args["hr"]
        appointment.finder = args["finder"]
        appointment.vacancy_id = args["vacancy_id"]

        session.add(appointment)
        session.commit()
        return jsonify({'success': 'OK'})
