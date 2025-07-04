import ollama
from dotenv import load_dotenv
import os
from openai import OpenAI

class LLMService:
    def __init__(self, model: str = "llama3.2", use_ollama: bool = True):
        load_dotenv()

        self.model = model
        self.use_ollama = use_ollama

        if not self.use_ollama:
            self.API_KEY = os.getenv("LLM_API_KEY")
            self.API_URL = os.getenv("LLM_API_URL", "https://api.openai.com/v1")
            self.client = OpenAI(api_key=self.API_KEY)
        
        else:
            OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            self.client = ollama.Client(host=OLLAMA_HOST)

    def generate_response(self, prompt: str = None, query: str = None, context = None) -> dict:
        """
        Sends a prompt to the Ollama model and retrieves the response.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            dict: The response from the Ollama model.
        """

        formatted_chunks = "\n\n".join(context) if context else ""
        prompt = f"""
            Answer the question based only on the context from various documents below.

            Context: 
            {formatted_chunks}

            Question: {query}
        """

        try:
            if self.use_ollama:
                print(f"Sending prompt to ollama model '{self.model}': {prompt}")
                response = self.client.generate(model=self.model, prompt=prompt)
                return response.response if response else {"message": "No response from model."}
            else:
                print(f"Sending prompt to OpenAI model '{self.model}': {prompt}")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content if response.choices else {"message": "No response from model."}
        except Exception as e:
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    print("Local ollama test...")
    ollama_service = LLMService(model="llama3.2")
    prompt_text = "What is the capital of France?"
    ollama_response = ollama_service.generate_response(query=prompt_text, context=["Paris is the capital of France.", "France is a country in Europe."])
    print(ollama_response)
    print("\n\n")

    print("OpenAI test...")
    openai_service = LLMService(model="gpt-3.5-turbo", use_ollama=False)
    openai_response = openai_service.generate_response(query=prompt_text, context=["Paris is the capital of France.", "France is a country in Europe."])
    print(openai_response)