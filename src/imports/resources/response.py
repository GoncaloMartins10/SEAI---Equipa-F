from flask import Response
from jsonpickle import encode


def build_response(body, status_code=400):
    return Response(encode(body, unpicklable=True), status=status_code)

