import streamlit as st
import requests
from datetime import datetime
import pytz
import uuid

# --- CONFIG ---
st.set_page_config(page_title="Client Management System", layout="wide")
tz = pytz.timezone("Asia/Karachi")

# --- PUSHBULLET TOKEN ---
PUSHBULLET_TOKEN = st.secrets["pushbullet_token"]  # Add your token in Streamlit secrets

AGENTS = ["Select Agent", "Arham Kaleem", "Arham Ali", "Haziq", "Usama", "Areeb"]
LLC_OPTIONS = ["Select LLC", "Bite Bazaar LLC", "Apex Prime Solutions"]

# --- FORM ---
st.title("Client Management System (Test Mode)")
st.write("Fill out all client details below:")

with st.form("transaction_form"):
    col1, col2 = st.columns(2)
    with col1:
        agent_name = st.selectbox("Agent Name", AGENTS)
        name = st.text_input("Client Name")
        phone = st.text_input("Phone Number")
        address = st.text_input("Address")
        email = st.text_input("Email")
        card_holder = st.text_input("Card Holder Name")
    with col2:
        card_number = st.text_input("Card Number")
        expiry = st.text_input("Expiry Date (MM/YY)")
        cvc = st.number_input("CVC", min_value=0, max_value=999, step=1)
        charge = st.text_input("Charge Amount")
        llc = st.selectbox("LLC", LLC_OPTIONS)
        date_of_charge = st.date_input("Date of Charge")

    submitted = st.form_submit_button("Submit")

# --- VALIDATION & NOTIFICATION ---
if submitted:
    missing_fields = []
    if agent_name == "Select Agent": missing_fields.append("Agent Name")
    if not name: missing_fields.append("Client Name")
    if not phone: missing_fields.append("Phone Number")
    if not charge: missing_fields.append("Charge Amount")
    if llc == "Select LLC": missing_fields.append("LLC")

    if missing_fields:
        st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")
        st.stop()

    # --- Send Notification ---
    try:
        record_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now(tz).strftime("%Y-%m-%d %I:%M:%S %p")

        message_title = f"🟢 New Client Added by {agent_name}"
        message_body = (
            f"Client: {name}\n"
            f"Phone: {phone}\n"
            f"Charge: {charge}\n"
            f"LLC: {llc}\n"
            f"Date: {date_of_charge.strftime('%Y-%m-%d')}\n"
            f"Ref: {record_id}\n"
            f"Time: {timestamp}"
        )

        response = requests.post(
            "https://api.pushbullet.com/v2/pushes",
            headers={"Access-Token": PUSHBULLET_TOKEN},
            json={"type": "note", "title": message_title, "body": message_body}
        )

        if response.status_code == 200:
            st.success(f"Notification sent! (Ref: {record_id})")
        else:
            st.error(f"Failed to send notification: {response.text}")

    except Exception as e:
        st.error(f"Error sending notification: {e}")
