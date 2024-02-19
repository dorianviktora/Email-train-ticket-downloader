import imaplib
import email
import time
import os

imap_server = "imap.seznam.cz"
imap = imaplib.IMAP4(imap_server)


def check_message(msg_id, expected_sender) -> int | None:
    _, data = imap.fetch(msg_id, "(RFC822)")

    message = email.message_from_bytes(data[0][1])
    sender = message.get('From')
    print(f"New email recived from: {sender}")

    if expected_sender not in sender.lower():
        print(f"New email is not from expected sender {expected_sender}. Continue waiting for ticket...")
        return

    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        data = part.get_payload(decode=True)

        if not filename:
            print("part.get_filename() error, abort")
            return -1
                    
        downloads_folder = os.path.join(os.path.expanduser("~"), '/sdcard/Download')
        if not os.path.exists(downloads_folder):
            print("/sdcard/Download/ folder does not exists, abort")
            return -1
                    
        file_path = os.path.join(downloads_folder, filename)

        with open(file_path, 'wb') as file:
            file.write(data)
            print(f"Attachment '{filename}' downloaded.")


def main():
    email_address = input("Enter your email adress: ")
    email_password = input("Enter password for your email: ")
    expected_sender = input("Enter expected email ticket sender. (jizdenky@idos.svt.cz): ")

    try:
        imap.login(email_address, email_password)
    except:
        print("Wrong password for your email address.")
        return

    while True:
        imap.select("Inbox")
        status, messages = imap.search(None, "(UNSEEN)")

        if status == "OK":

            for msg_id in messages[0].split():
                if check_message(msg_id, expected_sender) is not None:
                    print("Exiting application.")
                    return

        time.sleep(10)


if __name__ == "__main__":
    main()
