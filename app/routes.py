from flask import Blueprint, render_template, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.analysis import rule_based_check
from app.ml_model import predict_email

routes = Blueprint('routes', __name__)

def create_pdf_report(email_text, ml_result, rule_result, final_result):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "MailShield - Phishing Email Analysis Report")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, "Email Text Analysis Summary:")

    preview_text = email_text[:300] + ("..." if len(email_text) > 300 else "")
    c.drawString(50, height - 110, f"Email Preview: {preview_text}")
    c.drawString(50, height - 140, f"ML Model Result: {'Phishing' if ml_result == 1 else 'Safe'}")
    c.drawString(50, height - 160, f"Rule-Based Check Result: {'Phishing' if rule_result else 'Safe'}")
    c.drawString(50, height - 180, f"Final Decision: {final_result}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

@routes.route("/", methods=["GET", "POST"])
def home():
    result = None
    email_text = ""
    ml_result = None
    rule_result = None

    if request.method == "POST":
        email_text = request.form.get("email_text", "")

        # Run ML model and rule-based analysis
        ml_result = predict_email(email_text)
        rule_result = rule_based_check(email_text)

        # Final result
        result = "Phishing" if ml_result == 1 or rule_result else "Safe"

        # Action handler
        action = request.form.get("action")
        if action == "download_report":
            pdf_buffer = create_pdf_report(email_text, ml_result, rule_result, result)
            return send_file(pdf_buffer, as_attachment=True, download_name="MailShield_Report.pdf", mimetype="application/pdf")

    return render_template("index.html", result=result, email_text=email_text)
