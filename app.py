from flask import Flask, render_template, request
import math

app = Flask(__name__)

THEP = 7850
THAN = 550
MM3 = 1_000_000_000


def fm(v):
    return f"{v:,.2f}"


def so(name):
    try:
        return float(request.form.get(name, 0))
    except:
        return 0


@app.route("/", methods=["GET", "POST"])
def home():

    ket_qua = ""

    if request.method == "POST":
        try:

            # ---------- INPUT ----------
            L_tong = so("Chiều dài tổng")
            L_thung = so("Chiều dài thùng")
            Rong = so("Chiều rộng")
            Cao = so("Chiều cao")
            Day = so("Độ dày tôn")
            Dau_vao = so("Kích thước đầu vào")

            U100 = so("U100x50")
            U150 = so("U150x75")

            so_tang = so("Số tầng")
            day_than = so("Chiều dày lớp than")

            dai_khay = so("Dài khay")
            rong_khay = so("Rộng khay")
            cao_khay = so("Cao khay")
            so_khay = so("Số khay")
            so_tang_khay = so("Số tầng khay")
            day_khay = so("Độ dày khay")
            dai_tong_khay = so("Chiều dài tổng khay")

            so_tam_loc = so("Số tấm lọc")

            # ---------- THÂN GIỮA ----------
            kl_than_giua = (
                (L_thung * Rong * 2 + L_thung * Cao * 2)
                * Day * THEP / MM3
            )

            # ---------- 2 ĐẦU ----------
            canh_rong = math.sqrt(
                (Rong/2 - Dau_vao/2)**2 +
                (L_tong/2 - L_thung/2)**2
            )

            canh_cao = math.sqrt(
                (Cao/2 - Dau_vao/2)**2 +
                (L_tong/2 - L_thung/2)**2
            )

            kl_2_dau = (
                (
                    (Rong + Dau_vao)/2 * canh_rong +
                    (Cao + Dau_vao)/2 * canh_cao
                ) * 4 + Rong * Cao
            ) * Day * THEP / MM3

            # ---------- CHÂN ĐẾ ----------
            kl_chan = U100/1000*9.35 + U150/1000*19

            # ---------- SÀN ----------
            kl_san = (
                L_thung * Rong * 11 * so_tang / 1_000_000
            )

            # ---------- TĂNG CỨNG ----------
            kl_tang_cung = (
                Rong * L_thung / 550
                * 2 * 100 * Day
                * THEP / MM3
            )

            # ---------- THAN ----------
            kl_than = (
                L_thung * Rong * day_than
                * THAN * so_tang
                / MM3
            )

            # ---------- KHAY ----------
            kl_khay = (
                (
                    (
                        dai_khay * (cao_khay + 35) * 2 +
                        rong_khay * (cao_khay + 40) +
                        (cao_khay + 115) * rong_khay +
                        (cao_khay + 150) * (rong_khay + 35) +
                        dai_khay * (cao_khay + 60) * 2
                    ) * so_khay
                    +
                    dai_khay * (
                        L_thung * so_tang_khay -
                        so_khay * rong_khay -
                        (L_thung - dai_tong_khay) * so_tang_khay
                    )
                )
                * day_khay * THEP / MM3
                +
                11 * 2 * so_khay * dai_khay * rong_khay / 1_000_000
            )

            # ---------- KHUNG LỌC ----------
            kl_loc = (
                (
                    149 * Cao * Day +
                    128 * Rong * Day * 2 +
                    108 * Rong * Day * 2 +
                    54 * Cao * Day * 4
                )
                * THEP / MM3
                * so_tam_loc
            )

            tong = (
                kl_than_giua + kl_2_dau + kl_chan +
                kl_san + kl_tang_cung + kl_khay + kl_loc
            )

            ket_qua = f"""
THÂN GIỮA : {fm(kl_than_giua)} Kg
2 ĐẦU     : {fm(kl_2_dau)} Kg
CHÂN ĐẾ   : {fm(kl_chan)} Kg
SÀN       : {fm(kl_san)} Kg
TĂNG CỨNG : {fm(kl_tang_cung)} Kg
THAN      : {fm(kl_than)} Kg
KHAY      : {fm(kl_khay)} Kg
KHUNG LỌC : {fm(kl_loc)} Kg

------------------------

TỔNG THÉP : {fm(tong)} Kg
"""

        except Exception as e:
            ket_qua = f"Lỗi: {e}"

    return render_template("index.html", ket_qua=ket_qua)


import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))