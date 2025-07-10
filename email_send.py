#自动发送邮件
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import sleep


# === 163邮箱 SMTP 配置 ===
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "your_email@163.com"         # 替换为你的 163 邮箱
AUTH_CODE = "your_smtp_auth_code"           # 替换为你的授权码（非登录密码）

# === 邮件发送函数 ===
def send_email(smtp_server, port, sender, password, receiver, subject, body):
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = Header(sender)
        msg["To"] = Header(receiver)
        msg["Subject"] = Header(subject)
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender, password)
            server.sendmail(sender, [receiver], msg.as_string())
        return True, ""
    except Exception as e:
        return False, str(e)

# === 主批量处理函数（接收参数） ===
def send_batch_emails(input_json_path, output_json_path, subject, body):
    with open(input_json_path, "r", encoding="utf-8") as f:
        contacts = json.load(f)
    results = []
    sent_emails = set()
    for entry in contacts:
        url = entry.get("url")
        for email in entry.get("emails", []):
            if email in sent_emails:
                continue
            print(f"[→] 正在发送给: {email}")
            success, error = send_email(SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, AUTH_CODE, email, subject, body)
            result = {
                "email": email,
                "url": url,
                "success": success,
                "error": error if not success else ""
            }
            results.append(result)
            sent_emails.add(email)
            print(f"[✓] 成功" if success else f"[x] 失败: {error}")
            sleep(1)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n 全部邮件处理完成，发送结果保存在: {output_json_path}")