from openai import OpenAI
from config import api_key

class BiasCheck:
    def __init__(self, model="gpt-4o-mini", api_key=api_key):
        self.config = {"base_model": model}
        self.api_key = api_key

    def _get_prompt(self):
        return input("How can I assist you? ")
    

    def _get_llm_output(self, prompt):
         try:
            client = OpenAI(
                api_key=api_key,)
            response = client.chat.completions.create(
                model=self.config["base_model"],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
         except Exception as e:
             return f"Error in _get_llm_output: {str(e)}"
         
    def run(self):
        user_input = self._get_prompt()
        output = self._get_llm_output(user_input)
        print(output)
        return output

bc = BiasCheck() 
result = bc.run()