import json

import psycopg
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.board import board
from app.db.db_connection import db_connection
from app.utils.board_tasks import create_board, delete_board, update_board, fetch_board, fetch_available_boards
from app.utils.key_tasks import create_key
from app.utils.task_tasks import get_tasks_for_board
from app.utils.user_tasks import authenticate_user


@board.route("/api/boards", methods=["GET"])
@cross_origin()
@db_connection
def get_boards(*args, connection: psycopg.Connection, **kwargs):
    """


    :param board_id:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if request.method == "GET":
        return jsonify({
            "token": user["token"],
            "boards": fetch_available_boards(user=user, conn=connection),
        })


@board.route("/api/board-view/<board_id>", methods=["GET"])
@cross_origin()
@db_connection
def get_board(*args, board_id: str, connection: psycopg.Connection, **kwargs):
    """


    :param board_id:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    return jsonify({
        "token": user["token"],
        "board": fetch_board(board_uuid=board_id, user=user),
        "tasks": get_tasks_for_board(board_uuid=board_id, user_uuid=user["user_uuid"])
    })


@board.route("/api/board/<board_id>", methods=["GET"])
@cross_origin()
@db_connection
def get_board_view(*args, board_id: str, connection: psycopg.Connection, **kwargs):
    """


    :param board_id:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    return jsonify({
        "token": user["token"],
        "board": fetch_board(board_uuid=board_id, user=user, conn=connection)
    })


@board.route("/api/board", methods=["POST", "PUT", "DELETE"])
@cross_origin()
@db_connection
def work_with_board(*args, connection: psycopg.Connection, **kwargs):
    """


    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    board_data = json.loads(request.data)
    if request.method == "POST":
        return create_board(board_data=board_data, user=user, conn=connection)

    if request.method == "PUT":
        return update_board(board=board_data, user=user, conn=connection)

    if request.method == "DELETE":
        return delete_board(board_uuid=board_data["boardUuid"], user=user, conn=connection)
