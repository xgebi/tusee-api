import json

import psycopg
from flask import render_template, request, flash, redirect, url_for, current_app, jsonify
from flask_cors import cross_origin

from app.db.db_connection import db_connection
from app.utils.note_tasks import get_notes_for_user, get_note_task, update_note_task, create_note_task, delete_note_task
from app.utils.user_tasks import authenticate_user
from app.note import note


@note.route("/api/notes", methods=["GET"])
@cross_origin()
@db_connection
def get_notes(*args, connection: psycopg.Connection, **kwargs):
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
            "tasks": get_notes_for_user(user_uuid=user['user_uuid'], connection=connection)
        })
    return jsonify({
        "loggedOut": True
    })


@note.route("/api/note/<note_uuid>", methods=["GET"])
@cross_origin()
@db_connection
def get_single_note(*args, note_uuid: str, connection: psycopg.Connection,**kwargs):
    """


    :param connection:
    :param args:
    :param note_uuid:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "tasks": get_note_task(user_uuid=user['user_uuid'], connection=connection, note_uuid=note_uuid)
        })
    return jsonify({
        "loggedOut": True
    })


@note.route("/api/note", methods=["PUT"])
@cross_origin()
@db_connection
def update_note(*args, connection: psycopg.Connection,**kwargs):
    """


    :param connection:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        note_data = json.loads(request.data)
        return jsonify({
            "token": user["token"],
            "tasks": update_note_task(user_uuid=user['user_uuid'], connection=connection, note=note_data)
        })
    return jsonify({
        "loggedOut": True
    })


@note.route("/api/note", methods=["POST"])
@cross_origin()
@db_connection
def create_note(*args, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param args:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        note_data = json.loads(request.data)
        return jsonify({
            "token": user["token"],
            "tasks": create_note_task(user_uuid=user['user_uuid'], connection=connection, note=note_data)
        })
    return jsonify({
        "loggedOut": True
    })


@note.route("/api/note/<note_uuid>", methods=["DELETE"])
@cross_origin()
@db_connection
def delete_note(*args, note_uuid: str, connection: psycopg.Connection, **kwargs):
    """


    :param connection:
    :param args:
    :param note_uuid:
    :param kwargs:
    :return:
    """
    user = authenticate_user(request=request, connection=connection)
    if user:
        return jsonify({
            "token": user["token"],
            "taskDeleted": delete_note_task(user_uuid=user['user_uuid'], connection=connection, note_uuid=note_uuid)
        })
    return jsonify({
        "loggedOut": True
    })
