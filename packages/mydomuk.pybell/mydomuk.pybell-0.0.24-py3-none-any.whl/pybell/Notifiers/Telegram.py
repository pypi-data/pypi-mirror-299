from .URLSplitInfo import URLSplitInfo
from .WebCall import WebCall
from .ExtraParms import ExtraParms
from urllib import parse

class Telegram(WebCall):
    def __init__(self, ntfy: dict) -> None:
        super().__init__(ntfy)
        self.url = "https://api.telegram.org:443"
        self.token = self.GetParm(ntfy, None, "token", "apptoken")
        self.chatid = self.GetParm(ntfy, None, "user", "channelid", "chatid")

    def Help(self):
        return "No Help"

    def SendMessage(self, title: str, message: str, extraparms: ExtraParms) -> bool:
        url = URLSplitInfo(self.url)
        method = "GET"
        messagetext = parse.quote(f"{title} : {message}")
        suffix = f"/bot{self.token}/sendMessage?chat_id={self.chatid}&text={messagetext}"
        return self.StandardWebCall(url, method, suffix, None, {})
