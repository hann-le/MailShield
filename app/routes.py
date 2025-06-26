from flask import Blueprint, render_template, request
from app.analysis import rule_based_check
from app.ml_model import predict_email

routes = Blueprint('routes', __name__)

@routes.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        email_text = request.form["email_text"]
        ml_result = predict_email(email_text)
        rule_result = rule_based_check(email_text)

        if ml_result == 1 or rule_result:
            result = "Phishing"
        else:
            result = "Safe"

    return render_template("index.html", result=result)