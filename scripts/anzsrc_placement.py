"""Placement of every ANZSRC 2020 FoR group (and overriding 6-digit fields) under a Taxonomy field and cell.

GROUP maps a 4-digit group to "FIELD.O.An". FIELD overrides a 6-digit field where it differs from its group.
Used by scripts/build_maps.py. Placements are editorial (Taxonomy), not part of ANZSRC.
"""

GROUP = {
    # 30 Agricultural, veterinary and food sciences
    "3001": "AG.O.A1", "3002": "AG.O.A5", "3003": "AG.O.A2", "3004": "AG.O.A2", "3005": "AG.O.A2",
    "3006": "AG.O.A4", "3007": "AG.O.A2", "3008": "AG.O.A2", "3009": "AG.O.A3", "3099": "AG.O.A5",
    # 31 Biological sciences
    "3101": "BI.O.A2", "3102": "BI.O.A1", "3103": "BI.O.A5", "3104": "BI.O.A4", "3105": "BI.O.A1",
    "3106": "BI.O.A2", "3107": "BI.O.A3", "3108": "BI.O.A3", "3109": "BI.O.A3", "3199": "BI.O.A3",
    # 32 Biomedical and clinical sciences
    "3201": "MD.O.A1", "3202": "MD.O.A3", "3203": "MD.O.A4", "3204": "MD.O.A2", "3205": "MD.O.A2",
    "3206": "MD.O.A4", "3207": "MD.O.A2", "3208": "MD.O.A2", "3209": "MS.O.A2", "3210": "MD.O.A5",
    "3211": "MD.O.A1", "3212": "MD.O.A1", "3213": "MD.O.A1", "3214": "MD.O.A4", "3215": "MD.O.A1",
    "3299": "MD.O.A2",
    # 33 Built environment and design
    "3301": "DE.O.A2", "3302": "DE.O.A5", "3303": "DE.O.A1", "3304": "DE.O.A4", "3399": "DE.O.A3",
    # 34 Chemical sciences
    "3401": "CH.O.A5", "3402": "CH.O.A2", "3403": "CH.O.A2", "3404": "CH.O.A5", "3405": "CH.O.A5",
    "3406": "CH.O.A3", "3407": "CH.O.A2", "3499": "CH.O.A1",
    # 35 Commerce, management, tourism and services
    "3501": "BU.O.A1", "3502": "BU.O.A2", "3503": "BU.O.A3", "3504": "BU.O.A3", "3505": "BU.O.A3",
    "3506": "BU.O.A4", "3507": "BU.O.A3", "3508": "BU.O.A4", "3509": "BU.O.A3", "3599": "BU.O.A5",
    # 36 Creative arts and writing
    "3601": "AR.O.A4", "3602": "AR.O.A1", "3603": "AR.O.A1", "3604": "AR.O.A1", "3605": "AR.O.A1",
    "3606": "AR.O.A1", "3699": "AR.O.A2",
    # 37 Earth sciences
    "3701": "EA.O.A4", "3702": "EA.O.A4", "3703": "EA.O.A1", "3704": "EA.O.A5", "3705": "EA.O.A3",
    "3706": "EA.O.A2", "3707": "EA.O.A4", "3708": "EA.O.A4", "3709": "EA.O.A4", "3799": "EA.O.A1",
    # 38 Economics
    "3801": "EC.O.A2", "3802": "EC.O.A4", "3803": "EC.O.A1", "3899": "EC.O.A5",
    # 39 Education
    "3901": "ED.O.A3", "3902": "ED.O.A1", "3903": "ED.O.A5", "3904": "ED.O.A2", "3999": "ED.O.A5",
    # 40 Engineering
    "4001": "EN.O.A2", "4002": "EN.O.A2", "4003": "EN.O.A1", "4004": "EN.O.A3", "4005": "EN.O.A1",
    "4006": "EN.O.A4", "4007": "EN.O.A4", "4008": "EN.O.A4", "4009": "EN.O.A4", "4010": "EN.O.A1",
    "4011": "EN.O.A2", "4012": "EN.O.A2", "4013": "EN.O.A1", "4014": "EN.O.A5", "4015": "EN.O.A2",
    "4016": "EN.O.A5", "4017": "EN.O.A1", "4018": "EN.O.A5", "4019": "EN.O.A5", "4099": "EN.O.A3",
    # 41 Environmental sciences
    "4101": "EV.O.A4", "4102": "EV.O.A4", "4103": "EV.O.A4", "4104": "EV.O.A4", "4105": "EV.O.A1",
    "4106": "EV.O.A2", "4199": "EV.O.A2",
    # 42 Health sciences
    "4201": "MD.O.A4", "4202": "MD.O.A5", "4203": "MD.O.A5", "4204": "MD.O.A4", "4205": "MD.O.A4",
    "4206": "MD.O.A5", "4207": "MD.O.A5", "4208": "MD.O.A4", "4299": "MD.O.A5",
    # 43 History, heritage and archaeology
    "4301": "HI.O.A1", "4302": "HI.O.A5", "4303": "HI.O.A4", "4399": "HI.O.A2",
    # 44 Human society
    "4401": "MS.O.A5", "4402": "LA.O.A3", "4403": "MS.O.A5", "4404": "EC.O.A4", "4405": "MS.O.A5",
    "4406": "EA.O.A5", "4407": "PO.O.A4", "4408": "PO.O.A2", "4409": "MS.O.A4", "4410": "MS.O.A5",
    "4499": "MS.O.A5",
    # 45 Indigenous studies (all provisional)
    "4501": "IK.O.A4", "4502": "IK.O.A4", "4503": "IK.O.A2", "4504": "IK.O.A3", "4505": "IK.O.A3",
    "4506": "IK.O.A1", "4507": "IK.O.A4", "4508": "IK.O.A4", "4509": "IK.O.A2", "4510": "IK.O.A3",
    "4511": "IK.O.A3", "4512": "IK.O.A1", "4513": "IK.O.A4", "4514": "IK.O.A4", "4515": "IK.O.A2",
    "4516": "IK.O.A3", "4517": "IK.O.A1", "4518": "IK.O.A3", "4519": "IK.O.A5", "4599": "IK.O.A5",
    # 46 Information and computing sciences
    "4601": "CS.O.A3", "4602": "CS.O.A4", "4603": "CS.O.A4", "4604": "CS.O.A5", "4605": "IS.O.A4",
    "4606": "CS.O.A3", "4607": "CS.O.A2", "4608": "CS.O.A3", "4609": "IS.O.A3", "4610": "IS.O.A2",
    "4611": "CS.O.A4", "4612": "CS.O.A1", "4613": "CS.O.A2", "4699": "CS.O.A1",
    # 47 Language, communication and culture
    "4701": "LN.O.A4", "4702": "AR.O.A4", "4703": "LN.O.A5", "4704": "LN.O.A2", "4705": "AR.O.A3",
    "4799": "LN.O.A4",
    # 48 Law and legal studies
    "4801": "LA.O.A2", "4802": "LA.O.A4", "4803": "LA.O.A1", "4804": "LA.O.A1", "4805": "LA.O.A5",
    "4806": "LA.O.A2", "4807": "LA.O.A4", "4899": "LA.O.A1",
    # 49 Mathematical sciences (refined by FIELD below)
    "4901": "MA.O.A4", "4902": "MA.O.A4", "4903": "MA.O.A4", "4904": "MA.O.A2", "4905": "MA.O.A5",
    "4999": "MA.O.A1",
    # 50 Philosophy and religious studies
    "5001": "PL.O.A4", "5002": "PL.O.A5", "5003": "PL.O.A1", "5004": "RE.O.A4", "5005": "RE.O.A1",
    "5099": "PL.O.A1",
    # 51 Physical sciences
    "5101": "PH.O.A3", "5102": "PH.O.A2", "5103": "PH.O.A1", "5104": "PH.O.A4", "5105": "PH.O.A5",
    "5106": "PH.O.A2", "5107": "PH.O.A2", "5108": "PH.O.A2", "5109": "PH.O.A3", "5110": "PH.O.A1",
    "5199": "PH.O.A5",
    # 52 Psychology
    "5201": "MS.O.A3", "5202": "MS.O.A2", "5203": "MS.O.A3", "5204": "MS.O.A1", "5205": "MS.O.A4",
    "5299": "MS.O.A1",
}

FIELD = {
    # Mathematics: pure maths by cell
    "490401": "MA.O.A2", "490402": "MA.O.A3", "490403": "MA.O.A2", "490404": "MA.O.A2",
    "490405": "MA.O.A2", "490406": "MA.O.A4", "490407": "MA.O.A1", "490408": "MA.O.A4",
    "490409": "MA.O.A4", "490410": "MA.O.A4", "490411": "MA.O.A4", "490412": "MA.O.A3",
    "490106": "MA.O.A5", "490108": "MA.O.A4", "490206": "MA.O.A5",
    # Physics: equilibrium vs non-equilibrium, gravitation
    "510304": "PH.O.A4", "510105": "PH.O.A3", "510405": "PH.O.A5", "519901": "PH.O.A5",
    "510602": "PH.O.A5", "510701": "PH.O.A3",
    # Politics: international relations and defence go to strategy where they concern conflict
    "440804": "ST.O.A3", "440808": "PO.O.A5", "440810": "ST.O.A4", "440811": "PL.O.A4",
    "440802": "PO.O.A1", "440803": "PO.O.A2", "440805": "PO.O.A4", "440806": "PO.O.A3",
    # Philosophy by cell
    "500301": "PL.O.A4", "500302": "PL.O.A4", "500303": "PL.O.A4", "500304": "PL.O.A4",
    "500305": "PL.O.A2", "500306": "PL.O.A4", "500307": "PL.O.A3", "500308": "PL.O.A3",
    "500309": "PL.O.A1", "500310": "PL.O.A2", "500311": "PL.O.A2", "500312": "PL.O.A2",
    "500313": "PL.O.A4", "500314": "PL.O.A3", "500315": "PL.O.A2", "500316": "RE.O.A1",
    "500317": "PL.O.A5", "500318": "PL.O.A1", "500319": "PL.O.A3", "500320": "PL.O.A2",
    "500321": "PL.O.A4",
    # Linguistics: signal, meaning. The 4704 group stays Form (LN.O.A2).
    "470405": "LN.O.A3",  # Discourse and pragmatics
    "470408": "LN.O.A3",  # Lexicography and semantics
    "470410": "LN.O.A1",  # Phonetics and speech science
    # Education: assessment was sitting with the 3904 specialist-studies group.
    "390402": "ED.O.A4",  # Education assessment and evaluation
}
