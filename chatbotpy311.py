import os
import pandas as pd
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

os.environ['OPENAI_API_KEY']

df = pd.read_csv('jCrewProductDataASCII2.csv')


"""## CSV Agent

NOTE: this agent calls the Pandas DataFrame agent under the hood, which in turn calls the Python agent, which executes LLM generated Python code - this can be bad if the LLM generated Python code is harmful. Use cautiously.
"""

agent = create_csv_agent(OpenAI(temperature=0), 
                         'jCrewProductDataASCII2.csv', 
                         verbose=True)

agent

agent.agent.llm_chain.prompt.template

"""
You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
You should use the tools below to answer the question posed of you:

python_repl_ast: A Python shell. Use this to execute python commands. Input should be a valid python command. When using this tool, sometimes output is abbreviated - make sure it does not look abbreviated before using it in your answer.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [python_repl_ast]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question


This is the result of `print(df.head())`:
{df}

Begin!
Question: {input}
{agent_scratchpad}"""

# method to be called by slackbothost.py
def query(str):
    response = agent.run(str)
    return response