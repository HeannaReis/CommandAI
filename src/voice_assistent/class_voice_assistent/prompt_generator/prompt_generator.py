from abc import ABC, abstractmethod

class PromptGenerator(ABC):
    @abstractmethod
    def generate_prompt(self, command, context, meeting):
        pass
