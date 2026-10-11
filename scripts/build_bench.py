"""Write the cross-connection catalogue and the locked retrodiction benchmark.

Source: research report "Taxonomy Knowledge Base", checked 2026-10-11. VERIFIED = bibliographic record checked on
Crossref, arXiv or the publisher that day; everything else is UNVERIFIED until its DOI is checked.
Outputs:
  bench/cross_connections.json   100 cases (kept beside the answer key: it contains the answers)
  bench/retrodiction_problems.json  problem statements only (safe to show a model)
  bench/retrodiction_answers.json   answer key (never put in a prompt or a card)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (n, problem, target, tool, source, who_when, citation, verified)
C = [
(1,"Recover signals and MRI images from far fewer samples than Nyquist","EN MD","l1 minimisation, uncertainty principles","MA 42 90","Candes, Romberg, Tao 2006","IEEE Trans Inf Theory 52(2):489-509, doi:10.1109/TIT.2005.862083",1),
(2,"Recover sparse signals from few measurements","EN","Compressed sensing, n-widths","MA 41 42","Donoho 2006","IEEE Trans Inf Theory 52(4):1289-1306, doi:10.1109/TIT.2006.871582",1),
(3,"Shape of high-dimensional data","ST CS","Persistent homology","MA 55","Carlsson 2009","Bull AMS 46(2):255-308, doi:10.1090/S0273-0979-09-01249-X",1),
(4,"Unstable GAN training","CS","Wasserstein optimal transport distance","MA 49","Arjovsky, Chintala, Bottou 2017","arXiv:1701.07875",1),
(5,"Densest sphere packing in dimension 8","MA","Modular forms","MA 11","Viazovska 2017","Ann Math 185(3):991-1015, doi:10.4007/annals.2017.185.3.7",1),
(6,"Asymptotic count of integer partitions","MA","Circle method (complex and Fourier analysis)","MA 30 42","Hardy and Ramanujan 1918","Proc LMS s2-17:75-115, doi:10.1112/plms/s2-17.1.75",0),
(7,"Why animal contests are mostly limited war","BI","Evolutionarily stable strategy (game theory)","EC MA 91","Maynard Smith and Price 1973","Nature 246:15-18, doi:10.1038/246015a0",1),
(8,"Fair price of an option","BU EC","Heat-equation PDE","PH MA 35","Black and Scholes 1973","J Polit Econ 81(3):637-654, doi:10.1086/260062",1),
(9,"Ranking web pages by importance","IS CS","Markov chain stationary distribution, principal eigenvector","MA 60 15","Brin and Page 1998","Comput Netw ISDN Syst 30:107-117, doi:10.1016/S0169-7552(98)00110-X",1),
(10,"Classifying the zoo of hadrons","PH","SU(3) representation theory","MA 22","Gell-Mann 1962","Phys Rev 125:1067-1084, doi:10.1103/PhysRev.125.1067",1),
(11,"Classifying hadrons","PH","SU(3) gauge invariance","MA 22","Ne'eman 1961","Nucl Phys 26:222-229, doi:10.1016/0029-5582(61)90134-1",0),
(12,"Reconstruct tissue density from X-ray projections","MD","Radon transform inversion","MA 44","Cormack 1963","J Appl Phys 34:2722-2727, doi:10.1063/1.1729798",1),
(13,"Clinical CT scanner","MD","Computational reconstruction","EN CS","Hounsfield 1973","Br J Radiol 46:1016-1022, doi:10.1259/0007-1285-46-552-1016",1),
(14,"Mechanism of site-specific recombination on DNA","BI","Tangle calculus (knot theory)","MA 57","Ernst and Sumners 1990","Math Proc Camb Phil Soc 108:489-515",0),
(15,"Why viruses persist on the Internet","MD CS","Scale-free network mean-field theory","PH","Pastor-Satorras and Vespignani 2001","PRL 86:3200, doi:10.1103/PhysRevLett.86.3200",1),
(16,"Collective states of neuron populations","MS BI","Maximum-entropy Ising model","PH","Schneidman, Berry, Segev, Bialek 2006","Nature 440:1007-1012, doi:10.1038/nature04701",1),
(17,"Associative memory in neural circuits","MS CS","Spin-glass energy function","PH","Hopfield 1982","PNAS 79:2554-2558, doi:10.1073/pnas.79.8.2554",1),
(18,"Chip placement and combinatorial optimisation","CS EN","Simulated annealing (Metropolis)","PH","Kirkpatrick, Gelatt, Vecchi 1983","Science 220:671-680, doi:10.1126/science.220.4598.671",1),
(19,"Archaeological chronology from radiocarbon dates","HI","Bayesian hierarchical models, MCMC","MA 62","Bronk Ramsey 2009","Radiocarbon 51(1):337-360, doi:10.1017/S0033822200033865",1),
(20,"Allocating radio spectrum licences","PO LA EC","Auction theory","EC MA 91","Milgrom 2000","J Polit Econ 108:245-272, doi:10.1086/262118",1),
(21,"Dating the origin of Indo-European","LN HI","Bayesian phylogenetics","BI","Gray and Atkinson 2003","Nature 426:435-439, doi:10.1038/nature02029",1),
(22,"Unravelling of the US medical residency match","MD","Stable matching (deferred acceptance)","MA EC 91","Gale and Shapley 1962; Roth and Peranson 1999","AMM 69:9-15 doi:10.1080/00029890.1962.11989827; AER 89:748-780 doi:10.1257/aer.89.4.748",1),
(23,"Kidney exchange between incompatible pairs","MD","Top-trading cycles, matching","EC","Roth, Sonmez, Unver 2004","QJE 119:457-488",0),
(24,"Public school assignment","ED","Deferred acceptance","EC MA 91","Abdulkadiroglu and Sonmez 2003","AER 93:729-747",0),
(25,"Real networks are both clustered and short-path","BI EN PO","Rewired lattice graphs (small world)","MA 05 PH","Watts and Strogatz 1998","Nature 393:440-442, doi:10.1038/30918",1),
(26,"Power laws in earthquakes, 1/f noise","EA","Self-organised criticality","PH","Bak, Tang, Wiesenfeld 1987","PRL 59:381-384, doi:10.1103/PhysRevLett.59.381",1),
(27,"Residential segregation from mild preferences","PO MS","Agent-based cellular model","EC","Schelling 1971","J Math Sociol 1:143-186, doi:10.1080/0022250X.1971.9989794",1),
(28,"Choice under risk violating expected utility","EC","Psychophysics of value and probability (prospect theory)","MS","Kahneman and Tversky 1979","Econometrica 47:263-291, doi:10.2307/1914185",1),
(29,"Fast spectral analysis of long series","EA EN","FFT factorisation","MA 65","Cooley and Tukey 1965","Math Comp 19:297-301, doi:10.1090/S0025-5718-1965-0178586-1 (nuclear-test motivation UNVERIFIED)",1),
(30,"Why epidemics end before everyone is infected","MD","Threshold ODE model (SIR)","MA 34 92","Kermack and McKendrick 1927","Proc R Soc A 115:700-721, doi:10.1098/rspa.1927.0118",1),
(31,"Entropy and redundancy of English","LN","Information theory","EN MA 94","Shannon 1951","Bell Syst Tech J 30:50-64",0),
(32,"Information content of DNA binding sites","BI","Shannon entropy","MA 94","Schneider, Stormo, Gold, Ehrenfeucht 1986","J Mol Biol 188:415-431",0),
(33,"Letter dependence in Eugene Onegin","LN","Markov chains","MA 60","Markov 1913","Bull Imp Acad Sci St Petersburg; see Hayes 2013, Am Sci 101:92",0),
(34,"Computing posterior distributions in high dimensions","MA","Metropolis algorithm, Gibbs sampling","PH","Metropolis et al. 1953; Gelfand and Smith 1990","J Chem Phys 21:1087; JASA 85:398",0),
(35,"Automatic speech recognition","CS LN","Hidden Markov models","MA 60 62","Baker 1975; Rabiner 1989","Proc IEEE 77:257-286",0),
(36,"Protein family modelling","BI","Profile HMMs","CS MA 62","Krogh et al. 1994","J Mol Biol 235:1501-1531",0),
(37,"Optimal protein and DNA sequence alignment","BI","Dynamic programming","MA 90","Needleman and Wunsch 1970","J Mol Biol 48:443-453",0),
(38,"Spacecraft navigation from noisy data","EN","Recursive linear estimation (Kalman filter)","MA 93 62","Kalman 1960","J Basic Eng 82:35-45",0),
(39,"Planning plywood production","EC BU","Linear programming","MA 90","Kantorovich 1939","Manag Sci 6:366-422 (1960 translation)",0),
(40,"Post-WWI fish catch oscillations in the Adriatic","BI AG","Predator-prey ODEs","MA 34","Volterra 1926","Nature 118:558-560",0),
(41,"How embryos form spots and stripes","BI","Reaction-diffusion instability","MA 35 CH","Turing 1952","Phil Trans R Soc B 237:37-72",0),
(42,"Mechanism of the action potential","BI MD","Equivalent-circuit and cable models","EN","Hodgkin and Huxley 1952","J Physiol 117:500-544",0),
(43,"Structure of DNA","BI","X-ray diffraction","PH","Franklin and Gosling; Watson and Crick 1953","Nature 171:737-738",0),
(44,"Imaging soft tissue without ionising radiation","MD","NMR with field gradients","PH","Lauterbur 1973","Nature 242:190-191",0),
(45,"Absolute dating of archaeological organic remains","HI","Radiocarbon decay","PH CH","Arnold and Libby 1949","Science 110:678-680",0),
(46,"Dating Pueblo ruins","HI","Tree-ring series","PH EA","A.E. Douglass 1929","Natl Geogr Mag 56:736-770",0),
(47,"Continental drift mechanism","EA","Paleomagnetic stripes","PH","Vine and Matthews 1963","Nature 199:947-949",0),
(48,"Limits of weather prediction","EA","Deterministic chaos","MA 37","Lorenz 1963","J Atmos Sci 20:130-141",0),
(49,"Fat-tailed cotton price changes","EC","Stable distributions, fractals","MA 60","Mandelbrot 1963","J Business 36:394-419",0),
(50,"Measuring intelligence from test correlations","MS","Factor analysis","MA 62","Spearman 1904","Am J Psychol 15:201-292",0),
(51,"Fair, comparable test scoring","ED","Rasch and IRT models","MA 62 MS","Rasch 1960","Probabilistic Models for Some Intelligence and Attainment Tests",0),
(52,"Separating perceptual sensitivity from response bias","MS","Signal detection theory","EN","Tanner and Swets 1954","Psychol Rev 61:401-409",0),
(53,"Limits of short-term memory and judgement","MS","Channel capacity","MA 94","Miller 1956","Psychol Rev 63:81-97",0),
(54,"Learning internal representations","CS","Backpropagation","MA MS","Rumelhart, Hinton, Williams 1986","Nature 323:533-536",0),
(55,"Search in rugged design spaces","CS EN","Evolution by selection (genetic algorithms)","BI","Holland 1975","Adaptation in Natural and Artificial Systems",0),
(56,"Shortest routes in networks","CS","Ant pheromone trails","BI","Dorigo, Maniezzo, Colorni 1996","IEEE Trans SMC-B 26:29-41",0),
(57,"Learning probability distributions","CS","Boltzmann distribution","PH","Ackley, Hinton, Sejnowski 1985","Cogn Sci 9:147-169",0),
(58,"Generating images from noise","CS","Non-equilibrium thermodynamics, diffusion","PH","Sohl-Dickstein et al. 2015","arXiv:1503.03585",0),
(59,"Secure communication without a shared secret","CS","Modular arithmetic, factoring","MA 11","Rivest, Shamir, Adleman 1978","CACM 21:120-126",0),
(60,"Smaller cryptographic keys","CS","Elliptic curves over finite fields","MA 11 14","Koblitz 1987; Miller 1985","Math Comp 48:203-209",0),
(61,"Error-free CD audio and deep-space links","EN","Polynomials over finite fields (Reed-Solomon)","MA 12 94","Reed and Solomon 1960","J SIAM 8:300-304",0),
(62,"Designing relay switching circuits","EN","Boolean algebra","MA 03 PL","Shannon 1938","Trans AIEE 57:713-723",0),
(63,"What is mechanically computable","MA CS","Turing machines","PL MA 03","Turing 1936","Proc LMS s2-42:230-265",0),
(64,"Programming languages with functions as data","CS","Lambda calculus","MA 03 PL","Church 1936; McCarthy 1960","CACM 3:184-195",0),
(65,"Gravity as geometry","PH","Riemannian geometry","MA 53","Einstein and Grossmann 1913","Z Math Phys 62:225-261",0),
(66,"Gauge fields and the Aharonov-Bohm effect","PH","Fibre bundles","MA 53 55","Wu and Yang 1975","Phys Rev D 12:3845",0),
(67,"Rigorous quantum mechanics","PH","Hilbert-space operator theory","MA 46 47","von Neumann 1932","Mathematische Grundlagen der Quantenmechanik",0),
(68,"Spacing of Riemann zeta zeros","MA","Random matrix statistics from nuclear spectra","PH","Montgomery 1973 (with Dyson)","Proc Symp Pure Math 24:181-193",0),
(69,"Quantised Hall conductance","PH","Chern numbers, topology","MA 55 57","Thouless, Kohmoto, Nightingale, den Nijs 1982","PRL 49:405",0),
(70,"Forbidden fivefold diffraction symmetry","CH","Aperiodic (Penrose) tilings","MA 52","Shechtman et al. 1984","PRL 53:1951",0),
(71,"Counting chemical isomers","CH","Trees, Polya enumeration","MA 05","Cayley 1874; Polya 1937","Acta Math 68:145-254",0),
(72,"Solving the crystallographic phase problem","CH","Probabilistic direct methods","MA 62","Hauptman and Karle 1953","ACA Monograph 3",0),
(73,"Tractable electronic structure of molecules","CH","Density functional theory","PH","Kohn and Sham 1965","Phys Rev 140:A1133",0),
(74,"Estimating ore grades between boreholes","EN","Kriging, geostatistics","MA 62","Krige 1951; Matheron 1963","Econ Geol 58:1246-1266",0),
(75,"Design of nature reserves","EV","Island biogeography","BI","MacArthur and Wilson 1967; Diamond 1975","Biol Conserv 7:129-146",0),
(76,"Is the tragedy of the commons inevitable","EC PO","Field studies of community resource institutions","IK PO","Ostrom 1990","Governing the Commons (CUP)",0),
(77,"Reducing late-dry-season wildfire emissions","EV","Aboriginal early-season burning","IK","Russell-Smith et al. 2013 (WALFA)","Front Ecol Environ 11:e55-e63",0),
(78,"Documenting Arctic sea-ice change","EA","Inuit observation and knowledge","IK","Krupnik and Jolly (eds) 2002","The Earth Is Faster Now (ARCUS)",0),
(79,"Drug-resistant malaria","MD","Ge Hong's 4th-century qinghao preparation","IK HI","Tu Youyou 1972; account 2011","Nat Med 17:1217-1220",0),
(80,"Was Polynesia settled by deliberate voyaging","HI","Traditional non-instrument wayfinding","IK","Finney and Mau Piailug, Hokule'a 1976","Finney 1979, Hokule'a: The Way to Tahiti",0),
(81,"Fixing the date of Easter","RE","Astronomical tables and computus","PH MA","Clavius, Gregorian reform 1582","Coyne, Hoskin, Pedersen (eds) 1983, Vatican Observatory",0),
(82,"Manuscript genealogy of The Canterbury Tales","LN HI","Phylogenetic software","BI","Barbrook et al. 1998","Nature 394:839",0),
(83,"Age of the Shroud of Turin","RE","AMS radiocarbon","PH","Damon et al. 1989","Nature 337:611-615",0),
(84,"Which Dead Sea Scroll fragments belong together","RE","Ancient DNA of parchment animals","BI","Anava et al. 2020","Cell 181:1218-1231",0),
(85,"Hidden earlier painting under a Van Gogh","AR","Synchrotron X-ray fluorescence","PH CH","Dik et al. 2008","Anal Chem 80:6436-6442",0),
(86,"Authenticating paintings by brushwork","AR","Wavelet image statistics","MA 42 CS","Johnson et al. 2008","IEEE Signal Process Mag 25(4):37-48",0),
(87,"Properties invariant under projection","MA","Renaissance perspective practice","AR","Desargues 1639","Field 1997, The Invention of Infinity (OUP)",0),
(88,"Quasi-periodic patterns in medieval architecture","AR HI","Quasicrystal geometry","PH MA 52","Lu and Steinhardt 2007","Science 315:1106-1110",0),
(89,"Reusable solutions in object-oriented software","CS","Architectural pattern language","DE","Alexander 1977; Gamma et al. 1994","Design Patterns (Addison-Wesley)",0),
(90,"Deployable solar arrays and maps","EN","Origami folding","AR DE","Miura 1985","ISAS Report 618",0),
(91,"Dry reversible adhesives","EN","Gecko setae","BI","Autumn et al. 2000","Nature 405:681-685",0),
(92,"Durable learning in schools","ED","Spacing effect","MS","Ebbinghaus 1885; Cepeda et al. 2006","Psychol Bull 132:354-380",0),
(93,"Probability errors in the Sally Clark trial","LA","Independence and the prosecutor's fallacy","MA 62","Royal Statistical Society 2001","RSS press statement, 23 Oct 2001",0),
(94,"Identifying individuals in criminal and immigration cases","LA","Minisatellite DNA fingerprints","BI","Jeffreys, Wilson, Thein 1985","Nature 316:76-79",0),
(95,"Detecting partisan gerrymanders in court","LA PO","Markov chain significance tests","MA 60","Chikina, Frieze, Pegden 2017","PNAS 114:2860-2864",0),
(96,"Can any voting rule be fair","PO","Axiomatic social choice","MA EC","Arrow 1951","Social Choice and Individual Values",0),
(97,"Disputed authorship of the Federalist Papers","HI PO","Bayesian word-frequency discrimination","MA 62","Mosteller and Wallace 1963","JASA 58:275-309",0),
(98,"Rise of the Medici","HI","Social network analysis","PO MA","Padgett and Ansell 1993","Am J Sociol 98:1259-1319",0),
(99,"Verifying concurrent programs","CS","Temporal and modal logic","PL","Pnueli 1977","Proc 18th FOCS, 46-57",0),
(100,"Inferring causation from observational data","MA MD","Graphical causal models","PL","Spirtes, Glymour, Scheines 1993; Pearl 2000","Causation, Prediction, and Search (Springer)",0),
]

# (id, date, problem as posed)
P = [
("R01","c. 2004","MRI scans are slow because the Nyquist rate seems to demand many Fourier samples. Can a sparse image be recovered exactly from far fewer, randomly chosen frequency measurements, and under what conditions?"),
("R02","c. 2000","Point-cloud data in high dimensions seem to have loops and voids. How can one robustly measure the shape of noisy data at every scale at once?"),
("R03","2014-16","Generative adversarial networks train unstably and collapse to a few modes. The divergence they minimise gives no useful gradient when distributions do not overlap. What distance between distributions would?"),
("R04","1611-2016","What is the densest packing of equal spheres in 8-dimensional space, and can it be proved optimal?"),
("R05","1910s","Find an asymptotic formula for p(n), the number of ways to write n as a sum of positive integers."),
("R06","c. 1970","Why do animals with lethal weapons usually fight ritualised contests instead of escalating? Group-selection explanations seem inadequate."),
("R07","1960s","What is the rational price of a call option, given that the stock follows a random walk and investors' risk preferences are unknown?"),
("R08","1996-97","Keyword search engines return huge, poorly ordered result lists. How can pages be ranked by importance using only the link structure of the Web?"),
("R09","1950s-61","Dozens of hadrons and resonances have been discovered with assorted charges and strangeness. Is there an organising principle that predicts missing particles?"),
("R10","1950s-60s","Radiologists want the 2-D distribution of X-ray absorption inside a body, but each measurement gives only total attenuation along a line. Can the distribution be recovered?"),
("R11","1980s","Enzymes such as recombinases change DNA topology. From the knotted or linked products seen under the electron microscope, can one infer the enzyme's mechanism?"),
("R12","c. 2000","Computer viruses survive for very long times at low prevalence, contradicting classical epidemic thresholds. Why?"),
("R13","2000s","Neurons in a retina patch have weak pairwise correlations. Does the population nonetheless behave collectively, and how can its states be modelled from limited data?"),
("R14","1970s-82","How can a network of simple neuron-like units store memories retrievable from partial cues, robustly and without a central address?"),
("R15","1980-82","Chip placement and wiring involve astronomically many configurations with many local optima. Is there a general heuristic that escapes local minima?"),
("R16","1980s-90s","Radiocarbon dates have irregular calibration errors. How should archaeologists combine many dates with stratigraphic order to get the tightest chronology?"),
("R17","early 1990s","Governments allocate interdependent radio spectrum licences by hearings or lotteries, which is slow and leaves value with speculators. How should licences be allocated efficiently?"),
("R18","1980s-2002","The Indo-European homeland is disputed (Kurgan steppe c. 6,000 years ago vs Anatolian farming c. 8,000-9,500 years ago). Can lexical data date the split independently?"),
("R19","1940s-50s","Hospitals and medical graduates face chaotic, unravelling offer timing for internships. Is there a centralised procedure that participants will not want to circumvent?"),
("R20","1990s","Patients with willing but incompatible living kidney donors cannot transplant. How can incompatible pairs be combined to maximise transplants?"),
("R21","late 1990s","City school-assignment systems such as the Boston mechanism reward strategic misreporting by parents. Can a mechanism be strategy-proof and fair?"),
("R22","1960s-90s","Social networks show six degrees of separation and high clustering together; regular and random graphs each give only one. What simple model gives both?"),
("R23","1980s","Earthquake magnitudes follow the Gutenberg-Richter power law, and many systems show 1/f noise with no tuning parameter. Why are scale-free fluctuations so common?"),
("R24","1960s","Neighbourhoods become highly segregated even where surveys show only mild preferences for same-group neighbours. How?"),
("R25","1950s-70s","People systematically violate expected-utility theory (Allais paradox, framing, reflection). What descriptive theory of risky choice fits the data?"),
("R26","1963-64","Seismic monitoring of nuclear tests and other large-scale spectral analyses need Fourier transforms of long series, which cost N squared operations. Can this be reduced?"),
("R27","1900s-20s","Epidemics such as plague in Bombay stop while many susceptibles remain. Is that due to falling virulence, or something structural?"),
("R28","1940s","How much redundancy does written English contain, and how predictable is the next letter?"),
("R29","1950s-80s","Biologists need the most probable evolutionary correspondence between two protein sequences of different lengths, allowing gaps. Exhaustive search is impossible."),
("R30","1958-60","A spacecraft's position must be estimated in real time from noisy sequential measurements with a computer of very limited memory."),
("R31","1920s","After WWI fishing pauses, Adriatic catches showed more predatory fish. Why should reduced fishing favour predators?"),
("R32","pre-1952","How does a nearly uniform embryo spontaneously develop regular patterns (spots, stripes, tentacles)?"),
("R33","1940s","What ionic mechanism generates and propagates the nerve action potential, quantitatively?"),
("R34","1940s-60s","Can soft tissue (e.g. tumours) be imaged in 3-D without ionising radiation?"),
("R35","pre-1949","Archaeologists lack absolute dates for organic remains beyond written records. How can the age of wood, bone or charcoal be measured?"),
("R36","1950s","If continents drift, what physical record on the ocean floor would prove seafloor spreading?"),
("R37","1960s-70s","Why do weather forecasts lose skill after a few days even with better models? Is there a fundamental limit?"),
("R38","1960s-70s","Factoring is hard but multiplying is easy. Can two strangers communicate secretly over a public channel without first sharing a key?"),
("R39","1930s","Telephone relay circuits are designed ad hoc. Is there a systematic calculus for simplifying and verifying switching circuits?"),
("R40","1907-12","A mathematical framework is needed in which gravitation is described covariantly for arbitrary coordinate systems."),
("R41","1970-80","The Hall conductance is quantised to extraordinary precision regardless of sample impurities. Why is it so robust?"),
("R42","1982-84","An electron-diffraction pattern of rapidly cooled Al-Mn shows sharp tenfold symmetry, which classical crystallography forbids. What kind of order is this?"),
("R43","1960s-80s","The commons literature predicts overuse of shared fisheries, forests and irrigation unless there is privatisation or state control, yet many communities manage commons sustainably for centuries. How?"),
("R44","1990s-2000s","Late-dry-season wildfires in northern Australian savannas emit large amounts of greenhouse gas and damage biodiversity. How can fire regimes be managed at landscape scale?"),
("R45","1960s","Chloroquine-resistant malaria is spreading in Southeast Asia. Where can a new antimalarial compound be found?"),
("R46","1950s-70s","Some scholars argued that Polynesia was settled by accidental drift voyages, because long-distance navigation without instruments seemed impossible. Could it be tested?"),
("R47","1970s-80s","Several hundred fragmentary manuscripts of The Canterbury Tales exist. Can their copying genealogy be reconstructed objectively?"),
("R48","1980s-90s","Object-oriented programmers keep reinventing solutions to recurring design problems. How can design know-how be captured and communicated?"),
("R49","late 1990s","In a murder trial, an expert claimed a 1-in-73-million chance of two cot deaths in one family. Was the reasoning sound?"),
("R50","1780s-1940s","Is there a voting rule for three or more options that respects unanimity, independence of irrelevant alternatives, and non-dictatorship?"),
]

# (id, field/subfield, tool, catalogue numbers)
A = [
("R01","MA 42 90","l1 compressed sensing",[1,2]),("R02","MA 55","Persistent homology",[3]),("R03","MA 49","Wasserstein distance",[4]),
("R04","MA 11","Modular forms, magic function and LP bound",[5]),("R05","MA 30 42","Circle method",[6]),("R06","EC MA 91","ESS",[7]),
("R07","PH MA 35","Heat equation, replicating portfolio",[8]),("R08","MA 60 15","PageRank eigenvector",[9]),("R09","MA 22","SU(3) eightfold way",[10,11]),
("R10","MA 44","Radon inversion",[12,13]),("R11","MA 57","Tangle calculus",[14]),("R12","PH","Scale-free mean field",[15]),
("R13","PH","Max-entropy Ising",[16]),("R14","PH","Hopfield energy (spin glass)",[17]),("R15","PH","Simulated annealing",[18]),
("R16","MA 62","Bayesian calibration, MCMC",[19]),("R17","EC","Simultaneous ascending auction",[20]),("R18","BI","Bayesian relaxed-clock trees",[21]),
("R19","MA EC 91","Deferred acceptance",[22]),("R20","EC","Top-trading cycles, exchange",[23]),("R21","EC MA 91","Student-proposing deferred acceptance",[24]),
("R22","MA 05 PH","Small-world rewiring",[25]),("R23","PH","Self-organised criticality",[26]),("R24","EC","Schelling agent-based model",[27]),
("R25","MS","Prospect theory",[28]),("R26","MA 65","FFT",[29]),("R27","MA 34 92","Threshold SIR model",[30]),
("R28","MA 94","Entropy estimation",[31]),("R29","MA 90","Dynamic programming",[37]),("R30","MA 93 62","Kalman filter",[38]),
("R31","MA 34","Lotka-Volterra",[40]),("R32","MA 35 CH","Reaction-diffusion instability",[41]),("R33","EN","Hodgkin-Huxley equivalent circuit",[42]),
("R34","PH","Gradient-encoded NMR imaging",[44]),("R35","PH","Radiocarbon dating",[45]),("R36","PH","Magnetic anomaly stripes",[47]),
("R37","MA 37","Sensitive dependence, chaos",[48]),("R38","MA 11","RSA public-key",[59]),("R39","MA 03 PL","Boolean algebra",[62]),
("R40","MA 53","Riemannian geometry, tensor calculus",[65]),("R41","MA 55 57","Chern number (TKNN)",[69]),("R42","MA 52","Aperiodic tilings, quasicrystals",[70]),
("R43","IK PO","Ostrom design principles",[76]),("R44","IK","Early-season cultural burning",[77]),("R45","IK HI","Low-temperature qinghao extraction",[79]),
("R46","IK","Experimental voyaging, wayfinding",[80]),("R47","BI","Cladistic software",[82]),("R48","DE","Pattern language",[89]),
("R49","MA 62","Dependence, prosecutor's fallacy",[93]),("R50","MA EC","Arrow's impossibility theorem (answer: no)",[96]),
]

SRC = "Research report 'Taxonomy Knowledge Base', checked 2026-10-11"


def main():
    cards = [{"id": f"XC{n:03d}", "problem": p, "target_fields": t.split(), "tool": tool, "source_field": s,
              "who_when": w, "citation": c, "status": "VERIFIED" if v else "UNVERIFIED", "checked": "2026-10-11"}
             for n, p, t, tool, s, w, c, v in C]
    (ROOT / "bench" / "cross_connections.json").write_text(json.dumps({"source": SRC, "cases": cards}, indent=1, ensure_ascii=False), encoding="utf-8")
    b = ROOT / "bench"
    b.mkdir(exist_ok=True)
    (b / "retrodiction_problems.json").write_text(json.dumps({"source": SRC, "note": "Problem statements only. Safe to show a model.",
        "problems": [{"id": i, "posed": d, "problem": q} for i, d, q in P]}, indent=1, ensure_ascii=False), encoding="utf-8")
    (b / "retrodiction_answers.json").write_text(json.dumps({"source": SRC, "note": "LOCKED answer key. Never put in a prompt, a card or the lexicon.",
        "answers": [{"id": i, "field": f, "tool": t, "cases": [f"XC{n:03d}" for n in ns]} for i, f, t, ns in A]}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(len(cards), len(P), len(A))


if __name__ == "__main__":
    main()
