"""Rebuild the EV classification groups. No model calls.

Deletes template summaries, regroups leaves by kind, inserts the loose
topics that belong in a named group, and routes the rest to a field code.

Other fields use scripts/rebuild_classification.py and pyramids/rebuild/<FIELD>.json.
This file stays the EV leaf rebuild. It does not call a model.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine" / "v3"))
from minto_check import minto_counts, minto_issues
from pyramid import IdBook, render_markdown

WORD = re.compile(r"[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)?")
VERBS = re.compile(r"\b(is|are|places|holds|covers|follows|aims)\b")
DEFINITION = (
    "An environmental topic names a human load on air, water, soil, or living systems, or the condition that results. "
    "It also names the harm, the action taken, or the limit that condition should not cross. "
    "A chemical, organism, earth science, disease, price, firm, law, place, machine, or data model is routed to its own field."
)
DRIVER_FOLD = (
    "A driver is the activity that creates a load. "
    "The load is the pressure, so drivers are grouped under pressures and are not a sixth key-line cell."
)

# (path, statement, basis, order, dimension)
SPECS = {}


def spec(path, statement, basis, order, dimension, rank_note=""):
    words = WORD.findall(statement)
    if not (statement.endswith(".") and statement.count(".") == 1 and VERBS.search(statement) and len(words) <= 25):
        raise SystemExit(f"bad statement: {statement}")
    SPECS[path] = {
        "statement": statement,
        "basis": basis,
        "order": order,
        "dimension": dimension,
        "rank_note": rank_note,
    }


def S(name):
    return tuple(name.split("/"))


# Pressures
spec(S("P/emissions"), "Emissions are the loads from greenhouse gases and other pollutants.", "kinds", "structure", "the kind of emitted load")
spec(S("P/emissions/pollutant"), "Pollutants are substances whose presence is an emission load.", "kinds", "structure", "the kind of pollutant fact")
spec(S("P/emissions/pollutant/movement"), "Pollutant movement is transport or retention of a pollutant.", "kinds", "structure", "the kind of movement")
spec(S("P/emissions/pollutant/movement/transport"), "Pollutant transport is movement of a pollutant through air, water, or soil.", "kinds", "structure", "the kind of pollutant movement")
spec(S("P/emissions/pollutant/movement/retention"), "Pollutant retention is a pollutant held, deposited, or given a pathway.", "kinds", "structure", "the kind of pollutant retention")
spec(S("P/emissions/pollutant/change"), "Pollutant change is loss or a shift in the pollutant.", "kinds", "structure", "the kind of pollutant change")
spec(S("P/emissions/pollutant/change/loss"), "Pollutant loss is degradation, elimination, or reduction of a pollutant.", "kinds", "structure", "the kind of loss")
spec(S("P/emissions/pollutant/change/shift"), "Pollutant shift is formation, evolution, behaviour, or immobilisation.", "kinds", "structure", "the kind of shift")
spec(S("P/emissions/pollutant/measure"), "Pollutant measures are the concentration, level, load, or immission of a pollutant.", "kinds", "structure", "the kind of pollutant measure")
spec(S("P/emissions/pollutant/class"), "Pollutant classes are chemistry, degradability, and the medium that is loaded.", "kinds", "structure", "the class of pollutant")
spec(S("P/emissions/pollutant/class/chemistry"), "Pollutant chemistry is the chemical class of an emitted pollutant.", "kinds", "structure", "the chemical class")
spec(S("P/emissions/pollutant/class/degradability"), "Pollutant degradability is whether an emitted pollutant breaks down.", "kinds", "structure", "the degradability class")
spec(S("P/emissions/pollutant/class/medium"), "Pollutant media are air, water and soil, or another physical form.", "kinds", "structure", "the medium that is loaded")
spec(S("P/emissions/pollutant/class/medium/air"), "Air pollutants are pollutants named as loads on air.", "kinds", "structure", "the air pollutant")
spec(S("P/emissions/pollutant/class/medium/land"), "Land and water pollutants are loads on soil, water, food, or a city.", "kinds", "structure", "the land or water pollutant")
spec(S("P/emissions/pollutant/class/medium/form"), "Physical pollutant forms are noise, radiation, and the bare pollutant name.", "kinds", "structure", "the physical form")
spec(S("P/emissions/waste"), "Wastes are discarded materials that load the environment.", "kinds", "structure", "the kind of waste")
spec(S("P/emissions/waste/household"), "Household wastes are discards from homes and consumers.", "kinds", "structure", "the household waste")
spec(S("P/emissions/waste/material"), "Material wastes are discards named by what they are made of.", "kinds", "structure", "the material of the waste")
spec(S("P/emissions/waste/gas"), "Waste gases are gaseous discards, including waste air and waste heat.", "kinds", "structure", "the gaseous waste")
spec(S("P/emissions/waste/gas-fate"), "Waste-gas fate is dispersion, emission, reduction, or a use of waste heat.", "kinds", "structure", "the fate of waste gas")
spec(S("P/extraction/taking/land"), "Land-stock taking is extraction of peat, sand, or water.", "kinds", "structure", "the land stock taken")
spec(S("R/conservation/water/area"), "Water protection areas are coasts, flood zones, and noise zones that are guarded.", "kinds", "structure", "the protected water area")
spec(S("R/conservation/water/catchment"), "Catchment protection is the guarding of groundwater, sea water, and the catchment.", "kinds", "structure", "the catchment protection")
spec(S("R/regulation/management/water"), "Water management is the response that directs a river, a supply, or water quality.", "kinds", "structure", "the water management")
spec(S("R/regulation/management/habitat"), "Habitat management is the response that directs a forest, landscape, or ecosystem.", "kinds", "structure", "the habitat management")
spec(S("R/regulation/management/stock"), "Stock management here is the response that directs a natural resource or a fishery.", "kinds", "structure", "the stock management")
spec(S("R/regulation/management/waste"), "Waste management is the response that directs manure or a waste system.", "kinds", "structure", "the waste management")
spec(S("R/regulation/management/waste/manure"), "Manure management is the response that directs animal waste and liquid manure.", "kinds", "structure", "the manure management")
spec(S("R/regulation/management/waste/system"), "Waste systems are the named systems that direct a waste stream.", "kinds", "structure", "the waste system")
spec(S("R/regulation/waste-treatment/special"), "Special treatment is thermal, surface, or phytosanitary treatment.", "kinds", "structure", "the special treatment")
spec(S("R/regulation/measures"), "Preventive measures are mitigation, prevention, and protection taken as a response.", "kinds", "structure", "the preventive measure")
spec(S("P/emissions/waste/handling"), "Waste handling is incineration, recycling, minimisation, or use of waste.", "kinds", "structure", "the handling of waste")
spec(S("P/emissions/emission"), "Emission records are inventories, factors, sources, and reductions of a load.", "kinds", "structure", "the kind of emission record")
spec(S("P/emissions/emission/source"), "Emission sources are the activities or places a load comes from.", "kinds", "structure", "the source of the emission")
spec(S("P/emissions/emission/record"), "Emission records are inventories, factors, levels, and estimates of a load.", "kinds", "structure", "the record of the emission")
spec(S("P/emissions/emission/reduction"), "Emission reduction is an action that cuts a pollutant load at source.", "cause_effect", "time", "the reduction step")
spec(S("P/emissions/fuel"), "Fuels are energy carriers whose use creates an emission load.", "kinds", "structure", "the kind of fuel")
spec(S("P/emissions/fertiliser"), "Fertilisers are nutrient loads applied to land.", "kinds", "structure", "the kind of fertiliser")
spec(S("P/land"), "Land and sea use changes are the loads from clearance, drainage, and building.", "kinds", "structure", "the kind of use change")
spec(S("P/land/urban"), "Urban loads are noise, pollution, traffic, and water supply in a city.", "kinds", "structure", "the urban load")
spec(S("P/land/development"), "Development loads are coastal and river-basin building.", "kinds", "structure", "the development load")
spec(S("P/extraction"), "Extraction is the load from taking water, minerals, or living stocks.", "kinds", "structure", "the kind of extraction")
spec(S("P/extraction/mining"), "Mining is the taking of minerals, coal, or rock from the ground.", "kinds", "structure", "the kind of mining")
spec(S("P/extraction/taking"), "Resource taking is extraction of water, gas, oil, gravel, or minerals.", "kinds", "structure", "the stock that is taken")
spec(S("P/extraction/fishing"), "Fishing is the taking of fish and the fishery that supports that taking.", "parts", "structure", "the part of the fishery")
spec(S("P/extraction/fishing/activity"), "Fishing activities are the ways fish are taken.", "kinds", "structure", "the way of fishing")
spec(S("P/extraction/fishing/fishery"), "Fisheries are the stocks and grounds from which fish are taken.", "kinds", "structure", "the kind of fishery")
spec(S("P/extraction/fishing/gear"), "Fishing gear is the fleet, vessel, or ground used to take fish.", "parts", "structure", "the part of the gear")
spec(S("P/introduced"), "Introduced species are the loads from pests and organisms people bring in.", "kinds", "structure", "the kind of introduction")
spec(S("P/drivers"), "Drivers are the activities that create a load, grouped here because the load is the pressure.", "kinds", "structure", "the kind of activity")
spec(S("P/drivers/food"), "Food and drink industries are activities that create organic and water loads.", "kinds", "structure", "the food activity")
spec(S("P/drivers/materials"), "Materials industries are activities that create mineral, metal, or energy loads.", "kinds", "structure", "the materials activity")
spec(S("P/drivers/other"), "Other load-creating industries are activities whose pressure is not a single stock taken.", "kinds", "structure", "the industry")
# "Other" is forbidden in statements. Fix that statement.
SPECS[S("P/drivers/other")]["statement"] = "General industries are activities whose load is not one named stock."

# States
spec(S("S/conditions"), "Measured conditions are the states of air, water, soil, and living systems.", "kinds", "structure", "the medium that is measured")
spec(S("S/conditions/biodiversity/cover"), "Ecosystem cover is forest, dryland, and aquatic vegetation state.", "kinds", "structure", "the cover")
spec(S("S/conditions/biodiversity/setting"), "Ecosystem settings are cold, high, zoned, and local habitats.", "kinds", "structure", "the setting")
spec(S("S/conditions/biodiversity/property"), "Ecosystem properties are services, condition, and form of a living system.", "kinds", "structure", "the property")
spec(S("S/hazards/weather"), "Hydro-meteorological hazards are floods, storms, cyclones, and extremes.", "kinds", "structure", "the weather hazard")
spec(S("S/hazards/process"), "Environmental processes are matter cycles and exchanges that set a state.", "kinds", "structure", "the process")
spec(S("S/conditions/air"), "Air quality is the measured state of the atmosphere.", "kinds", "structure", "the kind of air state")
spec(S("S/conditions/air/climate"), "Climate states are the measured classes of climate.", "kinds", "structure", "the climate class")
spec(S("S/conditions/air/climate-change"), "Climate-change states are measured shifts in climate, apart from the response to them.", "kinds", "structure", "the climate-change state")
spec(S("S/conditions/air/ozone"), "Ozone states are the measured condition of ozone in the atmosphere.", "kinds", "structure", "the ozone measure")
spec(S("S/conditions/air/temperature"), "Temperature states are the measured warmth of air.", "kinds", "structure", "the temperature measure")
spec(S("S/conditions/air/level"), "Air levels are measured background or noise levels in the atmosphere.", "kinds", "structure", "the air level")
spec(S("S/conditions/fresh"), "Freshwater quality is the measured state of rivers, lakes, and groundwater.", "kinds", "structure", "the freshwater body")
spec(S("S/conditions/marine"), "The marine environment is the measured state of the sea.", "kinds", "structure", "the kind of marine state")
spec(S("S/conditions/marine/water"), "Sea water states are the measured condition of seawater and the open sea.", "kinds", "structure", "the seawater state")
spec(S("S/conditions/marine/level"), "Sea level states are measured changes in the height of the sea.", "kinds", "structure", "the sea-level state")
spec(S("S/conditions/marine/motion"), "Sea motion is circulation, current, or waves in the ocean.", "kinds", "structure", "the kind of sea motion")
spec(S("S/conditions/marine/coast"), "Coastal states are the measured condition of the coast and the shore.", "kinds", "structure", "the coastal state")
spec(S("S/conditions/marine/bed"), "Sea-bed states are the measured condition of the bed and its cover.", "kinds", "structure", "the sea-bed state")
spec(S("S/conditions/soil"), "Soil state is the measured condition of the land surface.", "kinds", "structure", "the soil state")
spec(S("S/conditions/biodiversity"), "Biodiversity status is the measured condition of ecosystems and habitats.", "kinds", "structure", "the kind of ecosystem state")
spec(S("S/conditions/biodiversity/cover/forest"), "Forest ecosystems are woodland and forest states.", "kinds", "structure", "the forest ecosystem")
spec(S("S/conditions/biodiversity/cover/dry"), "Dryland ecosystems are arid and semi-arid states.", "kinds", "structure", "the dryland ecosystem")
spec(S("S/conditions/biodiversity/cover/water"), "Aquatic ecosystems are freshwater, marine, and wetland states.", "kinds", "structure", "the aquatic ecosystem")
spec(S("S/conditions/biodiversity/setting/cold"), "Cold ecosystems are polar, arctic, antarctic, and permafrost states.", "kinds", "structure", "the cold ecosystem")
spec(S("S/conditions/biodiversity/setting/high"), "Highland ecosystems are mountain and highland states.", "kinds", "structure", "the highland ecosystem")
spec(S("S/conditions/biodiversity/setting/zone"), "Climate-zone ecosystems are tropical, subtropical, temperate, and terrestrial states.", "kinds", "structure", "the climate zone")
spec(S("S/conditions/biodiversity/setting/place"), "Local ecosystems are urban, island, grassland, and underground states.", "kinds", "structure", "the local ecosystem")
spec(S("S/conditions/biodiversity/property/services"), "Ecosystem services are the benefits a living system provides.", "kinds", "structure", "the ecosystem service")
spec(S("S/conditions/biodiversity/property/condition"), "Ecosystem condition is vulnerability, stability, and resilience.", "kinds", "structure", "the ecosystem condition")
spec(S("S/conditions/biodiversity/property/form"), "Ecosystem form is the type, boundary, interaction, and process of a system.", "kinds", "structure", "the ecosystem form")
spec(S("S/conditions/biodiversity/property/status"), "Ecosystem status is the system itself and whether it is sensitive or important.", "kinds", "structure", "the ecosystem status")
spec(S("S/hazards"), "Natural hazards and processes are geological, weather, and ecological events.", "kinds", "structure", "the kind of natural event")
spec(S("S/hazards/geological"), "Geological hazards are ground-failure and volcanic events.", "kinds", "structure", "the geological hazard")
spec(S("S/hazards/ground"), "Ground-failure hazards are earthquakes, landslides, and avalanches.", "kinds", "structure", "the ground-failure hazard")
spec(S("S/hazards/volcanic"), "Volcanic hazards are eruptions and volcanism.", "kinds", "structure", "the volcanic hazard")
spec(S("S/hazards/weather/flood"), "Floods are hydro-meteorological hazards in which water covers land.", "kinds", "structure", "the flood hazard")
spec(S("S/hazards/weather/storm"), "Storms are hydro-meteorological hazards of wind, thunder, and hail.", "kinds", "structure", "the storm hazard")
spec(S("S/hazards/weather/cyclone"), "Cyclones are tropical and extratropical storms named as cyclone, hurricane, or typhoon.", "kinds", "structure", "the cyclonic storm")
spec(S("S/hazards/weather/extreme"), "Weather extremes are drought, heat, and cold as hazards.", "kinds", "degree", "from dry, to hot, to cold", "Drought, then heat, then cold, by the stress on water and temperature.")
spec(S("S/hazards/weather/disaster"), "Disaster names are the labels for a natural hazard taken as one event.", "kinds", "structure", "the disaster label")
spec(S("S/hazards/process/cycles"), "Matter cycles are biogeochemical, carbon, and water cycles that set a state.", "parts", "structure", "the part of the cycle")
spec(S("S/hazards/process/nitrogen"), "Nitrogen transformations are fixation, ammonification, and denitrification.", "cause_effect", "time", "the nitrogen step")
spec(S("S/hazards/process/exchange"), "Water exchange is evaporation and evapotranspiration from land and water.", "kinds", "structure", "the water-exchange process")
spec(S("S/resources"), "Natural resources are stocks of water, minerals, energy, and living systems.", "kinds", "structure", "the kind of stock")
spec(S("S/resources/water"), "Water resources are stocks of fresh and fluvial water.", "kinds", "structure", "the water stock")
spec(S("S/resources/living"), "Living resources are stocks of forests, fisheries, and genetic material.", "kinds", "structure", "the living stock")
spec(S("S/resources/mineral"), "Mineral resources are stocks of minerals and deposits.", "kinds", "structure", "the mineral stock")
spec(S("S/resources/energy"), "Energy resources are stocks of energy, including renewable and primary energy.", "kinds", "structure", "the energy stock")
spec(S("S/resources/class"), "Resource classes are renewable and non-renewable stocks, named as a class.", "kinds", "structure", "the resource class")

# Impacts
spec(S("I/ecosystem"), "Ecosystem harm is the loss of function or species after a changed state.", "kinds", "structure", "the system that is harmed")
spec(S("I/health"), "Human health impact is the harm to people that follows an exposure.", "kinds", "structure", "the health harm")
spec(S("I/attribution"), "Attribution is the share of an observed change assigned to a stated pressure.", "kinds", "structure", "the attribution")

# Responses
spec(S("R/restoration"), "Restoration is the response that aims at measured recovery.", "kinds", "structure", "the kind of restoration")
spec(S("R/conservation"), "Conservation is the response that protects areas and cuts pressures on them.", "kinds", "structure", "the kind of protection")
spec(S("R/conservation/nature"), "Nature protection is the response that guards species, habitats, and landscapes.", "kinds", "structure", "the nature protection")
spec(S("R/conservation/nature/area"), "Protected areas are sites, biotopes, and marine conservation areas.", "kinds", "structure", "the protected area")
spec(S("R/conservation/nature/species"), "Species protection is the response that guards animals, plants, and biodiversity.", "kinds", "structure", "the species protection")
spec(S("R/conservation/nature/landscape"), "Landscape protection is the response that guards forests, mountains, and landscape.", "kinds", "structure", "the landscape protection")
spec(S("R/conservation/nature/general"), "Conservation responses are the general acts and policies of protection.", "kinds", "structure", "the conservation response")
spec(S("R/conservation/water"), "Water protection is the response that guards water and coasts from a load.", "kinds", "structure", "the water protection")
spec(S("R/conservation/institution"), "Protection bodies are agencies and organisations that carry out environmental protection.", "kinds", "structure", "the protection body")
spec(S("R/regulation"), "Regulation is the response whose environmental effect is what this field measures.", "kinds", "structure", "the kind of regulation")
spec(S("R/regulation/water-treatment"), "Water treatment is the response that cleans waste water or sewage.", "kinds", "structure", "the kind of water treatment")
spec(S("R/regulation/water-treatment/stage"), "Treatment stages are primary, then secondary, then tertiary cleaning.", "cause_effect", "time", "the treatment stage")
spec(S("R/regulation/water-treatment/plant"), "Treatment plants are the works that clean waste water or sewage.", "kinds", "structure", "the treatment plant")
spec(S("R/regulation/water-treatment/mode"), "Treatment modes are biological and on-site ways of cleaning waste water.", "kinds", "structure", "the treatment mode")
spec(S("R/regulation/waste-treatment/process"), "Treatment processes are biological, chemical, and aerobic ways of treating waste.", "kinds", "structure", "the treatment process")
spec(S("R/regulation/waste-treatment/plant"), "Waste plants are the works that treat a gas, sludge, or effluent.", "kinds", "structure", "the waste plant")
spec(S("R/regulation/waste-treatment/general"), "General treatment is the unnamed treatment response and its residue.", "kinds", "structure", "the general treatment")
spec(S("R/regulation/control/pollution"), "Pollution control is equipment, a measure, or a technology that limits a load.", "kinds", "structure", "the pollution control")
spec(S("R/regulation/control/hazard"), "Hazard control is the response to drought or flood.", "kinds", "structure", "the hazard control")
spec(S("R/regulation/control/general"), "General control is a control measure or a regulatory control.", "kinds", "structure", "the general control")
spec(S("R/regulation/management/climate"), "Climate management is adaptation and mitigation of climate change.", "kinds", "structure", "the climate management")
spec(S("R/regulation/management/place"), "Place management is the response that directs a basin, a fishery, or manure.", "kinds", "structure", "the place management")
spec(S("R/regulation/management/general"), "General management is the unnamed management response, including risk.", "kinds", "structure", "the general management")
spec(S("P/emissions/fuel/fossil"), "Fossil fuels are coal, oil, and diesel carriers that create a load.", "kinds", "structure", "the fossil fuel")
spec(S("P/emissions/fuel/other"), "Nuclear and alternative fuels are carriers that are not named as fossil fuels.", "kinds", "structure", "the fuel carrier")
spec(S("P/emissions/emission/source/air"), "Air emissions are loads named as releases to air.", "kinds", "structure", "the air emission")
spec(S("P/emissions/emission/source/activity"), "Activity emissions are loads from industry, traffic, or mining gas.", "kinds", "structure", "the activity emission")
spec(S("P/emissions/emission/source/listed"), "Listed emissions are the source label and releases to water or of radiation.", "kinds", "structure", "the listed emission")
spec(S("P/emissions/emission/record/inventory"), "Emission inventories are factors, estimates, and inventory books.", "kinds", "structure", "the inventory")
spec(S("P/emissions/emission/record/state"), "Emission state is the bare emission, its level, and its situation.", "kinds", "structure", "the emission state")
spec(S("P/emissions/waste/handling/burn"), "Waste burning is incineration of a discard.", "kinds", "structure", "the burning")
spec(S("P/emissions/waste/handling/reduce"), "Waste reduction is minimisation, recycling, or use as energy.", "kinds", "structure", "the reduction")
spec(S("P/emissions/waste/handling/record"), "Waste records are the state and the volume of a discard.", "kinds", "structure", "the waste record")
spec(S("P/emissions/waste/material/organic"), "Organic wastes are degradable, plastic, and organic discards.", "kinds", "structure", "the organic waste")
spec(S("P/emissions/waste/material/hazard"), "Hazardous wastes are radioactive, sludge, and abatement wastes.", "kinds", "structure", "the hazardous waste")
spec(S("P/extraction/mining/rock"), "Rock mining is the taking of coal, lignite, or rock salt.", "kinds", "structure", "the rock mining")
spec(S("P/extraction/mining/sea"), "Sea mining is mining of the deep sea, the offshore, or the sea bed.", "kinds", "structure", "the sea mining")
spec(S("P/extraction/mining/surface"), "Surface mining is opencast and strip mining, and mining named as such.", "kinds", "structure", "the surface mining")
spec(S("P/extraction/mining/output"), "Mining outputs are the product and the waste of mining.", "kinds", "structure", "the mining output")
spec(S("P/extraction/taking/mineral"), "Mineral taking is extraction of aggregate, gravel, or a mineral.", "kinds", "structure", "the mineral taking")
spec(S("P/extraction/taking/fluid"), "Fluid taking is extraction of oil, gas, or groundwater.", "kinds", "structure", "the fluid taking")
spec(S("P/introduced/release"), "Species release is accidental release or introduction of animals or plants.", "kinds", "structure", "the release")
spec(S("P/introduced/organism"), "Introduced organisms are pests, modified organisms, and organisms named as such.", "kinds", "structure", "the introduced organism")
spec(S("P/drivers/food/drink"), "Drink industries are beverage, brewing, and distilling activities.", "kinds", "structure", "the drink industry")
spec(S("P/drivers/food/food"), "Food industries are dairy, food, and oil-and-fat activities.", "kinds", "structure", "the food industry")
spec(S("P/drivers/materials/metal"), "Metal industries are iron, steel, and non-ferrous activities.", "kinds", "structure", "the metal industry")
spec(S("P/drivers/materials/mineral"), "Mineral industries are cement, glass, coal, and mining activities.", "kinds", "structure", "the mineral industry")
spec(S("P/drivers/materials/products"), "Metal-product industries are metal products and metallurgy.", "kinds", "structure", "the product industry")
spec(S("S/conditions/air/climate/hot"), "Hot climates are desert, equatorial, tropical, and Mediterranean classes.", "kinds", "structure", "the hot climate")
spec(S("S/conditions/air/climate/mild"), "Mild climates are temperate, oceanic, continental, and mountain classes.", "kinds", "structure", "the mild climate")
spec(S("S/conditions/air/climate/meta"), "Climate labels are the bare climate name, its factor, its type, and the global class.", "kinds", "structure", "the climate label")
spec(S("S/conditions/air/ozone/present"), "Ozone presence is ozone in the air and in the ozone layer.", "kinds", "structure", "the ozone presence")
spec(S("S/conditions/air/ozone/loss"), "Ozone loss is depletion, its potential, and the precursor.", "kinds", "structure", "the ozone loss")
spec(S("S/resources/energy/carrier"), "Energy carriers are energy, its source, and an energy resource.", "kinds", "structure", "the energy carrier")
spec(S("S/resources/energy/flow"), "Energy flows are wave, biomass, and primary energy.", "kinds", "structure", "the energy flow")
spec(S("S/resources/living/food"), "Food resources are grain, fishery, and living marine stocks.", "kinds", "structure", "the food resource")
spec(S("S/resources/living/stock"), "Living stocks are forest, genetic, and microbial resources.", "kinds", "structure", "the living stock")
spec(S("I/ecosystem/land"), "Land harm is degradation of soil, land, or a natural resource.", "kinds", "structure", "the land harm")
spec(S("I/ecosystem/system"), "System harm is degradation of an ecosystem, the environment, or freshwater, including a climate impact.", "kinds", "structure", "the system harm")
spec(S("I/health/harm"), "Health harms are effects on human health from an environmental exposure.", "kinds", "structure", "the health harm")
spec(S("R/regulation/waste-treatment"), "Waste treatment is the response that processes a solid or gaseous waste.", "kinds", "structure", "the waste treatment")
spec(S("R/regulation/control"), "Pollution control is the response that limits a stated load.", "kinds", "structure", "the control")
spec(S("R/regulation/management"), "Environmental management is the response that directs how a load is handled.", "kinds", "structure", "the management response")
spec(S("R/regulation/instrument"), "Environmental instruments are policies and laws whose effect on a load is measured here.", "kinds", "structure", "the instrument")
spec(S("R/engineering"), "Environmental engineering is the technical work that changes a pressure or a state.", "kinds", "structure", "the kind of work")
spec(S("R/engineering/convey"), "Water conveyance is the pumps, sluices, and aqueducts that move water.", "parts", "structure", "the part that moves water")
spec(S("R/engineering/supply"), "Water supply works are distribution systems and waterworks.", "kinds", "structure", "the supply work")
spec(S("R/engineering/sewage"), "Sewage works are farms, beds, sewers, and digesters that treat dirty water.", "kinds", "structure", "the sewage work")
spec(S("R/engineering/separation"), "Separation works are filtration and osmosis that pull a contaminant from water.", "kinds", "structure", "the separation work")
spec(S("R/engineering/land"), "Land water works are drainage and irrigation systems.", "kinds", "structure", "the land water work")

# Limits
spec(S("L/threshold"), "Thresholds are the critical values past which a system shifts.", "kinds", "structure", "the kind of threshold")
spec(S("L/standard"), "Standards are the agreed limits a measured state is held to.", "kinds", "structure", "the kind of standard")
spec(S("L/standard/concentration"), "Concentration limits are the highest amount of a substance a medium may hold.", "kinds", "degree", "from intake, to exposure, to a maximum", "The rank runs from an intake, to an exposure limit, to a maximum concentration.")
spec(S("L/standard/quality"), "Quality standards are agreed conditions for air, water, or emissions.", "kinds", "structure", "the quality standard")
spec(S("L/standard/norm"), "Environmental norms are stated criteria and norms for pollution.", "kinds", "structure", "the norm")
spec(S("L/capacity"), "Carrying capacity is the limit of what a system can sustain.", "kinds", "structure", "the kind of capacity")
spec(S("L/capacity/carry"), "Carrying capacities are the loads a land or ecological system can sustain.", "kinds", "structure", "the carrying capacity")
spec(S("L/capacity/bio"), "Biocapacity is the biological productive capacity, including assimilation of waste.", "kinds", "structure", "the biocapacity")

# Methods (not an object cell)
spec(S("M"), "Environmental methods are measurement, monitoring, and assessment of a state or a harm.", "kinds", "structure", "the kind of method")
spec(S("M/monitor"), "Monitoring is repeated measurement of an environmental state.", "parts", "structure", "the part of monitoring")
spec(S("M/monitor/practice"), "Monitoring practice is the act and technique of watching a state.", "kinds", "structure", "the monitoring practice")
spec(S("M/monitor/system"), "Monitoring systems are the networks and stations that watch a state.", "parts", "structure", "the part of the system")
spec(S("M/monitor/record"), "Monitoring records are the data and criteria a monitoring system keeps.", "kinds", "structure", "the monitoring record")
spec(S("M/measure"), "Measurement is the method that puts a number on a state.", "parts", "structure", "the part of measurement")
spec(S("M/measure/measuring"), "Measuring is the method, instrument, and programme that produce a number.", "parts", "structure", "the part of measuring")
spec(S("M/measure/sampling"), "Sampling is the taking of a portion so that a state can be measured.", "kinds", "structure", "the sampling method")
spec(S("M/measure/field"), "Field measures are hydrometry and sound measurement in place.", "kinds", "structure", "the field measure")
spec(S("M/assess"), "Assessment is the method that judges a state, a harm, or a risk.", "kinds", "structure", "the kind of assessment")
spec(S("M/assess/environment"), "Environmental assessment is the judgement of a state or of an impact.", "kinds", "structure", "the environmental assessment")
spec(S("M/assess/risk"), "Risk assessment is the judgement of the chance of an environmental harm.", "kinds", "structure", "the risk assessment")
spec(S("M/assess/audit"), "Environmental audit is a check of a stated environmental performance.", "kinds", "structure", "the audit")


FIX = {
    S("P/drivers/other"): "General industries are activities whose load is not one named stock.",
}
for path, statement in FIX.items():
    words = WORD.findall(statement)
    if not (statement.endswith(".") and statement.count(".") == 1 and VERBS.search(statement) and len(words) <= 25):
        raise SystemExit(statement)
    SPECS[path]["statement"] = statement

TRANSPORT = {"pollutant dispersion", "pollutant distribution", "pollutant migration", "pollutant mobilisation", "pollutant remobilisation"}
RETENTION = {"pollutant absorption", "pollutant accumulation", "pollutant deposition", "pollutant pathway"}
CHANGE_LOSS = {"pollutant degradation", "pollutant elimination", "pollutant reduction"}
CHANGE_SHIFT = {"pollutant formation", "pollutant evolution", "pollutant immobilisation", "pollutant behaviour"}
MEASURE = {"pollutant concentration", "pollutant level", "pollutant load", "pollutant immission"}
CHEM = {"organic pollutant", "inorganic pollutant", "halogenated pollutant", "persistant organic pollutant", "bioaccumulative pollutant"}
DEGRAD = {"biodegradable pollutant", "non-biodegradable pollutant", "biological pollutant", "chemical pollutant"}
MEDIUM_AIR = {"air pollutant", "gaseous air pollutant"}
MEDIUM_LAND = {"soil pollutant", "water pollutant", "urban pollutant", "food pollutant"}
MEDIUM_FORM = {"noise pollutant", "physical pollutant", "radioactive pollutant", "pollutant"}

HOUSE = {"domestic waste", "household waste", "consumer waste"}
MATERIAL = {"organic waste", "plastic waste", "radioactive waste", "degradable waste", "biologically degradable waste", "residual waste sludge", "pollution abatement waste"}
GAS = {"waste air", "waste gas", "waste heat", "waste air purification (gas)", "waste degasification"}
HANDLING = {"incineration of waste", "waste incineration", "waste recycling", "waste minimisation", "use of waste as energy source", "state of waste", "waste volume"}

SRC = {"emission source", "emission to air", "emission to water", "industrial emission", "traffic emission", "motor vehicle emission", "aircraft engine emission", "mine gas emission", "atmospheric emission", "carbon emission", "noise emission", "radioactive emission", "sound emission"}
REC = {"emission", "emission inventory", "emission factor", "emission levels", "emission estimation", "emission situation", "air pollutant emission inventory guidebook"}
RED = {"emission reduction", "emission reduction banking"}

MINING = {"coal mining", "deep sea mining", "lignite mining", "mining", "mining product", "mining waste", "offshore mining", "opencast mining", "rock salt mining", "sea bed mining", "strip mining"}
TAKING = {"aggregate extraction", "extraction", "gravel extraction", "groundwater extraction", "mineral extraction", "natural gas extraction", "oil extraction"}

FISH_ACT = {"fishing", "coastal fishing", "deep sea fishing", "drift net fishing", "open sea fishing"}
FISHERY = {"fishery", "commercial fishery", "inland fishery", "marine fishery"}
GEAR = {"fishing fleet", "fishing vessel", "fishing ground"}

FOOD_IND = {"beverage industry", "brewing industry", "dairy industry", "distilling industry", "food industry", "oil and fat industry"}
MAT_IND = {"cement industry", "coal industry", "glass industry", "iron and steel industry", "iron industry", "metal products industry", "metallurgical industry", "mineral industry", "mining industry", "non-ferrous metal industry", "steel industry"}
OTH_IND = {"extractive industry", "timber industry", "waste removal industry", "industry", "fishing industry"}

INTRO = {"genetically modified organism", "pest infestation", "organisms", "accidental release of organisms", "introduction of animal species", "introduction of plant species"}

CLIMATE = {"climate", "climate factor", "climate type", "continental climate", "desert climate", "equatorial climate", "global climate", "mediterranean climate", "mountain climate", "oceanic climate", "temperate climate", "tropical climate"}
CCL = {"climate change", "global temperature increase", "temperature change"}
OZONE = {"atmospheric ozone", "ground-level ozone", "ozone", "ozone depletion", "ozone depletion potential", "ozone layer", "ozone precursor", "tropospheric ozone"}
TEMP = {"air temperature", "temperature"}
LEVEL = {"background level", "noise level"}

FRESH = {"lake", "river bed", "lake basin", "international river basin", "river basin"}
URBAN = {"urban noise", "urban pollution", "urban traffic", "urban water supply"}
DEVELOP = {"coastal development", "river basin development"}
SEA_WATER = {"sea", "sea water", "open sea", "deep sea", "ocean"}
SEA_LEVEL = {"sea level", "rising sea level", "arctic sea ice loss"}
SEA_MOTION = {"sea circulation", "ocean circulation", "ocean current", "sea wave", "seismic sea wave"}
COAST = {"coastal area", "coastal environment", "coastal water", "coastal flooding", "intertidal zone"}
BED = {"sea bed", "deep sea deposit", "sea grass bed", "ocean temperature", "ocean acidification"}

FOREST = {"forest ecosystem", "tropical forest ecosystem", "woodland ecosystem"}
DRY = {"arid land ecosystem", "semi-arid land ecosystem"}
COLD = {"polar ecosystem", "arctic ecosystem", "antarctic ecosystem", "permafrost ecosystem"}
HIGH = {"mountain ecosystem", "highland ecosystem"}
AQUA = {"aquatic ecosystem", "marine ecosystem", "benthic ecosystem", "wetlands ecosystem", "estuarine ecosystem"}
ZONE = {"tropical ecosystem", "subtropical ecosystem", "temperate ecosystem", "terrestrial ecosystem"}
PLACE_ECO = {"urban ecosystem", "island ecosystem", "grassland ecosystem", "underground ecosystem"}
PROP_SERVICES = {"ecosystem services", "cultural ecosystem services"}
PROP_CONDITION = {"ecosystem vulnerability", "ecosystem stability", "ecosystem resilience"}
PROP_FORM = {"ecosystem type", "ecosystem boundary", "ecosystem interaction", "ecosystem process"}
PROP_STATUS = {"ecosystem", "internationally important ecosystem", "sensitive ecosystem"}

GROUND = {"earthquake", "seismic activity", "landslide", "avalanche", "geological disaster"}
VOLC = {"volcanic eruption", "volcanism"}
FLOOD = {"flood", "flooding", "flash flood", "flood hazard"}
STORM = {"storm", "thunderstorm", "tornado", "hail"}
CYCLONE = {"cyclone", "hurricane", "typhoon"}
EXTREME = {"drought", "heat wave", "cold"}
DISASTER = {"natural disaster", "hydrologic disaster", "meteorological disaster"}
CYCLES = {"biogeochemical cycle", "carbon cycle", "hydrologic cycle", "balance of matter", "biodegradation"}
NITRO = {"denitrification", "biological nitrogen fixation", "ammonification"}
EXCHANGE = {"evaporation", "evapotranspiration"}

RES_WATER = {"freshwater resource", "fluvial resource", "water resource"}
RES_LIVING = {"forest resource", "fishery resource", "living marine resource", "genetic resource", "microbial resource", "grain"}
RES_MIN = {"mineral resource", "mineral deposit"}
RES_EN = {"energy resource", "energy source", "primary energy", "biomass energy", "wave energy", "energy"}
RES_CLASS = {"renewable natural resource", "non-renewable natural resource", "renewable raw material"}

HARM = {"degradation of natural resources", "freshwater degradation", "ecosystem degradation", "degradation of the environment", "soil degradation", "land degradation"}
HEALTH = {"effect on health"}

RESTORE = {"environmental rehabilitation and restoration", "installation restoration", "land restoration"}
NATURE_AREA = {"landscape protection area", "site protection", "biotope protection", "marine conservation area", "estuarine conservation area"}
NATURE_SPECIES = {"animal protection", "protection of animals", "protection of species", "plant protection", "biodiversity protection"}
NATURE_LAND = {"landscape protection", "forest protection", "mountain protection", "protected marine zone"}
NATURE_GENERAL = {"conservation", "flexible approach to environmental protection", "landscape conservation policy", "nature conservation policy", "protection", "environmental protection"}
WATER_P = {"water protection area", "flood protection", "coast protection", "noise protection"}
INST_P = {"environmental protection agency", "environmental protection organisation", "environmental protection association", "environmental protection advice"}

WATER_T = {"urban waste water treatment", "water treatment", "sewage treatment system", "waste water treatment plant", "biological waste water treatment", "collective waste water treatment", "individual waste water treatment", "industrial waste water treatment", "on-site waste water treatment", "primary treatment", "secondary treatment", "tertiary treatment", "water purification. water treatment and conditioning. saline"}
WASTE_T = {"waste treatment plant", "waste treatment effluent", "waste gas treatment", "sludge treatment", "chemical treatment of waste", "treatment of gases", "biological treatment", "chemical treatment", "physicochemical treatment", "aerobic treatment", "anaerobic treatment", "treatment", "treatment residue"}
CONTROL = {"pollution control equipment", "pollution control measure", "pollution control technology", "drought control", "flood control", "control", "control measure", "regulatory control"}
MANAGE = {"river basin management", "dry manure management system", "risk management", "management", "good management"}
INSTR = {"legislation on pollution", "urban waste water treatment directive", "pollution control investment"}

CONVEY = {"aqueduct", "pump", "sluice", "sluice-gate"}
SUPPLY = {"water distribution system", "water distribution systems", "waterworks"}
SEWAGE = {"sewage farm", "bacterial bed", "rain water sewer system", "digester"}
SEPAR = {"reverse osmosis", "microfiltration"}
LANDW = {"drainage system", "irrigation system"}

THRESH = {"threshold value", "critical level", "critical load", "noel", "irreversibility of the phenomenon"}
CONC = {"acceptable daily intake", "permissible exposure limit", "maximum admissible concentration", "maximum immission concentration", "immission limit"}
QUAL = {"environmental quality standard", "quality standard", "emission standard", "environmental quality objective", "environmental quality criterion"}
NORM = {"limit value", "norm", "pollution norm", "pollution criterion", "environmental criterion"}
CARRY = {"carrying capacity", "ecological carrying capacity", "land carrying capacity", "ecological capacity"}
BIOCAP = {"biocapacity", "world biocapacity", "waste assimilation capacity"}

MON_P = {"monitoring", "environmental monitoring", "monitoring technique"}
MON_S = {"monitoring network", "monitoring station", "monitoring system"}
MON_R = {"monitoring data", "monitoring criterion"}
MEAS = {"measuring", "measuring instrument", "measuring method", "measuring programme"}
SAMP = {"sampling", "sampling technique"}
FIELD_M = {"hydrometry", "sound measurement"}
ASS_E = {"environmental assessment", "environmental impact assessment", "integrated environmental assessment", "indicator-based assessment", "urban environment assessment", "environmental assessment and monitoring"}
ASS_R = {"environmental risk assessment", "risk analysis", "natural risk analysis", "sustainability risk assessment", "risk assessment"}
AUD = {"environmental auditing", "environmental statement (eco-audit)"}

# Field routes. First match wins. Environmental groups are tested before this.
ROUTES = [
    (re.compile(r"\b(psycholog|ethic|perception|history|teaching|culture|terminology)\b", re.I), "MS", "a mind, culture, or teaching term is not an environmental state"),
    (re.compile(r"\b(economics|economic|cost|price|revenue|taxation|budget|credit|pay policy|accounting)\b", re.I), "EC", "a price, cost, or account is economics"),
    (re.compile(r"\b(legislation|directive|law|court|legal)\b", re.I), "LA", "a legal instrument is law"),
    (re.compile(r"\b(policy)\b", re.I), "PO", "a policy programme is politics"),
    (re.compile(r"geology|geomorpholog|geophysic|hydrolog|oceanograph|geograph|glaciolog|sedimentolog|mineralog|geodesy|palaeoclimat|atmospheric physics|atmospheric science|soil science|water science|tectonics|earth's crust", re.I), "EA", "an earth-system science is earth science"),
    (re.compile(r"\b(ecology|embryogenesis|pheromone|photosynthesis|leaf|seed \(biology\)|animal behaviour|animal nutrition)\b", re.I), "BI", "an organism process with no human load is biology"),
    (re.compile(r"\b(hydrolysis|oxidation|sorption|fermentation|distillation|chromatograph|ames test)\b", re.I), "CH", "a chemical reaction or lab method is chemistry"),
    (re.compile(r"\b(engineering|technology|machinery|equipment|refrigerat|vulcanisation|etching)\b", re.I), "EN", "a machine or general technology is engineering"),
    (re.compile(r"\b(gis|raster|informatics|data model)\b", re.I), "IS", "a data-model term is information science"),
    (re.compile(r"\b(health|disease|clinical|toxicolog|pharmaco)\b", re.I), "MD", "a clinical or toxicological term is medicine"),
    (re.compile(r"\b(farming|agricultur|crop|livestock|apiculture)\b", re.I), "AG", "a farming practice is agriculture"),
]


def norm(name):
    return (name or "").strip().lower()


EXACT = {}
for names, path in (
    (TRANSPORT, S("P/emissions/pollutant/movement/transport")),
    (RETENTION, S("P/emissions/pollutant/movement/retention")),
    (CHANGE_LOSS, S("P/emissions/pollutant/change/loss")),
    (CHANGE_SHIFT, S("P/emissions/pollutant/change/shift")),
    (MEASURE, S("P/emissions/pollutant/measure")),
    (CHEM, S("P/emissions/pollutant/class/chemistry")),
    (DEGRAD, S("P/emissions/pollutant/class/degradability")),
    (MEDIUM_AIR, S("P/emissions/pollutant/class/medium/air")),
    (MEDIUM_LAND, S("P/emissions/pollutant/class/medium/land")),
    (MEDIUM_FORM, S("P/emissions/pollutant/class/medium/form")),
    (HOUSE, S("P/emissions/waste/household")),
    (MATERIAL, S("P/emissions/waste/material")),
    (GAS, S("P/emissions/waste/gas")),
    (HANDLING, S("P/emissions/waste/handling")),
    (SRC, S("P/emissions/emission/source")),
    (REC, S("P/emissions/emission/record")),
    (RED, S("P/emissions/emission/reduction")),
    (MINING, S("P/extraction/mining")),
    (TAKING, S("P/extraction/taking")),
    (FISH_ACT, S("P/extraction/fishing/activity")),
    (FISHERY, S("P/extraction/fishing/fishery")),
    (GEAR, S("P/extraction/fishing/gear")),
    (FOOD_IND, S("P/drivers/food")),
    (MAT_IND, S("P/drivers/materials")),
    (OTH_IND, S("P/drivers/other")),
    (INTRO, S("P/introduced")),
    (CLIMATE, S("S/conditions/air/climate")),
    (CCL, S("S/conditions/air/climate-change")),
    (OZONE, S("S/conditions/air/ozone")),
    (TEMP, S("S/conditions/air/temperature")),
    (LEVEL, S("S/conditions/air/level")),
    (FRESH, S("S/conditions/fresh")),
    (URBAN, S("P/land/urban")),
    (DEVELOP, S("P/land/development")),
    (SEA_WATER, S("S/conditions/marine/water")),
    (SEA_LEVEL, S("S/conditions/marine/level")),
    (SEA_MOTION, S("S/conditions/marine/motion")),
    (COAST, S("S/conditions/marine/coast")),
    (BED, S("S/conditions/marine/bed")),
    (FOREST, S("S/conditions/biodiversity/cover/forest")),
    (DRY, S("S/conditions/biodiversity/cover/dry")),
    (COLD, S("S/conditions/biodiversity/setting/cold")),
    (HIGH, S("S/conditions/biodiversity/setting/high")),
    (AQUA, S("S/conditions/biodiversity/cover/water")),
    (ZONE, S("S/conditions/biodiversity/setting/zone")),
    (PLACE_ECO, S("S/conditions/biodiversity/setting/place")),
    (PROP_SERVICES, S("S/conditions/biodiversity/property/services")),
    (PROP_CONDITION, S("S/conditions/biodiversity/property/condition")),
    (PROP_FORM, S("S/conditions/biodiversity/property/form")),
    (PROP_STATUS, S("S/conditions/biodiversity/property/status")),
    (GROUND, S("S/hazards/ground")),
    (VOLC, S("S/hazards/volcanic")),
    (FLOOD, S("S/hazards/weather/flood")),
    (STORM, S("S/hazards/weather/storm")),
    (CYCLONE, S("S/hazards/weather/cyclone")),
    (EXTREME, S("S/hazards/weather/extreme")),
    (DISASTER, S("S/hazards/weather/disaster")),
    (CYCLES, S("S/hazards/process/cycles")),
    (NITRO, S("S/hazards/process/nitrogen")),
    (EXCHANGE, S("S/hazards/process/exchange")),
    (RES_WATER, S("S/resources/water")),
    (RES_LIVING, S("S/resources/living")),
    (RES_MIN, S("S/resources/mineral")),
    (RES_EN, S("S/resources/energy")),
    (RES_CLASS, S("S/resources/class")),
    (HARM, S("I/ecosystem")),
    (HEALTH, S("I/health")),
    (RESTORE, S("R/restoration")),
    (NATURE_AREA, S("R/conservation/nature/area")),
    (NATURE_SPECIES, S("R/conservation/nature/species")),
    (NATURE_LAND, S("R/conservation/nature/landscape")),
    (NATURE_GENERAL, S("R/conservation/nature/general")),
    (WATER_P, S("R/conservation/water")),
    (INST_P, S("R/conservation/institution")),
    (WATER_T, S("R/regulation/water-treatment")),
    (WASTE_T, S("R/regulation/waste-treatment")),
    (CONTROL, S("R/regulation/control")),
    (MANAGE, S("R/regulation/management")),
    (INSTR, S("R/regulation/instrument")),
    (CONVEY, S("R/engineering/convey")),
    (SUPPLY, S("R/engineering/supply")),
    (SEWAGE, S("R/engineering/sewage")),
    (SEPAR, S("R/engineering/separation")),
    (LANDW, S("R/engineering/land")),
    (THRESH, S("L/threshold")),
    (CONC, S("L/standard/concentration")),
    (QUAL, S("L/standard/quality")),
    (NORM, S("L/standard/norm")),
    (CARRY, S("L/capacity/carry")),
    (BIOCAP, S("L/capacity/bio")),
    (MON_P, S("M/monitor/practice")),
    (MON_S, S("M/monitor/system")),
    (MON_R, S("M/monitor/record")),
    (MEAS, S("M/measure/measuring")),
    (SAMP, S("M/measure/sampling")),
    (FIELD_M, S("M/measure/field")),
    (ASS_E, S("M/assess/environment")),
    (ASS_R, S("M/assess/risk")),
    (AUD, S("M/assess/audit")),
):
    for name in names:
        EXACT[name] = path

# Fertilisers and fuels by pattern, plus a few singles.
for name in ("chemical fertiliser", "inorganic fertiliser", "nitrogenous fertiliser", "phosphatic fertiliser", "potassium fertiliser"):
    EXACT[name] = S("P/emissions/fertiliser")
for name in ("alternative fuel", "diesel fuel", "domestic fuel", "fossil fuel", "fossil fuel consumption", "fuel consumption", "non-polluting fuel", "nuclear fuel"):
    EXACT[name] = S("P/emissions/fuel")

DEEPER = {
    "fossil fuel": S("P/emissions/fuel/fossil"),
    "fossil fuel consumption": S("P/emissions/fuel/fossil"),
    "diesel fuel": S("P/emissions/fuel/fossil"),
    "domestic fuel": S("P/emissions/fuel/fossil"),
    "alternative fuel": S("P/emissions/fuel/other"),
    "nuclear fuel": S("P/emissions/fuel/other"),
    "non-polluting fuel": S("P/emissions/fuel/other"),
    "fuel consumption": S("P/emissions/fuel/other"),
    "emission inventory": S("P/emissions/emission/record/inventory"),
    "air pollutant emission inventory guidebook": S("P/emissions/emission/record/inventory"),
    "emission factor": S("P/emissions/emission/record/inventory"),
    "emission estimation": S("P/emissions/emission/record/inventory"),
    "emission": S("P/emissions/emission/record/state"),
    "emission levels": S("P/emissions/emission/record/state"),
    "emission situation": S("P/emissions/emission/record/state"),
    "emission to air": S("P/emissions/emission/source/air"),
    "atmospheric emission": S("P/emissions/emission/source/air"),
    "carbon emission": S("P/emissions/emission/source/air"),
    "noise emission": S("P/emissions/emission/source/air"),
    "sound emission": S("P/emissions/emission/source/air"),
    "industrial emission": S("P/emissions/emission/source/activity"),
    "traffic emission": S("P/emissions/emission/source/activity"),
    "motor vehicle emission": S("P/emissions/emission/source/activity"),
    "aircraft engine emission": S("P/emissions/emission/source/activity"),
    "mine gas emission": S("P/emissions/emission/source/activity"),
    "emission source": S("P/emissions/emission/source/listed"),
    "emission to water": S("P/emissions/emission/source/listed"),
    "radioactive emission": S("P/emissions/emission/source/listed"),
    "incineration of waste": S("P/emissions/waste/handling/burn"),
    "waste incineration": S("P/emissions/waste/handling/burn"),
    "waste minimisation": S("P/emissions/waste/handling/reduce"),
    "waste recycling": S("P/emissions/waste/handling/reduce"),
    "use of waste as energy source": S("P/emissions/waste/handling/reduce"),
    "state of waste": S("P/emissions/waste/handling/record"),
    "waste volume": S("P/emissions/waste/handling/record"),
    "organic waste": S("P/emissions/waste/material/organic"),
    "plastic waste": S("P/emissions/waste/material/organic"),
    "degradable waste": S("P/emissions/waste/material/organic"),
    "biologically degradable waste": S("P/emissions/waste/material/organic"),
    "radioactive waste": S("P/emissions/waste/material/hazard"),
    "residual waste sludge": S("P/emissions/waste/material/hazard"),
    "pollution abatement waste": S("P/emissions/waste/material/hazard"),
    "coal mining": S("P/extraction/mining/rock"),
    "lignite mining": S("P/extraction/mining/rock"),
    "rock salt mining": S("P/extraction/mining/rock"),
    "deep sea mining": S("P/extraction/mining/sea"),
    "offshore mining": S("P/extraction/mining/sea"),
    "sea bed mining": S("P/extraction/mining/sea"),
    "opencast mining": S("P/extraction/mining/surface"),
    "strip mining": S("P/extraction/mining/surface"),
    "mining": S("P/extraction/mining/surface"),
    "mining product": S("P/extraction/mining/output"),
    "mining waste": S("P/extraction/mining/output"),
    "aggregate extraction": S("P/extraction/taking/mineral"),
    "gravel extraction": S("P/extraction/taking/mineral"),
    "mineral extraction": S("P/extraction/taking/mineral"),
    "extraction": S("P/extraction/taking/mineral"),
    "natural gas extraction": S("P/extraction/taking/fluid"),
    "oil extraction": S("P/extraction/taking/fluid"),
    "groundwater extraction": S("P/extraction/taking/fluid"),
    "accidental release of organisms": S("P/introduced/release"),
    "introduction of animal species": S("P/introduced/release"),
    "introduction of plant species": S("P/introduced/release"),
    "genetically modified organism": S("P/introduced/organism"),
    "pest infestation": S("P/introduced/organism"),
    "organisms": S("P/introduced/organism"),
    "beverage industry": S("P/drivers/food/drink"),
    "brewing industry": S("P/drivers/food/drink"),
    "distilling industry": S("P/drivers/food/drink"),
    "dairy industry": S("P/drivers/food/food"),
    "food industry": S("P/drivers/food/food"),
    "oil and fat industry": S("P/drivers/food/food"),
    "iron industry": S("P/drivers/materials/metal"),
    "steel industry": S("P/drivers/materials/metal"),
    "iron and steel industry": S("P/drivers/materials/metal"),
    "non-ferrous metal industry": S("P/drivers/materials/metal"),
    "cement industry": S("P/drivers/materials/mineral"),
    "glass industry": S("P/drivers/materials/mineral"),
    "coal industry": S("P/drivers/materials/mineral"),
    "mineral industry": S("P/drivers/materials/mineral"),
    "mining industry": S("P/drivers/materials/mineral"),
    "metal products industry": S("P/drivers/materials/products"),
    "metallurgical industry": S("P/drivers/materials/products"),
    "desert climate": S("S/conditions/air/climate/hot"),
    "equatorial climate": S("S/conditions/air/climate/hot"),
    "tropical climate": S("S/conditions/air/climate/hot"),
    "mediterranean climate": S("S/conditions/air/climate/hot"),
    "temperate climate": S("S/conditions/air/climate/mild"),
    "oceanic climate": S("S/conditions/air/climate/mild"),
    "continental climate": S("S/conditions/air/climate/mild"),
    "mountain climate": S("S/conditions/air/climate/mild"),
    "climate": S("S/conditions/air/climate/meta"),
    "climate factor": S("S/conditions/air/climate/meta"),
    "climate type": S("S/conditions/air/climate/meta"),
    "global climate": S("S/conditions/air/climate/meta"),
    "ozone": S("S/conditions/air/ozone/present"),
    "atmospheric ozone": S("S/conditions/air/ozone/present"),
    "ground-level ozone": S("S/conditions/air/ozone/present"),
    "tropospheric ozone": S("S/conditions/air/ozone/present"),
    "ozone layer": S("S/conditions/air/ozone/present"),
    "ozone depletion": S("S/conditions/air/ozone/loss"),
    "ozone depletion potential": S("S/conditions/air/ozone/loss"),
    "ozone precursor": S("S/conditions/air/ozone/loss"),
    "energy": S("S/resources/energy/carrier"),
    "energy source": S("S/resources/energy/carrier"),
    "energy resource": S("S/resources/energy/carrier"),
    "wave energy": S("S/resources/energy/flow"),
    "biomass energy": S("S/resources/energy/flow"),
    "primary energy": S("S/resources/energy/flow"),
    "grain": S("S/resources/living/food"),
    "fishery resource": S("S/resources/living/food"),
    "living marine resource": S("S/resources/living/food"),
    "forest resource": S("S/resources/living/stock"),
    "genetic resource": S("S/resources/living/stock"),
    "microbial resource": S("S/resources/living/stock"),
    "soil degradation": S("I/ecosystem/land"),
    "land degradation": S("I/ecosystem/land"),
    "degradation of natural resources": S("I/ecosystem/land"),
    "freshwater degradation": S("I/ecosystem/system"),
    "ecosystem degradation": S("I/ecosystem/system"),
    "degradation of the environment": S("I/ecosystem/system"),
    "climate change impact": S("I/ecosystem/system"),
    "effect on health": S("I/health"),
    "health effect of noise": S("I/health"),
    "environmental health": S("I/health"),
    "human health": S("I/health"),
    "environmental health hazard": S("I/health"),
    "pollution control equipment": S("R/regulation/control/pollution"),
    "pollution control measure": S("R/regulation/control/pollution"),
    "pollution control technology": S("R/regulation/control/pollution"),
    "drought control": S("R/regulation/control/hazard"),
    "flood control": S("R/regulation/control/hazard"),
    "control": S("R/regulation/control/general"),
    "control measure": S("R/regulation/control/general"),
    "regulatory control": S("R/regulation/control/general"),
    "climate change adaptation": S("R/regulation/management/climate"),
    "climate change mitigation": S("R/regulation/management/climate"),
    "dry manure management system": S("R/regulation/management/place"),
    "river basin management": S("R/regulation/management/place"),
    "fisheries management": S("R/regulation/management/place"),
    "management": S("R/regulation/management/general"),
    "good management": S("R/regulation/management/general"),
    "risk management": S("R/regulation/management/general"),
    "primary treatment": S("R/regulation/water-treatment/stage"),
    "secondary treatment": S("R/regulation/water-treatment/stage"),
    "tertiary treatment": S("R/regulation/water-treatment/stage"),
    "sewage treatment system": S("R/regulation/water-treatment/plant"),
    "urban waste water treatment": S("R/regulation/water-treatment/plant"),
    "waste water treatment plant": S("R/regulation/water-treatment/plant"),
    "water treatment": S("R/regulation/water-treatment/plant"),
    "water purification. water treatment and conditioning. saline": S("R/regulation/water-treatment/plant"),
    "biological waste water treatment": S("R/regulation/water-treatment/mode"),
    "collective waste water treatment": S("R/regulation/water-treatment/mode"),
    "individual waste water treatment": S("R/regulation/water-treatment/mode"),
    "industrial waste water treatment": S("R/regulation/water-treatment/mode"),
    "on-site waste water treatment": S("R/regulation/water-treatment/mode"),
    "biological treatment": S("R/regulation/waste-treatment/process"),
    "chemical treatment": S("R/regulation/waste-treatment/process"),
    "physicochemical treatment": S("R/regulation/waste-treatment/process"),
    "aerobic treatment": S("R/regulation/waste-treatment/process"),
    "anaerobic treatment": S("R/regulation/waste-treatment/process"),
    "waste gas treatment": S("R/regulation/waste-treatment/plant"),
    "sludge treatment": S("R/regulation/waste-treatment/plant"),
    "chemical treatment of waste": S("R/regulation/waste-treatment/plant"),
    "waste treatment plant": S("R/regulation/waste-treatment/plant"),
    "waste treatment effluent": S("R/regulation/waste-treatment/plant"),
    "treatment": S("R/regulation/waste-treatment/general"),
    "treatment residue": S("R/regulation/waste-treatment/general"),
    "treatment of gases": S("R/regulation/waste-treatment/general"),
}
for name, path in DEEPER.items():
    EXACT[name] = path

MORE = {
    "pollutant emission": S("P/emissions/pollutant/measure"),
    "waste gas dispersion": S("P/emissions/waste/gas-fate"),
    "waste gas emission": S("P/emissions/waste/gas-fate"),
    "waste gas reduction": S("P/emissions/waste/gas-fate"),
    "waste heat charge": S("P/emissions/waste/gas-fate"),
    "waste heat utilisation": S("P/emissions/waste/gas-fate"),
    "emissions": S("P/emissions/emission/record/state"),
    "peat extraction": S("P/extraction/taking/land"),
    "sand extraction": S("P/extraction/taking/land"),
    "water extraction": S("P/extraction/taking/land"),
    "climate protection": S("R/regulation/management/climate"),
    "climate regulation": S("R/regulation/management/climate"),
    "air quality management": S("R/regulation/management/climate"),
    "groundwater protection": S("R/conservation/water/catchment"),
    "sea water protection": S("R/conservation/water/catchment"),
    "water catchment protection": S("R/conservation/water/catchment"),
    "water protection area": S("R/conservation/water/area"),
    "flood protection": S("R/conservation/water/area"),
    "coast protection": S("R/conservation/water/area"),
    "noise protection": S("R/conservation/water/area"),
    "avalanche protection": S("R/conservation/nature/landscape"),
    "municipal water management": S("R/regulation/management/water"),
    "surface water management": S("R/regulation/management/water"),
    "water quality management": S("R/regulation/management/water"),
    "water quantity management": S("R/regulation/management/water"),
    "river basin management": S("R/regulation/management/water"),
    "forest management": S("R/regulation/management/habitat"),
    "landscape management": S("R/regulation/management/habitat"),
    "ecosystem management": S("R/regulation/management/habitat"),
    "wildlife and habitat management": S("R/regulation/management/habitat"),
    "mountain management": S("R/regulation/management/habitat"),
    "natural resource management": S("R/regulation/management/stock"),
    "resources management": S("R/regulation/management/stock"),
    "land management and planning": S("R/regulation/management/stock"),
    "fisheries management": S("R/regulation/management/stock"),
    "animal waste management": S("R/regulation/management/waste/manure"),
    "animal waste management systems": S("R/regulation/management/waste/manure"),
    "manure management system": S("R/regulation/management/waste/manure"),
    "liquid manure management system": S("R/regulation/management/waste/manure"),
    "waste management system": S("R/regulation/management/waste/system"),
    "dual waste management": S("R/regulation/management/waste/system"),
    "radioactive waste management": S("R/regulation/management/waste/system"),
    "thermal treatment": S("R/regulation/waste-treatment/special"),
    "surface treatment": S("R/regulation/waste-treatment/special"),
    "phytosanitary treatment": S("R/regulation/waste-treatment/special"),
    "desertification control": S("R/regulation/control/hazard"),
    "erosion control": S("R/regulation/control/hazard"),
    "emission control": S("R/regulation/control/pollution"),
    "immission control": S("R/regulation/control/pollution"),
    "mitigation measure": S("R/regulation/measures"),
    "prevention measure": S("R/regulation/measures"),
    "protective measure": S("R/regulation/measures"),
}
for name, path in MORE.items():
    EXACT[name] = path

ROUTE_EXACT = {
    "soil sciences": ("EA", "soil science as a discipline is earth science"),
    "soil science": ("EA", "soil science as a discipline is earth science"),
    "climate change adaptation": ("R/regulation/management", None),  # filled below as path
    "climate change mitigation": ("R/regulation/management", None),
    "climate change impact": ("I/ecosystem", None),
    "fishery economics": ("EC", "fishery economics is economics"),
    "fishing revenue": ("EC", "fishing revenue is economics"),
    "fishery policy": ("PO", "fishery policy is politics"),
    "fisheries management": ("R/regulation/management", None),
    "birth control": ("MD", "birth control is medicine"),
    "data protection": ("IS", "data protection is information"),
    "social protection": ("MS", "social protection is a social condition"),
    "fire protection": ("EN", "fire protection is a technical safety practice"),
    "health protection": ("MD", "health protection is medicine"),
    "crop protection": ("AG", "crop protection is agriculture"),
    "plant protection product": ("AG", "a plant protection product is agriculture"),
    "testing of plant protection products": ("AG", "testing a plant protection product is agriculture"),
    "radiation protection law": ("LA", "a protection law is law"),
    "water protection directive": ("LA", "a protection directive is law"),
    "ec directive on water protection": ("LA", "a protection directive is law"),
    "environmental protection order": ("LA", "a protection order is law"),
    "environmental protection regulation": ("LA", "a protection regulation is law"),
    "eu green bond standard": ("EC", "a green bond standard is finance"),
    "barents sea": ("EA", "a named sea is a place in earth science"),
    "black sea": ("EA", "a named sea is a place in earth science"),
    "caspian sea": ("EA", "a named sea is a place in earth science"),
    "mediterranean sea": ("EA", "a named sea is a place in earth science"),
    "wadden sea": ("EA", "a named sea is a place in earth science"),
    "antarctic ocean": ("EA", "a named ocean is a place in earth science"),
    "arctic ocean": ("EA", "a named ocean is a place in earth science"),
    "indian ocean": ("EA", "a named ocean is a place in earth science"),
    "north atlantic ocean": ("EA", "a named ocean is a place in earth science"),
    "north pacific ocean": ("EA", "a named ocean is a place in earth science"),
    "south atlantic ocean": ("EA", "a named ocean is a place in earth science"),
    "south pacific ocean": ("EA", "a named ocean is a place in earth science"),
    "health": ("MD", "health as such is medicine"),
    "risk": ("EV", "risk as a bare word is too broad for a limit"),
    "measure": ("EV", "measure as a bare word is too broad for a limit"),
    "responses": ("EV", "a bare responses label is the cell, not a member"),
    "legislation": ("LA", "legislation as such is law"),
    "policy": ("PO", "policy as such is politics"),
    "soil process": ("S/conditions/soil", None),
    "soil": ("S/conditions/soil", None),
    "estuarine conservation area": ("R/conservation/nature", None),
    "marine conservation area": ("R/conservation/nature", None),
    "protected marine zone": ("R/conservation/nature", None),
    "ocean outfall": ("R/engineering/sewage", None),
    "coastal development": ("P/land", None),
    "river basin development": ("P/land", None),
    "environmental protection cost": ("EC", "a protection cost is economics"),
    "environmental protection technology": ("R/engineering/separation", None),
    "integrated environmental protection technology": ("R/engineering/separation", None),
    "respiratory protection apparatus": ("MD", "respiratory protection apparatus is medicine"),
    "radiation protection": ("MD", "radiation protection of a person is medicine"),
    "civilian protection": ("MS", "civilian protection is a social condition"),
    "property protection": ("LA", "property protection is law"),
    "protection from neighbours": ("LA", "protection from neighbours is law"),
    "environmental protection in the enterprise": ("BU", "protection inside a firm is business"),
}

for name, field, reason in (
    ("hearing protection", "MD", "hearing protection is medicine"),
    ("biological pest control", "AG", "pest control on a crop is agriculture"),
    ("chemical pest control", "AG", "pest control on a crop is agriculture"),
    ("integrated pest control", "AG", "pest control on a crop is agriculture"),
    ("weed control", "AG", "weed control is agriculture"),
    ("disaster control service", "PO", "a control service is a public body"),
    ("state control", "PO", "state control is politics"),
    ("traffic control", "EN", "traffic control is engineering"),
    ("financial management", "EC", "financial management is economics"),
    ("stock management", "BU", "stock management is business"),
    ("chain management", "BU", "chain management is business"),
    ("patrimonial management", "EC", "patrimonial management is economics"),
    ("touristic activity management", "BU", "tourism management is business"),
    ("human settlement management", "MS", "settlement management is a social condition"),
    ("delegated management", "PO", "delegated management is politics"),
    ("crisis management", "PO", "crisis management is politics"),
    ("agricultural management", "AG", "agricultural management is agriculture"),
    ("life-cycle management", "BU", "life-cycle management of a product is business"),
    ("energy management", "EN", "energy management is engineering"),
    ("multiple use management area", "EV", "a multiple-use label is too broad for one group"),
):
    ROUTE_EXACT[name] = (field, reason)

for name in (
    "environmentally friendly management",
    "ecosystem-based management",
    "sustainable management",
    "integrated management",
    "environmental management system",
    "good management",
    "management",
    "dry manure management system",
    "risk management",
    "legislation on pollution",
    "urban waste water treatment directive",
    "pollution control investment",
):
    EXACT.pop(name, None)
    if name == "dry manure management system":
        EXACT[name] = S("R/regulation/management/waste/manure")
    elif name == "legislation on pollution":
        ROUTE_EXACT[name] = ("LA", "a pollution law is law")
    elif name == "urban waste water treatment directive":
        ROUTE_EXACT[name] = ("LA", "a treatment directive is law")
    elif name == "pollution control investment":
        ROUTE_EXACT[name] = ("EC", "a control investment is economics")
    elif name == "risk management":
        ROUTE_EXACT[name] = ("EV", "risk management as a bare label is too broad for a group")
    else:
        ROUTE_EXACT[name] = ("EV", "a bare management label is too broad for a group")


def _nest_geological(path):
    if len(path) >= 3 and path[0] == "S" and path[1] == "hazards" and path[2] in ("ground", "volcanic"):
        return ("S", "hazards", "geological") + path[2:]
    return path


EXACT = {name: _nest_geological(path) for name, path in EXACT.items()}
SPECS = {_nest_geological(path): meta for path, meta in SPECS.items()}


def field_of(name):
    """A field code for a topic that is not an environmental group member."""
    key = norm(name)
    if key in EXACT:
        return "EV"
    hit = ROUTE_EXACT.get(key)
    if hit and hit[0] in ("MA", "PH", "CH", "BI", "EA", "MD", "EN", "CS", "MS", "EC", "BU", "ST", "PO", "LA", "PL", "HI", "LN", "AR", "RE", "ED", "DE", "AG", "EV", "IS", "IK"):
        if hit[1]:
            return hit[0]
    for pattern, code, _reason in ROUTES:
        if pattern.search(name or ""):
            return code
    return ""


def destination(name):
    key = norm(name)
    if key in EXACT:
        return ("group", EXACT[key])
    hit = ROUTE_EXACT.get(key)
    if hit:
        if hit[1] is None and isinstance(hit[0], str) and hit[0][:1] in "PSRILM" and "/" in hit[0]:
            return ("group", S(hit[0]))
        if hit[1] is None and hit[0].startswith(("P/", "S/", "I/", "R/", "L/", "M/")):
            return ("group", S(hit[0]))
        if hit[1]:
            return ("route", hit[0], hit[1])
        if hit[0] in ("EV",):
            return ("route", "EV", hit[1] or "too broad to place")
    # loose process and engineering names fall through to field routes
    for pattern, code, reason in ROUTES:
        if pattern.search(name or ""):
            return ("route", code, reason)
    return ("miss", key)


def walk_leaves(points):
    for point in points:
        anchor = str(point.get("anchor") or "")
        if anchor.startswith("node:"):
            yield point
        yield from walk_leaves((point.get("support") or {}).get("points") or [])


def _clean_leaf_name(name):
    text = (name or "").replace(".", " ").replace("–", " ").replace("—", " ")
    return re.sub(r"\s+", " ", text).strip(" ,;/-")


def sentence_for_leaf(name, path):
    noun = {
        "P": "pressure",
        "S": "state",
        "I": "impact",
        "R": "response",
        "L": "limit",
        "M": "method",
    }[path[0]]
    text = _clean_leaf_name(name)
    statement = f"{text[:1].upper() + text[1:]} is recorded as a {noun}." if text else f"This item is recorded as a {noun}."
    words = statement.split()
    while len(WORD.findall(statement)) > 25 and words:
        words = words[:-1]
        statement = " ".join(words).rstrip(".") + "."
        if " is recorded as a " not in statement.lower():
            break
    if not VERBS.search(statement):
        statement = f"This item is recorded as a {noun}."
    return statement


ANCHORS = {
    ("P", "emissions"): "facet:EV.O.A1:emissions",
    ("P", "land"): "facet:EV.O.A1:land",
    ("P", "extraction"): "facet:EV.O.A1:extraction",
    ("P", "introduced"): "facet:EV.O.A1:introduced",
    ("S", "conditions"): "facet:EV.O.A2:conditions",
    ("S", "conditions", "air"): "facet:EV.O.A2:air",
    ("S", "conditions", "fresh"): "facet:EV.O.A2:freshwater",
    ("S", "conditions", "marine"): "facet:EV.O.A2:marine",
    ("S", "conditions", "soil"): "facet:EV.O.A2:soil",
    ("S", "conditions", "biodiversity"): "facet:EV.O.A2:biodiversity",
    ("S", "hazards"): "facet:EV.O.A2:natural",
    ("S", "hazards", "geological"): "facet:EV.O.A2:geological",
    ("S", "hazards", "weather"): "facet:EV.O.A2:hydrometeorological",
    ("S", "hazards", "process"): "facet:EV.O.A2:biogeochemical",
    ("S", "resources"): "facet:EV.O.A2:resources",
    ("I", "ecosystem"): "facet:EV.O.A3:ecosystem",
    ("I", "health"): "facet:EV.O.A3:health",
    ("R", "restoration"): "facet:EV.O.A4:restoration",
    ("R", "conservation"): "facet:EV.O.A4:conservation",
    ("R", "regulation"): "facet:EV.O.A4:regulation",
    ("R", "engineering"): "facet:EV.O.A4:engineering",
    ("L", "threshold"): "facet:EV.O.A5:threshold",
    ("L", "standard"): "facet:EV.O.A5:standard",
    ("L", "capacity"): "facet:EV.O.A5:capacity",
}
SPEC_ORDER = {path: index for index, path in enumerate(SPECS)}
# Ground, then weather, then the processes that set a state.
SPEC_ORDER[("S", "hazards", "geological")] = -3
SPEC_ORDER[("S", "hazards", "weather")] = -2
SPEC_ORDER[("S", "hazards", "process")] = -1
LEAF_RANK = {
    S("S/hazards/weather/extreme"): ["drought", "heat wave", "cold"],
    S("L/standard/concentration"): [
        "acceptable daily intake",
        "permissible exposure limit",
        "maximum admissible concentration",
        "maximum immission concentration",
        "immission limit",
    ],
}


def anchor_for(path):
    return ANCHORS.get(path, "group:" + "/".join(path))


def group_node(path, child_points, ids, parent_id):
    meta = SPECS[path]
    anchor = anchor_for(path)
    # Keep a facet anchor where the group replaces an existing facet.
    pid = ids.get(parent_id, anchor)
    sources = []
    seen = set()
    for point in child_points:
        for src in point.get("sources") or []:
            key = (src.get("file"), src.get("id"))
            if key in seen:
                continue
            seen.add(key)
            sources.append(src)
        if len(sources) >= 8:
            break
    if not sources:
        raise SystemExit(f"no sources for {path}")
    node = {
        "id": pid,
        "anchor": anchor,
        "statement": meta["statement"],
        "idea_type": "situation",
        "sources": sources[:8],
        "question_raised": "which_ones",
        "support": {
            "logic_type": "inductive",
            "plural_noun": "members",
            "mece_dimension": meta["dimension"],
            "basis": meta["basis"],
            "order": meta["order"],
            "question_raised": "which_ones",
            "points": child_points,
        },
    }
    if meta.get("rank_note"):
        node["support"]["rank_note"] = meta["rank_note"]
    return node


def leaf_node(item, ids, parent_id):
    anchor = item["anchor"]
    pid = ids.get(parent_id, anchor)
    point = {
        "id": pid,
        "anchor": anchor,
        "statement": item["statement"],
        "idea_type": "situation",
        "sources": item["sources"],
        "name": item["name"],
        "cell": item["cell"],
    }
    return point


CELL = {"P": "EV.O.A1", "S": "EV.O.A2", "I": "EV.O.A3", "R": "EV.O.A4", "L": "EV.O.A5", "M": "EV.M"}


def build_level(path, buckets, ids, parent_id):
    """Return points for the children of path."""
    child_paths = sorted(
        {key[: len(path) + 1] for key in buckets if len(key) > len(path) and key[: len(path)] == path},
        key=lambda item: SPEC_ORDER.get(item, 10**6),
    )
    leaves = buckets.get(path, [])
    points = []
    if child_paths and leaves:
        raise SystemExit(f"mixed leaves and groups at {path}: {len(leaves)} leaves")
    if leaves:
        if not 2 <= len(leaves) <= 5:
            raise SystemExit(f"leaf group {path} has {len(leaves)}: {[i['name'] for i in leaves]}")
        rank = LEAF_RANK.get(path) or []
        rank_index = {name: index for index, name in enumerate(rank)}

        def leaf_key(item):
            return (rank_index.get(item["name"].lower(), 10**6), item["name"].lower())

        for item in sorted(leaves, key=leaf_key):
            points.append(leaf_node(item, ids, parent_id))
        return points
    nodes = []
    for child in child_paths:
        wrapper_id = ids.get(parent_id, anchor_for(child))
        grandchildren = build_level(child, buckets, ids, wrapper_id)
        if not grandchildren:
            ids.abandon(anchor_for(child))
            continue
        if not 2 <= len(grandchildren) <= 5:
            raise SystemExit(f"group {child} has {len(grandchildren)}")
        node = group_node(child, grandchildren, ids, parent_id)
        # group_node calls get again and must return the same id
        if node["id"] != wrapper_id:
            raise SystemExit(f"id mismatch {node['id']} {wrapper_id}")
        nodes.append(node)
    if nodes and not 2 <= len(nodes) <= 5:
        raise SystemExit(f"parent {path} has {len(nodes)} groups")
    return nodes


def main():
    pyramid = json.loads((ROOT / "pyramids" / "EV.json").read_text(encoding="utf-8"))
    before = minto_counts(pyramid)
    print("BEFORE", json.dumps(before))
    queue = json.loads((ROOT / "pyramids" / "queues" / "EV.json").read_text(encoding="utf-8"))
    gemet = json.loads((ROOT / "maps" / "EV" / "gemet.json").read_text(encoding="utf-8"))
    gemet_ids = {node["id"]: node for node in gemet["nodes"]}
    rows = []
    for line in (ROOT / "pyramids" / "queues" / "EV.placed.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    by_node = {}
    for row in rows:
        if (row.get("task") or "place") == "place":
            by_node[row.get("node_id")] = row

    items = []
    routed = []
    missed = []

    def add_item(name, node_id, sources, statement=None):
        dest = destination(name)
        if dest[0] == "route":
            routed.append({"node_id": node_id, "name": name, "field": dest[1], "reason": dest[2]})
            return
        if dest[0] != "group":
            missed.append(name)
            routed.append({"node_id": node_id, "name": name, "field": field_of(name) or "EV", "reason": "no named group yet"})
            return
        path = dest[1]
        if path not in SPECS:
            raise SystemExit(f"missing spec {path} for {name}")
        cell = CELL[path[0]]
        items.append({
            "name": name,
            "anchor": f"node:{node_id}",
            "sources": sources,
            "statement": statement or sentence_for_leaf(name, path),
            "cell": cell,
            "path": path,
            "node_id": node_id,
        })

    for point in walk_leaves(pyramid["key_line"]["points"]):
        add_item(point.get("name") or "", point["anchor"][5:], point.get("sources") or [], point.get("statement"))

    loose_ids = {
        row["node_id"]
        for row in by_node.values()
        if row.get("status") == "placed" and str(row.get("group_id") or "").count(".") == 4
    }
    # Limits and resources that the groups need, even when the row is not in the 281.
    extra_names = set(THRESH) | set(CONC) | set(QUAL) | set(NORM) | set(CARRY) | set(BIOCAP)
    extra_names |= set(RES_WATER) | set(RES_LIVING) | set(RES_MIN) | set(RES_EN) | set(RES_CLASS)
    extra_names |= {"effect on health", "health effect of noise", "environmental health", "human health", "environmental health hazard"}
    have = {item["node_id"] for item in items}
    for row in by_node.values():
        if row.get("node_id") in have:
            continue
        name = row.get("name") or ""
        take = row.get("node_id") in loose_ids or norm(name) in extra_names
        if not take:
            continue
        if destination(name)[0] != "group":
            if row.get("node_id") in loose_ids:
                dest = destination(name)
                if dest[0] == "route":
                    routed.append({"node_id": row["node_id"], "name": name, "field": dest[1], "reason": dest[2]})
                else:
                    missed.append(name)
            continue
        node = gemet_ids.get(row["node_id"])
        if not node:
            routed.append({"node_id": row["node_id"], "name": name, "field": field_of(name) or "EV", "reason": "no GEMET source"})
            continue
        sources = [{"scheme": "GEMET", "id": node["id"], "code": node.get("code") or node["id"].split(":")[-1], "file": "maps/EV/gemet.json"}]
        add_item(name, row["node_id"], sources)

    tree_anchors = {point["anchor"] for point in walk_leaves(pyramid["key_line"]["points"])}
    tree_miss = [item for item in routed if item.get("reason") == "no named group yet" and f"node:{item['node_id']}" in tree_anchors]
    print("tree misses", len(tree_miss), "loose routed", len(routed))
    for item in tree_miss:
        print("  TREE", item["name"])
    buckets = defaultdict(list)
    for item in items:
        buckets[item["path"]].append(item)
    # A repeated label past five members is the same concept, not a new kind.
    for path, group in list(buckets.items()):
        if len(group) <= 5:
            continue
        kept = []
        seen = {}
        for item in group:
            seen[item["name"].lower()] = seen.get(item["name"].lower(), 0) + 1
            if seen[item["name"].lower()] > 1 and len(kept) >= 5:
                routed.append({"node_id": item["node_id"], "name": item["name"], "field": "EV", "reason": "duplicate label of a member already in the group"})
                continue
            kept.append(item)
        buckets[path] = kept[:5] if len(kept) > 5 and len({i["name"].lower() for i in kept}) < len(kept) else kept
        if len(buckets[path]) > 5:
            # drop pure duplicates first
            uniq = []
            names = set()
            for item in buckets[path]:
                key = item["name"].lower()
                if key in names:
                    routed.append({"node_id": item["node_id"], "name": item["name"], "field": "EV", "reason": "duplicate label of a member already in the group"})
                    continue
                names.add(key)
                uniq.append(item)
            buckets[path] = uniq
    # Report sizes
    bad = []
    for path, group in sorted(buckets.items(), key=lambda kv: "/".join(kv[0])):
        kids = [key for key in buckets if len(key) == len(path) + 1 and key[: len(path)] == path]
        if kids and group:
            bad.append(("mixed", path, len(group)))
        if not kids and not 2 <= len(group) <= 5:
            bad.append(("size", path, len(group), [i["name"] for i in group]))
    # parents that exist only as prefixes
    parents = {path[:-1] for path in buckets}
    for path in sorted(parents):
        if path in buckets:
            continue
        kids = [key for key in list(buckets) + list(parents) if len(key) == len(path) + 1 and key[: len(path)] == path]
        # unique immediate
        imm = {key[: len(path) + 1] for key in buckets if len(key) > len(path) and key[: len(path)] == path}
        if not 2 <= len(imm) <= 5:
            bad.append(("kids", path, sorted("/".join(k) for k in imm)))
    if bad or tree_miss:
        print("BAD", len(bad))
        for row in bad[:50]:
            print(row)
        raise SystemExit(1)
    print("sizes ok", len(items), "groups", len(buckets))

    ids = IdBook("EV", pyramid)
    cell_by_face = {}
    for point in pyramid["key_line"]["points"]:
        ids.get("EV.P", point["anchor"])
        cell_by_face[point["anchor"].split(":")[-1]] = point
    face_of = {"P": "EV.O.A1", "S": "EV.O.A2", "I": "EV.O.A3", "R": "EV.O.A4", "L": "EV.O.A5"}
    support_meta = {
        "P": ("loads", "the kind of load", "kinds", "structure"),
        "S": ("states", "the kind of state", "kinds", "structure"),
        "I": ("harms", "the kind of harm", "kinds", "structure"),
        "R": ("responses", "the kind of response", "kinds", "structure"),
        "L": ("limits", "the kind of limit", "kinds", "structure"),
    }
    for face, point in ((face, cell_by_face[face_of[face]]) for face in "PSIRL"):
        plural, dimension, basis, order = support_meta[face]
        children = build_level((face,), buckets, ids, point["id"])
        if not 2 <= len(children) <= 5:
            raise SystemExit(f"cell {face} has {len(children)} groups")
        point["support"] = {
            "logic_type": "inductive",
            "plural_noun": plural,
            "mece_dimension": dimension,
            "basis": basis,
            "order": order,
            "question_raised": "which_ones",
            "points": children,
        }
    methods_id = ids.get("EV.P", "facet:EV.O.A4:methods")
    method_points = build_level(("M",), buckets, ids, methods_id)
    if not 2 <= len(method_points) <= 5:
        raise SystemExit(f"methods have {len(method_points)} groups")
    pyramid["method_line"] = {
        "id": methods_id,
        "anchor": "facet:EV.O.A4:methods",
        "cell": "EV.O.A4",
        "statement": SPECS[("M",)]["statement"],
        "logic_type": "inductive",
        "plural_noun": "methods",
        "mece_dimension": SPECS[("M",)]["dimension"],
        "basis": SPECS[("M",)]["basis"],
        "order": SPECS[("M",)]["order"],
        "question_raised": "which_ones",
        "points": method_points,
    }
    pyramid["key_line"]["basis"] = "cause_effect"
    pyramid["key_line"]["order"] = "time"
    pyramid["environmental_definition"] = DEFINITION
    pyramid["driver_fold"] = DRIVER_FOLD
    pyramid["retired"] = ids.finish()

    previous = json.loads((ROOT / "pyramids" / "EV.json").read_text(encoding="utf-8"))
    old_ids = {point["anchor"][5:] for point in walk_leaves(previous["key_line"]["points"])}
    if previous.get("method_line"):
        old_ids |= {point["anchor"][5:] for point in walk_leaves(previous["method_line"].get("points") or [])}
    # walk_leaves on the rebuilt tree. The in-memory pyramid is already rebuilt,
    # so read the new leaves from the object we just wrote into.
    new_ids = {point["anchor"][5:] for point in walk_leaves(pyramid["key_line"]["points"])}
    new_ids |= {point["anchor"][5:] for point in walk_leaves(pyramid["method_line"]["points"])}
    queue_path = ROOT / "pyramids" / "queues" / "EV.json"
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    place_items = [item for item in queue["items"] if item.get("task", "place") == "place"]
    other_items = [item for item in queue["items"] if item.get("task", "place") != "place"]
    place_by_id = {item["node_id"]: item for item in place_items}
    build = pyramid["build"]
    names = {item["node_id"]: item["name"] for item in items}
    for row in routed:
        names.setdefault(row["node_id"], row["name"])

    for node_id in sorted(old_ids - new_ids):
        if node_id in place_by_id:
            continue
        row = next((entry for entry in routed if entry["node_id"] == node_id), None)
        place_by_id[node_id] = {
            "task": "place",
            "node_id": node_id,
            "name": names.get(node_id) or node_id,
            "cell": None,
            "reason": (row or {}).get("reason") or "routed out of the environmental classification",
            "field": (row or {}).get("field") or "",
            "margin": None,
            "candidates": [],
            "status": "out_of_scope",
            "group_id": "out_of_scope",
        }
        build["queued"] += 1
        build["placed"] -= 1
        build["placed_by_rules"] -= 1
    for node_id in sorted(new_ids - old_ids):
        if node_id in place_by_id:
            place_by_id.pop(node_id)
            build["queued"] -= 1
            build["placed"] += 1
            build["placed_by_rules"] += 1
        else:
            build["placed"] += 1
            build["placed_by_rules"] += 1
            build["after_dedupe"] += 1
    queue["items"] = list(place_by_id.values()) + other_items
    build["placed"] = build["placed_by_rules"] + build["placed_by_embeddings"]
    if build["after_dedupe"] != build["placed"] + build["queued"]:
        raise SystemExit(f"accounting {build['after_dedupe']} != {build['placed']} + {build['queued']}")

    after = minto_counts(pyramid)
    print("AFTER", json.dumps(after))
    issues = minto_issues(pyramid)
    for key, rows in issues.items():
        if rows:
            print(key, rows[:8])
    if any(issues.values()):
        raise SystemExit(1)

    (ROOT / "pyramids" / "EV.json").write_text(json.dumps(pyramid, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "pyramids" / "EV_minto.md").write_text(render_markdown(pyramid), encoding="utf-8")
    queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    route_path = ROOT / "pyramids" / "queues" / "EV.routes.jsonl"
    with route_path.open("w", encoding="utf-8") as handle:
        for row in sorted(routed, key=lambda item: (item.get("field") or "", item.get("name") or "")):
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("wrote", len(new_ids), "leaves", len(routed), "routes")


if __name__ == "__main__":
    main()
