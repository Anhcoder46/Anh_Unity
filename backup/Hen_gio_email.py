import schedule
import time
import shutil
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv

load_dotenv(dotenv_path="D:\Tu_dong_hoa_python\Bai_tap_chuong3\demo.env")
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")
print(f"SENDER_EMAIL: [{sender_email}]")
print(f"SENDER_PASSWORD: [{sender_password}]")
print(f"RECEIVER_EMAIL: [{receiver_email}]")

def backup():
    backup = "backup"
    os.makedirs(backup, exist_ok=True)
    n = datetime.now()
    times = n.strftime("%Y%m%d_%H%M%S")
    success = True
    backed_up_files = []

    try:
        for filename in os.listdir("."):
            if filename.endswith("hen_gio.sql"):
                source_path = filename
                destination_path = os.path.join(backup, f"{filename}_{times}")
                shutil.copy2(source_path, destination_path)
                backed_up_files.append(filename)

        if backed_up_files:
            subject = f"Thông báo Backup Database ({n.strftime('%Y-%m-%d %H:%M:%S')})"
            
        else:
            subject = f"Trần Đức Anh gửi tới lúc {n.strftime('%Y-%m-%d %H:%M:%S')}"
            body = "Chào em, anh đứng đây từ chiều kkkk."

    except Exception as e:
        subject = f"Lỗi Backup ({n.strftime('%Y-%m-%d %H:%M:%S')})"
        body = f"Đã xảy ra lỗi trong quá trình sao lưu database: {e}"
        success = False

    send_notification_email(subject, body)
    print(f"[{n.strftime('%Y-%m-%d %H:%M:%S')}] Hoàn thành backup và gửi email thông báo.")
    return success

def send_notification_email(subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print(f"Email đã được gửi đến {receiver_email}")
        server.quit()
    except Exception as e:
        print(f"Lỗi gửi email thông báo: {e}")

def schedule_backup():
    schedule.every().day.at("00:00").do(backup)
    print("Đã lên lịch backup database hàng ngày vào lúc 00:00.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_backup()