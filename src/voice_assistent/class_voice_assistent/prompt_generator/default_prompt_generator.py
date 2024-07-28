from prompt_generator.prompt_generator import PromptGenerator

class DefaultPromptGenerator(PromptGenerator):
    def generate_prompt(self, command, context, meeting):
        return f"""
        Regras:
        Você é um assistente inteligente, deve utilizar o context para aprender com perguntas e respostas anteriores e gerar uma nova resposta.
        - Você pode fazer pesquisas online para responder a pergunta de str_texto.
        - Resuma de forma clara e Objetiva.
        - Não acrescentar título nas respostas.
        - Respostas só em Texto e não gerar código exemplo ``` linguagem ```
        [context]: {context}
        -------
        [str_texto]: {command}
        """