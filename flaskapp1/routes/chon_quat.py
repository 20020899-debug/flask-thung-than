from flask import render_template

def register(app):

    @app.route("/chon_quat")
    def chon_quat():
        return render_template("chon_quat.html")