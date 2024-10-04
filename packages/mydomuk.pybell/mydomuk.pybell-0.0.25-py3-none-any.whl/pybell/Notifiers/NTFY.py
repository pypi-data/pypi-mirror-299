from .URLSplitInfo import URLSplitInfo
from .WebCall import WebCall
from .ExtraParms import ExtraParms

class NTFY(WebCall):
    prioritymap = {"vlow":"1", "low":"2","norm":"3","high":"4","vhigh":"5"}
    def __init__(self, ntfy: dict) -> None:
        super().__init__(ntfy)
        self.url = self.GetParm(ntfy, None, "url")
        self.topic = self.GetParm(ntfy, None, "topic")
        self.token = self.GetParm(
            ntfy, None,
            "token",
            "apptoken",
            "accesstoken"
            )
        self.priority = self.GetParm(ntfy, "norm", "priority")
        self.tags = self.GetParm(ntfy, None, "tag", "tags")
        self.icon = self.GetParm(ntfy, None, "icon")
        self.additional_headers = self.GetParm(
            ntfy, {},
            "additional_headers",
            "additionalheaders",
            "additional-headers"
            )

    def Help(self):
        return """
More information on the NTFY system can be found at https://docs.ntfy.sh

The Configuration file for NTFY requires as a minimum a URL and a TOKEN

Other values can be provided in the Configuration file and the Command line.

The -e --extras parameter may be used to pass the NTFY specific options in key=value format

Key      Value           Description
======== =========       ======================================
attach   File URL        URL of a file to attach to the outgoing message
filename File Name       Path/Name for a file to attach to the outgoing message
click    URL             URL to Open when the Notification is Clicked
delay    Time            Delay sending until later eg 10am; tomorrow, 3pm; 2h; 30m
icon     ICON URL        URL of an ICON to attach to the outgoing message
email    Email Address   Email Address to forward the message to
"""

    def SendMessage(self, title: str, message: str, extraparms: ExtraParms) -> bool:
        url = URLSplitInfo(self.url)
        method = "POST"

        if extraparms.topic != None:
            suffix = f"/{extraparms.topic}"
        elif self.topic != None:
            suffix = f"/{self.topic}"
        else:
            suffix = f"/pybell"

        datablob = message

        # "Content-Type":"application/x-www-form-urlencoded"

        headers = {}
        if title != None:
            headers["Title"] = title
        if self.token != None:
            headers["Authorization"] = f"Bearer {self.token}"
        headers["Priority"] = self.GetPriority(
            NTFY.prioritymap,
            extraparms.priorityoverride,
            self.priority)
        for key, value in self.additional_headers.items():
            if key.lower() in ["priority", "authorization"]:
                print(f"Error : {self.name} - ",
                        f"Ignoring Additional Header : {key}")
                continue
            headers[key] = str(value)

        tags = None
        if extraparms.tags != None:
            tags = extraparms.tags
        elif self.tags != None:
            tags = self.tags
        if tags != None:
            taglist = [x.lstrip().rstrip() for x in tags.split(",")]
            headers["Tags"] = ",".join(taglist)
        if extraparms.action != None:
            headers["Actions"] = extraparms.action
        if extraparms.sched != None:
            headers["X-Delay"] = extraparms.sched
        if extraparms.extras != None:
            for key, value in extraparms.extras.items():
                svalue = str(value[0]) if isinstance(value, list) else str(value)
                if key in ["icon", "ntfy_icon"]:
                    headers["Icon"] = svalue
                elif key in ["click", "ntfy_click"]:
                    headers["Click"] = svalue
                elif key in ["delay", "ntfy_delay"]:
                    headers["X-Delay"] = svalue
                elif key in ["attach", "ntfy_attach"]:
                    headers["Attach"] = svalue

        if "Icon" not in headers and self.icon != None:
            headers["Icon"] = self.icon

        if extraparms.debug:
            print(f"URL     : {url}")
            print(f"Suffix  : {suffix}")
            print(f"Method  : {method}")
            print(f"Headers : {headers}")
            print(f"Data : {datablob}")
        return self.StandardWebCall(url, method, suffix, datablob, headers, True)
