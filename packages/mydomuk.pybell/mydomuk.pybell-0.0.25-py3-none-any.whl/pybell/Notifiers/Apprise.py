from .URLSplitInfo import URLSplitInfo
from .WebCall import WebCall
from .ExtraParms import ExtraParms

class Apprise(WebCall):
    def __init__(self, ntfy: dict) -> None:
        super().__init__(ntfy)
        self.url = ntfy["url"] if "url" in ntfy else None
        self.config = ntfy["config"] if "config" in ntfy else "apprise"
        self.tag = ntfy["tag"] if "tag" in ntfy else None
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
        suffix = url.path + f"/notify/{self.config}"
        method = "POST"
        datablob = {}
        datablob['title'] = title
        datablob['body'] = message
        if self.tag != None:
            datablob["tag"] = self.tag
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        for key, value in self.additional_headers.items():
            if key.lower() in ["content-type"]:
                print(f"Error : {self.name} - ",
                        f"Ignoring Additional Header : {key}")
                continue
            headers[key] = str(value)

        return self.StandardWebCall(url, method, suffix, datablob, headers)
