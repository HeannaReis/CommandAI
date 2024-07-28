from prompt_generator.prompt_generator import PromptGenerator

class MeetingPromptGenerator(PromptGenerator):
    def generate_prompt(self, command, context, meeting):
        return f"""
        Regras de Meeting:
        - Você é responsável por observar or principais tópicos do meeting, analisar, debater, sugerir e informar melhorias.
        - Resuma de forma clara e Objetiva.
        - Não acrescentar título nas respostas.
        [context]: {context}
        -------
        [meeting]: {meeting}
        -------
        [str_texto]: {command}
        """
