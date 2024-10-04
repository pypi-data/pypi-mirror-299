#!/usr/bin/python3
import os
from posixpath import join
import sys
from yaml import load, Loader
from .SendNotify import SendNotify
from .constants import *
from .Notifiers.ExtraParms import ExtraParms

def Version():
        print("PyBell Version " + appversion)

def Usage():
        print("""
PyBell Version """ + appversion + """

Usage : pybell arg1 arg2 ... argn

Argument List
=============
-t  | --title title          : Message title
-m  | --message message      : Message text
-c  | --config configfile    : Configuration file, if not specified then PyBell will look in
                               ~/.config/pybell.yaml
                               /etc/default/pybell.yaml
-n  | --notify notifylist    : Optional Notification list, see below for more details
-p  | --priority override    : Optional priority override for all notifications
                               must be one of vlow, low, norm, high, vhigh
-a  | --action               : Optional Action to send with the message where   
-w  | --when                 : Optional schedule in time delay
-e  | --extra extravalue     : Optional extra parm extra=value or just extra which will be set to true 
-g  | --tags                 : Optional Tags to send with the message where supported
-s  | --topic                : Topic to send with the message (NTFY)
-sp | --syslog-program       : Program name to use in Syslog, default pybell
-sl | --syslog-level         : Level for Syslog can be one of I(nfo), W(arn), E(rror), C(ritical) or D(ebug)
-l  | --list                 : List the configurations notification names
-d  | --debug                : Debugging option
-h  | -? | --help            : Display this usage information
-ch | --confighelp           : Display configuration file help
-nh | --notifyhelp           : Notify help based upon -n option value

A notifylist is a comma seperated list of notify names from the config file.
If no notifylist is provided then all names from the config file will be used in the
sequence that they are defined to form a single notifylist

Multiple notifylists may be specified by repeating the -n notifylist command line option

Each notifylist will be used to send the notification to the 1st name that works,
after that all other names in the list are ignored.

Multiple notifylists will be treated seperately from other notifylists

e.g -n NTFYA, NTFYB -n NTFYC will notify A or B whichever works and also C

Exit Codes
==========
0 - Config loaded and all OK, notify sent (help also returns 0)
1 - Config loaded and at least 1 notification sent but some errors
2 - Config loaded but unable to send any notifications
4 - Command line error, no notifications sent
8 - Configuration file error
""")

def ConfigHelp():
    print("""
The configuration file is a standard YAML file with a top level node of notify
The notify node contains a list of notification elements with parameters varying
by each type.

Standard Example Format
=======================

---
notify:
  - name: notification_name_1
    type: apprise|gotify|ntfy|pushover|syslog|telegram
    description: Descriptive Text to describe this for the list command
    ...
  - name: notification_name_2
    type: apprise|gotify|ntfy|pushover|syslog|telegram
    description: Descriptive Text to describe this for the list command
    ...

Each notification requires the name and type and then takes parameters according
to the notification type as specified in the type parameter.

Apprise Example Snippet
=======================

  - name: notification_name
    type: apprise
    url: http://127.0.0.1:8000                       URL String to the Apprise Applicartion
    config: apprise                                  Configuration to use for sending, default apprise
    tag: taglist                                     Comma seperated list of tags to send to
    description: Apprise Example Snippet
    additional_headers:                              Optional additional headers
      header1: value1
      header2: value2

Gotify Example Snippet
======================

  - name: notification_name
    type: gotify
    url: http://127.0.0.1:8001                       URL String to the Gotify Application
    apptoken: application_token_value                This is from the Gotify Site
    priority: high                                   Can be one of vlow, low, norm, high, vhigh
    description: Gotify Example Snippet
    additional_headers:                              Optional additional headers
      header1: value1
      header2: value2

NTFY Example Snippet
======================

  - name: notification_name
    type: ntfy
    url: https://ntfy.sh                             URL String to the NTFY Server
    token: user_token_value                          This is from the NTFY Site
    icon: https:/webaddressforicon.com               Optional ICON for messages
    tag: TagName                                     Optional Tag to send with Message
    priority: norm                                   Can be one of vlow, low, norm, high, vhigh
    description: NTFY Example Snippet
    additional_headers:                              Optional additional headers
      header1: value1
      header2: value2

PushOver Example Snippet
========================

  - name: notification_name
    type: pushover
    authtoken: application authorization token       This is from pushover.net
    usersecret: user secret token                    This is from pushover.net
    priority: norm                                   Can be one of vlow, low, norm, high, vhigh
    description: PushOver Example Snippet

Telegram Example Snippet
========================

  - name: notification_name
    type: telegram
    token: bot token                                 This is the token for the Bot used to hook into
    chatid: chat identifier                          This is the chat identity to put the message into
    description: Telegram Example Snippet

    """)

def main():

    notifylist: 'list[str]' = []
    pybellconfig: str = None
    args = sys.argv
    argcount: int = len(args) - 1
    title: str = None
    message: str = None
    extraparms: ExtraParms = ExtraParms()
    if argcount == 0:
        print(f"Error - too few arguments")
        Usage()
        exit(4)

    params = args[1:]
    lastarg = None
    argstrings = []
    listnames = False
    notifyhelp = False
    while len(params) > 0:
        arg = params[0]
        params = params[1:]
        if arg in PARM_VALID_LIST or arg in FLAG_VALID_LIST:
            if lastarg != None:
                #   Process the last arg that we got
                joined = ' '.join(argstrings)
                argstrings = []
                if lastarg in PARM_CONFIG:
                    pybellconfig = joined
                elif lastarg in PARM_TITLE:
                    title = joined
                elif lastarg in PARM_MESSAGE:
                    message = joined
                elif lastarg in PARM_NOTIFY:
                    notifylist.append(joined.lower())
                elif lastarg in PARM_PRIORITY:
                    extraparms.priorityoverride = joined.lower()
                elif lastarg in PARM_SYSLOG_PROGRAM:
                    extraparms.syslogprogram = joined.lower()
                elif lastarg in PARM_SYSLOG_LEVEL:
                    extraparms.sysloglevel = joined.lower()
                elif lastarg in PARM_TOPIC:
                    extraparms.topic = joined
                elif lastarg in PARM_TAGS:
                    extraparms.tags = joined
                elif lastarg in PARM_ACTION:
                    extraparms.action = joined
                elif lastarg in PARM_SCHED_DELAY:
                    extraparms.sched = joined
                elif lastarg in PARM_EXTRA:
                    extraparms.addExtra(joined)
                elif lastarg != None:
                    print(f"Error : Parameter Not Recognised : {lastarg}")
                lastarg = None
            if arg in PARM_VALID_LIST:
                lastarg = arg
            elif arg in FLAG_VALID_LIST:
                lastarg = None
                if arg in FLAG_HELP:
                    Usage()
                    exit(0)
                elif arg in FLAG_CONFIG_HELP:
                    ConfigHelp()
                    exit(0)
                elif arg in FLAG_VERSION:
                    Version()
                    exit(0)
                elif arg in FLAG_LIST:
                    listnames = True
                elif arg in FLAG_NOTIFY_HELP:
                    notifyhelp = True
                elif arg in FLAG_DEBUG:
                    extraparms.debug = True
                else:
                    raise Exception(f"Error - Flag {arg} not handled")
        else:
            argstrings.append(arg)

    if lastarg != None and len(argstrings) > 0:
        joined = ' '.join(argstrings)
        if lastarg in PARM_CONFIG:
            pybellconfig = joined
        elif lastarg in PARM_TITLE:
            title = joined
        elif lastarg in PARM_MESSAGE:
            message = joined
        elif lastarg in PARM_NOTIFY:
            notifylist.append(joined.lower())
        elif lastarg in PARM_PRIORITY:
            extraparms.priorityoverride = joined.lower()
        elif lastarg in PARM_SYSLOG_PROGRAM:
            extraparms.syslogprogram = joined.lower()
        elif lastarg in PARM_SYSLOG_LEVEL:
            extraparms.sysloglevel = joined.lower()
        elif lastarg in PARM_TOPIC:
            extraparms.topic = joined
        elif lastarg in PARM_TAGS:
            extraparms.tags = joined
        elif lastarg in PARM_ACTION:
            extraparms.action = joined
        elif lastarg in PARM_EXTRA:
            extraparms.addExtra(joined)

    if extraparms.debug:
        if extraparms.extras is not None:
            print(f"ExtraParms Extras")
            for key, value in extraparms.extras.items():
                print(f"  Key : {key} : Value : {value}")
    if listnames == False and notifyhelp == False:
        if title == None or message == None:
            print("Error : PyBell must be called with a title and a message use -t and -m")
            exit(4)

        if extraparms.priorityoverride != None:
            if extraparms.priorityoverride not in PRIORITY_VALID_LIST:
                print(f"Error : PyBell command line priority must be one of {', '.join(PRIORITY_VALID_LIST)}")
                exit(4)

        if extraparms.sysloglevel != None:
            if extraparms.sysloglevel not in SYSLOG_VALID_LEVELS:
                print(f"Error : PyBell command line syslog level must be on of {', '.join(SYSLOG_VALID_LEVELS).upper()}")
                exit(4)

    if pybellconfig == None:
        userpath = os.path.expanduser('~')
        userconfig = os.path.join(userpath, CONFIG_USER_PATH)
        if os.path.isdir(userconfig):
            userspybell = os.path.join(userconfig, CONFIG_FILE_NAME)
            if os.path.isfile(userspybell):
                pybellconfig = userspybell
        if pybellconfig == None:
            if os.path.isdir(CONFIG_DEFAULT_PATH) and os.path.isfile(CONFIG_DEFAULT_NAME):
                pybellconfig = CONFIG_DEFAULT_NAME
            else:
                print("Error - No PyBell Configuration file found")
                exit(8)
    configdata = None
    with open(pybellconfig, "r") as stream:
        configdata = load(stream, Loader=Loader)

    if listnames:
        print(f"PyBell Notification Names")
        for key, values in configdata.items():
            if key == "notify":
                for value in values:
                    ntfyname = ""
                    ntfytype = "Unknown"
                    ntfydescription = ""
                    if "name" in value:
                        ntfyname = value["name"]
                    if "type" in value:
                        ntfytype = value["type"]
                    if "description" in value:
                        ntfydescription = f" Description : {value['description']}"
                    print(f" Name : {ntfyname:16s} Type : {ntfytype:12s}{ntfydescription}")
    elif notifyhelp:
        print(f"PyBell Notification Help")
        notify = {}
        for key, values in configdata.items():
            if key == "notify":
                for value in values:
                    if "name" in value and "type" in value:
                        notify[value['name'].lower()] = value
        for notifyname in notifylist:
            notifynames = notifyname.split(",")
            while len(notifynames) > 0:
                name = notifynames.pop(0).lstrip().rstrip()
                if name in notify:
                    send = SendNotify(notify[name])
                    print(f"Notify Help for {send.name}")
                    print(send.Help())

    else:
        notify = {}
        fulllist = []
        doall = len(notifylist) == 0
        for key, values in configdata.items():
            if key == "notify":
                for value in values:
                    if "name" in value:
                        notifyname = value["name"].lower()
                        notify[notifyname] = value
                        if doall:
                            fulllist.append(notifyname)

        if doall:
            notifylist.append(','.join(fulllist))

        errorcount = 0
        okcount = 0
        for notifyname in notifylist:
            notifynames = notifyname.split(",")
            while len(notifynames) > 0:
                name = notifynames.pop(0).lstrip().rstrip()
                if name not in notify:
                    print(f"Error : Notification {name} not possible as not defined in list from configuration")
                    errorcount += 1
                else:
                    send = SendNotify(notify[name])
                    if send.sendMessage(title, message, extraparms):
                        print(f"Notification sent by {send.name}")
                        okcount += 1
                        notifynames = []
        if errorcount > 0:
            if okcount > 0:
                exit(1)
            else:
                exit(2)

if __name__ == "__main__":
    main()


