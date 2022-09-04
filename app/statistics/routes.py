import json

import psycopg
from flask import request, jsonify
from flask_cors import cross_origin

from app.db.db_connection import db_connection
from app.utils.statistics_tasks import get_statistics_for_user, get_statistics_entry_task, update_statistics_entry_task, create_statistics_entry_task, delete_statistics_entry_task
from app.utils.user_tasks import authenticate_user
from app.statistics import statistics


@statistics.route("/api/statistics", methods=["GET"])
@cross_origin()
@db_connection
def get_statistics(*args, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "statistics": get_statistics_for_user(user_uuid=user['user_uuid'], connection=connection)
        })
    return jsonify({
        "loggedOut": True
    })


@statistics.route("/api/statistics-entry/<stat_uuid>", methods=["GET"])
@cross_origin()
@db_connection
def get_single_statistics_entry(*args, stat_uuid: str, connection: psycopg.Connection,**kwargs):
    """


    :param connection:
    :param args:
    :param stat_uuid:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "entry": get_statistics_entry_task(user_uuid=user['user_uuid'], connection=connection, stat_uuid=stat_uuid)
        })
    return jsonify({
        "loggedOut": True
    })


@statistics.route("/api/statistics-entry", methods=["PUT"])
@cross_origin()
@db_connection
def update_statistics_entry(*args, connection: psycopg.Connection,**kwargs):
    """


    :param connection:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        stat_data = json.loads(request.data)
        return jsonify({
            "token": user["token"],
            "entry": update_statistics_entry_task(user_uuid=user['user_uuid'], connection=connection, stat=stat_data)
        })
    return jsonify({
        "loggedOut": True
    })


@statistics.route("/api/statistics-entry", methods=["POST"])
@cross_origin()
@db_connection
def create_statistics_entry(*args, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        stat_data = json.loads(request.data)
        return jsonify({
            "token": user["token"],
            "entry": create_statistics_entry_task(user_uuid=user['user_uuid'], connection=connection, stat=stat_data)
        })
    return jsonify({
        "loggedOut": True
    })


@statistics.route("/api/statistics-entry/<stat_uuid>", methods=["DELETE"])
@cross_origin()
@db_connection
def delete_statistics_entry(*args, stat_uuid: str, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param args:
    :param stat_uuid:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "statisticsEntryDeleted": delete_statistics_entry_task(
                user_uuid=user['user_uuid'],
                connection=connection,
                stat_uuid=stat_uuid
            )
        })
    return jsonify({
        "loggedOut": True
    })
