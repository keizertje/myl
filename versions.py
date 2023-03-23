class VersionManager:
    def __init__(self, startvalue: str = ""):
        self._version: int = 0
        self._versions: list = [startvalue]

    @property
    def current(self):
        return self._versions[self._version]

    def add_version(self, version: str = ""):
        self._versions = self._versions[0:self._version + 1]
        self._versions.append(version)
        self._version = len(self._versions) - 1

    def change_version(self, value):
        self._version = self._version + value
        if self._version < 0:
            self._version = 0
        elif self._version > len(self._versions) - 1:
            self._version = len(self._versions) - 1
        print(self._version)
        print(self._versions)
