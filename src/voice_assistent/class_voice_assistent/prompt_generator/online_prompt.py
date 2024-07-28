from prompt_generator.prompt_generator import PromptGenerator

class OnlineResearchPromptGenerator(PromptGenerator):
    def generate_prompt(self, command, context, meeting):
        return f"""
        [context]: {context}
        -------
        [str_texto]: {command}
        """