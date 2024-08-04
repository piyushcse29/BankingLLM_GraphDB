import gradio as gr
import logging
import sys
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import Settings, PromptTemplate, StorageContext, load_index_from_storage
import torch
from huggingface_hub import login
import os

#Login to HF
login(token=os.environ["HF_TOKEN"])

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

# Log message to indicate the start of the application
logger.info("Starting Chat with the BankingLLM")

Settings, PromptTemplate, StorageContext, load_index_from_storage

# Set up logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

# Log message to indicate the start of the application
logger.info("Starting Chat with the BankingLLM")

# Define system prompt
SYSTEM_PROMPT = """
You are an AI assistant that answers questions in a friendly manner, based on the given source documents. Here are some rules you always follow:
- Generate human-readable output, avoid creating output with gibberish text.
- Generate only the requested output, don't include any other language before or after the requested output.
- Generate professional language.
- Never generate offensive or foul language.
- Replace TSB bank name with Dummy Bank
- Treat the user as a customer of Dummy Bank
- Always provide a friendly response ans emphasize the customer's needs
"""

# Define query wrapper prompt
query_wrapper_prompt = PromptTemplate("[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] ")
logger.info("Defined system and query wrapper prompts")

# Initialize HuggingFaceLLM
llm = HuggingFaceLLM(
    context_window=2048,
    max_new_tokens=256,
    generate_kwargs={"temperature": 0.25, "do_sample": False},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name="mistralai/Mistral-7B-Instruct-v0.2",
    model_name="mistralai/Mistral-7B-Instruct-v0.2",
    device_map="auto",
    tokenizer_kwargs={"max_length": 2048},
    model_kwargs={"torch_dtype": torch.float16}
)

logger.info("Initialized HuggingFaceLLM")

# Configure settings
Settings.chunk_size = 512
Settings.llm = llm
Settings.embed_model = "local"
logger.info("Configured settings")


# Load the chat engine
storage_context = StorageContext.from_defaults(persist_dir="./data/llama_index")
index = load_index_from_storage(storage_context)
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        # Use the chat engine to generate a response
        response = chat_engine.chat(message)
        bot_message = response.response
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(server_name="0.0.0.0", server_port=7860, share=False)