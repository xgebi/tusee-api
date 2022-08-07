import json

import psycopg
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.db.db_connection import db_connection
from app.task import task
from app.utils.task_tasks import get_standalone_tasks_for_user, get_single_task, update_task, create_task, delete_task
from app.utils.user_tasks import authenticate_user


@task.route("/api/standalone-tasks", methods=["GET"])
@cross_origin()
@db_connection
def get_standalone_tasks(*args, connection: psycopg.Connection, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "tasks": get_standalone_tasks_for_user(user_uuid=user['user_uuid'], conn=connection, is_active=True)
        })
    return jsonify({
        "loggedOut": True
    })


@task.route("/api/task/<task_id>", methods=["GET"])
@cross_origin()
@db_connection
def get_task_detail(*args, task_id: str, connection: psycopg.Connection, **kwargs):
    """


    :param args:
    :param task_id:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if request.method == "GET":
        return get_single_task(task_uuid=task_id, user=user, conn=connection)


@task.route("/api/task", methods=["POST", "PUT"])
@cross_origin()
@db_connection
def work_with_task(*args, connection: psycopg.Connection, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        task_data = json.loads(request.data)
        if request.method == "POST":
            return create_task(task=task_data, user=user, conn=connection)

        if request.method == "PUT":
            return update_task(task=task_data, user=user, conn=connection)

        if request.method == "DELETE":
            return delete_task(task_uuid=task_data["task_uuid"], user=user, conn=connection)
    return jsonify({"loggedOut": True})


@task.route("/api/task/<task_id>", methods=["DELETE"])
@cross_origin()
@db_connection
def remove_task(*args, task_id: str, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param task_id:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return delete_task(task_uuid=task_id, user=user, conn=connection)
    return jsonify({"loggedOut": True})
