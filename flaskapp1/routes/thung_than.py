from flask import Blueprint, render_template, request
import math

from utils import fm, get_float
from constants import THEP, THAN, MM3

thung_bp = Blueprint("thung", __name__)


@thung_bp.route("/thung-than", methods=["GET", "POST"])
def thung_than():

    ket_qua = ""

    if request.method == "POST":

        L_tong = get_float(request, "Chiều dài tổng")
        L_thung = get_float(request, "Chiều dài thùng")
        Rong = get_float(request, "Chiều rộng")
        Cao = get_float(request, "Chiều cao")
        Day = get_float(request, "Độ dày tôn")
        Dau_vao = get_float(request, "Kích thước đầu vào")

        U100 = get_float(request, "U100x50")
        U150 = get_float(request, "U150x75")

        so_tang = get_float(request, "Số tầng")
        day_than = get_float(request, "Chiều dày lớp than")

        dai_khay = get_float(request, "Dài khay")
        rong_khay = get_float(request, "Rộng khay")
        cao_khay = get_float(request, "Cao khay")
        so_khay = get_float(request, "Số khay")
        so_tang_khay = get_float(request, "Số tầng khay")
        day_khay = get_float(request, "Độ dày khay")
        dai_tong_khay = get_float(request, "Chiều dài tổng khay")

        so_tam_loc = get_float(request, "Số tấm lọc")

        kl_than_giua = (L_thung * Rong * 2 + L_thung * Cao * 2) * Day * THEP / MM3

        kl_2_dau = (
            (
                (Rong + Dau_vao) / 2 *
                math.sqrt(((Rong - Dau_vao)/2)**2 + ((L_tong - L_thung)/2)**2)
                +
                (Cao + Dau_vao) / 2 *
                math.sqrt(((Cao - Dau_vao)/2)**2 + ((L_tong - L_thung)/2)**2)
            ) * 4 + Rong * Cao
        ) * Day * THEP / MM3

        kl_chan = U100/1000*9.35 + U150/1000*19

        kl_san = (
            2 * (L_thung * Rong / 500)
            * 3 * so_tang * THEP / MM3
            + L_thung * Rong * 11 * so_tang / 1_000_000
        )

        kl_tang_cung = Rong * L_thung / 550 * 2 * 100 * Day * THEP / MM3

        kl_than = L_thung * Rong * day_than * THAN * so_tang / MM3

        kl_khay = 0  # giữ nguyên nếu chưa tối ưu

        kl_loc = (149*Cao*Day + 128*Rong*Day*2 + 108*Rong*Day*2 + 54*Cao*Day*4) * THEP / MM3 * so_tam_loc

        tong = kl_than_giua + kl_2_dau + kl_chan + kl_san + kl_tang_cung + kl_than + kl_khay + kl_loc

        ket_qua = f"""
THÂN GIỮA : {fm(kl_than_giua)} Kg
2 ĐẦU     : {fm(kl_2_dau)} Kg
CHÂN ĐẾ   : {fm(kl_chan)} Kg
SÀN       : {fm(kl_san)} Kg
TĂNG CỨNG : {fm(kl_tang_cung)} Kg
THAN      : {fm(kl_than)} Kg
KHUNG LỌC : {fm(kl_loc)} Kg

------------------------
TỔNG THÉP : {fm(tong)} Kg
"""

    return render_template("thung_than.html", ket_qua=ket_qua, form=request.form, active_page="thung")