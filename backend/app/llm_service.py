import ollama

class OllamaService:
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self.client = ollama.Client()

    def generate_response(self, prompt: str):
        """
        Sends a prompt to the Ollama model and retrieves the response.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            dict: The response from the Ollama model.
        """
        try:
            print(f"Sending prompt to model '{self.model}': {prompt}")
            response = self.client.generate(model=self.model, prompt=prompt)
            return response
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    ollama_service = OllamaService(model="llama3.2")
    prompt_text = "What is the capital of France?"
    response = ollama_service.generate_response(prompt=prompt_text)
    print(response.response)