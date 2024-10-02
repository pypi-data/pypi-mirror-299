# llm_package/memory.py

class Memory:
    @staticmethod
    def prompt_1():
        return "Recall the most important details from the previous conversation."

    @staticmethod
    def prompt_2():
        return "Summarize the key points discussed so far."

    @staticmethod
    def prompt_3():
        return "What information seems most relevant to the current context?"

    @staticmethod
    def prompt_4():
        return "Identify any patterns or recurring themes in the conversation history."

    @staticmethod
    def prompt_5():
        return "What details might be important to remember for future reference?"