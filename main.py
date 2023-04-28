# Bring in deps
import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

try:
    os.environ['OPENAI_API_KEY'] = apikey
except:
    os.environ['OPENAI_API_KEY'] = st.secrets["apikey"]

# App framework
st.title('Calculate Calorie Chat Bot 🥗🤖')
prompt = st.text_input('Write the food whose calories you want')

# Prompt templates
title_template = PromptTemplate(
    input_variables=['topic'],
    template='write calorie of {topic}.'
)

script_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template='write me a youtube video script based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
)

# Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt:
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt)
    script = script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title)

    with st.expander('Wikipedia Research'):
        st.info(wiki_research)
