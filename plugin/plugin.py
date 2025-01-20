from flogin import Plugin

class DeepSeek(Plugin):
    def __init__(self, **options):
        self.model = self.settings["model"]
    
    def get_model(self):
        return self.model