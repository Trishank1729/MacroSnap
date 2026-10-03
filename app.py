import streamlit as st
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT, SUMMARY_REQUEST_PROMPT
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# -------------------------
# Page Settings
# -------------------------

st.set_page_config(
    page_title="MacroSnap",
    page_icon="🥗",
    layout="centered"
)


# -------------------------
# Simple UI
# -------------------------

st.markdown("""
<style>

    .stApp {
        background-color: #0e1117;
    }

    h1 {
        text-align: center;
        margin-bottom: 0;
    }

    [data-testid="stCaptionContainer"] {
        text-align: center;
    }

    /* Move chat input slightly upward */
    div[data-testid="stChatInput"] {
        bottom: 65px !important;
    }

    /* Place email button directly below chat input */
    div.stButton {
        position: fixed;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        width: min(610px, calc(100vw - 40px));
        z-index: 999;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)


# -------------------------
# Email Function
# -------------------------

def send_email(to_email, subject, body):

    sender_email = st.secrets["GMAIL_ADDRESS"]
    app_password = st.secrets["GMAIL_APP_PASSWORD"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)


# -------------------------
# Gemini Setup
# -------------------------

api_key = st.secrets["GEMINI_API_KEY"]


@st.cache_resource
def get_gemini_client():

    return genai.Client(
        api_key=api_key
    )


client = get_gemini_client()


# -------------------------
# Page Heading
# -------------------------

st.title("🥗 MacroSnap")
st.caption("Your AI Nutrition Buddy")


# -------------------------
# Create Chat
# -------------------------

if "chat" not in st.session_state:

    st.session_state.chat = client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )


# -------------------------
# Store Messages
# -------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# -------------------------
# Display Conversation
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["type"] == "image":

            st.image(message["content"])

        else:

            st.write(message["content"])


# -------------------------
# Chat Input
# -------------------------

user_input = st.chat_input(
    "Ask about your food or upload a meal photo",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"]
)


# -------------------------
# Process User Input
# -------------------------

if user_input:

    photo = (
        user_input.files[0]
        if user_input.files
        else None
    )

    text = user_input.text

    parts = []


    # -------------------------
    # User Photo
    # -------------------------

    if photo is not None:

        photo_bytes = photo.getvalue()

        st.session_state.messages.append({
            "role": "user",
            "type": "image",
            "content": photo_bytes
        })

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type
            )
        )


    # -------------------------
    # User Text
    # -------------------------

    if text:

        st.session_state.messages.append({
            "role": "user",
            "type": "text",
            "content": text
        })

        parts.append(text)


    # -------------------------
    # Photo Only
    # -------------------------

    elif photo is not None:

        parts.append(
            "What is this meal? "
            "Give me the estimated calories, "
            "protein, carbs, and fat."
        )


    # -------------------------
    # Gemini Response
    # -------------------------

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your meal..."):

            response = st.session_state.chat.send_message(
                parts
            )

        st.write(response.text)


    # Save assistant response

    st.session_state.messages.append({
        "role": "assistant",
        "type": "text",
        "content": response.text
    })


    # Refresh so the conversation is displayed correctly

    st.rerun()


# -------------------------
# Email Summary
# -------------------------

if st.button(
    "📧 Send Meal Summary",
    use_container_width=True
):

    with st.spinner("Creating your meal summary..."):

        summary_response = (
            st.session_state.chat.send_message(
                SUMMARY_REQUEST_PROMPT
            )
        )

        summary = summary_response.text

    send_email(
        st.secrets["GMAIL_ADDRESS"],
        "MacroSnap - Your Nutrition Summary",
        summary
    )

    st.toast(
        "🟡Meal summary sent to your Gmail!",
        icon="📧"
    )