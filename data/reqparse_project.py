from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('link', required=True)
parser.add_argument('developer_id', required=True)