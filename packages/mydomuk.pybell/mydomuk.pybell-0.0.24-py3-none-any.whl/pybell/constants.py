appversion = "0.0.24"

# These are simple flags On or Off

FLAG_HELP   = ["-h", "--help", "-?"]
FLAG_CONFIG_HELP = ["-ch", "--confighelp"]
FLAG_LIST = ["-l", "--list"]
FLAG_VERSION = ["-v", "--version"]
FLAG_DEBUG   = ["-d", "--debug"]
FLAG_NOTIFY_HELP = ["-nh", "--notifyhelp"]

FLAG_VALID_LIST = [
    *FLAG_HELP,
    *FLAG_CONFIG_HELP,
    *FLAG_LIST,
    *FLAG_VERSION,
    *FLAG_DEBUG,
    *FLAG_NOTIFY_HELP
]

# These are parameters where values are required

PARM_CONFIG = ["-c", "--config"]
PARM_NOTIFY = ["-n", "--notify"]
PARM_TITLE  = ["-t", "--title"]
PARM_MESSAGE = ["-m", "--message"]
PARM_PRIORITY = ["-p", "--priority"]
PARM_SYSLOG_PROGRAM = ["-sp", "--syslog-program"]
PARM_SYSLOG_LEVEL = ["-sl", "--syslog-level"]
PARM_TOPIC = ["-s", "--topic", "--subscription"]
PARM_TAGS = ["-g", "--tags", "--tag"]
PARM_ACTION = ["-a", "--action", "--actions"]
PARM_EXTRA  = ["-e", "--extra", "--extras"]
PARM_SCHED_DELAY = ["-w", "--when", "--delay"]

PARM_VALID_LIST = [
    *PARM_CONFIG,
    *PARM_NOTIFY,
    *PARM_TITLE,
    *PARM_MESSAGE,
    *PARM_PRIORITY,
    *PARM_SYSLOG_PROGRAM,
    *PARM_SYSLOG_LEVEL,
    *PARM_TOPIC,
    *PARM_TAGS,
    *PARM_ACTION,
    *PARM_EXTRA,
    *PARM_SCHED_DELAY
]

PRIORITY_VALID_LIST = [
    "vlow","low", "norm", "high","vhigh"
]

SYSLOG_VALID_LEVELS = [
    "i","w","e","c","d"
]

CONFIG_FILE_NAME = "pybell.yaml"
CONFIG_USER_PATH = ".config"
CONFIG_DEFAULT_PATH = "/etc/default"
CONFIG_DEFAULT_NAME = "/etc/default/pybell.yaml"

NOTIFY_APPRISE = "apprise"
NOTIFY_GOTIFY = "gotify"
NOTIFY_NTFY = "ntfy"
NOTIFY_PUSHBULLET = "pushbullet"
NOTIFY_PUSHOVER = "pushover"
NOTIFY_SYSLOG = "syslog"
NOTIFY_TELEGRAM = "telegram"

NOTIFY_VALID_TYPES = [
    NOTIFY_APPRISE,
    NOTIFY_GOTIFY,
    NOTIFY_NTFY,
    NOTIFY_PUSHBULLET,
    NOTIFY_PUSHOVER,
    NOTIFY_SYSLOG,
    NOTIFY_TELEGRAM
]
