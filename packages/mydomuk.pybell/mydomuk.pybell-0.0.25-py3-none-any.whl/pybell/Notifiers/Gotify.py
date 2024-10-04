from .URLSplitInfo import URLSplitInfo
from .WebCall import WebCall
from .ExtraParms import ExtraParms

class Gotify(WebCall):
    prioritymap = {"vlow":"0", "low":"3","norm":"6","high":"9","vhigh":"12"}

    def __init__(self, ntfy: dict) -> None:
        super().__init__(ntfy)
        self.url = self.GetParm(ntfy, None, "url")
        self.apptoken = self.GetParm(ntfy, None, "token", "apptoken")
        self.priority = self.GetParm(ntfy, "norm", "priority")
        self.additional_headers = self.GetParm(
            ntfy, {},
            "additional_headers",
            "additionalheaders",
            "additional-headers"
            )


    def Help(self):
        return "No Help"

    def SendMessage(self, title: str, message: str, extraparms: ExtraParms) -> bool:
        url = URLSplitInfo(self.url)
        suffix = url.path + f"/message?token={self.apptoken}"
        method = "POST"
        datablob = {}
        datablob['title'] = title
        datablob['message'] = message
        datablob['priority'] =  self.GetPriority(
            Gotify.prioritymap,
            extraparms.priorityoverride,
            self.priority)
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        for key, value in self.additional_headers.items():
            if key.lower() in ["content-type"]:
                print(f"Error : {self.name} - ",
                        f"Ignoring Additional Header : {key}")
                continue
            headers[key] = str(value)

        return self.StandardWebCall(url, method, suffix, datablob, headers)