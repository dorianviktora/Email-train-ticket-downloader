import imaplib
import email
import time

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
                        print("part.get_filename() error")
                        return
                    
                    with open(filename, 'wb') as file:
                        file.write(data)
                        print(f"Attachment '{filename}' downloaded.")
                
        time.sleep(20)


if __name__ == "__main__":
    main()
