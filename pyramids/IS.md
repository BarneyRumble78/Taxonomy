# IS — Information and the record

New field, added at the owner's direction. Standard v2 cited, not copied. Why it is here: ANZSRC 46 mixes computation with the record. CS owns cost and correctness. Nothing owned the catalogue, the archival rule, or retrieval as a claim about records. This pyramid is also the natural home of the Pyramids of Knowledge themselves, as a classification.

## 1. SCQA
**Situation.** Library, archival and information science states how records are identified, described, arranged, found and kept.
**Complication.** CS owned the algorithms, HI owned source criticism, and LN owned language. The catalogue, the classification scheme and the archive had no owner, though every pyramid depends on them.
**Question.** By what dimension can each claim about records be placed once?
**Answer.** By the stage in the life of a record the claim concerns: the item, its description, its arrangement, its retrieval, and its preservation.

## 2. Governing thought
Information science is exhausted by four faces of one pyramid: objects, methods, warrants and bridges.
Its objects divide into five stages of a record's life: items, description, arrangement, retrieval, and preservation.

## 3. Key line
Dimension: **the stage in the life of a record.** Order: from creation to keeping.
1. Items
2. Description
3. Arrangement
4. Retrieval
5. Preservation

## 4. Face O — Objects

### IS.O.A1 Items
**Situation.** Every claim about records presupposes a unit that can be named, counted and cited. Libraries, archives and research data services each fix that unit in their own way.
**Complication.** A book, a letter and a data set are not the same kind of unit. The cataloguing, archival and data communities use different models, and identifiers are issued for all three.
**Question.** What counts as one record, and by what rule is it identified?
**Answer.** IS owns the model of the unit and the rule of identity. The historian's criticism of a record's content is HI.

**Key line** (inductive; plural noun: units of record; dimension: the kind of unit being identified; order: structure, from the abstract unit to the name that points to any unit). Members (4): Works and manifestations · Records as evidence · Data sets · Persistent identifiers.

- **IS.O.A1.1 Works and manifestations.** **FRBR and its successor LRM distinguish four entities: work, expression, manifestation and item.** FRBR is the IFLA report of 1998 and LRM is the IFLA consolidation of 2017. Both are conceptual models, not data formats.
  - IS.O.A1.1.1 Work and expression. In FRBR a translation is a new expression of the same work, and an adaptation into another medium is a new work. Cataloguers can disagree on borderline cases, so agreement can be measured.
  - IS.O.A1.1.2 Manifestation and item. Copies from one production share one manifestation description. Features of a single copy, such as annotation, binding or ownership history, belong to the item.
  - IS.O.A1.1.3 BIBFRAME entities. BIBFRAME is an RDF vocabulary with Work, Instance and Item and no separate expression entity. Whether this loses information that FRBR keeps is CONTESTED. A round-trip conversion test measures the loss.
- **IS.O.A1.2 Records as evidence.** **An archival record is evidence of an activity.** Its source criticism for history is HI.
  - IS.O.A1.2.1 Record characteristics. ISO 15489-1:2016 states that a record should be authentic, reliable, have integrity and be usable. A records system is tested against each term by audit (W12 with W4).
  - IS.O.A1.2.2 Life cycle and continuum. The life-cycle model places a record in successive phases from creation to disposal. Upward's records continuum treats creation, management and use as concurrent. CONTESTED: neither model has a decisive test, and they differ most for digital records.
  - IS.O.A1.2.3 Diplomatics. Diplomatics analyses the form of a record to judge its authenticity. Mabillon's De re diplomatica (1681) founded it for medieval charters. Its use on current records is IS. CONTESTED: for historical documents the alternative home is HI.O.A1.4 (uses HI.O.A1.4).
  - IS.O.A1.2.4 Appraisal values. Schellenberg separated primary values to the creator from secondary values to others, the latter evidential and informational (Modern Archives, 1956). The retention decision is IS. A legal duty to retain is LA.
- **IS.O.A1.3 Data sets.** **A research data set is an item with its own identity, version and provenance.**
  - IS.O.A1.3.1 Versioned citation. A data set can change after deposit, so a citation must name a version or a retrieval date. The FORCE11 Joint Declaration of Data Citation Principles (2014) states eight principles, including persistence and specificity.
  - IS.O.A1.3.2 FAIR principles. FAIR (Wilkinson and others, 2016) asks that data be findable, accessible, interoperable and reusable. The principles are guidance and do not require data to be open. Compliance is assessed against a stated metric set.
  - IS.O.A1.3.3 Data set boundary. OPEN: no rule fixes where one data set ends and the next begins, notably for continuously updated data. The depositor declares the boundary. A subset citation is tested by re-extracting the subset.
  - IS.O.A1.3.4 Provenance model. W3C PROV (2013) describes provenance as relations among entities, activities and agents. It assumes the activities were logged when they happened. A provenance record is a claim about the past, supported by logs (W7).
- **IS.O.A1.4 Persistent identifiers.** **A persistent identifier is a string issued under a registry's rules, so its validity is a stipulation (W12).** Examples are DOI, ORCID and ISBN.
  - IS.O.A1.4.1 Check digits. The last digit of an ISBN-13 makes a weighted sum, with weights 1 and 3 alternating, a multiple of 10. It detects every single-digit error and every adjacent transposition except where the two digits differ by 5. ISBN-10 uses modulus 11 and detects every adjacent transposition. The number theory is MA (uses MA.O.A2).
  - IS.O.A1.4.2 Persistence as service. A DOI persists only while its registrant keeps its metadata and target current. The DOI system is ISO 26324 and resolves through the Handle System. The failure rate is measured by sampling resolution (W4).
  - IS.O.A1.4.3 Identifier scope. An identifier names one entity at a stated granularity. An ORCID identifier names one person's record, and duplicates can arise when one person registers twice. The duplicate rate is measurable by comparing records.

Named objects: FRBR and LRM (conceptual models; they assume a catalogue's user tasks and the four entities as defined); BIBFRAME (RDF vocabulary; Work, Instance, Item); ISO 15489-1 record characteristics; records continuum; diplomatics; Schellenberg's values; FAIR principles (guidance, no formal hypotheses); PROV (activities were logged at the time); ISBN check digits (fixed weights and modulus; random digit errors); DOI (registrant keeps the target current).

### IS.O.A2 Description
**Situation.** A record is found through a description of it. Descriptions follow standards that fix the elements, the rules for filling them and the vocabulary of the values.
**Complication.** Metadata schemes, cataloguing codes and subject vocabularies were built by different communities for different carriers. Mapping between them loses information.
**Question.** What must a description state, by what rule, and in what form?
**Answer.** IS owns the element sets, the cataloguing rules, the subject vocabularies and their publication as linked data. The logic of the RDF layer is MA.

**Key line** (inductive; plural noun: description practices; dimension: the part of a description the claim concerns; order: structure, from the element set to its machine-readable form). Members (4): Metadata standards · Cataloguing rules · Subject indexing · Linked data.

- **IS.O.A2.1 Metadata standards.** **A metadata standard stipulates which elements describe a resource and how they are encoded (W12).** Examples are Dublin Core and MARC.
  - IS.O.A2.1.1 Dublin Core elements. The Dublin Core Metadata Element Set (ISO 15836) has fifteen elements. They are title, creator, subject, description, publisher, contributor, date, type, format, identifier, source, language, relation, coverage and rights. Each is optional and repeatable.
  - IS.O.A2.1.2 MARC 21 structure. A MARC record has a leader, a directory and variable fields. Data fields carry a three-digit tag, two indicator positions and coded subfields. ISO 2709 serialises the record.
  - IS.O.A2.1.3 Crosswalks. A crosswalk maps the elements of one scheme to another. It loses or merges information where element meanings differ. Loss is measured by converting a record set and back, then comparing.
  - IS.O.A2.1.4 Application profiles. A profile selects and constrains elements from one or more schemes for one community. A record conforms when it meets the stated cardinalities and value rules, which a validator tests (W11).
- **IS.O.A2.2 Cataloguing rules.** **Cataloguing rules prescribe how a resource is described and how its access points are chosen.** RDA is a current standard.
  - IS.O.A2.2.1 User tasks. FRBR names four user tasks for a catalogue: find, identify, select and obtain. LRM adds explore. A rule is justified in so far as it supports a task, which is argued (W9).
  - IS.O.A2.2.2 Authority control. An authority record fixes one authorised form of a name and refers variants to it. The effect is tested by comparing name searches with and without authority records. The hypothesis is that the file is maintained.
  - IS.O.A2.2.3 Content, media and carrier types. RDA records content type, media type and carrier type. It replaces the optional general material designation of AACR2. The change separates what a resource says from the physical form that carries it.
  - IS.O.A2.2.4 Cataloguer consistency. UNVERIFIED: agreement between cataloguers is higher for transcribed elements than for name and subject access points. Test by independent cataloguing of one sample.
- **IS.O.A2.3 Subject indexing.** **Subject indexing assigns terms from a controlled vocabulary so that records on one subject meet under one term.** Examples are MeSH and LCSH.
  - IS.O.A2.3.1 Thesaurus relations. ISO 25964 defines three relations among terms: equivalence (USE and UF), hierarchical (BT and NT) and associative (RT). Hierarchical links are of three kinds: generic, partitive and instance. Mixing kinds breaks the inference from a broad term to its narrower terms.
  - IS.O.A2.3.2 Pre- and post-coordination. A pre-coordinated heading, such as an LCSH heading with subdivisions, fixes a combination of concepts in advance. A post-coordinated system combines terms at search time and can match terms that belong to different parts of a record.
  - IS.O.A2.3.3 Exhaustivity and specificity. Exhaustivity is the number of subjects indexed per record. Specificity is how narrow the terms are. Higher exhaustivity tends to raise recall and lower precision. Higher specificity tends to raise precision. These hold for a fixed vocabulary and searching practice.
  - IS.O.A2.3.4 Indexing consistency. Consistency is the share of terms that two indexers both assign to one record. Several formulas exist, so a report states which one it uses. Low consistency limits retrieval by controlled terms.
- **IS.O.A2.4 Linked data.** **Linked data publishes descriptions as RDF statements about identified resources, and SKOS expresses vocabularies in that form.** The logic is MA.O.A1; the vocabulary is IS.
  - IS.O.A2.4.1 Four principles. Berners-Lee (2006) gave four rules. Name things with URIs. Use HTTP URIs so that they can be looked up. Return useful information in standards such as RDF. Include links to other URIs. The rules are guidance (W12).
  - IS.O.A2.4.2 SKOS hierarchy. SKOS (W3C, 2009) represents concepts with preferred and alternative labels and broader, narrower and related links. The property skos:broader is not transitive by itself. The transitive closure is a separate property.
  - IS.O.A2.4.3 Open-world reading. RDF and OWL semantics treat a missing statement as unknown, not false. A closed-world check, such as a SHACL shapes test (W3C, 2017), finds missing required data. The logic is MA (uses MA.O.A1).
  - IS.O.A2.4.4 Identity links. The property owl:sameAs states that two names denote one thing, so every property of one holds for the other. Using it for similar or related things licenses false inferences. A set of links is tested for inferences that contradict known facts.

Named objects: Dublin Core (ISO 15836; elements are optional and repeatable); MARC 21 (ISO 2709 encoding); crosswalk (element meanings are comparable); application profile; RDA (user tasks as stated; applied by trained cataloguers); authority file (maintained); thesaurus (ISO 25964; hierarchical links are of one kind); LCSH and MeSH; SKOS (concept schemes, not class axioms); RDF (open-world statements); SHACL (closed-world shapes); owl:sameAs (strict identity).

### IS.O.A3 Arrangement
**Situation.** Descriptions must be organised so that related records are found together. A scheme fixes the groups, their order and the notation that marks them.
**Complication.** A shelf has one order, but a work may concern several subjects. Schemes also grow by accretion, so classes overlap and residual classes appear.
**Question.** By what principle does each arrangement place a record, and does it place it once?
**Answer.** IS owns schemes, facets, archival arrangement, ontologies and the application of a scheme to claims. Whether an ontology's commitments are true is PL.

**Key line** (inductive; plural noun: arrangement principles; dimension: what fixes an item's position; order: structure, from enumerated schedules, through combined facets and creator provenance, to axiomatised ontologies, then the application to claims). Members (5): Classification schemes · Faceted classification · Archival arrangement · Ontologies · This taxonomy.

- **IS.O.A3.1 Classification schemes.** **A classification scheme assigns each item one class in a stipulated hierarchy (W12).** Whether its classes are mutually exclusive and exhaustive is testable (W9 with W4). Examples are LCC, DDC, UDC and MSC.
  - IS.O.A3.1.1 Dewey Decimal. DDC (first published 1876) has ten main classes, each divided into ten divisions and each division into ten sections. Decimal notation limits each level to ten branches. Topics of unequal size can be forced into equal slots.
  - IS.O.A3.1.2 Library of Congress. LCC has 21 lettered main classes. Each class has its own schedule, maintained separately, so notation and depth differ between classes. The scheme follows the Library's collection, which is literary warrant.
  - IS.O.A3.1.3 Exclusivity test. A scheme level is mutually exclusive if each item fits one class there. It is exhaustive if some class fits every item. The tests are the double-classing rate and the residual-class rate over a sample (W4). A residual class such as general records a failure of exhaustiveness.
  - IS.O.A3.1.4 Single location. A single-hierarchy scheme gives a work on two subjects one place. The second subject is reachable only through the catalogue. Browsing one class then finds a subset of the relevant works. The share shelved elsewhere is measurable (W4).
- **IS.O.A3.2 Faceted classification.** **A faceted scheme describes an item by independent facets combined at the time of classing.** Ranganathan's Colon Classification uses the PMEST facets.
  - IS.O.A3.2.1 PMEST. Colon Classification (1933) analyses a subject into Personality, Matter, Energy, Space and Time. CONTESTED: whether five categories suffice for all subjects. Other category lists have been proposed.
  - IS.O.A3.2.2 Facet independence. Facet analysis assumes that the facets of a domain are mutually exclusive and that the values within each facet are too. It fails where one value is defined by another. Test by searching for items whose value in one facet depends on another.
  - IS.O.A3.2.3 Citation order. The order in which facets are combined fixes where an item files and what is collocated. Changing the order moves items. The order is a design decision (W12), not a fact about the subject.
  - IS.O.A3.2.4 Faceted search. A search interface offers facets as filters where records carry controlled values for each facet. A filter is only as complete as the share of records with a value. Coverage is measurable (W4).
- **IS.O.A3.3 Archival arrangement.** **Archival arrangement keeps records by their creator (respect des fonds) and in the order the creator gave them (original order).**
  - IS.O.A3.3.1 Provenance. Under respect des fonds, records of one creator are kept apart from those of other creators. A French instruction of 1841 (Natalis de Wailly) is the usual source. The test is whether each record can be assigned to one creating body.
  - IS.O.A3.3.2 Original order. Original order keeps records as the creator arranged them, because that order is evidence of how the creator worked. Where no original order can be shown, the archivist imposes one and records that. The test is whether the order can be reconstructed from the creator's registers.
  - IS.O.A3.3.3 Multilevel description. ISAD(G) describes records in levels, such as fonds, series, file and item. Its four rules are description from the general to the particular, information relevant to the level, linking of descriptions, and non-repetition of information. Conformity is testable (W11).
  - IS.O.A3.3.4 Digital original order. OPEN: file names, folders and dates in a digital collection may reflect software behaviour and not the creator's practice. Whether original order can be recovered from file-system metadata is tested case by case.
- **IS.O.A3.4 Ontologies.** **An ontology is a formal specification of the classes and relations of a domain.** BFO and DOLCE are upper-level examples. Their philosophical commitments are PL.
  - IS.O.A3.4.1 Definition and test. Gruber (1993) defined an ontology as an explicit specification of a conceptualisation. An ontology is tested by the competency questions it must answer and by logical consistency. A reasoner checks consistency (W11). The truth of its axioms about the domain is argued (W9).
  - IS.O.A3.4.2 OWL 2 DL. Reasoning in OWL 2 DL is decidable under restrictions on the use of complex roles. Reasoning in OWL 2 Full is not decidable. The proofs are MA (uses MA.O.A1). The cost class of reasoning is CS (uses CS.O.A2.3).
  - IS.O.A3.4.3 Upper-level ontologies. BFO divides entities into continuants and occurrents. DOLCE divides them into endurants and perdurants. CONTESTED: choosing between them is a philosophical commitment (uses PL.O.A1.1). Whether either improves integration is tested by alignment studies.
  - IS.O.A3.4.4 Alignment. Ontology alignment is scored against reference alignments, as in the OAEI campaigns. The scores assume that the reference is correct and complete. A different reference gives different scores.
- **IS.O.A3.5 This taxonomy.** **This taxonomy classifies claims, not documents, and each claim has one home.** Its reliability is tested by the placement protocol.
  - IS.O.A3.5.1 Unit of claim. The unit classified is a sentence-level claim, not a document or a topic. A compound sentence is split into atomic claims before placement (Standard v3, section 4a). Test: two placers split one text and compare the claims.
  - IS.O.A3.5.2 One home. Each claim has one owning pyramid, face and cell, and other pyramids cite it. Independent placers can test the rule. OPEN: no agreement figure is held in this file.
  - IS.O.A3.5.3 Key-line discipline. Each level has two to five members, one named dimension, one order and no residual member. A script checks counts and repeated members (R2, R7). Whether the dimension chosen is the best one is argued (W9).
  - IS.O.A3.5.4 Protocol reliability. The placement protocol is a classification procedure. Its reliability is the share of test claims placed in the cell a specialist would choose. OPEN: no such test is recorded here.

Named objects: Dewey Decimal Classification (ten classes; decimal notation); Library of Congress Classification (21 classes; literary warrant); Universal Decimal Classification (synthesis by auxiliary signs); MSC; Colon Classification and PMEST (facets are independent); citation order; respect des fonds (a creator can be identified); original order (the order is evidence); ISAD(G) (levels are nested); OWL 2 DL (decidable under stated restrictions); BFO and DOLCE (distinct upper-level commitments); OAEI alignment scores (reference is correct); this taxonomy's one-home rule.

### IS.O.A4 Retrieval
**Situation.** Arranged records are useful only if the right ones can be found. Retrieval is tested by comparing what a system returns with what a judge calls relevant.
**Complication.** Relevance depends on the person and the moment. Ranking algorithms are CS and the mind of the searcher is MS, so the claim about finding itself had no home.
**Question.** How well are records found, by whom, and how is that measured?
**Answer.** IS owns the effectiveness measures, the concept of relevance, the quantitative laws of literatures and the models of seeking. The algorithm's cost is CS and the cognitive mechanism is MS.

**Key line** (inductive; plural noun: findability claims; dimension: what is measured about finding; order: structure, from the system's output to the judge, the literature and the seeker). Members (4): Retrieval effectiveness · Relevance · Bibliometrics · Information behaviour.

- **IS.O.A4.1 Retrieval effectiveness.** **Retrieval effectiveness is measured by precision and recall against relevance judgements.** The algorithm's cost is CS.
  - IS.O.A4.1.1 Precision and recall. Precision is the share of retrieved items that are relevant. Recall is the share of relevant items that are retrieved. Recall needs the number of relevant items in the collection, which is unknown for large collections and is estimated.
  - IS.O.A4.1.2 Cranfield design. Cleverdon's Cranfield tests fixed a document collection, a set of topics and relevance judgements. The design assumes one judgement per document and topic holds across users. Transfer to real users is tested separately (W4).
  - IS.O.A4.1.3 Pooling. TREC (from 1992) judges the union of the top results of the participating systems. It assumes that unjudged documents are not relevant. A system outside the pool can be underscored. Test by removing one participant's contribution and rescoring.
  - IS.O.A4.1.4 Rank-based measures. Average precision and nDCG score a ranked list. The nDCG measure (Järvelin and Kekäläinen, 2002) uses graded relevance and a logarithmic discount by rank. The discount assumes a model of user attention, so the measure is valid for that model only.
- **IS.O.A4.2 Relevance.** **Relevance is a judgement of a document against a need, as topical relevance or user relevance.** Assessors make the judgement, so it is measured (W4).
  - IS.O.A4.2.1 Topical and user relevance. Topical relevance is whether a document is about the topic. User relevance is whether it is useful to this person in this situation. A test collection measures the first.
  - IS.O.A4.2.2 Assessor disagreement. Different assessors judge the same documents differently. Voorhees (2000) reported that system rankings stayed largely stable under such variation, although absolute scores changed. UNVERIFIED: the extent of the stability. Test by swapping assessor sets.
  - IS.O.A4.2.3 Graded relevance. Judgements on a scale, such as not, partly and highly relevant, are ordinal. Averaging grades treats them as interval. The gain values assigned to grades are stipulations (W12) and change the value of a measure.
  - IS.O.A4.2.4 Relevance feedback. Rocchio (1971) moves a query towards documents judged relevant and away from those judged not relevant, in a vector space. It assumes relevant documents resemble each other in term space. The gain is IS; the algorithm's cost is CS.
- **IS.O.A4.3 Bibliometrics.** **Lotka's law (author productivity) and Bradford's law (scattering) are empirical regularities within stated literatures.**
  - IS.O.A4.3.1 Lotka's law. Lotka (1926) found that the number of authors with n publications falls roughly as 1/n² in the literatures he studied. The exponent varies between literatures. The fit is tested in each literature (W4).
  - IS.O.A4.3.2 Bradford's law. Bradford (1934) ranked journals by yield on one subject. He found zones that each gave the same number of articles. The journal counts in the zones stand in the ratio 1 : n : n². The law is stated for a single subject bibliography. It is a regularity, not a derivation.
  - IS.O.A4.3.3 Citation analysis. Citation counts indicate use by authors, not quality. Citing practice differs by field and year, so counts are normalised. Counts compare only works of comparable field and age.
  - IS.O.A4.3.4 Indicators. The h-index (Hirsch, 2005) is the largest h such that h of an author's papers have at least h citations each. It ignores field and career length. Citation distributions are skewed, so a journal's mean citation rate can differ from a typical article's.
- **IS.O.A4.4 Information behaviour.** **Information behaviour is how people identify a need, seek information and use it.** The cognitive mechanism is MS.
  - IS.O.A4.4.1 Information search process. Kuhlthau's model has six stages: initiation, selection, exploration, formulation, collection and presentation. It holds that uncertainty is high early and falls after formulation. UNVERIFIED: the evidence base is mainly students in library tasks. CONTESTED: its generality.
  - IS.O.A4.4.2 Berrypicking. Bates (1989) argued that a query evolves as the searcher reads and that information is gathered in pieces from varied sources. This conflicts with the fixed query in the Cranfield design. Log studies of query reformulation test it (W4).
  - IS.O.A4.4.3 Information foraging. Pirolli and Card (1999) model searchers as maximising information gained per unit cost, guided by cues called information scent. The model assumes the searcher can estimate cost and gain. It is tested by comparing predicted and observed paths.
  - IS.O.A4.4.4 Information need. Taylor described four levels of need, from the unexpressed to the formal question. Belkin's anomalous state of knowledge holds that a searcher cannot fully specify what is missing. Both imply that a query is an imperfect expression of need.

Named objects: precision and recall (relevance judgements exist for a test collection); Cranfield design (judgements transfer across users); pooling (unjudged documents are not relevant); average precision and nDCG (a user model of attention); BM25 (terms are independent; parameters are tuned to the collection); inverse document frequency (Spärck Jones 1972; rare terms discriminate); Rocchio feedback (relevant documents are similar); Lotka's law; Bradford's law; h-index; Information Search Process; berrypicking; information foraging (searcher maximises gain per cost); anomalous state of knowledge.

### IS.O.A5 Preservation
**Situation.** Records outlast their creators only if their carriers, formats and rights are managed. Keeping a record usable is a continuing activity, not a state.
**Complication.** Paper decays chemically, digital files depend on software, and access is limited by law and consent. The claims were spread across chemistry, computer science and law.
**Question.** What must be kept for a record to stay usable, and who may use it?
**Answer.** IS owns the rules for keeping the carrier and the content, and for stating access. The chemistry is CH, the licence law is LA, and tradition-internal authority over Indigenous data is IK.

**Key line** (inductive; plural noun: preservation claims; dimension: the threat or limit to continued use; order: structure, from the physical carrier to the digital object, then rights, then governance). Members (4): Physical conservation · Digital preservation · Access and rights · Indigenous data governance.

- **IS.O.A5.1 Physical conservation.** **Physical conservation slows the decay of the material carrier.** The chemistry of paper and media is CH.
  - IS.O.A5.1.1 Agents of deterioration. The Canadian Conservation Institute lists ten agents. They are physical forces; thieves, vandals and displacers; fire; water; pests; contaminants; light, ultraviolet and infrared radiation; incorrect temperature; incorrect relative humidity; and dissociation. Preventive conservation controls them, and each can be audited.
  - IS.O.A5.1.2 Storage conditions. The decay of paper and film slows at lower temperature and lower relative humidity. Over a narrow range the rate follows the Arrhenius form (uses CH.O.A4.2). A storage specification states set points with tolerances (W12).
  - IS.O.A5.1.3 Intervention. Conservation codes ask for documented treatment and minimal intervention. Reversibility is often stated as a goal. CONTESTED: some treatments cannot be reversed, and retreatability is proposed in its place.
  - IS.O.A5.1.4 Media decay. Cellulose acetate film decays by hydrolysis that releases acetic acid and speeds further decay, called vinegar syndrome. The binder of magnetic tape can hydrolyse and shed or stick. Each medium has a dominant mechanism, so a storage rule names the medium (uses CH.O.A4).
- **IS.O.A5.2 Digital preservation.** **Digital preservation keeps digital objects usable over time, and the OAIS reference model (ISO 14721) stipulates its functions (W12).**
  - IS.O.A5.2.1 OAIS entities. OAIS has six functional entities: ingest, archival storage, data management, administration, preservation planning and access. Content moves as submission, archival and dissemination information packages. An archive claims conformance by mapping its functions to these (W11).
  - IS.O.A5.2.2 Designated community. OAIS defines success relative to a designated community whose knowledge base is stated. When that knowledge changes, more representation information is needed. The claim assumes the community can be identified.
  - IS.O.A5.2.3 Migration and emulation. Migration converts the bitstream to a current format. Emulation keeps the bitstream and reproduces the software environment. Each can lose properties that matter. CONTESTED: which properties are significant, since that depends on the user. Compare rendered output before and after (W4).
  - IS.O.A5.2.4 Fixity and copies. A stored checksum detects change in a copy. With several independent copies, a corrupted copy can be found and replaced from an intact one. This assumes a collision-resistant hash and independent failures (uses CS.O.A5.1).
- **IS.O.A5.3 Access and rights.** **Access and rights state who may read and reuse a record, including through open access.** Copyright is LA.
  - IS.O.A5.3.1 Gold and green. Gold open access publishes the work openly at the publisher. Green open access deposits a version in a repository. The share of each varies by field and year, so any share needs a stated sample (W4).
  - IS.O.A5.3.2 Licence statements. A licence such as Creative Commons Attribution states permitted reuse. Whether the licence is valid in law is LA. Whether a record carries a clear, machine-readable licence statement is IS, and an audit tests it.
  - IS.O.A5.3.3 Conditions of access. ISAD(G) has a description element for conditions governing access. A closure period or restriction on a record is recorded there, and its legal basis is LA. Test by sampling closed records for a stated condition.
- IS.O.A5.4 Indigenous data governance — the CARE principles; Māori data sovereignty (Te Mana Raraunga). Tradition-internal authority over the data is IK. Held as first written; no content is added here, and the Māori-led review gate in Standard v3 applies.

Named objects: Canadian Conservation Institute agents of deterioration (a stated list); Arrhenius rate dependence (a narrow temperature range; one dominant reaction); vinegar syndrome (acetate base); OAIS (a designated community is identified); submission, archival and dissemination packages; ISO 16363 (audit of trustworthy digital repositories); fixity checksum (stored apart from the file; recomputed on a schedule); migration; emulation; gold and green open access; Creative Commons licences; ISAD(G) access element.

## 5. Face M — Methods

| ID | Role | Shared role | Example |
|---|---|---|---|
| IS.M.1 | Describe and classify | M1 Represent | cataloguing, indexing |
| IS.M.2 | Appraise | M7 Verify | archival appraisal, quality control |
| IS.M.3 | Evaluate retrieval | M3 Observe | test collections (TREC-style) |
| IS.M.4 | Measure literatures | M5 Compute | bibliometric analysis |
| IS.M.5 | Study users | M3 Observe | user studies |

### Heuristics register (outside the count)
Literary warrant (classify by what is published); "more product, less process" in archives; collect broadly, weed later. Each is a rule of thumb with exceptions, and none is a warrant.

### Field examples
- IS.M.1: a cataloguer describes a monograph under RDA, assigns an LCSH heading and a DDC number, and records the ISBN. Two cataloguers can be compared on the same item.
- IS.M.2: an archivist appraises an accession against retention criteria, and a repository audit compares fixity logs with stored checksums. The criteria must be written before the appraisal.
- IS.M.3: a TREC-style run scores systems on topics with pooled judgements. It holds if the judgements are complete enough and the topics represent real use.
- IS.M.4: a Bradford analysis fits zones to a subject bibliography. It holds if the bibliography is complete for the subject and the database coverage is stated.
- IS.M.5: a user study records think-aloud protocols and search logs. It holds if the participants and tasks represent the population of interest.

## 6. Face W — Warrants

| Cell | Warrant | Standard | Typical defeaters |
|---|---|---|---|
| IS.O.A1 | W12 + W7 | conformity with identity rules; provenance | lost provenance |
| IS.O.A2 | W12 + W4 | standard followed; indexer consistency measured | low inter-indexer agreement |
| IS.O.A3 | W12 + W9 + W4 | scheme rules; argued MECE; reliability measured | overlap, residual classes |
| IS.O.A4 | W4 | test collection with stated relevance judgements | assessor disagreement |
| IS.O.A5 | W11 + W4 | conformity with OAIS; fixity checks | format obsolescence |

### Field examples
- IS.O.A1: an ISBN is valid if its check digit matches (W12). The custody of an accession is shown by registers and transfer lists (W7). A broken custody chain defeats the claim.
- IS.O.A2: a record conforms to MARC 21 if a validator accepts it. Indexer consistency is measured on a sample indexed twice (W4). A low value defeats the claim that terms are reliable access points.
- IS.O.A3: the top level of a scheme is tested for double-classing and residual-class rates on a sample of catalogue records (W4). A high rate of either defeats the MECE claim.
- IS.O.A4: a system's precision at a cut-off is stated with the topic set and the judgements. Relevant documents that nobody judged defeat the score.
- IS.O.A5: a fixity audit recomputes checksums on a schedule and logs every mismatch. A format with no available renderer defeats the claim that an object is usable.

## 7. Face B — Bridges

| ID | Field | Cells | Methods | Substrate |
|---|---|---|---|---|
| IS.B.C1 | Library science | A1–A3 | M.1 | collections |
| IS.B.C2 | Archival science | A1.2, A3.3, A5 | M.2 | archives |
| IS.B.C3 | Information retrieval | A4.1, A4.2 | M.3 | test collections (uses CS) |
| IS.B.C4 | Scientometrics | A4.3 | M.4 | literatures |
| IS.B.C5 | Knowledge organisation | A3 | M.1 | schemes (ISKO) |
| IS.B.C6 | Digital humanities (shared) | A2, A4 | M.4 | texts (uses HI, AR) |
| IS.B.C7 | Museum studies (shared) | A1, A5 | M.1 | collections (uses HI) |

### Field examples
- IS.B.C1: cataloguing and classing a legal-deposit collection under RDA, LCSH and DDC.
- IS.B.C2: arranging a government department's files into series and writing multilevel descriptions.
- IS.B.C3: evaluating a search engine on a test collection with pooled judgements.
- IS.B.C4: fitting Bradford zones to a subject bibliography and reporting citation indicators with their normalisation.
- IS.B.C5: designing a faceted scheme for one domain and testing its facets for independence.
- IS.B.C6: encoding a letter collection in a text standard and indexing its names (shared; uses HI, AR).
- IS.B.C7: documenting an object's provenance and condition, and setting its storage conditions (shared; uses HI).

## 8. Assignment rules
1. Place by the record's life stage.
2. The algorithm's cost or correctness is CS; the retrieval effectiveness claim is IS.
3. Source criticism for a historical claim is HI; the archival rule is IS.
4. Copyright is LA.
5. Tradition-internal authority over Indigenous data is IK; its governance framework as a records rule is IS.

## 9. Scope boundary

| Refused | Owner |
|---|---|
| algorithms and systems | CS |
| historical source criticism | HI |
| copyright and privacy law | LA |
| media and communication effects | MS |
| philosophy of information | PL |

## 10. External crosswalk
**ANZSRC 46** (checked 9 Oct 2026 against the ABS file anzsrc2020_for.xlsx) has 14 groups. 4610 Library and information studies lands in A1–A5. 4609 Information systems and 4605 Data management are split: records go to IS, systems to CS. The remaining groups go to CS. Coverage for IS: 1 group whole and 2 in part, of 13 substantive groups.

## 11. Validation
Sizes: key line 5. Face O 5 cells + 21 sub-cells = 26. M roles 5. Heuristics 3. W rows 5. B bridges 7.
Second level: 77 cells (IS.O.An.m.k) under 20 of the 21 sub-cells. IS.O.A5.4 has none, because Indigenous content is held as first written.
Key line, word for word: Items. Description. Arrangement. Retrieval. Preservation.
Cell key lines, word for word:
- A1 (4): Works and manifestations. Records as evidence. Data sets. Persistent identifiers.
- A2 (4): Metadata standards. Cataloguing rules. Subject indexing. Linked data.
- A3 (5): Classification schemes. Faceted classification. Archival arrangement. Ontologies. This taxonomy.
- A4 (4): Retrieval effectiveness. Relevance. Bibliometrics. Information behaviour.
- A5 (4): Physical conservation. Digital preservation. Access and rights. Indigenous data governance.
CONTESTED: data management in IS vs CS.
CONTESTED: BIBFRAME against FRBR (A1.1.3); diplomatics, IS or HI (A1.2.3); PMEST as a complete category list (A3.2.1); choice of upper-level ontology (A3.4.3); generality of Kuhlthau's model (A4.4.1); reversibility as a conservation goal (A5.1.3); significant properties (A5.2.3).
OPEN: data set boundary (A1.3.3); original order in digital records (A3.3.4); placement agreement and protocol reliability (A3.5.2, A3.5.4).
UNVERIFIED: cataloguer consistency (A2.2.4); extent of assessor stability (A4.2.2); evidence base of the Information Search Process (A4.4.1).

## 12. Registry rows

| ID | Label | Home | Uses |
|---|---|---|---|
| IS.O.A1 | Items | O/A1 | — |
| IS.O.A1.1 | Works and manifestations | O/A1 | — |
| IS.O.A1.1.1 | Work and expression | O/A1 | — |
| IS.O.A1.1.2 | Manifestation and item | O/A1 | — |
| IS.O.A1.1.3 | BIBFRAME entities | O/A1 | — |
| IS.O.A1.2 | Records as evidence | O/A1 | HI |
| IS.O.A1.2.1 | Record characteristics | O/A1 | — |
| IS.O.A1.2.2 | Life cycle and continuum | O/A1 | — |
| IS.O.A1.2.3 | Diplomatics | O/A1 | HI.O.A1.4 |
| IS.O.A1.2.4 | Appraisal values | O/A1 | LA |
| IS.O.A1.3 | Data sets | O/A1 | — |
| IS.O.A1.3.1 | Versioned citation | O/A1 | — |
| IS.O.A1.3.2 | FAIR principles | O/A1 | — |
| IS.O.A1.3.3 | Data set boundary | O/A1 | — |
| IS.O.A1.3.4 | Provenance model | O/A1 | — |
| IS.O.A1.4 | Persistent identifiers | O/A1 | — |
| IS.O.A1.4.1 | Check digits | O/A1 | MA.O.A2 |
| IS.O.A1.4.2 | Persistence as service | O/A1 | — |
| IS.O.A1.4.3 | Identifier scope | O/A1 | — |
| IS.O.A2 | Description | O/A2 | — |
| IS.O.A2.1 | Metadata standards | O/A2 | — |
| IS.O.A2.1.1 | Dublin Core elements | O/A2 | — |
| IS.O.A2.1.2 | MARC 21 structure | O/A2 | — |
| IS.O.A2.1.3 | Crosswalks | O/A2 | — |
| IS.O.A2.1.4 | Application profiles | O/A2 | — |
| IS.O.A2.2 | Cataloguing rules | O/A2 | — |
| IS.O.A2.2.1 | User tasks | O/A2 | — |
| IS.O.A2.2.2 | Authority control | O/A2 | — |
| IS.O.A2.2.3 | Content, media and carrier types | O/A2 | — |
| IS.O.A2.2.4 | Cataloguer consistency | O/A2 | — |
| IS.O.A2.3 | Subject indexing | O/A2 | — |
| IS.O.A2.3.1 | Thesaurus relations | O/A2 | — |
| IS.O.A2.3.2 | Pre- and post-coordination | O/A2 | — |
| IS.O.A2.3.3 | Exhaustivity and specificity | O/A2 | — |
| IS.O.A2.3.4 | Indexing consistency | O/A2 | — |
| IS.O.A2.4 | Linked data | O/A2 | MA.O.A1 |
| IS.O.A2.4.1 | Four principles | O/A2 | — |
| IS.O.A2.4.2 | SKOS hierarchy | O/A2 | — |
| IS.O.A2.4.3 | Open-world reading | O/A2 | MA.O.A1 |
| IS.O.A2.4.4 | Identity links | O/A2 | — |
| IS.O.A3 | Arrangement | O/A3 | — |
| IS.O.A3.1 | Classification schemes | O/A3 | — |
| IS.O.A3.1.1 | Dewey Decimal | O/A3 | — |
| IS.O.A3.1.2 | Library of Congress | O/A3 | — |
| IS.O.A3.1.3 | Exclusivity test | O/A3 | — |
| IS.O.A3.1.4 | Single location | O/A3 | — |
| IS.O.A3.2 | Faceted classification | O/A3 | — |
| IS.O.A3.2.1 | PMEST | O/A3 | — |
| IS.O.A3.2.2 | Facet independence | O/A3 | — |
| IS.O.A3.2.3 | Citation order | O/A3 | — |
| IS.O.A3.2.4 | Faceted search | O/A3 | — |
| IS.O.A3.3 | Archival arrangement | O/A3 | — |
| IS.O.A3.3.1 | Provenance | O/A3 | — |
| IS.O.A3.3.2 | Original order | O/A3 | — |
| IS.O.A3.3.3 | Multilevel description | O/A3 | — |
| IS.O.A3.3.4 | Digital original order | O/A3 | — |
| IS.O.A3.4 | Ontologies | O/A3 | PL |
| IS.O.A3.4.1 | Definition and test | O/A3 | — |
| IS.O.A3.4.2 | OWL 2 DL | O/A3 | MA.O.A1, CS.O.A2.3 |
| IS.O.A3.4.3 | Upper-level ontologies | O/A3 | PL.O.A1.1 |
| IS.O.A3.4.4 | Alignment | O/A3 | — |
| IS.O.A3.5 | This taxonomy | O/A3 | — |
| IS.O.A3.5.1 | Unit of claim | O/A3 | — |
| IS.O.A3.5.2 | One home | O/A3 | — |
| IS.O.A3.5.3 | Key-line discipline | O/A3 | — |
| IS.O.A3.5.4 | Protocol reliability | O/A3 | — |
| IS.O.A4 | Retrieval | O/A4 | — |
| IS.O.A4.1 | Retrieval effectiveness | O/A4 | CS |
| IS.O.A4.1.1 | Precision and recall | O/A4 | — |
| IS.O.A4.1.2 | Cranfield design | O/A4 | — |
| IS.O.A4.1.3 | Pooling | O/A4 | — |
| IS.O.A4.1.4 | Rank-based measures | O/A4 | — |
| IS.O.A4.2 | Relevance | O/A4 | — |
| IS.O.A4.2.1 | Topical and user relevance | O/A4 | — |
| IS.O.A4.2.2 | Assessor disagreement | O/A4 | — |
| IS.O.A4.2.3 | Graded relevance | O/A4 | — |
| IS.O.A4.2.4 | Relevance feedback | O/A4 | CS |
| IS.O.A4.3 | Bibliometrics | O/A4 | — |
| IS.O.A4.3.1 | Lotka's law | O/A4 | — |
| IS.O.A4.3.2 | Bradford's law | O/A4 | — |
| IS.O.A4.3.3 | Citation analysis | O/A4 | — |
| IS.O.A4.3.4 | Indicators | O/A4 | — |
| IS.O.A4.4 | Information behaviour | O/A4 | MS |
| IS.O.A4.4.1 | Information search process | O/A4 | — |
| IS.O.A4.4.2 | Berrypicking | O/A4 | — |
| IS.O.A4.4.3 | Information foraging | O/A4 | — |
| IS.O.A4.4.4 | Information need | O/A4 | — |
| IS.O.A5 | Preservation | O/A5 | — |
| IS.O.A5.1 | Physical conservation | O/A5 | CH |
| IS.O.A5.1.1 | Agents of deterioration | O/A5 | — |
| IS.O.A5.1.2 | Storage conditions | O/A5 | CH.O.A4.2 |
| IS.O.A5.1.3 | Intervention | O/A5 | — |
| IS.O.A5.1.4 | Media decay | O/A5 | CH.O.A4 |
| IS.O.A5.2 | Digital preservation | O/A5 | — |
| IS.O.A5.2.1 | OAIS entities | O/A5 | — |
| IS.O.A5.2.2 | Designated community | O/A5 | — |
| IS.O.A5.2.3 | Migration and emulation | O/A5 | — |
| IS.O.A5.2.4 | Fixity and copies | O/A5 | CS.O.A5.1 |
| IS.O.A5.3 | Access and rights | O/A5 | LA |
| IS.O.A5.3.1 | Gold and green | O/A5 | — |
| IS.O.A5.3.2 | Licence statements | O/A5 | LA |
| IS.O.A5.3.3 | Conditions of access | O/A5 | LA |
| IS.O.A5.4 | Indigenous data governance | O/A5 | IK |

## 13. Self-check against R1–R12

| Rule | Result | If FAIL: sentence and repair |
|---|---|---|
| R1–R3 | PASS | — |
| R4 | PASS | ANZSRC 46 split stated (checked). |
| R5 | PASS | Regularities stated as empirical within stated literatures. Named methods and models carry their hypotheses. |
| R6–R10 | PASS | CONTESTED, OPEN and UNVERIFIED items are labelled in section 11. |
| R11 | PASS (thin) | Standards named are well attested. Items marked UNVERIFIED need a specialist check. |
| R12 | PASS | — |
