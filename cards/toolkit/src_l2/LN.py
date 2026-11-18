D = C("A catalogue heading for one language, family or literature. Methods sit at P1-1091 and PA1-199.")
T = {
"P1-1091": K("show that languages share a source, find the units of a language, and measure usage", "task=infer classify compare|structure=text_language sequence",
  [("Comparative method", "reconstructs a parent language from regular correspondences", "sound correspondences are regular; compared words are inherited, not borrowed; enough related word sets"),
   ("Minimal pair test", "shows two sounds are distinct units", "the words differ in one sound in the same position; both from one variety"),
   ("Constituency tests", "show which word groups act as units in a sentence", "speakers' acceptability judgements are reliable; several tests agree"),
   ("Corpus frequency analysis", "counts forms and patterns in texts", "the collection represents the variety studied")],
  "word lists; recordings; sentences; texts", "reconstructions; sound inventory; structure; frequencies"),
"PA1-199": K("recover the wording of a text that survives only in copies", "task=infer construct|structure=hierarchy_tree text_language|direction=inverse",
  [("Stemmatics", "builds a family tree of manuscripts from shared errors", "each copy was made from one exemplar; shared errors show shared descent")],
  "collated manuscripts", "family tree; reconstructed text"),
"PJ1001-1989": K("read a script no one can read any longer", "task=infer|direction=inverse|structure=text_language",
  [("Decipherment with a bilingual text", "matches known names and words to unknown signs", "a parallel text in a known language exists; the underlying language or a relative is known")],
  "inscriptions; parallel text", "sign values"),
}
