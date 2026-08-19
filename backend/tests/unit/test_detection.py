from detection.core import aggregate,diagnostics,label,normalize,paragraphs
def test_normalization_preserves_display():
 original="A  line\r\n\r\nNext"; clean,w=normalize(original); assert original=="A  line\r\n\r\nNext"; assert clean=="A line\n\nNext"
def test_paragraphs_and_labels(): assert len(paragraphs("one\n\ntwo"))==2 and label(34)=="Likely human-patterned" and label(65)=="Likely AI-patterned"
def test_weighted_aggregation(): assert aggregate([0,1],[1,3])[0]==.75
def test_diagnostics(): assert diagnostics("One sentence. Another sentence!")["version"]=="1.0"
