import yaylib
import random
from time import sleep
import os
from dotenv import load_dotenv
load_dotenv()

class Client:
    def __init__(self):
        self.bot = yaylib.Client()
        self.bot_islogin = False
    
    def login(self):
        try:
            if self.bot_islogin:
                print("Already logged in.")
                return
            email = os.getenv("mail")
            password = os.getenv("pass")
            if email is None or password is None:
                print("Missing MAIL or PASS environment variables.")
                return
            self.bot.login(email, password)
            self.bot_islogin = True
        except Exception as e:
            print(f"Error logging in: {e}")

    def imagepost(self, fillpath):
        if not self.bot_islogin:
            print("Not logged in.")
            return
        try:
            self.bot.create_post(text="", attachment_filename=fillpath)
        except Exception as e:
            print(f"Error posting content: {e}")