from flask import Blueprint, jsonify
from extensions import mongo

log_bp = Blueprint("logs", __name__)


@log_bp.route("/logs", methods=["GET"])
def get_logs():
    logs = list(mongo.db.logs.find({}, {"_id": 0}))
    return jsonify(logs)