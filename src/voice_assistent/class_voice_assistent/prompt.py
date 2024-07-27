def create_prompt(command, context, meeting):
    keywords = ["faça um resumo da última reunião.", "tópicos da última reunião", "resuma a última reunião", "pesquise", "pesquisar", "procure"]
    if any(keyword in command.lower() for keyword in keywords):
        return f"""
        Regras de Meeting:
        - Você é responsável por analisar, debater, sugerir e informar melhorias.
        - Resuma de forma clara e Objetiva.
        - Não acrescentar título nas respostas.

        [context]: {context}
        -------
        [meeting]: {meeting}
        -------
        [str_texto]: {command}
        """
    else:
        return f"""
        [context]: {context}
        -------
        [str_texto]: {command}
        """