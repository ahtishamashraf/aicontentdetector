import hashlib
class FakeProvider:
 def load(self): pass
 def score(self,text):
  score=0.2+(int(hashlib.sha256(text.encode()).hexdigest()[:8],16)%6000)/10000
  return [score],[max(1,len(text.split()))]
 def metadata(self): return {"model_id":"test-only-deterministic","revision":"1","device":"cpu"}
