# Main module for api
import websocket
import json
import threading
import requests

class BinanceAPI:
    def __init__(self,url):
        self.ws_url = url

    def start(self,on_mess,error,cls,opn):
        self.on_mess = on_mess
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.get_data,
            on_error=error,
            on_close=cls,
            on_open=opn
        )

        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def get_data(self, ws, message):
        self.data = json.loads(message)
        self.on_mess()

class RestAPI:
    def __init__(self,url):
        self.ws_url = url

    def get_data(self,params):
        self.data = requests.get(self.ws_url, params=params).json()
        return self.data