import streamlit as st
from graph import EssayWriter
import os
import base64

st.set_page_config(page_title="Essay Writer Chat Bot", page_icon="🤖")
st.image("./media/cover.jpg", use_column_width=True)

if "messages" not in st.session_state:
    st.session_state.messages =  [{"role": "assistant", "content": "Hello!"}]
    st.session_state.app = None
    st.session_state.chat_active = True

with st.sidebar:
    st.info(" * This app uses the GROQ API to generate text, please provide your API key."
            "\n\n * This app uses the 'mixtral-8x7b-32768' model. Cost effective and efficient."
            "\n\n * App keys are not stored or saved in any way."
            "\n\n * Writing essay may take some time, please be patient. Approximately 1-2 minutes."
            "\n\n * If you like this app, consider buying me a coffee ☕")
    openai_key_input = st.text_input("GROQ API Key", type="password",value="1234")
    developer_mode = st.checkbox("I don't have key, use developer's money 😓", value=False)
    openai_key = openai_key_input or (st.secrets["GROQ_API_KEY"] if developer_mode else "")




def initialize_agents():
    os.environ["GROQ_API_KEY"] = openai_key
    essay_writer = EssayWriter().graph

    if len(openai_key) < 1:
        st.error("Please enter your GROQ_API_KEY and Initialize the agents.")

        st.session_state.chat_active = True
    else:
        st.success("Agents successfully initialized")
        st.session_state.chat_active = False

    return essay_writer

with st.sidebar:
    if st.button("Initialize Agents", type="primary"):
        st.session_state.app = initialize_agents()
    st.divider()

app = st.session_state.app
def generate_response(topic):
    return app.invoke(input={"topic": topic})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if topic:= st.chat_input(placeholder="Ask a question", disabled=st.session_state.chat_active):
    st.chat_message("user").markdown(topic)

    st.session_state.messages.append({"role": "user", "content": topic})
    with st.spinner("Thinking..."):
        response = generate_response(topic)

    with st.chat_message("assistant"):
        if "pdf_name" in response:
            with open(f"./{response['pdf_name']}", "rb") as file:
                file_bytes = file.read()
                b64 = base64.b64encode(file_bytes).decode()
            href = f"<a href='data:application/octet-stream;base64,{b64}' download='{response['pdf_name']}'>Click here to download the PDF</a>"

            st.markdown(f"{response['response']}: {href}", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": f"{response['response']}: {href}"})
        else:
            st.markdown(response["response"])
            st.session_state.messages.append({"role": "assistant", "content": response["response"]})






