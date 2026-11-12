# Indigenous knowledge. No tools are listed for any card. The builder adds the review note to every card.
def K(solves, sig):
    return (solves, sig, [], [], [])
CUL = K(["hold and pass on a people's knowledge, language and past in that people's own terms"], {"task": "explain"})
EDU = K(["teach in a way that follows a people's own knowledge and protocols"], {"task": "design"})
ENV = K(["care for land and water using long observation of one place"], {"task": "control", "structure": "field_spatial"})
HEA = K(["support wellbeing using a people's own understanding of health"], {"task": "design"})
SOC = K(["describe a people's communities and ways of deciding in their own terms"], {"task": "explain"})
SCI = K(["apply systematic place-based observation to the natural world"], {"task": "explain predict"})
T = {
"4501": CUL, "4502": EDU, "4503": ENV, "4504": HEA, "4505": SOC, "4506": SCI,
"4507": CUL, "4508": EDU, "4509": ENV, "4510": HEA, "4511": SOC, "4512": SCI,
"4513": CUL, "4514": EDU, "4515": ENV, "4516": HEA, "4517": SCI, "4518": SOC,
"4519": K(["work with data and research methods under a people's own authority"], {"task": "design"}),
"4599": K(["locate work on this subject within the field's catalogue"], {"task": "classify"}),
}
