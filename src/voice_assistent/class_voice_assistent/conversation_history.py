class ConversationHistory:
    def __init__(self):
        self.history = []

    def add_interaction(self, question, answer):
        self.history.append({"question": question, "answer": answer})

    def get_context(self):
        context = ""
        for interaction in self.history:
            context += f"Pergunta: {interaction['question']}\nResposta: {interaction['answer']}\n"
        return context
