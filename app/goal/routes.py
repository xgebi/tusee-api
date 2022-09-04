import json

import psycopg
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.db.db_connection import db_connection
from app.utils.goal_tasks import get_goals_for_user_doneness, get_goal_task, update_goal_task, create_goal_task, \
    delete_goal_task, get_all_goals_for_user
from app.utils.user_tasks import authenticate_user
from app.goal import goal


@goal.route("/api/goals", methods=["GET"])
@cross_origin()
@db_connection
def get_goals(*args, connection: psycopg.Connection, **kwargs):
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
            "goals": get_goals_for_user_doneness(user_uuid=user['user_uuid'], connection=connection, doneness=False)
        })
    return jsonify({
        "loggedOut": True
    })


@goal.route("/api/goals/done", methods=["GET"])
@cross_origin()
@db_connection
def get_done_goals(*args, connection: psycopg.Connection, **kwargs):
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
            "goals": get_goals_for_user_doneness(user_uuid=user['user_uuid'], connection=connection, doneness=True)
        })
    return jsonify({
        "loggedOut": True
    })


@goal.route("/api/goals/all", methods=["GET"])
@cross_origin()
@db_connection
def get_all_goals(*args, connection: psycopg.Connection, **kwargs):
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
            "goals": get_all_goals_for_user(user_uuid=user['user_uuid'], connection=connection)
        })
    return jsonify({
        "loggedOut": True
    })


@goal.route("/api/goal/<goal_uuid>", methods=["GET"])
@cross_origin()
@db_connection
def get_single_goal(*args, goal_uuid: str, connection: psycopg.Connection,**kwargs):
    """


    :param connection:
    :param args:
    :param goal_uuid:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "goal": get_goal_task(user_uuid=user['user_uuid'], connection=connection, goal_uuid=goal_uuid)
        })
    return jsonify({
        "loggedOut": True
    })


@goal.route("/api/goal", methods=["PUT"])
@cross_origin()
@db_connection
def update_goal(*args, connection: psycopg.Connection,**kwargs):
    """


    :param connection:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        goal_data = json.loads(request.data)
        return jsonify({
            "token": user["token"],
            "goal": update_goal_task(user_uuid=user['user_uuid'], connection=connection, goal=goal_data)
        })
    return jsonify({
        "loggedOut": True
    })


@goal.route("/api/goal", methods=["POST"])
@cross_origin()
@db_connection
def create_goal(*args, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        goal_data = json.loads(request.data)
        return jsonify({
            "token": user["token"],
            "goal": create_goal_task(user_uuid=user['user_uuid'], connection=connection, goal=goal_data)
        })
    return jsonify({
        "loggedOut": True
    })


@goal.route("/api/goal/<goal_uuid>", methods=["DELETE"])
@cross_origin()
@db_connection
def delete_goal(*args, goal_uuid: str, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param args:
    :param goal_uuid:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "goalDeleted": delete_goal_task(user_uuid=user['user_uuid'], connection=connection, goal_uuid=goal_uuid)
        })
    return jsonify({
        "loggedOut": True
    })
