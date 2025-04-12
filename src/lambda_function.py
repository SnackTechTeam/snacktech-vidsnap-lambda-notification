import json
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from string import Template

gmail_user = "teste19930902@gmail.com"
gmail_pass = "oymyvypqpibxomgi"

TEMPLATE_DIR = Path(__file__).parent / 'templates'

def load_template(status: str) -> Template:
    template_file = TEMPLATE_DIR / f"{status}.html"
    if not template_file.exists():
        raise FileNotFoundError(f"Template '{status}.html' não encontrado.")
    with open(template_file, 'r', encoding='utf-8') as f:
        return Template(f.read())
    
def send_email(to_email,subject, html_body):
    msg = MIMEText(html_body, "html")
    msg["From"] = "VidSnap Application"
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(gmail_user,gmail_pass)
        smtp.sendmail(gmail_user, to_email,msg.as_string())


def handler (event, context):    
    try:
        for record in event['Records']:
            body = json.loads(record['body'])
            print(f"Mensagem recebida: {body}...")

            name = body["name"]
            status = body["status"]
            to_email = body["email"]
            subject = f"{name} seu vídeo foi processado com {status}!"

            template = load_template(status)

            html_body = template.safe_substitute(body)

            send_email(to_email,subject,html_body)
            
            print("Email enviado com sucesso...")

        return {
            'statusCode': 200,
            'body': json.dumps('Mensagem processada com sucesso!')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Erro durante processamento {e}!')
        }


if __name__ == "__main__":
    with open('src/event.json') as f:
        event = json.load(f)

    handler(event, None)
