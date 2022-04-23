import json
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.board import board
from app.utils.board_tasks import create_board, delete_board, update_board, fetch_board, fetch_available_boards
from app.utils.key_tasks import create_key
from app.utils.task_tasks import get_tasks_for_board
from app.utils.user_tasks import authenticate_user


@board.route("/api/boards", methods=["GET"])
@cross_origin()
def get_boards(*args, **kwargs):
    """


    :param board_id:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
    if request.method == "GET":
        return jsonify({
            "token": user["token"],
            "boards": fetch_available_boards(user=user),
        })


@board.route("/api/board/<board_id>", methods=["GET"])
@cross_origin()
def get_board(*args, board_id: str, **kwargs):
    """


    :param board_id:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
    return jsonify({
        "token": user["token"],
        "boardInfo": fetch_board(board_uuid=board_id, user=user),
        "tasks": get_tasks_for_board(board_uuid=board_id, user_uuid=user["userUuid"])
    })


@board.route("/api/board", methods=["POST", "PUT", "DELETE"])
@cross_origin()
def work_with_board(*args, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request)
    board_data = json.loads(request.data)
    if request.method == "POST":
        return create_board(board_data=board_data, user=user)

    if request.method == "PUT":
        return update_board(board=board_data, user=user)

    if request.method == "DELETE":
        return delete_board(board_uuid=board_data["board_uuid"], user=user)
