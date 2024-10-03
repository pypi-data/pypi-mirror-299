import logging 
import logging.handlers 
import syslog
from .URLSplitInfo import URLSplitInfo
from .WebCall import WebCall
from .ExtraParms import ExtraParms


class Syslog(WebCall):
    def __init__(self, ntfy: dict) -> None:
        super().__init__(ntfy)
        self.url = ntfy["url"] if "url" in ntfy else None
        self.config = ntfy["config"] if "config" in ntfy else "apprise"
        self.tag = ntfy["tag"] if "tag" in ntfy else None

    def Help(self):
        return "No Help"

    def getLoggingCommand(self, textlevel: str):
        if textlevel == "i":
            return logging.info
        if textlevel == "w":
            return logging.warning
        if textlevel == "e":
            return logging.error
        if textlevel == "c":
            return logging.critical
        if textlevel == "d":
            return logging.debug
        if textlevel is None:
            return logging.info
        print(f"Error : Syslog Level value {textlevel.upper()} is not valid! Defaulting to INFO")

        return logging.info
        
    def SendMessageOLD(self, title: str, message: str, extraparms: ExtraParms) -> bool: 
        syslog.syslog(self.getSyslogLevel(extraparms.sysloglevel), title + " - " + message)
        return True

    def SendMessage(self, title: str, message: str, extraparms: ExtraParms) -> bool:
        h = logging.handlers.SysLogHandler()
        #h.setFormatter(
        #    logging.Formatter("%(name)s: %(levelname)s %(message)s")
        #)
        if extraparms.syslogprogram is not None:
            h.ident = extraparms.syslogprogram
        else:
            h.ident = "PyBell"
        
        cmd = self.getLoggingCommand(extraparms.sysloglevel)
        cmd(title + " - " + message)
        return True