from flask import Blueprint, render_template, jsonify
import pandas as pd
import os

chon_quat_bp = Blueprint(
    "chon_quat",
    __name__
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

FAN_FILE = os.path.join(
    BASE_DIR,
    "fan_database.xlsx"
)

try:
    fan_df = pd.read_excel(FAN_FILE)
except:
    fan_df = pd.DataFrame()

@chon_quat_bp.route("/chon_quat")
def chon_quat():

    return render_template(
        "chon_quat.html",
        active_page="quat"
    )

@chon_quat_bp.route("/fan_data")
def fan_data():

    return jsonify(
        fan_df.to_dict("records")
    )
