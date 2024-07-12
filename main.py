from flask import Flask, jsonify, request
from configparser import ConfigParser
from core import config
from core import zm_ftp_lib

import logging
from logging.handlers import RotatingFileHandler


CONFIG = config.load_config("core/config.ini")
BACKUP_FOLDER = "recipe_backup"
LOG_FILE = "cvd.log"
app = Flask(__name__)


@app.route('/list_recipe')
def list_recipe():
    ret = FTP.list_recipe_from_path()

    return jsonify(list(ret.keys()))


@app.route('/list_recipe_backup')
def list_recipe_backup():
    ret = FTP.list_recipe_from_path(BACKUP_FOLDER)

    return jsonify(list(ret.keys()))


@app.route('/get_recipes_content', methods=['POST'])
def get_recipes_content():
    """
    input:
        {
            "recipes": ["a", "b"]
        }
    output:
        {
            "a": {
                "a.proc": "",
                "a.proc1": "",
                "a.hdr": ""
            },
        }
    """
    recipe_list = request.get_json().get("recipes", [])

    ret = FTP.get_recipes_content_from_path(recipe_list)

    return jsonify(ret)


@app.route('/get_backup_recipes_content', methods=['POST'])
def get_backup_recipes_content():
    """
    input:
        {
            "recipes": ["a", "b"]
        }
    output:
        {
            "a": {
                "a.proc": "",
                "a.proc1": "",
                "a.hdr": ""
            },
        }
    """
    recipe_list = request.get_json().get("recipes", [])
    ret = FTP.get_recipes_content_from_path(recipe_list, BACKUP_FOLDER)

    return jsonify(ret)


@app.route('/create_recipes', methods=['POST'])
def create_recipes():
    """
    input:
        {
            "a": {
                "a.proc": "",
                "a.proc1": "",
                "a.hdr": ""
            }
        }
    """
    recipe_dict = request.get_json()

    # backup if existed
    recipe_already_in_folder = FTP.list_recipe_from_path()
    recipe_to_backup = []

    for recipe in recipe_dict.keys():
        if recipe in recipe_already_in_folder:
            recipe_to_backup.append(recipe)

    backup_recipes_content = FTP.get_recipes_content_from_path(
        recipe_to_backup)
    FTP.write_recipe(backup_recipes_content, BACKUP_FOLDER)

    # write new recipe
    ret = FTP.write_recipe(recipe_dict)
    return jsonify(ret)


@app.route('/recover', methods=['POST'])
def recover():
    """
    input:
        {
            "recipes": ["a", "b"]
        }
    """
    ret = []
    recipe_already_backup = FTP.list_recipe_from_path(BACKUP_FOLDER)

    recover_list = request.get_json().get("recipes", [])
    recover_list_checked = []

    for recipe in recover_list:
        if recipe in recipe_already_backup:
            recover_list_checked.append(recipe)
        else:
            ret.append(f"{recipe} not found")

    recover_content = FTP.get_recipes_content_from_path(
        recover_list_checked, BACKUP_FOLDER)
    ret.extend(FTP.write_recipe(recover_content))
    return jsonify(ret)


if __name__ == "__main__":
    logHandler = RotatingFileHandler(LOG_FILE, mode="a", maxBytes=10*1024*1024,
                                     backupCount=2, encoding=None, delay=0)
    logFormatter = logging.Formatter(
        "%(asctime)s %(levelname)s -> %(message)s")
    logHandler.setFormatter(logFormatter)
    logHandler.setLevel(logging.INFO)

    ftpLog = logging.getLogger("ftp")
    ftpLog.setLevel(logging.WARNING)
    ftpLog.addHandler(logHandler)

    FTP = zm_ftp_lib.ZM_FTP(CONFIG, ftpLog, BACKUP_FOLDER)

    app.run()
