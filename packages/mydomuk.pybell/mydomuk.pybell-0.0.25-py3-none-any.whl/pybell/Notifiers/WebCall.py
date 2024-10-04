from .URLSplitInfo import URLSplitInfo
import http.client
from urllib import parse

class WebCall:
    def __init__(self, ntfy: dict) -> None:
        self.name = ntfy["name"]

    def GetParm(self, jdict, defaultvalue, *args):
        for arg in args:
            if arg in jdict:
                return jdict[arg]
        return defaultvalue

    def GetPriority(self, mapping: dict, *args):
        for arg in args:
            if arg is not None and arg in mapping:
                return mapping[arg]
        return None

    def StandardWebCall(self, url: URLSplitInfo, method, suffix, datablob, headers, raw=False) -> bool:
        sentOK = False
        conn = None
        if url.scheme == "http":
            conn = http.client.HTTPConnection(url.host,url.port)
        elif url.scheme == "https":
            conn = http.client.HTTPSConnection(url.host, url.port)
        else:
            print(f"{self.name} Error : Invalid URL scheme : {url.scheme}, should be http or https")

        if conn is not None:
            try:
                if headers and '"user-agent' not in headers:
                    headers['user-agent'] = "PyBell"
                if raw:
                    data = datablob
                    conn.request(method, suffix, data, headers)
                else:
                    data = parse.urlencode(datablob) if datablob != None else None
                    conn.request(method, suffix, data, headers)

                resp = conn.getresponse()
                if resp.status != 200:
                    print(f"{self.name} Error : Notification Failure Reason {resp.reason} Code {resp.status}")
                else:
                    sentOK = True
            except Exception as e:
                print(f"{self.name} Error : {e}")
            conn.close()
        return sentOK