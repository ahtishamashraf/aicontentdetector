import os
os.environ["DETECTOR_BACKEND"]="fake"
from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_health(): assert c.get("/api/v1/health/live").json()=={"status":"ok"}
def test_short_is_honest(): assert c.post("/api/v1/analyses/text",json={"text":"short text"}).json()["label"]=="Insufficient text"
def test_analysis():
 text=" ".join(["This is a complete sentence for measured writing analysis."]*20)
 r=c.post("/api/v1/analyses/text",json={"text":text}); assert r.status_code==200 and 0<=r.json()["score"]<=100
