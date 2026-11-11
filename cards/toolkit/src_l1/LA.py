JUR = "A jurisdiction catalogue heading. Tools sit at K and apply under that jurisdiction's own sources."
T = {
"K": (["work out what a binding text requires in a given case", "decide whether an earlier decision governs a new one"],
  {"task": "decide_existence classify explain", "structure": "text_language", "constraints": "legal_or_normative", "domain_type": "symbolic"},
  [("Statutory interpretation", "reads a provision by its text, context and purpose", ["the text is in force", "the jurisdiction's own rules of interpretation are applied"]),
   ("Doctrine of precedent", "applies the reason for an earlier decision to like cases", ["the earlier court binds the later one", "the material facts are comparable"]),
   ("Functional method of comparative law", "compares how different systems solve the same problem", ["the systems face a comparable problem"])],
  ["the texts and decisions", "the facts"], ["a reasoned conclusion on what the law requires"]),
"KDZ": C(JUR), "KE": C(JUR), "KF": C(JUR), "KG": C(JUR), "KH": C(JUR),
"KZ": (["work out what states have bound themselves to", "decide whether an unwritten rule binds states"],
  {"task": "decide_existence explain", "structure": "text_language", "constraints": "legal_or_normative", "agents": "multiple_competing"},
  [("Treaty interpretation under the Vienna Convention, articles 31 and 32", "reads a treaty in good faith by ordinary meaning, context and purpose", ["the treaty is in force between the parties", "the Convention applies, or its rules are accepted as custom"]),
   ("Identification of customary international law", "finds a rule from what states do and accept as law", ["a general practice of states", "the practice is accepted as law"])],
  ["treaty texts", "records of state practice"], ["a reasoned conclusion on the obligation"]),
}
