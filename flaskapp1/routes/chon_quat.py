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


@chon_quat_bp.route("/tim_quat")
def tim_quat():

    try:
        q = float(request.args.get("q", 0))
        p = float(request.args.get("p", 0))
    except:
        return jsonify([])

    ket_qua = []

    for _, row in df.iterrows():

        if (
            row["Qmin"] <= q <= row["Qmax"]
            and
            row["Pmin"] <= p <= row["Pmax"]
        ):

            ket_qua.append({
                "Model": row["Model"],
                "Loai": row["Loai"],
                "Qmin": row["Qmin"],
                "Qmax": row["Qmax"],
                "Pmin": row["Pmin"],
                "Pmax": row["Pmax"],
                "Kw": row["Kw"]
            })

    return jsonify(ket_qua)
