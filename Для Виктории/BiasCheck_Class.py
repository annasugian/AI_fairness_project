import csv
import os
from openai import OpenAI
from config import api_key

class BiasCheck:
    '''
    Класс для проверки и документации предвзятости в пользовательском вводе и выводе LLM.
    '''
    LOG_FILE = "bias_check_log.csv"

    def __init__(self, model="gpt-4o-mini", api_key=api_key):
        self.config = {"base_model": model}
        self.api_key = api_key
        self._ensure_log_file()

    def _ensure_log_file(self):
        '''
        Проверяет существование файла логов и создает его, если он не существует.
        '''
        if not os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, mode='w', newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['event_type', 'text', 'result'])

    def log_event(self, event_type: str, text: str, result: str):
        '''
        Записывает событие (prompt/output) в лог-файл.
        '''

        with open(self.LOG_FILE, mode='a', newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                event_type, 
                text.replace("\n", " "), 
                result])
    
    def _get_prompt(self):
        '''
        Получает ввод от пользователя.
        '''
        return input("How can I assist you: ")
    
    def check_prompt(self, prompt):
        '''
        Проверяет, содержит ли ввод пользователя предвзятое или оскорбительное содержание.
        '''
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
            
            answer = response.choices[0].message.content.lower()
            result = 'Biased' if 'yes' in answer else 'Non-biased'
            self.log_event("prompt_check", prompt, result)
            return result
        
        except Exception as e:
            return f"Error in check_prompt: {str(e)}"
    
    def _get_llm_output(self, prompt):
        '''
        Получает вывод от LLM на основе пользовательского непредвзятого ввода.
        '''
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
    
    def check_llm_output(self, output):
        '''
        Проверяет, содержит ли вывод LLM предвзятое или оскорбительное содержание.
        '''
        try:
            client = OpenAI(
                api_key=api_key,)

            response = client.chat.completions.create(
                model=self.config["base_model"],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Check if the following text contains any offensive or biased content. "
                                                "If it does, please respond with 'Yes' or 'No'.\n\n"
                                                f"Text: \"{output}\""}
                ]
            )
            answer = response.choices[0].message.content.lower()
            result = 'Biased' if 'yes' in answer else 'Non-biased'
            self.log_event("output_check", output, result)
            return result
            
        except Exception as e:
            return f"Error in check_prompt: {str(e)}"
            

    def run(self):
        '''
        Запускает процесс проверки на предвзятость.
        '''
        user_input = self._get_prompt()
        checked_input = self.check_prompt(user_input)
        print(checked_input)

        if checked_input == 'Non-biased':
            output = self._get_llm_output(user_input)
            print(output)
            evaluation = self.check_llm_output(output)
            print(evaluation)
            return evaluation
        else:
            print('I cannot assist you with this request as it contains biased content.')
            return checked_input
        
if __name__ == "__main__":
    bc = BiasCheck() 
    result = bc.run()
