# EC — Economics

Standard v2 cited, not copied. Diagnosis: audit_mind_econ_business.md. v1 source: twelve.txt 3464–3729. Proofs are owned by MA, mostly MA.B.C4 (MSC 91, game theory and economics). The choice of game, and moves that reshape it, are ST.

## 1. SCQA
**Situation.** Economics states how scarce resources are allocated among people with competing wants.
**Complication.** v1 let a theorem, the allocation it implies and the strategic game behind it share one cell. It stated welfare theorems, Arrow and Coase without hypotheses, and it confused VAT with sales tax.
**Question.** How can every economic claim be placed once, with the theorem, the allocation and the game kept apart?
**Answer.** Place it by the scale at which the allocation is settled. The theorem stays in MA and the choice of game stays in ST. EC owns the claim that this allocation results, or would result, in this economy.

## 2. Governing thought
Economics is exhausted by four faces of one pyramid: objects, methods, warrants and bridges.
Its objects divide into five scales of allocation: choice, markets, mechanisms and institutions, the aggregate economy, and welfare and public choice.

## 3. Key line
Dimension: **the scale at which an allocation is settled.** Order: from one agent to the whole society.
1. Choice
2. Markets
3. Mechanisms and institutions
4. The aggregate economy
5. Welfare and public choice

**The three-way border (the economics repair).** Take any equilibrium result. The existence proof is MA (uses MA.O.A3 fixed-point theorems, via MA.B.C4). The choice of which game the parties are in, and any move that changes it, is ST. The claim that an actual or counterfactual allocation follows is EC.

## 4. Face O — Objects

### EC.O.A1 Choice

Situation. Allocation begins with agents choosing under constraints. Complication. Choice theory is precise, but people often depart from its axioms. v1 placed the psychological cause and the economic consequence in one cell. Question. What is claimed about how agents choose, and which part of that claim does economics own? Answer. Economics owns the representation of choice, its implications for demand, and the allocative effect of departures. The psychological mechanism is MS, and every representation proof is MA.

Key line (inductive; plural noun: choice settings; dimension: what the chooser faces beyond a fixed budget; order: certainty, then risk, then departures from both, then time). Members (4): Preferences and demand · Choice under risk · Behavioural departures · Intertemporal choice.

- EC.O.A1.1 Preferences and demand. **Rational preferences have a utility representation, and demand theory follows from it.** Complete, transitive and continuous preferences have a utility representation (Debreu; proof uses MA). Demand theory follows, with the Slutsky decomposition.
  - EC.O.A1.1.1 Utility representation. On a connected, separable space, a complete, transitive and continuous preference has a continuous utility function (uses MA.O.A3). The function is ordinal: any increasing transform represents the same preference.
  - EC.O.A1.1.2 Slutsky decomposition. A price change splits into a substitution effect and an income effect. The compensated own-price effect is never positive. A Giffen good needs an inferior good with a large income effect.
  - EC.O.A1.1.3 Revealed preference. A finite set of price and choice observations can be rationalised by a locally non-satiated utility function if and only if it satisfies GARP (Afriat; proof uses MA). The test is falsifiable on household data.

- EC.O.A1.2 Choice under risk. **Expected utility follows from four axioms on lotteries.** Expected utility follows from the von Neumann–Morgenstern axioms (completeness, transitivity, continuity, independence).
  - EC.O.A1.2.1 Representation and uniqueness. Under the four axioms, preferences over lotteries are represented by the expectation of a utility over outcomes. That utility is unique up to a positive affine transform (uses MA.O.A5).
  - EC.O.A1.2.2 Risk aversion. Within expected utility, an agent is risk averse if and only if the utility over wealth is concave. The Arrow–Pratt coefficient measures local risk aversion and orders agents by willingness to insure.

- EC.O.A1.3 Behavioural departures. **Observed choices violate expected utility in systematic ways, and economics owns the allocative consequence.** The Allais paradox violates independence; prospect theory fits loss aversion. The psychological mechanism is MS; the allocative consequence is EC.
  - EC.O.A1.3.1 Allais pattern. Many subjects prefer the sure gain in one pair of lotteries and the riskier option in a matched pair. No single expected-utility function produces both choices.
  - EC.O.A1.3.2 Reference dependence. Prospect theory values outcomes as gains or losses from a reference point, with losses weighted more than equal gains. It also weights probabilities non-linearly (uses MS.O.A1).
  - EC.O.A1.3.3 Endowment effect. Willingness to accept often exceeds willingness to pay for the same good. Its size outside the laboratory, and in experienced traders, is CONTESTED.

- EC.O.A1.4 Intertemporal choice. **The form of discounting decides whether plans stay consistent over time.** Exponential discounting is time-consistent; quasi-hyperbolic discounting is not.
  - EC.O.A1.4.1 Exponential discounting. With a constant per-period discount factor, a plan made today remains optimal when re-evaluated later. Preference reversals between dated rewards cannot occur.
  - EC.O.A1.4.2 Present bias. With a beta–delta discount function and beta below one, a sophisticated agent values commitment devices. Demand for commitment, such as locked savings, is a testable prediction.

Named objects: utility function (hypotheses: completeness, transitivity, continuity), Slutsky equation, Afriat's theorem (finite data, local non-satiation), GARP, von Neumann–Morgenstern expected utility (four axioms), Arrow–Pratt measure (twice-differentiable utility), Allais paradox, prospect theory (reference point, loss aversion, probability weighting), endowment effect, exponential discounting, quasi-hyperbolic (beta–delta) model.

### EC.O.A2 Markets

Situation. Choices meet in markets, where prices coordinate them. Complication. Markets clear under strong conditions, but firms may set prices, information may be hidden, and taxes shift burdens. v1 merged the game between firms with the resulting allocation. Question. When do markets clear, and what allocation results when they depart from competition? Answer. Economics owns equilibrium prices, quantities and burdens. Existence and game-equilibrium proofs are MA, and the choice of game is ST.

Key line (inductive; plural noun: market conditions; dimension: which assumption of the competitive benchmark the claim keeps or drops; order: benchmark, then fewer sellers, then hidden information, then input markets, then taxes). Members (5): Competitive equilibrium · Market power · Information · Factor markets · Tax incidence.

- EC.O.A2.1 Competitive equilibrium. **A price system can clear all markets at once under convexity and continuity.** A general equilibrium exists given continuous, convex, locally non-satiated preferences, convex production, and endowments in the interior (Arrow–Debreu; proof MA).
  - EC.O.A2.1.1 Existence. Under the stated hypotheses, a price vector exists at which aggregate excess demand is zero (uses MA.O.A3, via MA.B.C4).
  - EC.O.A2.1.2 Indeterminacy of aggregate demand. Individual rationality restricts aggregate excess demand only weakly (Sonnenschein–Mantel–Debreu; proof MA). Uniqueness and stability of equilibrium therefore need extra assumptions.
  - EC.O.A2.1.3 Partial equilibrium. A single-market supply-and-demand analysis approximates general equilibrium when the market is small and income effects are negligible.

- EC.O.A2.2 Market power. **Fewer sellers raise price above marginal cost, by an amount the game decides.** Monopoly, oligopoly, entry. The equilibrium of the Cournot or Bertrand game is MA. Which game the firms are in is ST. The resulting prices and quantities are EC.
  - EC.O.A2.2.1 Monopoly markup. A profit-maximising single-price monopolist sets the Lerner index, (P − MC)/P, equal to the inverse of the absolute elasticity of demand.
  - EC.O.A2.2.2 Bertrand outcome. With two or more firms, identical constant marginal cost, homogeneous goods and no capacity limit, price equals marginal cost in equilibrium.
  - EC.O.A2.2.3 Cournot outcome. With quantity competition and linear demand, the equilibrium price lies between the monopoly and competitive prices. It approaches marginal cost as the number of firms grows.

- EC.O.A2.3 Information. **Hidden quality and hidden action change which trades occur.** Adverse selection (Akerlof), moral hazard, signalling. A market can unravel when quality is hidden and sellers know more than buyers.
  - EC.O.A2.3.1 Unravelling. If buyers pay for average quality and sellers know their own, the best sellers may withdraw. In the limit only the lowest quality trades.
  - EC.O.A2.3.2 Signalling. A costly signal can separate types when its cost falls more steeply for high types (Spence). The signal may carry no productive value.
  - EC.O.A2.3.3 Moral hazard. When effort is unobserved, an optimal contract trades insurance against incentives. Full insurance removes the incentive to take care.

- EC.O.A2.4 Factor markets. **Input prices follow from the value of what inputs produce and from market structure.** Labour and capital; wages and returns.
  - EC.O.A2.4.1 Competitive factor pricing. In a competitive market, each input is paid the value of its marginal product.
  - EC.O.A2.4.2 Monopsony. A single buyer of labour pays below the value of marginal product. A minimum wage set in a range can raise both wage and employment. Its empirical relevance is CONTESTED.

- EC.O.A2.5 Tax incidence. **The economic burden of a tax does not depend on who legally remits it.** In a competitive market, the burden falls by relative elasticities of supply and demand, not by who legally pays. Incidence is EC; the duty to pay is LA; computing the tax is BU.
  - EC.O.A2.5.1 Elasticity rule. For a small per-unit tax, the consumer share of the burden is approximately the supply elasticity divided by the sum of supply and demand elasticities.
  - EC.O.A2.5.2 Excess burden. For a small tax in a single market, the deadweight loss rises approximately with the square of the tax rate (Harberger approximation).

Named objects: Arrow–Debreu equilibrium (convexity, continuity, local non-satiation, interior endowments), Sonnenschein–Mantel–Debreu result, partial equilibrium, Lerner index, Bertrand model (homogeneous goods, equal constant cost), Cournot model (quantity choice), market for lemons, Spence signalling model (single crossing), principal–agent model, marginal productivity theory, monopsony, incidence rule, Harberger triangle (small tax, linear approximation).

### EC.O.A3 Mechanisms and institutions

Situation. Many allocations are settled by designed rules or by institutions, not by anonymous prices. Complication. The same theorem can serve auction design, collusion and law, and v1 filed its use in several places. Question. Which rules produce which allocations, and under what conditions? Answer. Economics owns the allocation each rule produces. Theorems are MA, the choice of protocol is ST, and legal validity is LA.

Key line (inductive; plural noun: allocation rules; dimension: how the rule is set; order: designed, then negotiated, then shaped by costs of exchange, then embedded in institutions, then sustained by repetition). Members (5): Mechanism design · Bargaining · Transaction costs · Institutions · Repeated interaction.

- EC.O.A3.1 Mechanism design. **Truthful direct mechanisms are enough to study what any mechanism can achieve.** The revelation principle: any equilibrium outcome of a mechanism can be achieved by a direct, truthful mechanism (proof MA). Vickrey auctions make truthful bidding dominant for private values.
  - EC.O.A3.1.1 Revelation principle. Any outcome implemented in Bayes–Nash equilibrium by some mechanism is implemented by a direct mechanism with truthful reports (uses MA.B.C4).
  - EC.O.A3.1.2 Second-price auction. In a sealed-bid second-price auction with private values, bidding one's value is a weakly dominant strategy.
  - EC.O.A3.1.3 Revenue equivalence. With risk-neutral bidders, independent private values from a common continuous distribution, the same allocation rule and zero surplus for the lowest type, standard auctions yield equal expected revenue.
  - EC.O.A3.1.4 Bilateral trade impossibility. With independent private values and overlapping supports, no mechanism is efficient, incentive compatible, individually rational and budget balanced together (Myerson–Satterthwaite; proof MA).

- EC.O.A3.2 Bargaining. **Under alternating offers, patience decides the split.** Rubinstein: with two players, alternating offers, an infinite horizon, complete information and discount factors below one, there is a unique subgame-perfect equilibrium with immediate agreement. The theorem is MA. The choice of bargaining protocol is ST. The split is EC.
  - EC.O.A3.2.1 Unique immediate agreement. Under Rubinstein's hypotheses, the first offer is accepted and no delay occurs on the equilibrium path (uses ST.O.A2 for protocol choice).
  - EC.O.A3.2.2 Patience advantage. The more patient player receives the larger share. As both discount factors approach one with equal rates, the split approaches one half each.
  - EC.O.A3.2.3 Nash bargaining solution. The unique solution meeting Nash's four axioms maximises the product of gains over the disagreement point. Rubinstein's equilibrium approaches it as offers become frequent.

- EC.O.A3.3 Transaction costs. **When exchange is costly, the initial assignment of rights affects the outcome.** Coase: with well-defined property rights, zero transaction costs and no wealth effects, bargaining reaches an efficient outcome whatever the initial assignment. With positive costs the assignment matters, and that is the theorem's main use.
  - EC.O.A3.3.1 Coase benchmark. Under the three hypotheses, the efficient level of a harmful activity does not depend on who holds the right. Only the distribution of gains changes.
  - EC.O.A3.3.2 Costly exchange. With positive bargaining costs, the efficient outcome may not be reached. The choice of liability rule then changes the allocation (legal rule uses LA).

- EC.O.A3.4 Institutions. **Property rights, contracts and firms are rules that change which allocations are reachable.** Property rights, contracts and firms as allocative rules. Political authority is PO; legal validity is LA.
  - EC.O.A3.4.1 Boundaries of the firm. Transactions move inside a firm when relationship-specific investment and uncertainty make market contracting costly (Williamson). The prediction is testable on make-or-buy data.
  - EC.O.A3.4.2 Hold-up. With incomplete contracts, a party anticipating renegotiation underinvests in specific assets. Assigning ownership to the party whose investment matters more reduces the loss.
  - EC.O.A3.4.3 Institutions and growth. Secure property rights and constraints on expropriation are associated with long-run income. The causal share relative to geography and culture is CONTESTED.

- EC.O.A3.5 Repeated interaction. **Repetition with patient players can sustain outcomes that one-shot play cannot.** Folk theorem: in an infinitely repeated game with a discount factor close enough to one, any feasible, strictly individually rational payoff is sustainable in equilibrium (with a full-dimensionality condition for more than two players). Theorem MA; use in collusion or cooperation EC; choice of game ST.
  - EC.O.A3.5.1 Folk theorem. Under the stated hypotheses, a continuum of equilibrium payoffs exists. The theorem does not select among them.
  - EC.O.A3.5.2 Finite horizon. If a stage game has a unique Nash equilibrium and is repeated a known finite number of times, the unique subgame-perfect outcome repeats that equilibrium.
  - EC.O.A3.5.3 Collusion conditions. Tacit collusion is easier to sustain with fewer firms, more frequent interaction and more observable prices. Each factor lowers the discount factor needed to sustain it.

Named objects: revelation principle (Bayes–Nash implementation), Vickrey auction (private values), revenue equivalence theorem (risk neutrality, independent private values, same allocation, zero lowest-type surplus), Myerson–Satterthwaite theorem, Rubinstein bargaining model (two players, alternating offers, infinite horizon, complete information, discounting), Nash bargaining solution (four axioms), Coase theorem (defined rights, zero transaction costs, no wealth effects), transaction-cost theory of the firm, hold-up problem, folk theorem (discount near one, full dimensionality for three or more players).

### EC.O.A4 The aggregate economy

Situation. Output, prices and employment move together across an economy. Complication. Aggregate relations estimated from data have broken down when policy changed, and v1 stated some identities as theories. Question. What determines output, prices and employment, and which aggregate claims survive a change of regime? Answer. Economics owns aggregate models and their identified effects. It labels identities, empirical regularities and policy rules separately.

Key line (inductive; plural noun: aggregate questions; dimension: which aggregate the claim explains; order: long-run trend, short-run deviation, nominal level, external position, policy regime). Members (5): Growth · Fluctuations · Money and inflation · Open economies · Expectations and policy.

- EC.O.A4.1 Growth. **Capital accumulation alone cannot sustain growth in output per worker.** The Solow model: with diminishing returns to capital and constant returns to scale, output per worker converges to a steady state, and long-run growth needs technical change.
  - EC.O.A4.1.1 Steady state. In the Solow model, capital per effective worker converges to a unique positive steady state from any positive start (uses MA.O.A4).
  - EC.O.A4.1.2 Conditional convergence. Economies with similar saving, population growth and technology should converge in income per worker. Absolute convergence across all countries is not observed.
  - EC.O.A4.1.3 Endogenous growth. Models in which ideas or human capital raise the growth rate itself remain an OPEN programme. Their quantitative fit is CONTESTED.

- EC.O.A4.2 Fluctuations. **Short-run output and unemployment deviate from trend, and the stable relations are few.** Business cycles; unemployment. The Phillips curve is an empirical relation that proved unstable once expectations adjusted.
  - EC.O.A4.2.1 Phillips instability. The inverse relation between inflation and unemployment shifted when inflation expectations rose. An expectations-augmented form predicts no long-run trade-off.
  - EC.O.A4.2.2 Okun's relation. Changes in unemployment move inversely with output growth. The coefficient varies by country and period, so it is an empirical regularity, not a law.
  - EC.O.A4.2.3 Sources of shocks. The relative weight of demand, supply and financial shocks in cycles is OPEN.

- EC.O.A4.3 Money and inflation. **An identity links money and prices; theory begins with assumptions about velocity and output.** The quantity equation MV = PY is an identity. A theory needs assumptions about V and Y. Central bank rules such as the Taylor rule are heuristics or policy prescriptions.
  - EC.O.A4.3.1 Identity versus theory. MV = PY holds by definition of V. The quantity theory adds that V is stable and Y is set by real factors.
  - EC.O.A4.3.2 Long-run neutrality. A permanent change in the money stock changes the price level but not real output in the long run. Short-run non-neutrality is widely accepted; its size is CONTESTED.
  - EC.O.A4.3.3 Taylor principle. In standard New Keynesian models, a policy rate that rises more than one for one with inflation gives a determinate equilibrium. The result is model-relative.

- EC.O.A4.4 Open economies. **Trade gains follow from differences in opportunity cost, and trade shifts income between factors.** Comparative advantage (Ricardo): with two goods and differing opportunity costs, both countries gain from specialisation and trade. Heckscher–Ohlin and Stolper–Samuelson hold under their stated factor and technology assumptions.
  - EC.O.A4.4.1 Comparative advantage. Under Ricardo's hypotheses, each country gains by specialising in the good with lower opportunity cost, even if one country is better at both.
  - EC.O.A4.4.2 Heckscher–Ohlin. With identical technologies, identical homothetic preferences and differing factor endowments, a country exports goods intensive in its abundant factor.
  - EC.O.A4.4.3 Stolper–Samuelson. In the two-good, two-factor model with both goods produced, a rise in a good's relative price raises the real return of the factor used intensively in it and lowers the other.
  - EC.O.A4.4.4 Gravity. Bilateral trade rises with the economic size of partners and falls with distance. It is among the best-fitting empirical relations in economics (W4).

- EC.O.A4.5 Expectations and policy. **Relations that depend on expectations change when policy changes.** The Lucas critique: relations estimated under one policy regime need not hold under another if agents' expectations change.
  - EC.O.A4.5.1 Lucas critique. A reduced-form relation estimated under one policy rule cannot, without structure, predict outcomes under a different rule.
  - EC.O.A4.5.2 Time inconsistency. A policymaker with discretion may find it optimal to depart from an announced plan (Kydland–Prescott). Rules or delegation can raise welfare.
  - EC.O.A4.5.3 Rational expectations. Assuming that agents' expectations equal the model's forecast is a modelling choice. Its realism, against learning and survey evidence, is CONTESTED.

Named objects: Solow model (diminishing returns to capital, constant returns, exogenous technology), conditional convergence, endogenous growth models, expectations-augmented Phillips curve, Okun's law (empirical), quantity equation (identity), quantity theory of money, long-run neutrality, Taylor rule (heuristic), Taylor principle (New Keynesian model), Ricardian model (two goods, labour only), Heckscher–Ohlin model, Stolper–Samuelson theorem, gravity equation (empirical), Lucas critique, time-inconsistency problem, rational expectations hypothesis.

### EC.O.A5 Welfare and public choice

Situation. Societies judge and alter allocations collectively. Complication. Welfare theorems are often cited without their hypotheses, and v1 confused VAT with sales tax. Question. When is an allocation good, how can it be corrected, and can a collective choose consistently? Answer. Economics owns efficiency claims and the effects of correction. The theorems are MA, and the normative weighting is PL.

Key line (inductive; plural noun: collective judgements; dimension: which question about the allocation the claim answers; order: is it efficient, can any efficient one be reached, where markets fail, how the state corrects, how a group decides). Members (5): First welfare theorem · Second welfare theorem · Market failure · Public finance · Social choice.

- EC.O.A5.1 First welfare theorem. **Competitive equilibria are efficient when the theorem's hypotheses hold.** With complete markets, price-taking agents, locally non-satiated preferences and no externalities, every competitive equilibrium is Pareto efficient. Theorem MA; use EC.
  - EC.O.A5.1.1 Statement. Under the four hypotheses, no feasible reallocation makes someone better off without making another worse off (uses MA.B.C4).
  - EC.O.A5.1.2 Failure conditions. Dropping any hypothesis can break the result. Externalities, market power, incomplete markets and asymmetric information are the standard cases.

- EC.O.A5.2 Second welfare theorem. **Any efficient allocation can be reached by markets after the right transfers.** With convex preferences and technologies, continuity and lump-sum transfers, any Pareto-efficient allocation can be supported as a competitive equilibrium. Theorem MA; use EC.
  - EC.O.A5.2.1 Statement. Under convexity, continuity and lump-sum transfers, prices exist that support a chosen efficient allocation as an equilibrium (uses MA.B.C4).
  - EC.O.A5.2.2 Practical limit. Lump-sum transfers based on fixed traits are rarely feasible. Real transfers distort incentives, so equity and efficiency trade off.

- EC.O.A5.3 Market failure. **Where costs or benefits fall outside prices, markets misallocate.** Externalities, public goods, common pool resources. Pigouvian taxes correct an externality when its marginal damage is known.
  - EC.O.A5.3.1 Pigouvian correction. A per-unit tax equal to marginal external damage at the efficient level restores efficiency in a competitive market.
  - EC.O.A5.3.2 Public goods. For a non-rival good, efficiency needs the sum of marginal rates of substitution to equal marginal cost (Samuelson). Voluntary provision falls short.
  - EC.O.A5.3.3 Common pool resources. Open access leads to overuse. Some communities sustain resources through local rules (Ostrom), so state or private ownership is not the only remedy (impact uses EV.O.A3).

- EC.O.A5.4 Public finance. **Taxes with similar incidence can differ in how they are collected.** Taxes and spending. A VAT is levied on value added at each stage, with credit for tax paid on inputs. A retail sales tax is levied once, on the final sale. Their economic incidence can be similar, but their collection differs.
  - EC.O.A5.4.1 VAT mechanics. Each registered seller remits tax on sales minus credit for tax on inputs. The sum across stages equals tax on the final sale.
  - EC.O.A5.4.2 Single-stage sales tax. A retail sales tax falls only on final sales. Exempting business inputs must be enforced at the till, so taxed inputs can cascade (computation uses BU.O.A5.3).
  - EC.O.A5.4.3 Ramsey rule. To raise given revenue with least excess burden, commodity taxes should be higher on goods with less elastic demand, under independent demands.

- EC.O.A5.5 Social choice. **No aggregation rule meets all of Arrow's conditions together.** Arrow: with at least three alternatives and a finite set of voters, no rule satisfies unrestricted domain, weak Pareto, independence of irrelevant alternatives and non-dictatorship together. Theorem MA; the meaning for collective choice is EC; the normative argument is PL.
  - EC.O.A5.5.1 Arrow's theorem. Under the stated conditions, any rule that meets the first three is a dictatorship (uses MA.B.C4).
  - EC.O.A5.5.2 Median voter. With single-peaked preferences on one dimension, majority rule selects the median voter's ideal point (Black).
  - EC.O.A5.5.3 Manipulability. With three or more outcomes, any onto, non-dictatorial voting rule can be manipulated by some voter (Gibbard–Satterthwaite; proof MA).

Named objects: first welfare theorem (complete markets, price taking, local non-satiation, no externalities), second welfare theorem (convexity, continuity, lump-sum transfers), Pareto efficiency, Pigouvian tax (known marginal damage), Samuelson condition, common-pool governance principles, value-added tax, retail sales tax, Ramsey rule (independent demands), Arrow's impossibility theorem, median voter theorem (single-peaked, one dimension), Gibbard–Satterthwaite theorem.

## 5. Face M — Methods

| ID | Role | Shared role | Example |
|---|---|---|---|
| EC.M.1 | Model | M1 Represent, M2 Derive | specify and solve a model |
| EC.M.2 | Measure | M3 Observe | national accounts, surveys |
| EC.M.3 | Identify causes | M3 Observe (causal) | instruments, difference in differences, regression discontinuity |
| EC.M.4 | Experiment | M4 Intervene | field and laboratory experiments |
| EC.M.5 | Estimate and simulate | M5 Compute | structural estimation, DSGE |

Field examples. EC.M.1: solving a Cournot model for equilibrium output (EC.O.A2.2.3). EC.M.2: GDP by the expenditure method, and household labour force surveys. EC.M.3: difference in differences on a minimum wage change across adjacent regions (EC.O.A2.4.2). Its key hypothesis is parallel trends. An instrument must be relevant and excluded. EC.M.4: laboratory auctions testing revenue equivalence (EC.O.A3.1.3); randomised trials of commitment savings (EC.O.A1.4.2). EC.M.5: estimating demand by structural methods, or simulating a DSGE model under alternative policy rules (EC.O.A4.5.1).

### Heuristics register (outside the count)
Ceteris paribus; "follow the money"; incentives matter; there is no free lunch; the representative agent as a convenience (flagged).

## 6. Face W — Warrants

| Cell | Warrant | Standard | Typical defeaters |
|---|---|---|---|
| EC.O.A1 | W3 + W4 | experimental or revealed-preference evidence | framing effects, hypothetical bias |
| EC.O.A2 | W5 + W1 | causal identification against a derived prediction | omitted variables, misspecified market definition |
| EC.O.A3 | W1 + W3 + W6 | theorem plus experimental or comparative evidence | hypotheses not met in the field |
| EC.O.A4 | W5 + W2 | identified macro evidence; model with stated fit | Lucas critique, small samples, revisions |
| EC.O.A5 | W1 + W9 + W5 | theorem; welfare argument; identified effect | contested welfare weights |

Field examples. A1: a GARP test on household scanner data is W4; an Allais choice pair in the laboratory is W3. A2: an incidence estimate from a tax change uses W5, defeated if a concurrent shock is omitted. A3: laboratory evidence that bidders overbid in first-price auctions defeats a risk-neutral revenue-equivalence prediction. A4: a Phillips curve fitted before a regime change is defeated by the Lucas critique. A5: a Pigouvian rate rests on W5 damage estimates; the choice of social discount rate is W9.

## 7. Face B — Bridges

| ID | Field | Cells | Methods | Substrate |
|---|---|---|---|---|
| EC.B.C1 | Microeconomics | A1, A2 | M.1 | agents, markets |
| EC.B.C2 | Industrial organisation | A2.2 | M.1, M.3 | industries |
| EC.B.C3 | Labour economics | A2.4 | M.3, M.4 | workers |
| EC.B.C4 | Macroeconomics | A4 | M.2, M.5 | economies |
| EC.B.C5 | International economics | A4.4 | M.1, M.3 | trade flows |
| EC.B.C6 | Public economics | A5 | M.1, M.3 | governments |
| EC.B.C7 | Development economics | A4.1, A3.4 | M.3, M.4 | low-income economies |
| EC.B.C8 | Behavioural and experimental economics | A1.3 | M.4 | subjects (uses MS) |
| EC.B.C9 | Environmental and resource economics | A5.3 | M.1, M.3 | resources (EV owns impact) |
| EC.B.C10 | Economic history | A4 | M.2 | the past (dated facts HI) |

Field examples. C1: deriving demand from a utility function. C2: a merger review that estimates the price effect of losing a rival. C3: minimum wage and monopsony studies. C4: estimating the output effect of a policy rate change. C5: gravity estimates of a trade agreement's effect. C6: incidence of a payroll tax. C7: randomised evaluation of a cash transfer. C8: present-bias experiments. C9: setting a carbon price from damage estimates. C10: explaining an episode of hyperinflation by money growth, with dates from HI.

## 8. Assignment rules
1. Place a claim by the scale at which the allocation is settled.
2. The theorem is MA, the allocation is EC, the choice of game is ST.
3. Incidence is economics; the duty is law; the computation is business.
4. A firm's accounts and capital structure are BU. The general-equilibrium price of risk is EC.
5. A psychological mechanism is MS; its allocative effect is EC.
6. Political authority over an allocation is PO; the legal rule is LA.
7. A dated economic event is HI; the explanation of its allocation is EC.
8. A normative welfare argument is PL; the efficiency claim is EC.

## 9. Scope boundary

| Refused | Owner |
|---|---|
| proofs of equilibrium, welfare, Arrow, folk and bargaining theorems | MA.B.C4 |
| choice of game and moves that change it | ST |
| tax duty and legal rules | LA |
| firm practice, accounts, tax computation | BU |
| psychological mechanism | MS |
| normative argument about justice | PL |
| dated economic events | HI |

## 10. External crosswalk
**JEL** has 20 top-level categories, A–R plus Y and Z (checked: aeaweb.org/jel/guide).

| Category | Home | Note |
|---|---|---|
| A General and teaching | ED (teaching) | refused as cell |
| B History of thought, methodology | HI, PL | refused |
| C Mathematical and quantitative methods | Face M; MA | refused as cell |
| D Microeconomics | A1–A3 | lands |
| E Macro and monetary | A4 | lands |
| F International | A4.4 | lands |
| G Financial | A2; BU | lands, split |
| H Public | A5 | lands |
| I Health, education, welfare | B.C6 | lands as bridge |
| J Labour and demographic | A2.4 | lands |
| K Law and economics | A3.3–A3.4 | lands |
| L Industrial organisation | A2.2 | lands |
| M Business, marketing, accounting | BU | refused |
| N Economic history | B.C10 | lands as bridge |
| O Development, growth | A4.1 | lands |
| P Political economy, systems | A3.4 | lands |
| Q Agricultural, environmental | B.C9; AG, EV | lands as bridge |
| R Urban, regional, transport | substrate | refused, catalogue |
| Y Miscellaneous | — | residual, not a cell |
| Z Other special topics | — | residual, not a cell |

Coverage: 13 of 20 land (D–L, N–Q); 7 are refused (A, B, C, M, R, Y, Z).
**ANZSRC 38** (checked 9 Oct 2026 against the ABS file anzsrc2020_for.xlsx) has four groups: 3801 Applied economics → A2–A5; 3802 Econometrics → Face M; 3803 Economic theory → A1–A3; 3899 Other → not a cell. Coverage: 2 of 3 substantive groups land as cells, and 1 as method.

## 11. Validation
Sizes: key line 5. Face O 5 cells + 24 sub-cells + 67 second-level cells = 96 (A1: 4 + 10; A2: 5 + 13; A3: 5 + 15; A4: 5 + 16; A5: 5 + 13). M roles 5. Heuristics 5. W rows 5. B bridges 10.
Key line, word for word: Choice. Markets. Mechanisms and institutions. The aggregate economy. Welfare and public choice.
A-cell key lines, word for word:
- A1: Preferences and demand. Choice under risk. Behavioural departures. Intertemporal choice.
- A2: Competitive equilibrium. Market power. Information. Factor markets. Tax incidence.
- A3: Mechanism design. Bargaining. Transaction costs. Institutions. Repeated interaction.
- A4: Growth. Fluctuations. Money and inflation. Open economies. Expectations and policy.
- A5: First welfare theorem. Second welfare theorem. Market failure. Public finance. Social choice.
OPEN: microfoundations of aggregate fluctuations; the cause of the productivity slowdown; endogenous growth (EC.O.A4.1.3); sources of shocks (EC.O.A4.2.3).
CONTESTED: financial economics split between EC and BU (alternative: all to EC.O.A2); the folk theorem in A3 rather than A2; endowment effect size (EC.O.A1.3.3); monopsony relevance (EC.O.A2.4.2); institutions and growth (EC.O.A3.4.3); endogenous growth fit (EC.O.A4.1.3); size of short-run non-neutrality (EC.O.A4.3.2); rational expectations (EC.O.A4.5.3).

## 12. Registry rows

| ID | Label | Home | Uses |
|---|---|---|---|
| EC.O.A1 | Choice | O/A1 | — |
| EC.O.A1.1 | Preferences and demand | O/A1 | MA.O.A3 |
| EC.O.A1.2 | Choice under risk | O/A1 | MA.O.A5 |
| EC.O.A1.3 | Behavioural departures | O/A1 | MS.O.A1 |
| EC.O.A1.4 | Intertemporal choice | O/A1 | — |
| EC.O.A2 | Markets | O/A2 | — |
| EC.O.A2.1 | Competitive equilibrium | O/A2 | MA.B.C4, MA.O.A3 |
| EC.O.A2.2 | Market power | O/A2 | MA.B.C4, ST.O.A2 |
| EC.O.A2.3 | Information | O/A2 | MA.B.C4 |
| EC.O.A2.4 | Factor markets | O/A2 | — |
| EC.O.A2.5 | Tax incidence | O/A2 | LA, BU.O.A5 |
| EC.O.A3 | Mechanisms and institutions | O/A3 | — |
| EC.O.A3.1 | Mechanism design | O/A3 | MA.B.C4 |
| EC.O.A3.2 | Bargaining (Rubinstein) | O/A3 | MA.B.C4, ST.O.A2 |
| EC.O.A3.3 | Transaction costs (Coase) | O/A3 | LA |
| EC.O.A3.4 | Institutions | O/A3 | PO, LA |
| EC.O.A3.5 | Repeated interaction (folk theorem) | O/A3 | MA.B.C4, ST.O.A2 |
| EC.O.A4 | The aggregate economy | O/A4 | — |
| EC.O.A4.1 | Growth | O/A4 | MA.O.A4 |
| EC.O.A4.2 | Fluctuations | O/A4 | — |
| EC.O.A4.3 | Money and inflation | O/A4 | — |
| EC.O.A4.4 | Open economies | O/A4 | — |
| EC.O.A4.5 | Expectations and policy | O/A4 | — |
| EC.O.A5 | Welfare and public choice | O/A5 | — |
| EC.O.A5.1 | First welfare theorem | O/A5 | MA.B.C4 |
| EC.O.A5.2 | Second welfare theorem | O/A5 | MA.B.C4 |
| EC.O.A5.3 | Market failure | O/A5 | EV.O.A3 |
| EC.O.A5.4 | Public finance (VAT vs sales tax) | O/A5 | BU.O.A5, LA |
| EC.O.A5.5 | Social choice (Arrow) | O/A5 | MA.B.C4, PL |
| EC.O.A1.1.1 | Utility representation | O/A1 | MA.O.A3 |
| EC.O.A1.1.2 | Slutsky decomposition | O/A1 | — |
| EC.O.A1.1.3 | Revealed preference | O/A1 | MA |
| EC.O.A1.2.1 | Representation and uniqueness | O/A1 | MA.O.A5 |
| EC.O.A1.2.2 | Risk aversion | O/A1 | — |
| EC.O.A1.3.1 | Allais pattern | O/A1 | — |
| EC.O.A1.3.2 | Reference dependence | O/A1 | MS.O.A1 |
| EC.O.A1.3.3 | Endowment effect | O/A1 | — |
| EC.O.A1.4.1 | Exponential discounting | O/A1 | — |
| EC.O.A1.4.2 | Present bias | O/A1 | — |
| EC.O.A2.1.1 | Existence | O/A2 | MA.B.C4, MA.O.A3 |
| EC.O.A2.1.2 | Indeterminacy of aggregate demand | O/A2 | MA |
| EC.O.A2.1.3 | Partial equilibrium | O/A2 | — |
| EC.O.A2.2.1 | Monopoly markup | O/A2 | — |
| EC.O.A2.2.2 | Bertrand outcome | O/A2 | — |
| EC.O.A2.2.3 | Cournot outcome | O/A2 | — |
| EC.O.A2.3.1 | Unravelling | O/A2 | — |
| EC.O.A2.3.2 | Signalling | O/A2 | — |
| EC.O.A2.3.3 | Moral hazard | O/A2 | — |
| EC.O.A2.4.1 | Competitive factor pricing | O/A2 | — |
| EC.O.A2.4.2 | Monopsony | O/A2 | — |
| EC.O.A2.5.1 | Elasticity rule | O/A2 | — |
| EC.O.A2.5.2 | Excess burden | O/A2 | — |
| EC.O.A3.1.1 | Revelation principle | O/A3 | MA.B.C4 |
| EC.O.A3.1.2 | Second-price auction | O/A3 | — |
| EC.O.A3.1.3 | Revenue equivalence | O/A3 | — |
| EC.O.A3.1.4 | Bilateral trade impossibility | O/A3 | MA |
| EC.O.A3.2.1 | Unique immediate agreement | O/A3 | ST.O.A2 |
| EC.O.A3.2.2 | Patience advantage | O/A3 | — |
| EC.O.A3.2.3 | Nash bargaining solution | O/A3 | — |
| EC.O.A3.3.1 | Coase benchmark | O/A3 | — |
| EC.O.A3.3.2 | Costly exchange | O/A3 | LA |
| EC.O.A3.4.1 | Boundaries of the firm | O/A3 | — |
| EC.O.A3.4.2 | Hold-up | O/A3 | — |
| EC.O.A3.4.3 | Institutions and growth | O/A3 | — |
| EC.O.A3.5.1 | Folk theorem | O/A3 | — |
| EC.O.A3.5.2 | Finite horizon | O/A3 | — |
| EC.O.A3.5.3 | Collusion conditions | O/A3 | — |
| EC.O.A4.1.1 | Steady state | O/A4 | MA.O.A4 |
| EC.O.A4.1.2 | Conditional convergence | O/A4 | — |
| EC.O.A4.1.3 | Endogenous growth | O/A4 | — |
| EC.O.A4.2.1 | Phillips instability | O/A4 | — |
| EC.O.A4.2.2 | Okun's relation | O/A4 | — |
| EC.O.A4.2.3 | Sources of shocks | O/A4 | — |
| EC.O.A4.3.1 | Identity versus theory | O/A4 | — |
| EC.O.A4.3.2 | Long-run neutrality | O/A4 | — |
| EC.O.A4.3.3 | Taylor principle | O/A4 | — |
| EC.O.A4.4.1 | Comparative advantage | O/A4 | — |
| EC.O.A4.4.2 | Heckscher–Ohlin | O/A4 | — |
| EC.O.A4.4.3 | Stolper–Samuelson | O/A4 | — |
| EC.O.A4.4.4 | Gravity | O/A4 | — |
| EC.O.A4.5.1 | Lucas critique | O/A4 | — |
| EC.O.A4.5.2 | Time inconsistency | O/A4 | — |
| EC.O.A4.5.3 | Rational expectations | O/A4 | — |
| EC.O.A5.1.1 | Statement | O/A5 | MA.B.C4 |
| EC.O.A5.1.2 | Failure conditions | O/A5 | — |
| EC.O.A5.2.1 | Statement | O/A5 | MA.B.C4 |
| EC.O.A5.2.2 | Practical limit | O/A5 | — |
| EC.O.A5.3.1 | Pigouvian correction | O/A5 | — |
| EC.O.A5.3.2 | Public goods | O/A5 | — |
| EC.O.A5.3.3 | Common pool resources | O/A5 | EV.O.A3 |
| EC.O.A5.4.1 | VAT mechanics | O/A5 | — |
| EC.O.A5.4.2 | Single-stage sales tax | O/A5 | BU.O.A5.3 |
| EC.O.A5.4.3 | Ramsey rule | O/A5 | — |
| EC.O.A5.5.1 | Arrow's theorem | O/A5 | MA.B.C4 |
| EC.O.A5.5.2 | Median voter | O/A5 | — |
| EC.O.A5.5.3 | Manipulability | O/A5 | MA |

## 13. Self-check against R1–R12

| Rule | Result | If FAIL: sentence and repair |
|---|---|---|
| R1 | PASS | Theorem, allocation and game are separated throughout. |
| R2 | PASS | Counts in section 11 match, including 67 second-level cells. |
| R3 | PASS | Heuristics are outside the count. |
| R4 | PASS | JEL 13 of 20 (checked: aeaweb.org); ANZSRC 38 checked. |
| R5 | PASS | Hypotheses are stated for Rubinstein, the folk theorem, both welfare theorems, Coase, Arrow, Arrow–Debreu, Solow, Ricardo and the revelation principle. Modigliani–Miller is in BU. |
| R6 | PASS | Four OPEN, eight CONTESTED. |
| R7 | PASS | Members are identical in sections 2, 3 and 11. |
| R8 | PASS | Section 9. |
| R9 | PASS | First descent is complete. |
| R10 | PASS | Plain register. |
| R11 | PASS | JEL list checked against aeaweb.org. |
| R12 | PASS | IDs are stable. |
