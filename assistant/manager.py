import os
import openai
import time
from dotenv import load_dotenv
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_to_openai(file):
    """Upload a file to OpenAI and return its file ID."""
    with open(file, "rb") as f:
        response = openai.files.create(file=f.read(), purpose="assistants")
    return response.id if response else None

def create_assistant(create,assistant_name,model_name,instructions,file_up):

    if create.lower() == "create":

        stored_file = []
        additional_file_id = upload_to_openai(file_up)
        stored_file.append(additional_file_id)

        my_assistant = client.beta.assistants.create(
                        instructions=instructions,
                        name=assistant_name,
                        tools=[{"type": "retrieval"}],
                        model=model_name,
                        file_ids=stored_file,
                    )
    return my_assistant

def chat_assistant(id_assistente, user_input):

        
    try:
        # Create a thread
        thread = client.beta.threads.create()
        my_thread_id = thread.id
    
    except:
        print("There was a problem with OpenAI Servers")
        time.sleep(5)
        return "There was a problem with OpenAI Servers"

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
            time.sleep(3)
        
        response = client.beta.threads.messages.list(
            thread_id=my_thread_id
        )

        if response.data:
            return response.data[0].content[0].text.value
        else:
            return "Sorry, I didn't understand. Can you rephrase?"
