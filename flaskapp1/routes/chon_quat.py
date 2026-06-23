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
TUI_FILE = os.path.join(
    BASE_DIR,
    "tui_vai.xlsx"
)
cyclone_df = pd.read_excel(CYCLONE_FILE)
thap_df = pd.read_excel(THAP_FILE)
than_df = pd.read_excel(THAN_FILE)
tui_df = pd.read_excel(TUI_FILE)

 # ======================
# GỢI Ý HỆ THỐNG
# ======================

@chon_quat_bp.route("/goi_y")
def goi_y():

    loai = request.args.get("loai")

    qmin = float(request.args.get("qmin", 0))
    qmax = float(request.args.get("qmax", 0))

    if loai == "cyclone":
        source = cyclone_df

    elif loai == "thap":
        source = thap_df

    elif loai == "than":
        source = than_df
    elif loai == "tuivai":
        source = tui_df

    else:
        return jsonify([])

    ket_qua = []

    for _, row in source.iterrows():

        if qmin <= row["Q"] <= qmax:

            ket_qua.append({
                "Model": row["Model"],
                "Q": row["Q"]
            })

    return jsonify(ket_qua)
