import smtplib
from email.mime.text import MIMEText

class EmailSMSClient:
    """
    A class to handle sending SMS messages via email using an SMTP server.
    """
    def __init__(self, email_address, email_password, smtp_server='smtp.gmail.com', smtp_port=465):
        """
        Initializes the EmailSMSClient with email credentials and SMTP server details.
        
        Parameters:
            email_address (str): Your email address used for sending messages.
            email_password (str): The password or app-specific password for your email account.
            smtp_server (str): The SMTP server address. Default is 'smtp.gmail.com'.
            smtp_port (int): The SMTP server port. Default is 465.
        """
        self.email_address = email_address
        self.email_password = email_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.server = None  # Will hold the SMTP server connection

    def connect(self):
        """
        Establishes a connection to the SMTP server.
        """
        try:
            self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            self.server.login(self.email_address, self.email_password)
            print("> Connected to SMTP server.")
        except Exception as e:
            print(f"> ERROR: An error occurred while connecting to the SMTP server: {e}")
            self.server = None  # Ensure server is None if connection fails

    def send(self, to_address, message_body):
        '''
        Send SMS or email to recipient
        '''
        if not self.server:
            print("> ERROR: SMTP server is not connected. Call connect() before sending messages.")
            return

        # Create the email message
        msg = MIMEText(message_body, 'plain')
        msg['From'] = self.email_address
        msg['To'] = to_address
        msg['Subject'] = 'Next Trains'  # Subject is usually ignored in SMS

        # Send the email via the SMTP server
        try:
            self.server.sendmail(self.email_address, to_address, msg.as_string())
            print(f"> Delivered message to: {to_address} via {self.email_address}")
        except Exception as e:
            print(f"> ERROR: An error occurred while sending to {to_address}: {e}")

    def disconnect(self):
        """
        Closes the connection to the SMTP server.
        """
        if self.server:
            self.server.quit()
            self.server = None
            print("> Disconnected from SMTP server.")

    def __enter__(self):
        """
        Enables use of the 'with' statement for automatic connection management.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensures the SMTP connection is closed when exiting the 'with' block.
        """
        self.disconnect()
