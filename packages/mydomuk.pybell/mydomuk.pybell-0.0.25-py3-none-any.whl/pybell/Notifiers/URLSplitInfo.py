from urllib.parse import urlsplit

class URLSplitInfo:
    def __init__(self, fqdn) -> None:
        self.host: str
        self.path: str
        self.port: int
        self.scheme: str
        self.split(fqdn)

    def split(self, fqdn):
        url = urlsplit(fqdn)
        if url.scheme == "":
            url = urlsplit("https://" + fqdn)
        if ":" in url.netloc:
            self.host, self.port = url.netloc.split(":",1)
        else:
            self.host = url.netloc
            if url.scheme == "http":
                self.port = 80
            elif url.scheme == "https":
                self.port = 443
        self.path = url.path
        if url.query != None and len(url.query) > 0:
            self.path += "?" + url.query
        self.scheme = url.scheme
        return url