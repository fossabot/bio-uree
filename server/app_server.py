from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib import parse

import RPi.GPIO as GPIO
from modules import lv_sensor, ph_meter

IP = "192.168.1.51"


class RequestHandler_httpd(BaseHTTPRequestHandler):
    def __init__(self, lv_pin, ph_meter, code, *args):
        self.lv_pin = lv_pin
        self.ph_meter = ph_meter
        self.code = code
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        self.request = self.requestline
        self.request = self.request[5 : int(len(self.request) - 9)].split("?")[0]
        self.calibrate = bool(
            parse.parse_qs(parse.urlsplit(self.path).query).get("calibrate", None)
        )
        self.reset = bool(
            parse.parse_qs(parse.urlsplit(self.path).query).get("reset", None)
        )
        if self.code == self.request:
            if self.calibrate:
                self.ph = str(self.ph_meter.calibrate())
            elif self.reset:
                self.ph_meter.reset()
                self.ph = "0"
            else:
                self.ph = str(self.ph_meter.read())
            self.cuve = GPIO.input(self.lv_pin)
            with open("logs/biouree.log") as log_file:
                self.logs = log_file.read().replace("\n", ",")
            self.app_response = bytes(f"{self.cuve}|{self.ph}|{self.logs}", "utf-8")
            self.send_response(200)
        else:
            self.app_response = bytes("Code d'accès invalide", "utf-8")
            self.send_response(403)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", len(self.app_response))
        self.end_headers()
        self.wfile.write(self.app_response)


class AppServer(Thread):
    def __init__(self, lv_pin, ph_meter, code):
        Thread.__init__(self)
        self.lv_pin = lv_pin
        self.ph_meter = ph_meter
        self.code = code
        self.server_address_httpd = (IP, 8080)
        self.server = HTTPServer(self.server_address_httpd, self.set_handler)

    def set_handler(self, *args):
        self.handler = RequestHandler_httpd(
            self.lv_pin, self.ph_meter, self.code, *args
        )

    def run(self):
        print("Starting app server...")
        self.server.serve_forever()
