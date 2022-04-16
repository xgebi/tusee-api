from flask import render_template, request, flash, redirect, url_for, current_app
from flask_cors import cross_origin

from app.task import task
from app.utils.task_tasks import get_standalone_tasks_for_user
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
        get_standalone_tasks_for_user(user['user_uuid'])


@task.route("/api/task/<id>", methods=["GET", "POST", "PUT"])
@cross_origin()
def set_task(*args, id: str, **kwargs):
    """


    :param args:
    :param id:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
