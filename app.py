import streamlit as st
from graph import EssayWriter
import openai

st.set_page_config(page_title="Essay Writer Chat Bot", page_icon="🤖")
st.image("./media/cover.jpg", use_column_width=True)

button_html = f'''
    <div style="display: flex; justify-content: center;">
        <a href="https://buymeacoffee.com/mesutduman" target="_blank">
            <button style="
                background-color: #FFDD00;
                border: none;
                color: black;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
            ">
            ☕ Buy Me a Coffee
            </button>
        </a>
    </div>
'''

if "messages" not in st.session_state:
    st.session_state.messages =  [{"role": "assistant", "content": "Hello!"}]
    st.session_state.app = None
with st.sidebar:
    st.info(" * This app uses the OpenAI API to generate text, please provide your API key."
            "\n\n * This app uses the 'gpt-4o-mini-2024-07-18' model. Cost effective and efficient."
            "\n\n * If you don't have an API key, you can get one [here](https://platform.openai.com/signup)."
            "\n\n * You can also find the source code for this app [here](https://github.com/mesutdmn/Autonomous-Multi-Agent-Systems-with-CrewAI-Essay-Writer)"
            "\n\n * App keys are not stored or saved in any way.")
    openai_key_input = st.text_input("OpenAI API Key", type="password")
    developer_mode = st.checkbox("I don't have key, use developer's money 😓", value=False)
    openai_key = openai_key_input or (st.secrets["OpenAI_API_KEY"] if developer_mode else "")
    openai.api_key = openai_key
    if len(openai_key) < 1:
        st.error("Please enter your OpenAI API key")

        chat_active = True
    else:
        chat_active = False


def initialize_agents():
    essay_writer = EssayWriter(api_key=openai_key).graph
    st.success("Agents successfully initialized")
    return essay_writer

with st.sidebar:
    if st.button("Initialize Agents", type="primary"):
        st.session_state.app = initialize_agents()
    st.divider()
    st.markdown(button_html, unsafe_allow_html=True)

app = st.session_state.app
def generate_response(topic):
    return app.invoke(input={"topic": topic})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if topic:= st.chat_input(placeholder="Ask a question", disabled=chat_active):
    st.chat_message("user").markdown(topic)

    st.session_state.messages.append({"role": "user", "content": topic})
    with st.spinner("Thinking..."):
        response = generate_response(topic)

    with st.chat_message("assistant"):
        if "pdf_name" in response:
            st.markdown(f"{response['response']}: [Download PDF]({response['pdf_name']})")
            st.session_state.messages.append({"role": "assistant", "content": f"{response['response']}: [Download PDF]({response['pdf_name']})"})
        else:
            st.markdown(response["response"])
            st.session_state.messages.append({"role": "assistant", "content": response["response"]})






