import logging
import os
import json
import traceback
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


# LOG_FILE=f"{datetime.now().strftime{'%m_%d_%y_%H_%M_%S'}}.log"
# log_path=os.path.join(os.getcwd(),"logs")

# LOG_FILEPATH=os.makedirs(log_path,exist_ok=True)\


# logging(level=logging.INFO,
#         filename=LOG_FILEPATH,
#         format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
#         )


# with open(r'C:\Users\ADITYA\mcqgen\Response.json', 'r') as file:
#         RESPONSE_JSON=json.load(file)


# Define the path to your JSON file
json_file_path = r'C:\Users\ADITYA\mcqgen\Response.json'

# Load and parse the JSON file
with open(json_file_path, 'r') as file:
    try:
        RESPONSE_JSON = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        RESPONSE_JSON = None


st.title("MCQs Creator Application with Langchain")


with st.form("user_input"):
        uploaded_file=st.file_uploader("upload a PDF or txt file")

        mcq_count=st.number_input("No. of MCQs", min_value=3,max_value=50)

        subject=st.text_input("Insert Subject",max_chars=20,placeholder="simple")

        tone=st.text_input("Complexity Level of Questions",max_chars=20,placeholder="Simple")

        button=st.form_submit_button("Create_MCQs")


        if button and uploaded_file is not None and mcq_count and subject and tone:
                with st.spinner("loading....."):
                        try:
                                text=read_file(uploaded_file)

                                with get_openai_callback() as cb:
                                        response=generate_evaluate_chain(
                                                {
                                                        "text":text,
                                                        "number":mcq_count,
                                                        "subject":subject,
                                                        "tone":tone,
                                                        "response_json":json.dumps(RESPONSE_JSON)
                                                }
                                        )


                        except Exception as e:
                                traceback.print_exception(type(e),e,e.__traceback__)
                                st.error("Error")
                        else:
                                print(f"Total tokens:{cb.total_tokens}")
                                print(f"Prompt tokens:{cb.prompt_tokens}")
                                print(f"CompletionTokens:{cb.completion_tokens}")
                                print(f"Total Cost:{cb.total_cost}")
                                if isinstance(response,dict):
                                        quiz=response.get("quiz",None)
                                        if quiz is not None:
                                                table_data=get_table_data(quiz)
                                                if table_data is not None :
                                                        df=pd.DataFrame(table_data)
                                                        df.index=df.index+1
                                                        st.table(df)

                                                        st.text_area(label="Review",value=response["review"])
                                                else:
                                                        st.error("Error in the table data")

                                        
                                else:
                                        st.write(response)




         