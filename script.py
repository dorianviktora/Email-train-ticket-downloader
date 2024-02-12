import imaplib
import email
import time
import os

imap_server = "imap.seznam.cz"
imap = imaplib.IMAP4(imap_server)


def main():
    email_address = input("Enter your email adress: ")
    email_password = input("Enter password for your email: ")

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
                _, data = imap.fetch(msg_id, "(RFC822)")

                message = email.message_from_bytes(data[0][1])
                print(f"New email recived from: {message.get('From')}")

                for part in message.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    data = part.get_payload(decode=True)

                    if not filename:
                        print("part.get_filename() error, abort")
                        return
                    
                    downloads_folder = os.path.join(os.path.expanduser("~"), 'Downloads')
                    if not os.path.exists(downloads_folder):
                        print("/Downloads/ folder does not exists, abort")
                        return
                    
                    file_path = os.path.join(downloads_folder, filename)

                    with open(file_path, 'wb') as file:
                        file.write(data)
                        print(f"Attachment '{filename}' downloaded.")

        time.sleep(20)


if __name__ == "__main__":
    main()
