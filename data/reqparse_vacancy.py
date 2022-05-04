from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('tags', required=True)
parser.add_argument('text', required=True)
parser.add_argument('salary', required=True)
parser.add_argument('is_actual')
parser.add_argument('hr_manager', required=True)
