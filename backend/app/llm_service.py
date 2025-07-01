import ollama
import os

class OllamaService:
    def __init__(self, model: str = "llama3.2"):

        OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model
        self.client = ollama.Client(host=OLLAMA_HOST)

    def generate_response(self, prompt: str = None, query: str = None, context: str = None) -> dict:
        """
        Sends a prompt to the Ollama model and retrieves the response.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            dict: The response from the Ollama model.
        """

        formatted_chunks = "\n\n".join(context)
        prompt = f""""
            Answer the question based only on the context from various documents below.

            Context: 
            {formatted_chunks}

            Question: {query}
        """

        # if not prompt:
        #     prompt = f"""
        #     You are a helpful assistant. Please provide a response to the following query: {query}. Use this context to help you answer: {context}.
        #     """
        try:
            print(f"Sending prompt to model '{self.model}': {prompt}")
            response = self.client.generate(model=self.model, prompt=prompt)
            return response.response if response else {"message": "No response from model."}
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    ollama_service = OllamaService(model="llama3.2")
    prompt_text = "What is the capital of France?"
    response = ollama_service.generate_response(prompt=prompt_text)
    print(response.response)