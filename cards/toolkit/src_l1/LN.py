FAM = "A language-family catalogue heading. Methods sit at P."
T = {
"P": (["show that two languages descend from one source", "find which sounds a language treats as distinct", "measure usage in a large body of text"],
  {"task": "infer classify compare", "structure": "text_language hierarchy_tree sequence", "direction": "inverse"},
  [("Comparative method", "reconstructs a parent language from regular correspondences", ["sound correspondences are regular", "the compared words are inherited, not borrowed", "enough related word sets exist"]),
   ("Minimal pair test", "shows two sounds are distinct units", ["the two words differ in one sound in the same position", "both come from the same language variety"]),
   ("Corpus frequency analysis", "counts forms and patterns in a text collection", ["the collection represents the variety studied"])],
  ["word lists", "recordings", "text collection"], ["reconstructed forms", "sound inventory", "frequency tables"]),
"PA": (["recover the wording of a text that survives only in copies"],
  {"task": "infer construct", "structure": "hierarchy_tree text_language", "direction": "inverse"},
  [("Stemmatics", "builds a family tree of manuscripts from shared errors", ["each copy was made from one exemplar", "shared errors show shared descent"])],
  ["collated manuscripts"], ["family tree of copies", "reconstructed text"]),
"PB": C(FAM), "PC": C(FAM), "PD": C(FAM), "PE": C(FAM), "PF": C(FAM), "PG": C(FAM),
"PH": C(FAM), "PJ": C(FAM), "PK": C(FAM), "PL": C(FAM), "PM": C(FAM),
}
