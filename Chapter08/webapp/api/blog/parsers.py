from flask_restful import reqparse

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument('page', type=int, location=['args', 'headers'])
post_get_parser.add_argument('user', type=str, location=['args', 'headers'])

post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help="Title is required",
    location=('json', 'values')
)
post_post_parser.add_argument(
    'text',
    type=str,
    required=True,
    help="Body text is required",
    location=('json', 'values')
)
post_post_parser.add_argument(
    'tags',
    type=str,
    action='append',
    location=('json', 'values')
)

post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(
    'title',
    type=str,
    location=('json', 'values')
)
post_put_parser.add_argument(
    'text',
    type=str,
    location=('json', 'values')
)
post_put_parser.add_argument(
    'tags',
    type=str,
    action='append',
    location=('json', 'values')
)
