from gzip import GzipFile
from io import BytesIO

from flask import request


class GZip(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(self.after_request)

    def after_request(self, response):
        encoding = request.headers.get('Accept-Encoding')

        if 'gzip' not in encoding or \
           not response.status_code == 200 or \
           'Content-Encoding' in response.headers:
            return response

        response.direct_passthrough = False

        gzip_buffer = BytesIO()
        with GzipFile(mode='wb', compresslevel=5, fileobj=gzip_buffer) as gzip_file:
            gzip_file.write(response.get_data())

        response.set_data(bytes(gzip_buffer.getvalue()))

        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = response.content_length

        return response
