import os 
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
import autogen
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
}
"""
stock_symbols = st.text_input("Enter the stock symbols separated by commas:")
stocks = list(map(str, stock_symbols.split(',')))"""

stocks = ["Reliance","Tata Motors"]

date_str = datetime.now().strftime("%Y-%m-%d")
financial_tasks = [
    f"""
**Task:**
Do not simulate fake data for this task. Use the real data from the stock market using angel one smart apiṅ.
1. **Retrieve {stocks} Information useing groww api useage ask user if any authentication required.:**
   - Get the full names and stock tickers of the spece over the past 6 months in terms of percentage change.
   - Include the following financial metrics, if applicable:
     - P/E ratio
     - Forward P/E
     - Dividends
     - Price to book
     - Debt/Eq
     - ROE

2. **Visualize Stock Prices:**
   - Prepare a figure of the normalized price of these stocks.
   - Save the figure to a file named `normalized_prices.png`.

3. **Analyze Correlation:**
   - Analyze the correlation between the stocks.
""","""
4. **Predict Future Stock Prices:**
   - Use the following methods to predict future stock prices:
     - MA (Moving Average)
     - AR (AutoRegressive)
     - ARIMA (AutoRegressive Integrated Moving Average)
     - LSTM (Long Short-Term Memory)
     - Prophet
     - SARIMAX (Seasonal AutoRegressive Integrated Moving-Average with eXogenous factors)
   - Perform technical and fundamental analysis.
   - Provide images of the technical analysis.
   - Save the code used for the analysis.
   - Include future predicted values based on news, technical analysis, and indicators.
   - Specify the method, timeframe, and stop-loss.

5. **Investigate Stock Performance:**
   - Retrieve market news headlines related to the stocks using Python.
   - Retrieve at least 10 headlines per stock.
   - Do not use a solution that requires an API key.
   - Do not perform sentiment analysis.

**Output:**
   - A table of prediction mechanisms, predicted prices, timeframes, and stop-loss.
   - Python code for Prophet, LSTM, and SARIMAX to predict the prices.
   - News headlines related to the stocks.
"""
]



writing_tasks = [
        """It looks like you want a comprehensive financial report that includes various analyses and visualizations. To proceed, I'll need the following information:

1. **Normalized Prices Figure**: Please provide the `normalized_prices.png` figure.
2. **Other Figures**: Any additional figures you want to include.
3. **Fundamental Ratios and Data**: Detailed information on the fundamental ratios and data for the stocks.
4. **Recent News Headlines**: Summaries or links to recent news headlines for each stock.
5. **Technical and Fundamental Analysis Images**: RSI images and any other technical analysis images.
6. **Advanced Stock Predicting Images**: Any images related to advanced stock prediction.
7. **Predicted Prices Table**: A table of predicted prices using different methods target value, and stop-loss with timeframe.
for this ommit legal reviewer and mention a disclamier.
        """]

exporting_task = ["""Save the report and only the report to a .md file using a python script."""]

financial_assistant = autogen.AssistantAgent(
    name="Financial_assistant",
    llm_config=llm_config,
)
research_assistant = autogen.AssistantAgent(
    name="Researcher",
    llm_config=llm_config,
)



writer = autogen.AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="""
        You are a professional writer, known for
        your insightful and engaging finance reports.
        You transform complex concepts into compelling narratives. 
        Include all metrics provided to you as context in your analysis.
        Only answer with the financial report written in markdown directly, do not include a markdown language block indicator.
        Only return your final work without additional comments.
        """,
)

export_assistant = autogen.AssistantAgent(
    name="Exporter",
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="You are a critic. You review the work of "
                "the writer and provide constructive "
                "feedback to help improve the quality of the content.",
)

legal_reviewer = autogen.AssistantAgent(
    name="Legal_Reviewer",
    llm_config=llm_config,
    system_message="You are a legal reviewer, known for "
        "your ability to ensure that content is legally compliant "
        "and free from any potential legal issues. "
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role.",
)

consistency_reviewer = autogen.AssistantAgent(
    name="Consistency_reviewer",
    llm_config=llm_config,
    system_message="You are a consistency reviewer, known for "
        "your ability to ensure that the written content is consistent throughout the report. "
        "Refer numbers and data in the report to determine which version should be chosen " 
        "in case of contradictions. "
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role. ",
)

textalignment_reviewer = autogen.AssistantAgent(
    name="Text_alignment_reviewer",
    llm_config=llm_config,
    system_message="You are a text data alignment reviewer, known for "
        "your ability to ensure that the meaning of the written content is aligned "
        "with the numbers written in the text. " 
        "You must ensure that the text clearely describes the numbers provided in the text "
        "without contradictions. "
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role. ",
)

completion_reviewer = autogen.AssistantAgent(
    name="Completion_Reviewer",
    llm_config=llm_config,
    system_message="You are a content completion reviewer, known for "
        "your ability to check that financial reports contain all the required elements. "
        "You always verify that the report contains: a news report about each asset, " 
        "a description of the different ratios and prices, "
        "a description of possible future scenarios, a table comparing fundamental ratios and "
        " at least a single figure. "
        "Make sure your suggestion is concise (within 3 bullet points), "
        "concrete and to the point. "
        "Begin the review by stating your role. ",
)

meta_reviewer = autogen.AssistantAgent(
    name="Meta_Reviewer",
    llm_config=llm_config,
    system_message="You are a meta reviewer, you aggregate and review "
    "the work of other reviewers and give a final suggestion on the content.",
)

def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content. 
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''

review_chats = [
    {
    "recipient": legal_reviewer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into a JSON object only:"
        "{'Reviewer': '', 'Review': ''}.",},
     "max_turns": 1},
    {"recipient": textalignment_reviewer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into a JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
    {"recipient": consistency_reviewer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into a JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
    {"recipient": completion_reviewer, "message": reflection_message, 
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt" : 
        "Return review into a JSON object only:"
        "{'reviewer': '', 'review': ''}",},
     "max_turns": 1},
     {"recipient": meta_reviewer, 
      "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.", 
     "max_turns": 1},
]

critic.register_nested_chats(
    review_chats,
    trigger=writer,
)

# ===

user_proxy_auto = autogen.UserProxyAgent(
    name="User_Proxy_Auto",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "work_dir",
        "use_docker": False,
    },  
)


chat_results = autogen.initiate_chats(
    [
        {
            "sender": user_proxy_auto,
            "recipient": financial_assistant,
            "message": financial_tasks[0],
            "silent": False,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt" : "Return the stock prices of the stocks, their performance and all other metrics"
                "into a JSON object only. Provide the name of all figure files created. Provide the full name of each stock.",
                            },
            "clear_history": False,
            "carryover": "Wait for confirmation of code execution before terminating the conversation. Verify that the data is not completely composed of NaN values. Reply TERMINATE in the end when everything is done."
        },
        
        {
            "sender": user_proxy_auto,
            "recipient": research_assistant,
            "message": financial_tasks[1],
            "silent": False,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt" : "Provide the news headlines as a paragraph for each stock, be precise but do not consider news events that are vague, return the result as a JSON object only.",
                            },
            "clear_history": False,
            "carryover": "Wait for confirmation of code execution before terminating the conversation. Reply TERMINATE in the end when everything is done."
        },
        
        {
            "sender": critic,
            "recipient": writer,
            "message": writing_tasks[0],
            "carryover": "I want to include a figure and a table of the provided data in the financial report.",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "sender": user_proxy_auto,
            "recipient": export_assistant,
            "message": exporting_task[0],
            "carryover": "Wait for confirmation of code execution before terminating the conversation. Reply TERMINATE in the end when everything is done.",
        },
    ]
)

