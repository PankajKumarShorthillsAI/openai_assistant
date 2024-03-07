import os
import openai
from openai import AzureOpenAI
import time
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_assistant_without_json_dataV2(create,assistant_name,model_name,instructions):

    if create.lower() == "create":
        # Creating assistant
        my_assistant = client.beta.assistants.create(
                        instructions=instructions,
                        name=assistant_name,
                        model=os.getenv("OPENAI_MODEL"),
                    )
        # Creating threads
        thread = client.beta.threads.create()
        my_thread_id = thread.id
    return my_assistant,my_thread_id

def chat_assistantV2(id_assistente, my_thread_id,user_input):
     
    def get_response(question):
        try:
            message = client.beta.threads.messages.create(
                thread_id=my_thread_id,
                role="user",
                content=question
            )
        
            # Run
            run = client.beta.threads.runs.create(
                thread_id=my_thread_id,
                assistant_id=id_assistente,
            )
        
            return run.id
        except:
            print("🛑 There was a problem with OpenAI Servers")
            time.sleep(5)
            return "There was a problem with OpenAI Servers"

    def check_status(run_id):
        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=my_thread_id,
                run_id=run_id,
            )
            return run.status
        except:
            print("🛑 There was a problem with OpenAI Servers")
            time.sleep(5)
            return "There was a problem with OpenAI Servers"

    if user_input:
        
        run_id = get_response(user_input)
        status = check_status(run_id)
        
        while status != "completed":
            status = check_status(run_id)
        
        response = client.beta.threads.messages.list(
            thread_id=my_thread_id
        )

        if response.data:
            return response.data[0].content[0].text.value
        else:
            return "Sorry, I didn't understand. Can you rephrase?"