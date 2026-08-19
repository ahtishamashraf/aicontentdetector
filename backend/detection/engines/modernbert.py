class ModernBertProvider:
 def __init__(self,model_id,revision=None): self.model_id,self.revision=model_id,revision; self.model=None
 def load(self):
  import torch
  from transformers import AutoModelForSequenceClassification,AutoTokenizer
  self.tok=AutoTokenizer.from_pretrained(self.model_id,revision=self.revision)
  self.model=AutoModelForSequenceClassification.from_pretrained(self.model_id,revision=self.revision,use_safetensors=True)
  self.device="cuda" if torch.cuda.is_available() else "cpu"; self.model.to(self.device).eval()
  mapping={str(v).lower():int(k) for k,v in self.model.config.id2label.items()}
  matches=[i for name,i in mapping.items() if "ai" in name or "machine" in name]
  if not matches: raise RuntimeError("Model config does not identify the AI label")
  self.ai_label=matches[0]
 def score(self,text):
  import torch
  ids=self.tok(text,add_special_tokens=False)["input_ids"]; out=[]; weights=[]
  for start in range(0,len(ids),320):
   window=ids[start:start+384]; encoded=self.tok.prepare_for_model(window,return_tensors="pt").to(self.device)
   with torch.inference_mode(): logits=self.model(**encoded).logits
   out.append(float(torch.softmax(logits,dim=-1)[0,self.ai_label])); weights.append(len(window))
   if start+384>=len(ids): break
  return out,weights
 def metadata(self):
  import torch,transformers
  return {"model_id":self.model_id,"revision":self.revision or "default","device":self.device,"torch":torch.__version__,"transformers":transformers.__version__}
