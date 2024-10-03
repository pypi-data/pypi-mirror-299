class Prompt:
    @staticmethod
    def qa_matching():
        return "Match the given question with the most appropriate answer from the available knowledge base."

    @staticmethod
    def search_public_knowledge():
        return "Search and retrieve relevant information from the public knowledge base to address the current query."

    @staticmethod
    def strategy_matching():
        return "Identify and select the most suitable strategy for the given situation or problem."

    @staticmethod
    def strategy_objective():
        return "Define clear and achievable objectives for the selected strategy."

    @staticmethod
    def strategy_completion():
        return "Develop a comprehensive plan to complete and implement the chosen strategy."

    @staticmethod
    def strategy_impact():
        return "Analyze and predict the potential impact of implementing the selected strategy."

    @staticmethod
    def emotional_impact():
        return "Assess the potential emotional impact of the strategy or response on the user or audience."

    @staticmethod
    def knowledge_extraction():
        return "Extract key knowledge points or insights from the given information or context."

    @staticmethod
    def entity_extraction():
        return "Identify and extract important entities (e.g., names, places, organizations) from the given text."

    @staticmethod
    def noise_identification():
        return "Detect and identify any noise or irrelevant information in the input data or context."

    @staticmethod
    def plugin_selection():
        return "Select the most appropriate plugin or tool to assist in executing the current task or strategy."