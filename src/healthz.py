from flask import Blueprint

healthz_blueprint = Blueprint("healthz", __name__)


# make a healthz route
@healthz_blueprint.route("/")
def healthz():
    return "ok"
