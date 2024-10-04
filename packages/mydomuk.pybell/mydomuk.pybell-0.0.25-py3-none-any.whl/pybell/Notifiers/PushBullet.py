from .URLSplitInfo import URLSplitInfo
from .WebCall import WebCall
from .ExtraParms import ExtraParms
import json

class PushBullet(WebCall):
    def __init__(self, ntfy: dict) -> None:
        super().__init__(ntfy)
        self.url = "https://api.pushbullet.com:443"
        self.accesstoken = self.GetParm(ntfy, None, "token", "apptoken", "accesstoken")

    def Help(self):
        return "No Help"
    
    def SendMessage(self, title: str, message: str, extraparms: ExtraParms) -> bool:
        url = URLSplitInfo(self.url)
        method = "POST"
        suffix = "/v2/pushes"
        datablob = {}
        datablob['title'] = title
        datablob['body'] = message
        datablob['type'] = 'note'
        headers = {}
        headers['Content-Type'] = "application/json"
        headers['Access-Token'] = self.accesstoken
        print(f"Blob {json.dumps(datablob)}")
        return self.StandardWebCall(url, method, suffix, json.dumps(datablob), headers, True)