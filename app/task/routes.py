import json

from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.task import task
from app.utils.task_tasks import get_standalone_tasks_for_user, get_single_task, update_task, create_task, delete_task, \
    get_done_standalone_tasks_for_user
from app.utils.user_tasks import authenticate_user


@task.route("/api/standalone-tasks", methods=["GET"])
@cross_origin()
def get_standalone_tasks(*args, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
    if user:
        return jsonify({
            "token": user["token"],
            "tasks": get_standalone_tasks_for_user(user['user_uuid'])
        })
    return jsonify({
        "loggedOut": True
    })


@task.route("/api/done-standalone-tasks", methods=["GET"])
@cross_origin()
def get_done_standalone_tasks(*args, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
    if user:
        return jsonify({
            "token": user["token"],
            "tasks": get_done_standalone_tasks_for_user(user['user_uuid'])
        })
    return jsonify({
        "loggedOut": True
    })


@task.route("/api/task/<task_id>", methods=["GET"])
@cross_origin()
def get_task_detail(*args, task_id: str, **kwargs):
    """


    :param args:
    :param task_id:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
    if user:
        return get_single_task(task_uuid=task_id, user=user)
    return jsonify({
        "loggedOut": True
    })


@task.route("/api/task", methods=["POST", "PUT", "DELETE"])
@cross_origin()
def work_with_task(*args, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
    if user:
        task_data = json.loads(request.data)
        if request.method == "POST":
            return create_task(task=task_data, user=user)

        if request.method == "PUT":
            return update_task(task=task_data, user=user)

        if request.method == "DELETE":
            return delete_task(task_uuid=task_data["task_uuid"], user=user)
    return jsonify({"loggedOut": True})


def get_task(task_uuid):
    pass
