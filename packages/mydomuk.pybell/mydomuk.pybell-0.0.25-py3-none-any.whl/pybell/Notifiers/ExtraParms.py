class ExtraParms():
    def __init__(self) -> None:
        self.priorityoverride: str = None
        self.syslogprogram: str = None
        self.sysloglevel: str = None
        self.topic: str = None
        self.tags: str = None
        self.action: str = None
        self.debug: bool = False
        self.sched: str = None
        self.extras: dict[str] = None

    def addExtra(self, evalue: str):
        if self.extras is None:
            self.extras = {}
        if "=" in evalue:
            key, _, value = evalue.partition("=")
            if key is not None and value is not None:
                lkey = key.lower()
                if lkey not in self.extras:
                    self.extras[lkey] = value
                else:
                    if isinstance(self.extras[lkey], list):
                        self.extras[lkey].append(value)
                    else:
                        temp = self.extras[lkey]
                        self.extras[lkey] = [temp, value]
            elif key is not None:
                lkey = key.lower()
                if lkey not in self.extras:
                    self.extras[lkey] = True
        else:
            key = evalue
            if key is not None:
                lkey = key.lower()
                if lkey not in self.extras:
                    self.extras[lkey] = True
