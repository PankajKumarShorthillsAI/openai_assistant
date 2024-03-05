from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .manager import create_assistant,chat_assistant,create_assistant_without_json_data,chat_assistant_azure
import os
import json
import time
from rest_framework import serializers

class ResponseDataSerializer(serializers.Serializer):
    new_suggestions = serializers.ListField(child=serializers.CharField())

class ResponseAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField()

class ResponseDataSerializerAzure(serializers.Serializer):
    answer = serializers.ListField(child=serializers.CharField())

class CreateAssistant(APIView):
    """""" 
    def post(self, request):
        try:
            
            json_data = request.data.get('json_data')
            create = request.data.get('create')
            assistant_name = request.data.get('assistant_name')
            model_name = request.data.get('model_name')
            instructions = request.data.get('instructions')
            #  instructions prompt for creating assistant

            # PROMPT_INTRUCTIONS = f"""chatbot assistant designed to assist customers with inquiries related to {instructions}. The chatbot will take input in the form of a JSON file, extracting relevant intents, keywords, and providing suggested questions along with their respective answers. The goal is to enhance user engagement and offer comprehensive information about {instructions}"""

            PROMPT_INTRUCTIONS = f"""chatbot assistant designed to assist customers with inquiries related to {instructions}."""

            if json_data:
                time.sleep(22) # Sleep put for simple api key
                json_data_dump = json.dumps(json_data, indent=2)
                file_path = os.path.join("file_json.json")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(json_data_dump)
            
                new_assistant = create_assistant(
                    create=create,
                    assistant_name=assistant_name,
                    model_name=model_name,
                    instructions=PROMPT_INTRUCTIONS,
                    file_up="file_json.json"
                )
                return Response({"message": "json_data_created_successfully",
                                "assistant_id": new_assistant.id,
                                }, status.HTTP_200_OK)
            else:
                # For azure key
                new_assistant = create_assistant_without_json_data(
                    create=create,
                    assistant_name=assistant_name,
                    model_name=model_name,
                    instructions=PROMPT_INTRUCTIONS
                )
                return Response({"message": "assistant_created_successfully",
                                "assistant_id": new_assistant.id,
                                }, status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)


class ChatAssistant(APIView):
    """""" 
    def post(self, request):
        try:
            
            
            assistant_id = request.data['assistant_id']
            chat_query = request.data['chat_query']
            instructions = request.data['instructions']
            # instructions for creating List of Intent
            if chat_query.lower() == "intent":
                time.sleep(22)
                # instructions = instructions + new prompt for getting list of intetns
                PROMPT_INTENT = """
                Is this Vehicle still available?
                How far is it from my current location?
                Can I take the test drive before I make a purchase decision?
                What is the trim?
                How old is the vehicle?
                How old is the vehicle? 
                What is the odometer reading?
                What is the mileage of this vehicle?
                Can I trust the dealer?
                What is the seating capacity of of this vehicle?
                What is the engine type?
                What is the price of this vehicle?
                What is the model of the vehicle?
                Are there any discounts? Are listed prices final or negotiable?


                Create keywords that I can use in a chatbot covering all these questions. Keep the keywords self explainatory. Give a python list of strings. Dont provide extra information/instructions. 

                EXAMPLE_OUTPUT_FORMAT: ["keyword_1","keyword_2",..]
                """


                response_data_str = chat_assistant(
                    id_assistente=assistant_id,
                    user_input=PROMPT_INTENT
                )
                response_data = eval(response_data_str)  # Convert the string to a list

                serializer = ResponseDataSerializer(data={"new_suggestions": response_data})
                serializer.is_valid(raise_exception=True)

                return Response({"intent": serializer.validated_data["new_suggestions"],
                                "assistant_id": assistant_id,
                                }, status.HTTP_200_OK)
            
            # List Query from intent
            if chat_query.lower() == "query_from_intent":
                time.sleep(22)
                # List of query from intent
                PROMPT_QUERY_INTENT = f"""
                Intent: {instructions}

                Create 3 questions that can be asked which are related to the context of the intent given above. Give a python list of string. Do not provide any extra details/instructions and give a clean list.

                OUTPUT_FORMAT: ["Example_question_1","Example_question_2"...]"""

                response_data_str = chat_assistant(
                    id_assistente=assistant_id,
                    user_input=PROMPT_QUERY_INTENT
                )

                response_data = eval(response_data_str)  # Convert the string to a list

                serializer = ResponseDataSerializer(data={"new_suggestions": response_data})
                serializer.is_valid(raise_exception=True)

                return Response({"new_suggestions": serializer.validated_data["new_suggestions"],
                                "assistant_id": assistant_id,
                                }, status.HTTP_200_OK)

            # Query chat
            if chat_query.lower() == "query":
                time.sleep(22)
                # Answering
                answer = chat_assistant(
                    id_assistente=assistant_id,
                    user_input=instructions
                )

                serializer_answer = ResponseAnswerSerializer(data={"answer": answer})
                serializer_answer.is_valid(raise_exception=True)
                time.sleep(22)
                # New query based on previous answer
                PROMPT_QUERY = f"""
                Question: {instructions}

                Create 3 questions that can be asked which are related to the context of the question given above. Give a python list of string. Do not provide any extra details/instructions and give a clean list.

                OUTPUT_FORMAT: ["Example_question_1","Example_question_2"...]"""
                
                response_data_str = chat_assistant(
                    id_assistente=assistant_id,
                    user_input=PROMPT_QUERY
                )
                response_data = eval(response_data_str)  # Convert the string to a list

                serializer = ResponseDataSerializer(data={"new_suggestions": response_data})
                serializer.is_valid(raise_exception=True)

                return Response({
                    "new_suggestions": serializer.validated_data["new_suggestions"],
                    "answer": serializer_answer.validated_data["answer"],
                    "assistant_id": assistant_id,
                }, status.HTTP_200_OK)
            

            # Query chat without json data initial query
            if chat_query.lower() == "intial_query_without_json_data":
                # Answering
                PROMPT_ANWERING_WITHOUT_JSON_DATA_INITIAL = f"""Answer the following question: {instructions}. Give a python list of string. Do not provide any extra details/instructions and give a clean list.
                OUTPUT_FORMAT: ["Example_question_1","Example_question_2"...]
                """

                answer = chat_assistant_azure(
                    id_assistente=assistant_id,
                    user_input=PROMPT_ANWERING_WITHOUT_JSON_DATA_INITIAL
                )
                answer = eval(answer)  # Convert the string to a list
                serializer_answer = ResponseDataSerializerAzure(data={"answer": answer})
                serializer_answer.is_valid(raise_exception=True)

                return Response({
                    "new_suggestions": serializer_answer.validated_data["answer"],
                    "assistant_id": assistant_id,
                }, status.HTTP_200_OK)

            # Query chat without json data
            if chat_query.lower() == "query_without_json_data":
                # Answering
                PROMPT_ANWERING_WITHOUT_JSON_DATA = f"""Answer the following question: {instructions}. Do not provide any extra details/instructions and give a clean answer. After giving answer do write anything extra"""
                
                answer = chat_assistant_azure(
                    id_assistente=assistant_id,
                    user_input=PROMPT_ANWERING_WITHOUT_JSON_DATA
                )
                
                answer = eval(answer)  # Convert the string to a list

                fliter_answer = [item for item in answer if item]
                serializer_answer = ResponseDataSerializerAzure(data={"answer": fliter_answer})
                serializer_answer.is_valid(raise_exception=True)

                # # New query based on previous answer
                # PROMPT_QUERY = f"""
                # Question: {instructions}

                # Create 3 questions that can be asked which are related to the context of the question given above. Give a python list of string. Do not provide any extra details/instructions and give a clean list.

                # OUTPUT_FORMAT: ["Example_question_1","Example_question_2"...]"""
                
                # response_data_str = chat_assistant_azure(
                #     id_assistente=assistant_id,
                #     user_input=PROMPT_QUERY
                # )
                # response_data = eval(response_data_str)  # Convert the string to a list

                # serializer = ResponseDataSerializer(data={"new_suggestions": response_data})
                # serializer.is_valid(raise_exception=True)

                return Response({
                    # "new_suggestions": serializer.validated_data["new_suggestions"],
                    "answer": serializer_answer.validated_data["answer"],
                    "assistant_id": assistant_id,
                }, status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)