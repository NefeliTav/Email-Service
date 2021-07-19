from locust import HttpUser, between, task

import json
import time
import random

RECEIVER = "ww@email.com"
PASSWORD = "F331l0f0s@"

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.login()
        #self.signup()

    def signup(self):
        # response = self.client.get('/auth/login/')
        # csrftoken = response.cookies['csrftoken']
        email = str(time.time() * 1000) + str(random.randint(0, 1000000000))

        req = {"first_name" : "Vladimir",
               "last_name"  : "Navalny",
               "email"      : email,
               "date_of_birth" : "2000-02-02",
               "password"   : PASSWORD,
               "confirm"    : PASSWORD}
        req = json.dumps(req)

        self.client.post("/auth/signup/", req)

    def login(self):
        response = self.client.get('/auth/login/')
        csrftoken = response.cookies['csrftoken']

        req = {"email"    : "zz",
               "password" : PASSWORD}
        req = json.dumps(req)

        self.client.post("/auth/login/", req)

    @task(3)
    def send_mail(self):
        req = {"receiver" : RECEIVER,
               "subject"  : "Report",
               "content"  : "We have several options"}
        req = json.dumps(req)

        self.client.post('/send/', req)

    @task
    def send_spam(self):
        req = {"receiver" : RECEIVER,
                "subject"  : "XXX porn",
                "content"  : "casino and porn"}
        req = json.dumps(req)

        self.client.post('/send/', req)
