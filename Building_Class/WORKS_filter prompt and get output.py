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
        checked_input = self.check_prompt(user_input)
        print(checked_input)
        if checked_input == 'No bias detected':
            output = self._get_llm_output(user_input)
            print(output)
            return output
        else:
            print('I cannot assist you with this request as it contains biased content.')
        
bc = BiasCheck() 
result = bc.run()

# Test 1:
# How can I assist you? Why are women so dumb?
# Bias detected
# I cannot assist you with this request as it contains biased content.

# Test 2:
# How can I assist you? What is GPT?
# No bias detected
# GPT stands for "Generative Pre-trained Transformer." It is a type of artificial intelligence model developed 
# by OpenAI that is designed to understand and generate human-like text. Here are the key components of GPT:

# 1. **Generative**: GPT can generate coherent and contextually relevant text based on the input it receives. 
# This means it can create new content rather than just classify or analyze existing data.

# 2. **Pre-trained**: GPT models are initially trained on a large dataset containing diverse text from the internet. 
# This pre-training phase allows the model to learn the structure of language, grammar, facts, and some reasoning abilities.

# 3. **Transformer**: This refers to the underlying neural network architecture that GPT uses. 
# The Transformer architecture, introduced in a paper titled "Attention is All You Need," enables the model 
# to effectively process and generate sequences of text by utilizing mechanisms called self-attention and feed-forward neural networks.

# These features allow GPT to perform a wide range of language tasks, such as answering questions, writing 
# essays, creating conversational agents, and more. The model can be fine-tuned for specific tasks or domains, 
# enhancing its performance in targeted applications. The most well-known versions of GPT include GPT-2 and GPT-3, 
# with each iteration improving in capabilities and complexity.