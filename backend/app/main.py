import time,uuid
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from app.core.config import get_settings
from detection.core import aggregate,diagnostics,label,normalize,paragraphs
settings=get_settings(); app=FastAPI(title="OriginLens API",version="1.0.0")
@app.middleware("http")
async def security(request:Request,call_next):
 response=await call_next(request); response.headers.update({"X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY","Referrer-Policy":"no-referrer","Content-Security-Policy":"default-src 'none'; frame-ancestors 'none'"}); response.headers["X-Correlation-ID"]=request.headers.get("X-Correlation-ID",str(uuid.uuid4())); return response
@app.get("/api/v1/health/live")
def live(): return {"status":"ok"}
@app.get("/api/v1/health/ready")
def ready(): return {"status":"ready","database":"configured","redis":"configured"}
@app.get("/api/v1/health/model")
def model(): return {"backend":settings.detector_backend,"model_id":settings.model_id,"load_status":"worker-managed"}
class Analyze(BaseModel): text:str=Field(min_length=1,max_length=50000); save_original_text:bool=False
@app.post("/api/v1/analyses/text")
def analyze(body:Analyze):
 clean,warnings=normalize(body.text); words=len(clean.split()); ps=paragraphs(body.text)
 base={"id":str(uuid.uuid4()),"status":"completed","counts":{"characters":len(body.text),"words":words,"paragraphs":len(ps)},"warnings":warnings,"disclaimers":["The score is an estimate, not proof of authorship.","Edited, paraphrased, translated, very short, formulaic, or domain-specific writing can be misclassified.","Human review and additional evidence are required for consequential decisions."]}
 if words<80: return base|{"label":"Insufficient text","score":None,"reliability":"insufficient","reliability_reasons":["At least 80 words are required"],"paragraphs":[]}
 from detection.engines.fake import FakeProvider
 if settings.detector_backend!="fake": return JSONResponse(status_code=503,content={"error":{"code":"analysis_unavailable","message":"Analysis worker is required for real-model inference","correlation_id":str(uuid.uuid4())}})
 provider=FakeProvider(); scores,weights=provider.score(clean); raw,stability=aggregate(scores,weights); score=round(raw*100)
 return base|{"label":label(score),"score":score,"raw_model_score":raw,"reliability":"low" if words<150 else "normal","reliability_reasons":["Limited text"] if words<150 else [],"features":diagnostics(clean)|{"window_stability":stability},"model":provider.metadata(),"paragraphs":[{"id":p.id,"index":p.index,"text":p.text if body.save_original_text else None,"words":p.words,"score":score,"label":label(score)} for p in ps]}
