import httpx
import streamlit as st
from rest.service import Chat, client

# Set page title
st.set_page_config(
    page_title="JuniaGPT",
    page_icon="🚀",
)

st.title("JuniaGPT 🚀")

# Set navbar
st.sidebar.title("Model parameters")

# Define temperature labels and corresponding values
temperature_mapping = {"Accurate": 0, "Balanced": 0.7, "Creative": 1}
temperature_choice = st.sidebar.radio(
    key="temperature",
    label="Model Behavior",
    options=temperature_mapping.keys(),
    index=1,
)
temperature = temperature_mapping.get(temperature_choice)

# Initialize chat history and variables
if "messages" not in st.session_state:
    st.session_state.messages = []

# Write queries and answers onto the page
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Query user prompt
if prompt := st.chat_input("What is your question?", key="user_prompt"):
    # store the new input from the user in the session_state "messages" key
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat = Chat(
            model="phi4",
            temperature=temperature,
            messages=st.session_state.messages,
        )

        response = client.post(chat=chat)

        if response.status_code == httpx.codes.OK:
            message = response.json()["answer"]
            st.markdown(message)

            st.session_state.messages.append(
                {"role": "assistant", "content": message},
            )

        else:
            st.write("It seems that something broke down 😅")
            st.write(response.status_code)
