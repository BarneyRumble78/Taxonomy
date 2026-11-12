TRAD = "A heading for one tradition. Authority inside it is tradition-internal (W13) and does not transfer to other fields. No tools are listed."
T = {
"BL": (["describe and compare systems of belief and practice without judging their truth"],
  {"task": "compare explain", "goal_quality": "qualitative", "structure": "text_language"},
  [("Comparative method in the study of religion", "sets traditions side by side under stated categories", ["the categories of comparison are stated", "each tradition is first described in its own terms", "truth claims are set aside"])],
  ["texts, practices and accounts"], ["argued similarities and differences"]),
"BM": C(TRAD), "BP": C(TRAD), "BQ": C(TRAD), "BR": C(TRAD),
"BS": (["recover the earliest wording of a text copied by hand many times", "place a text in the time it was written"],
  {"task": "infer construct explain", "structure": "text_language hierarchy_tree", "direction": "inverse"},
  [("Textual criticism", "weighs variant readings to recover the earliest text", ["several manuscript witnesses survive", "rules such as preferring the harder reading are rules of thumb"]),
   ("Historical-critical exegesis", "reads the text as a document of its period", ["the text can be dated and placed", "the results are historical and settle no doctrinal question"])],
  ["manuscript witnesses", "historical context"], ["critical text with variants", "historical reading"]),
"BT": C(TRAD),
"BV": C("A heading for religious practice. Authority is tradition-internal (W13). No tools are listed."),
"BX": C(TRAD),
"KB": C("A heading for comparing religious legal systems. Comparative tools sit in law at K."),
"KBM": C(TRAD), "KBP": C(TRAD), "KBR": C(TRAD), "KBU": C(TRAD),
}
