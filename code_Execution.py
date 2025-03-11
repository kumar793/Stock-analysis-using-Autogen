import os 
import pdb
from dotenv import load_dotenv
from autogen.code_utils import create_virtual_env
from autogen.coding import CodeBlock, LocalCommandLineCodeExecutor
from autogen import AssistantAgent
from autogen import ConversableAgent
import datetime
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
api = os.getenv("GEMINI_API_KEY")
config_list  = [
    {
        "model": "gemini-2.0-flash",
        "api_key": api,
        "api_type": "google"
    }
]
llm_config = {
    "config_list" :config_list,
    "cache":None
}


#Executor environment setup
venv_dir = ".env_llm"
venv_context = create_virtual_env(venv_dir)
executor = LocalCommandLineCodeExecutor(
    virtual_env_context=venv_context,
    timeout = 200,
    work_dir = "coding")
print(executor.execute_code_blocks(code_blocks=[
    CodeBlock(
        language="python",
        code="import sys; print(sys.executable)"
    )
]))


code_writer_agent = AssistantAgent(
    name = "code_writer_agent",
    llm_config=llm_config,
    code_execution_config = False,
    human_input_mode="NEVER"
)

code_writer_agent_system_message = code_writer_agent.system_message
print(code_writer_agent_system_message)
pdb.set_trace()


# Agent that executes code
code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS",
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)


today = datetime.datetime.now().date()

message = f"Today is {today}. "\
"Create a plot showing the normalized price of NVDA and BTC-USD for the last 5 years "\
"with their 60 weeks moving average. "\
"Make sure the code is in markdown code block, print the normalized prices, save the figure"\
" to a file asset_analysis.png and show it. Provide all the code necessary in a single python bloc. "\
"Re-provide the code block that needs to be executed with each of your messages. "\
"If python packages are necessary to execute the code, provide a markdown "\
"sh block with only the command necessary to install them and no comments."

# Let's define the chat and initiate it !
chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message
)