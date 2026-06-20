from flask import Blueprint, render_template, jsonify, request
import pandas as pd
import os

chon_quat_bp = Blueprint(
    "chon_quat",
    __name__
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

EXCEL_FILE = os.path.join(
    BASE_DIR,
    "chon_quat.xlsx"
)

try:
    df = pd.read_excel(EXCEL_FILE)
    print("Đọc file quạt OK")
except Exception as e:
    print("Lỗi:", e)
    df = pd.DataFrame()

# ======================
# Trang chọn quạt
# ======================

@chon_quat_bp.route("/chon_quat")
def chon_quat():

    return render_template(
        "chon_quat.html",
        active_page="quat"
    )

# ======================
# API lấy toàn bộ dữ liệu
# ======================

@chon_quat_bp.route("/fan_data")
def fan_data():

    return jsonify(
        df.to_dict("records")
    )
