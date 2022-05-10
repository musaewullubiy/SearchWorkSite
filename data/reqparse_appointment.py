from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('message', required=True)
parser.add_argument('date', required=True)
parser.add_argument('time', required=True)
parser.add_argument('platform', required=True)
parser.add_argument('link', required=True)
parser.add_argument('hr', required=True)
parser.add_argument('finder', required=True)
parser.add_argument('vacancy_id', required=True)