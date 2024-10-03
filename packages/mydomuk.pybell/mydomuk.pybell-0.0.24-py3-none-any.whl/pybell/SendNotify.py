from .Notifiers.Apprise import Apprise
from .Notifiers.Gotify import Gotify
from .Notifiers.PushOver import PushOver
from .Notifiers.Telegram import Telegram
from .Notifiers.PushBullet import PushBullet
from .Notifiers.ExtraParms import ExtraParms
from .Notifiers.Syslog import Syslog
from .Notifiers.NTFY import NTFY
from .constants import *

class SendNotify:
    def __init__(self, ntfy: dict) -> None:
        self.name = ntfy["name"]
        self.__type = ntfy["type"] if "type" in ntfy else None
        self.__isvalid: bool = True
        self.__ltype: str = None
        self.sendMessage = self.dfltsendMessage
        self.Help = self.dfltHelp
        if self.__type == None:
            print(f"Error in notify {self.name} - no type specified")
            self.__isvalid = False
        else:
            self.__ltype = self.__type.lower()
            if self.__ltype == NOTIFY_APPRISE:
                self.apprise = Apprise(ntfy)
                self.sendMessage = self.apprise.SendMessage
                self.Help = self.apprise.Help
            elif self.__ltype == NOTIFY_GOTIFY:
                self.gotify = Gotify(ntfy)
                self.sendMessage = self.gotify.SendMessage
                self.Help = self.gotify.Help
            elif self.__ltype == NOTIFY_NTFY:
                self.ntfy = NTFY(ntfy)
                self.sendMessage = self.ntfy.SendMessage
                self.Help = self.ntfy.Help
            elif self.__ltype == NOTIFY_PUSHBULLET:
                self.pushbullet = PushBullet(ntfy)
                self.sendMessage = self.pushbullet.SendMessage
                self.Help = self.pushbullet.Help
            elif self.__ltype == NOTIFY_PUSHOVER:
                self.pushover = PushOver(ntfy)
                self.sendMessage = self.pushover.SendMessage
                self.Help = self.pushover.Help
            elif self.__ltype == NOTIFY_TELEGRAM:
                self.telegram = Telegram(ntfy)
                self.sendMessage = self.telegram.SendMessage
                self.Help = self.telegram.Help
            elif self.__ltype == NOTIFY_SYSLOG:
                self.syslog = Syslog(ntfy)
                self.sendMessage = self.syslog.SendMessage
                self.Help = self.syslog.Help
            else:
                print(f"Error in notify {self.name} invalid type : {self.__type} must be one of {', '.join(NOTIFY_VALID_TYPES)}")
                self.__isvalid = False

    def dfltsendMessage(self, title: str, message: str, extraparms: ExtraParms) -> bool:
        print(f"Unable to send message as {self.name} is invalid")
        return False
    
    def dfltHelp(self):
        return ""





