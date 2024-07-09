from flask import Flask, jsonify
from configparser import ConfigParser
from core import config
from core import zm_ftp_lib

import logging
from logging.handlers import RotatingFileHandler


CONFIG = config.load_config("core/config.ini")
LOG_FILE = "cvd.log"
app = Flask(__name__)


@app.route('/get_recipe_list')
def get_recipe_list():
    ret = FTP.list_all_recipe()

    return jsonify(ret)


@app.route('/get_recipes')
def get_recipes():
    """
    input:
        ["a", "b"]
    output:
        {
            "a": [
                "a.proc": "",
                "a.proc1": "",
                "a.hdr": ""
            ],
        }
    """
    ret = {}
    return jsonify(ret)


@app.route('/write_back')
def write_back():
    """
    func:
        backup -> write
    input:
        {
            "a": [
                "a.proc": "",
                "a.proc1": "",
                "a.hdr": ""
            ],
        }
    output:
        200
    """
    ret = {}
    return jsonify(ret)


@app.route('/recover')
def recover():
    """
    func:
        backup_file -> recipe
    input:
        get ["a", "b"] -> ret current backup file content
        post ["a", "b"] -> recover
    output:
        200
    """
    ret = {"status": "OK"}
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

    FTP = zm_ftp_lib.ZM_FTP(CONFIG, ftpLog)

    app.run()
    FTP.quit()
