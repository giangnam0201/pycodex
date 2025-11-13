
class PluginAPI:
    def __init__(self, main_window, registry):
        self.main_window = main_window
        self.registry = registry

    def register_command(self, cmd_id, label, func):
        self.registry.register(cmd_id, label, func)
