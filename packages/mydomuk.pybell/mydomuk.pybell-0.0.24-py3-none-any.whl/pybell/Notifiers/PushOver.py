from .URLSplitInfo import URLSplitInfo
from .WebCall import WebCall
from .ExtraParms import ExtraParms

class PushOver(WebCall):
    prioritymap = {"vlow":"-2", "low":"-1","norm":"0","high":"1","vhigh":"2"}
    def __init__(self, ntfy: dict) -> None:
        super().__init__(ntfy)
        self.url = "https://api.pushover.net:443"
        self.authtoken = self.GetParm(ntfy, None, "token", "apptoken", "authtoken")
        self.usersecret = self.GetParm(ntfy, None, "user", "secret", "usersecret")
        self.priority = self.GetParm(ntfy, "norm", "priority")
        self.sound = self.GetParm(ntfy, "pushover", "sound")

    def Help(self):
        return "No Help"
    
    def SendMessage(self, title: str, message: str, extraparms: ExtraParms) -> bool:
        url = URLSplitInfo(self.url)
        method = "POST"
        suffix = "/1/messages.json"
        datablob = {}
        datablob['token'] = self.authtoken
        datablob['user'] = self.usersecret
        datablob['title'] = title
        datablob['message'] = message
        datablob['priority'] = self.GetPriority(
            PushOver.prioritymap, 
            extraparms.priorityoverride, 
            self.priority)

        datablob['sound'] = self.sound
        if extraparms.priorityoverride != None:
            datablob['priority'] = self.prioritymap[extraparms.priorityoverride]
        else:
            datablob['priority'] = self.prioritymap[str(self.priority)]
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        return self.StandardWebCall(url, method, suffix, datablob, headers)