from collections import deque

class ContextManager:
    def __init__(self, maxlen=10):
        self.recent_context = deque(maxlen=maxlen)

    def add_context(self, command, response):
        self.recent_context.append((command, response))

    def get_context(self):
        return "\n".join([context for context, _ in self.recent_context])
