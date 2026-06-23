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

    q = float(request.args.get("q", 0))
    p = float(request.args.get("p", 0))

    loai = request.args.get("loai", "").strip()

    ket_qua = []

    for _, row in df.iterrows():

        # Lọc loại quạt nếu người dùng chọn
        if loai:
            if str(row["Loai"]).strip() != loai:
                continue

        # Có nhập áp suất
        if p > 0:

            match = (
                row["Qmin"] <= q <= row["Qmax"]
                and
                row["Pmin"] <= p <= row["Pmax"]
            )

        # Không nhập áp suất
        else:

            match = (
                row["Qmin"] <= q <= row["Qmax"]
            )

        if match:

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
    # ======================
# chọn hệ
# ======================
    
CYCLONE_FILE = os.path.join(
    BASE_DIR,
    "cyclone.xlsx"
)

THAP_FILE = os.path.join(
    BASE_DIR,
    "thap_loc.xlsx"
)

THAN_FILE = os.path.join(
    BASE_DIR,
    "thung_than.xlsx"
)

cyclone_df = pd.read_excel(CYCLONE_FILE)
thap_df = pd.read_excel(THAP_FILE)
than_df = pd.read_excel(THAN_FILE)
 # ======================
# GỢI Ý HỆ THỐNG
# ======================
def goi_y_he_thong():

    qmin = float(request.args.get("qmin", 0))
    qmax = float(request.args.get("qmax", 0))

    cyclone = []
    thap = []
    than = []

    # Cyclone
    for _, row in cyclone_df.iterrows():

        if qmin <= row["Q"] <= qmax:

            cyclone.append({
                "Model": row["Model"],
                "Q": row["Q"]
            })

    # Tháp
    for _, row in thap_df.iterrows():

        if qmin <= row["Q"] <= qmax:

            thap.append({
                "Model": row["Model"],
                "Q": row["Q"]
            })

    # Than
    for _, row in than_df.iterrows():

        if qmin <= row["Q"] <= qmax:

            than.append({
                "Model": row["Model"],
                "Q": row["Q"]
            })

    return jsonify({
        "cyclone": cyclone,
        "thap": thap,
        "than": than
    })
