from flask import Blueprint, Response, request
from resources.response import build_response

mod_HealthIndex = Blueprint('mod_HealthIndex', __name__)


@mod_HealthIndex.route("/", methods=['GET'])
def HI_get():
    # ainda temos de definir o que surge aqui
    return build_response({}, status_code=400)

@mod_HealthIndex.route("/sub1", methods=['GET'])
def sub1_get():
    # ainda temos de definir o que surge aqui
    return build_response({}, status_code=400)

@mod_HealthIndex.route("/sub2", methods=['GET'])
def sub2_get():
    # ainda temos de definir o que surge aqui
    return build_response({}, status_code=400)

@mod_HealthIndex.route("/sub3", methods=['GET'])
def sub3_get():
    # ainda temos de definir o que surge aqui
    return build_response({}, status_code=400)

@mod_HealthIndex.route("/sub4", methods=['GET'])
def sub4_get():
    # ainda temos de definir o que surge aqui
    return build_response({}, status_code=400)

