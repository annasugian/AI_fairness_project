from openai import OpenAI
from config import api_key

class BiasCheck:
    def __init__(self, model="gpt-4o-mini", api_key=api_key):
        self.config = {"base_model": model}
        self.api_key = api_key

    def _get_prompt(self):
        return input("How can I assist you? ")
    
    def check_prompt(self, prompt):
        try:
            client = OpenAI(
                api_key=api_key,)

            response = client.chat.completions.create(
                model=self.config["base_model"],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Check if the following text contains any offensive or biased content. "
                                                "If it does, please respond with 'Yes' or 'No'.\n\n"
                                                f"Text: \"{prompt}\""}
                ]
            )
            if "yes" in response.choices[0].message.content.lower():
                return 'Bias detected'
            else:
                return 'No bias detected'
            
        except Exception as e:
            return f"Error in check_prompt: {str(e)}"
         
    def run(self):
        user_input = self._get_prompt()
        evaluation = self.check_prompt(user_input)
        print(evaluation)
        return evaluation

bc = BiasCheck() 
result = bc.run()