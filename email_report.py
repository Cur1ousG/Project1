import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fpdf import FPDF
from src.utils import get_timestamp, sanitize_for_email, ensure_directory

REPORTS_DIR = "reports"
ensure_directory(REPORTS_DIR)

def create_pdf_report(summary, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Daily System Log Summary", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Errors: {len(summary['errors'])}", ln=True)
    pdf.cell(200, 10, txt=f"Warnings: {len(summary['warnings'])}", ln=True)
    pdf.cell(200, 10, txt=f"Login Attempts: {len(summary['login_attempts'])}", ln=True)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Top 5 Errors:", ln=True)
    for line in summary['errors'][:5]:
        pdf.multi_cell(0, 10, sanitize_for_email(line))
    pdf.ln(5)

    pdf.cell(200, 10, txt="Top 5 Warnings:", ln=True)
    for line in summary['warnings'][:5]:
        pdf.multi_cell(0, 10, sanitize_for_email(line))
    pdf.ln(5)

    pdf.cell(200, 10, txt="Login Attempts:", ln=True)
    for line in summary['login_attempts'][:5]:
        pdf.multi_cell(0, 10, sanitize_for_email(line))

    pdf.output(filename)

def send_html_email_with_pdf(summary):
    sender = "shawnmasule07l@gmail.com"
    recipient = "shawnmasule2019@gmail.com"
    app_password = "123456789"

    date_str = get_timestamp().split()[0]  # YYYY-MM-DD
    pdf_path = f"{REPORTS_DIR}/daily_report_{date_str}.pdf"
    create_pdf_report(summary, pdf_path)

    html = f"""
    <html>
    <body>
        <h2>🧾 Daily System Log Summary - {date_str}</h2>
        <p><strong>Errors:</strong> {len(summary['errors'])}</p>
        <p><strong>Warnings:</strong> {len(summary['warnings'])}</p>
        <p><strong>Login Attempts:</strong> {len(summary['login_attempts'])}</p>

        <h3>🔴 Top Errors</h3>
        <ul>
            {''.join(f'<li>{sanitize_for_email(line)}</li>' for line in summary['errors'][:5])}
        </ul>

        <h3>🟠 Top Warnings</h3>
        <ul>
            {''.join(f'<li>{sanitize_for_email(line)}</li>' for line in summary['warnings'][:5])}
        </ul>

        <h3>🔐 Login Attempts</h3>
        <ul>
            {''.join(f'<li>{sanitize_for_email(line)}</li>' for line in summary['login_attempts'][:5])}
        </ul>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = f"Daily Log Summary - {date_str}"
    message.attach(MIMEText(html, "html"))

    with open(pdf_path, "rb") as f:
        attach_pdf = MIMEApplication(f.read(), _subtype="pdf")
    attach_pdf.add_header('Content-Disposition', 'attachment', filename=f"daily_report_{date_str}.pdf")
    message.attach(attach_pdf)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.send_message(message)
    print(f"✅ Email sent to {recipient} with attached PDF report.")