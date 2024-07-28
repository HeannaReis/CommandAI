from prompt_generator.prompt_generator import PromptGenerator

class DefaultPromptGenerator(PromptGenerator):
    def generate_prompt(self, command, context, meeting):
        return f"""
        [context]: {context}
        -------
        [str_texto]: {command}
        """