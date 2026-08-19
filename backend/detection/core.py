import math,re,statistics,unicodedata
from dataclasses import dataclass
LABELS=((0,34,"Likely human-patterned"),(35,64,"Uncertain or mixed signals"),(65,100,"Likely AI-patterned"))
@dataclass(frozen=True)
class Paragraph: id:str; index:int; text:str; words:int

def normalize(text:str)->tuple[str,list[str]]:
    warnings=[]
    if any(unicodedata.category(c)=="Cf" for c in text): warnings.append("invisible_characters")
    normalized=unicodedata.normalize("NFC",text).replace("\r\n","\n").replace("\r","\n")
    normalized=re.sub(r"[ \t]+"," ",normalized)
    if re.search(r"[ \t]{8,}",text): warnings.append("excessive_whitespace")
    return normalized,warnings

def paragraphs(text:str)->list[Paragraph]:
    parts=[p.strip() for p in re.split(r"\n\s*\n",text) if p.strip()]
    return [Paragraph(f"p-{i+1}",i,p,len(re.findall(r"\b\w+\b",p))) for i,p in enumerate(parts)]
def label(score:float)->str:
    n=max(0,min(100,round(score)))
    return next(name for lo,hi,name in LABELS if lo<=n<=hi)
def aggregate(scores:list[float],weights:list[int])->tuple[float,float]:
    if not scores or len(scores)!=len(weights) or sum(weights)<=0: raise ValueError("valid windows required")
    mean=sum(s*w for s,w in zip(scores,weights,strict=True))/sum(weights)
    return mean, statistics.pstdev(scores) if len(scores)>1 else 0.0
def diagnostics(text:str)->dict:
    words=re.findall(r"\b[\w']+\b",text.lower()); sentences=[s for s in re.split(r"[.!?]+",text) if s.strip()]
    lengths=[len(re.findall(r"\b\w+\b",s)) for s in sentences]
    mean=statistics.mean(lengths) if lengths else 0; sd=statistics.pstdev(lengths) if len(lengths)>1 else 0
    def repeated(n):
        grams=[tuple(words[i:i+n]) for i in range(max(0,len(words)-n+1))]
        return round((len(grams)-len(set(grams)))/len(grams),4) if grams else 0
    return {"version":"1.0","sentence_length":{"mean":round(mean,2),"sd":round(sd,2),"cv":round(sd/mean,3) if mean else 0},"type_token_ratio":round(len(set(words))/len(words),4) if words else 0,"repeated_ngrams":{"2":repeated(2),"3":repeated(3),"4":repeated(4)},"punctuation":{c:text.count(c) for c in ",;:!?"}}
