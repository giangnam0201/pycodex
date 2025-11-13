
from collections import OrderedDict

class CommandRegistry:
    def __init__(self, parent):
        self.parent = parent
        self._cmds = OrderedDict()

    def register(self, cmd_id: str, label: str, func):
        self._cmds[cmd_id] = (label, func)

    def list(self):
        return [(cid, lbl) for cid, (lbl, _) in self._cmds.items()]

    def run(self, cmd_id: str):
        _, func = self._cmds[cmd_id]
        return func()
