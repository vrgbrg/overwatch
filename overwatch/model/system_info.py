class SystemInfo:
    def __init__(self, name, system, release):
        self.name = name
        self.system = system
        self.release = release

    def __str__(self):
        return self.system + ' - ' + self.release