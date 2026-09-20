import streamlit as st
import requests

st.set_page_config(page_title="AI FDE Customer Assistant", layout="centered")

st.title("🤖 Enterprise AI Support Assistant")
st.caption("AI FDE System: Multi-Tenant Auth, RAG Querying & Fallback Workflows")

api_key = st.text_input("Enter Enterprise API Key:", value="enterprise_token_123", type="password")
backend_url = st.text_input("FastAPI Backend URL:", value="http://localhost:8000")

user_query = st.text_area("Ask a question about SLA, Pricing, or Security:")

if st.button("Submit Query"):
    if not api_key:
        st.error("Please provide an API Key.")
    else:
        headers = {"x-api-key": api_key}
        payload = {"question": user_query}
        
        try:
            res = requests.post(f"{backend_url}/api/v1/query", json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                st.success("Response Received!")
                st.write(f"**Answer:** {data['answer']}")
                st.write(f"**Confidence Score:** {data['confidence']}")
                st.write(f"**Source Document:** {data['source']}")
                st.write(f"**Status:** {data['status']}")
            else:
                st.error(f"Authentication Failed or Server Error! Code: {res.status_code}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
