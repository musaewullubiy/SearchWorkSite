from flask_restful import reqparse

vacancy_parser = reqparse.RequestParser()
vacancy_parser.add_argument('tags', required=True)
vacancy_parser.add_argument('text', required=True)
vacancy_parser.add_argument('salary', required=True)
vacancy_parser.add_argument('is_actual')
vacancy_parser.add_argument('hr_manager', required=True)
