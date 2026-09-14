https://discord.com/channels/1102309240145707049/1223618394570494013
scr of form

The archive documents a market structure in which individual investors usually are not registered owners, unsettled positions can persist inside a netting system, public fail data conceal the age and origin of failures, and voting entitlements can diverge from customer account records. Those mechanics create serious transparency and accountability questions even without proof of misconduct.

## 1. DTC acknowledged that its own rules could obstruct oversight of indirect participants

This is the strongest current governance finding. In 2026, DTC stated that Rule 2 contained language that could prevent it from obtaining information needed to identify, monitor, and manage risks posed by indirect participants. The rule had expressly excluded records concerning a participant's customers, their accounts, and their market activity from DTC's inspection authority. DTC removed that restriction to comply more fully with the covered-clearing-agency risk standard.

Why it matters: the central securities depository said a longstanding provision could complicate its ability to see risks created below the direct-participant level. That is evidence of a real oversight blind spot, although the 2026 amendment is also evidence that the gap was addressed prospectively.

Vault evidence: `PDF Manuals/Rules/dtc_rules.md`, supplemented by the later rule filing.

## 2. The proxy system can credit customers with shares that the broker has not received—and then ration the associated votes

The SEC documented that a broker with a fail-to-receive position will usually credit the customer's account on settlement date even though DTC has not credited the broker with the securities or voting entitlement. If that imbalance survives through a voting record date, the broker may have more customer voting instructions than DTC-recognized votes. The SEC also explained that securities lending can produce the same imbalance because shares are held in fungible bulk and it may be unclear which customer lost the vote.

At the time of the SEC's 2010 review, neither SEC nor SRO rules mandated a particular reconciliation or allocation method. Depending on the method a broker chose, some customers who submitted voting instructions could receive fewer votes than their account position implied.

Why it matters: an account statement can show an economic position without guaranteeing a matching, independently traceable vote at the issuer. This is a concrete investor-rights problem documented by the regulator itself. The archive does not establish whether later reforms have eliminated every form of this problem.

Vault evidence: `Overvoting.md`, `FTD.md`, `Share Lending.md`, and `Fungible bulk.md`.

## 3. Public fail-to-deliver data cannot reveal how old a fail is, who caused it, or whether successive totals contain the same failures

The SEC publishes only the aggregate net fail balance for each security and settlement date across all NSCC members. It warns that the data do not identify the age of failures and that the underlying sources may change from one day to the next. The SEC also disclaims any guarantee of data accuracy.

Why it matters: the public can observe that fails exist but cannot use the published dataset alone to determine duration, responsible member, originating transaction, long-versus-short-sale source, or whether a chronic-looking total is one old obligation or a changing pool of new failures. This sharply limits outside scrutiny. It also means the data cannot, by themselves, prove abusive or naked short selling.

Vault evidence: `FTD.md`, `Naked Short.md`, `Close Out.md`, and `Rule 203.md`.

## 4. CNS normalizes persistence by netting and carrying failed positions forward instead of preserving a trade-by-trade chain

NSCC Rule 11 describes prior long and short positions as being brought forward on a perpetual basis, merged with new activity, netted, and carried forward, leaving failed deliveries or receipts in each member's account. NSCC becomes the central counterparty, replacing the original broker-to-broker obligation with member-to-NSCC positions. Its allocation process then distributes available securities according to priority groups, position age, and—in ties—daily random numbers.

Why it matters: CNS is designed to reduce risk and settlement traffic, but it also breaks the public-facing link between a particular failed delivery and its original counterparty. A fail becomes part of a rolling net position rather than a transparent, trade-specific chain. Read together with the limitations of the SEC dataset, this makes persistent settlement problems difficult for issuers and investors to reconstruct from public information.

Vault evidence: `CNS.md`, `PDF Manuals/Rules/nscc_rules.md` at Rule 11 and Procedure VII, and `PDF Manuals/CNS/cns182_allocation_priority_order_2023Oct26.md` at pages 1–2.

## 5. Members can control whether available securities are automatically delivered to satisfy CNS shorts

The archived 2022 CNS exemptions manual says a member could direct NSCC not to settle part or all of a short position, including withholding delivery during both night and day cycles. DTCC's current CNS page still states that members may use exemptions to control automatic delivery from their DTC accounts, including partial settlement.

The material should not be described as an unrestricted loophole: DTCC says exemptions serve legitimate purposes such as avoiding segregation violations and meeting other delivery needs. The mechanism is also changing. Level 2 exemption processing has been discontinued, while Level 1 processing is being migrated to DTC's delivery-authorization system; the final decommission date has not yet been set.

Why it matters: even when securities exist in a member's DTC account, delivery against a CNS short is not always mechanically unavoidable. A serious oversight inquiry should ask how often authorization or exemption controls delay settlement, for how long, for which securities, and under what compliance justification.

Vault evidence: `PDF Manuals/CNS/cns183_exemptions_2023Oct26.md` at pages 1–3 and `PDF Manuals/Rules/nscc_rules.md` at Procedure VII.

> exemptions are elections provided by each [[Member]] that controls the delivery of all or part of any short position. This exemption instruction applies to any short positions the [[Member]] has on their [[CNS]] Projection Report: AutoRoute 02042022 file / AutoRoute 02040009 report, issued the day before the [[settlement]] date. By indicating a particular quantity as an exemption, the [[Member]] directs [[The Corporation]] not to settle certain short positions or portions thereof

## 6. Most investors depend on a layered ownership ledger rather than appearing on the issuer's register

The SEC explains that most investors are beneficial owners holding through brokers or banks. Securities deposited at DTC are registered to DTC's nominee, Cede & Co.; DTC participants hold pro rata positions in fungible bulk, and their customers hold pro rata interests through those participants. Individual shares are not specifically identifiable within that bulk.

Why it matters: ownership evidence, voting, corporate-action distributions, and reconciliation depend on a chain of intermediaries whose internal customer records sit below the issuer and DTC ledgers. This structure does not itself create extra shares, but it explains how a customer's account entitlement can diverge temporarily from securities actually credited at DTC. Direct registration is the clearest structural alternative because the investor appears on the issuer's books through its transfer agent.

Vault evidence: `street name.md`, `Cede & Co.md`, `Beneficial Owner.md`, `Fungible bulk.md`, `Direct Registration.md`, and `DRS.md`.

## 7. DTCC is a user-owned utility serving—and owned by—the institutions it regulates operationally

DTCC describes itself as owned by its users, including broker-dealers, banks, investment managers, and other financial institutions. Full participants or members are owners, and DTCC generally returns volume-related excess revenue through rebates or fee reductions.

Why it matters: this is not proof of regulatory capture or improper conduct. It is, however, an inherent governance tension worth examining because the firms subject to membership rules and operational controls collectively own the infrastructure. The relevant questions are whether public, issuer, and retail-investor interests have sufficient independent representation; how conflicts are managed; and whether enforcement and disclosure incentives are strong enough when they impose costs on owners.

Vault evidence: `DTCC.md`, `NSCC.md`, and `DTC.md`.

## Primary sources

- [DTC's 2026 rule filing on its former indirect-participant information restriction](https://www.sec.gov/rules-regulations/self-regulatory-organization-rulemaking/sr-dtc-2026-005)
- [SEC concept release describing securities-lending, fail-to-deliver, and vote-reconciliation problems](https://www.sec.gov/rules/concept/2010/34-62495fr.pdf)
- [SEC fails-to-deliver dataset and limitations](https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data)
- [DTCC description of CNS netting, open fails, exemptions, and corporate-action accounting](https://www.dtcc.com/clearing-and-settlement-services/equities-clearing-services/cns)
- [DTCC's 2026 update on CNS exemption decommissioning and migration](https://www.dtcc.com/-/media/Files/Downloads/Transformation/CNS-Exemptions.pdf)
- [SEC staff explanation of DTC, Cede & Co., beneficial ownership, and fungible bulk](https://www.sec.gov/rules-regulations/staff-guidance/staff-legal-bulletins/shareholder-proposals-staff-legal-bulletin-no-14f-cf)
- [Investor.gov explanation of street-name, direct-registration, and physical-certificate holding](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-97)
- [DTCC guide describing its user-owned utility structure](https://www.dtcc.com/-/media/Files/Downloads/Press-Room/DTCC-Clearance-Settlement-Interactive-2021.pdf)
