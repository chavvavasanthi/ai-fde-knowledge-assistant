import os
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings

app = FastAPI(title="AI FDE Enterprise Knowledge Assistant")

# Mock Auth Token Check (Q.5)
VALID_API_KEYS = {"enterprise_token_123": "Enterprise_Client_A"}

def authenticate_user(x_api_key: str = Header(...)):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid Customer Authentication Key")
    return VALID_API_KEYS[x_api_key]

class QueryRequest(BaseModel):
    question: str

# Sample Mock Database (Q.6 & Q.7)
MOCK_KNOWLEDGE_BASE = {
    "sla": "Standard customer support SLA response time is 2 hours for high-priority tickets.",
    "pricing": "Enterprise pricing starts at $1000/month including full workflow integration.",
    "security": "All customer data is encrypted using AES-256 both at rest and in transit."
}

@app.get("/")
def home():
    return {"message": "AI FDE Core System Active"}

@app.post("/api/v1/query")
async def process_customer_query(request: QueryRequest, client_name: str = Depends(authenticate_user)):
    q = request.question.lower()
    
    # Matching knowledge base (Q.11 & Q.12)
    matched_key = next((k for k in MOCK_KNOWLEDGE_BASE if k in q), None)
    
    if matched_key:
        return {
            "client": client_name,
            "answer": MOCK_KNOWLEDGE_BASE[matched_key],
            "confidence": 0.95,
            "status": "success",
            "source": f"Internal Doc: {matched_key.upper()}_Policy.pdf"
        }
    else:
        # Fallback / Escalation logic (Q.12)
        return {
            "client": client_name,
            "answer": "Exact information not found in internal docs. Escalating to human agent.",
            "confidence": 0.20,
            "status": "escalated_to_human",
            "source": "None"
        }
