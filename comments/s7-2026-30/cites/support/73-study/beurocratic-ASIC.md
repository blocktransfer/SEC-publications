for the basis and prespcecitve and wrap into CCS, see senate.md

it shoeld come after the MN docs

### orig (SEC cite in CP)

BASIC AA https://www.sechistorical.org/collection/papers/1980/1984_0401_BasicTeamwork_1.pdf WHICH IS FR CP @ n.298

one option for this is te shotlink it to Jack's comment andthen to chang ethe ref after we both subti to the appendix page of WhyDCS 

then i can do thelicenect text as m appx

cite th eformal irc

### precursory annual report

https://test.sechistorical.org/collection/papers/1970/1971_0201_BasicReport.pdf

there is a lot here

it says out the groendwork for coordinated restircuting of the UCC

this is really imrptont for establishng tha power scheme inmplied _infra_ the note on ~~[dtcc copr strictoir]]~~ OCC1 n.16 link 3

## Poor Reccomnatins

### keeping transfer-agent and registrar functions seperate

this shows teh alignment form teh accoentonntns and banketrs that fifnirally benenefitted form teh gorucp

,,,'That's what the terse sentence in the February 1971 report means when it says separate registrar and transfer functions did not delay transfers enough that a “forced union is warranted.”
1969 Rockwell Study had taken the opposite direction like an intelligent human

BASIC wasn't even defending permanent institutional separation. Its underlying paper expressly contemplated one institution acting as both transfer agent and registrar, provided the registrar-like audit still occurred
the CP notes that the American Stock Exchange did not require an independent registrar at the time
Before 1971, NYSE rules required the registrar function to be performed independently of the transfer agent, whether the transfer agent was the issuer itself or an independent bank or trust company. The SEC later described that rule history explicitly.
https://www.govinfo.gov/content/pkg/FR-1984-11-27/pdf/FR-1984-11-27.pdf whic is teh same CP ref as earleire (it's at 83–84) & NYSE went the rest of the way in SR-NYSE-84-33 (CP n.298)[^1]

NEW

        Organization A
       /              \
Transfer function   Registrar function
       \              /
        internal controls
        + independent audit


this is fun becaces it gets into theverififatn of actual shaols outsatding usitnig the orverissunace rule
ofc tehre is no such restinicton on the amoune of entiitliemnts dasitirtubetd by the Custoidal STricucitrue

## Single v. Multipl CCP Subentires

SINGLE-DEPOSITORY MODEL

        CENTRAL DEPOSITORY
        ├── Bank A ........ 30
        ├── Bank B ........ 20
        ├── Broker A ...... 15
        ├── Broker B ...... 25
        └── Broker C ...... 10


TWO-MODULE MODEL

             CENTRAL DEPOSITORY
             ├── Bank A ............. 30
             ├── Bank B ............. 20
             └── BROKER MODULE ...... 50
                       │
                       ├── Broker A .. 15
                       ├── Broker B .. 25
                       └── Broker C .. 10

the mulitmodel woeld've alleviated Dentzor's conecs over the broker infireidce becaese it cagetegitarlly could limimt tehir voting power
this is backed up in teh 73 anual repontq:
> Depository Trust was created pursuant to a Memorandum of Understanding between the NYSE and other members of BASIC to transform Central Certificate Service as a _depository for broker dealers_ into a _depository for all segments of the financial industry_, to be operated under user-based ownership. The objective of expanded ownership was to give financial institutions which were potential users of the depository representation in its management and control, thereby encouraging them to deposit security certificates which they held into the depository; this would facilitate securities transactions and effect significant efficiencies by immobilizing security certificates and permitting book-entry deliveries within a computerized system.
uemphasisi odadodd
potential users of the depository is really thie likn becaes after it was lockecd in they were CUT and LOCKED with teh 94 amendments which put uveveyon in teh same boat


rest in tartoscnt

---

> [!SPECULATION]
> We wolud intoredie BASIC with VOC and creation of credit risk

docs: 

1. **Arthur D. Little, *A Securities Handling System for the 1975 Era* (Nov. 1969)** — commissioned by the NYSE. The original report was reproduced in the House's 1971 *Study of the Securities Industry* hearings at **printed pp. 2560–2595**. Its proposal divides the system into **Broker, Banking, and Custodian and Co-Transfer modules**; BASIC's retrospective reproduces that description and cites hearing p. 2562. 
   [House 1971 hearings, Part 5 — GovInfo (ADL report at pp. 2560–2595)](https://www.govinfo.gov/app/details/CHRG-92hhrg67228Op5/CHRG-92hhrg67228Op5)   ************************************todo****************************** CITE ••

2. **BASIC Task Force, *A Consideration of the Mechanics of Operation of Two Alternative Depository Systems* (Oct. 19, 1970)** — the **47-page** comparison of the modular system against one comprehensive depository. I still have **not found the standalone 47-page memorandum digitized online**. BASIC's own retrospective identifies its title, date and length and summarizes its conclusions at printed **p. 21**. 
   [BASIC — Interindustry Teamwork, discussion of the Oct. 19, 1970 memorandum](https://www.sechistorical.org/collection/papers/1980/1984_0401_BasicTeamwork_1.pdf)

3. **BASIC, *Year-End Report* (Feb. 1971)** — the public summary. Project **12, “Single Depository vs. ‘Two Module’ System,”** is on **printed p. 6** (continuing into the CSDS discussion on p. 7). It expressly describes the alternative where brokers' balances reside in a broker module that itself has an account with the central depository. ([SEC Historical Society][1])
   [BASIC February 1971 Year-End Report — direct PDF](https://www.sechistorical.org/collection/papers/1970/1971_0201_BasicReport.pdf)

the committee had made that last choice by March

[1]: https://www.sechistorical.org/collection/papers/1970/1971_0201_BasicReport.pdf "14. Organization and Operations on CSDS."
[2]: https://www.sechistorical.org/collection/papers/1980/1984_0401_BasicTeamwork_1.pdf "BASIC~ ~nterindustry Teamwork"


### The biggest difference could have been the stock-borrow/fail mechanism

The later NSCC Stock Borrow Program depended on securities that participants had **on deposit at DTC**. If one participant failed to deliver, NSCC could use securities another participant had voluntarily made available at DTC to complete the receiving side, while leaving the original failing participant's obligation open. The SEC says that program began in the **late 1970s**. ([SEC][1])

With a broker module, bank securities might instead have sat **outside the broker settlement pool**:

```text
Single DTC structure:

Bank inventory ─┐
Broker inventory├── DTC pool available to settlement mechanisms
Broker inventory┘


Two-module structure:

Bank inventory ─── Central Depository

Broker inventory ─ Broker Module ── CNS
```

Unless somebody built a very efficient cross-module borrowing interface, the broker clearing system would have had **less immediately accessible securities inventory** with which to cure temporary shortages.

That could actually have meant **more immediate broker FTDs**, or at least more pressure to buy them in, rather than fewer.

### But persistent fails might also have been harder to socialize

There's another side.

In CNS, NSCC becomes the central counterparty and converts many trades into each participant's **single net position in each security**. If somebody doesn't deliver, the result is an open CNS position; NSCC allocates the corresponding failure to receive to another member. ([SEC][1])

That structure means this:

```text
A sells to B
B sells to C
C sells to D
D sells to E
```

doesn't remain a chain of individually identifiable delivery relationships.

It gets reduced toward:

```text
NSCC

A: net deliver 100
E: net receive 100
```

If A fails, there's an **NSCC FTD/FTR**, rather than E having a direct claim against A arising from that specific trade.

A separate broker module could certainly have developed **exactly the same CNS architecture internally**, so this distinction isn't inevitable. But if the modular structure instead preserved more bilateral or exchange-specific settlement, there might have been stronger linkage between:

**the broker that failed → the particular delivery obligation → the broker that didn't receive.**

That might have created greater commercial pressure for prompt buy-ins.

### And this changes how we'd even measure the FTD problem

The SEC's public FTD series today is the **aggregate net balance of fails in NSCC CNS**. It is not a count of every individual failed trade. ([SEC][3])

If BASIC had selected the modular alternative, we might instead have ended up with:

```text
Broker-module FTDs
        +
Bank ↔ broker-module interface fails
        +
possibly bilateral institutional fails
```

rather than one dominant CNS dataset.

So something we now call **“the FTD problem” might never have emerged as a single national statistic in quite the same way**.

The most interesting counterfactual to me is therefore not *“Would there have been naked shorting?”* There almost certainly still would have been delivery failures for the same basic reasons—customers failing to deliver, inability to borrow, transfer delays, etc. The SEC still identifies all of those as ordinary sources of FTDs. ([SEC][1])

It's more:

> **Would failed delivery have become a centrally netted, fungible obligation capable of persisting inside one national clearing system, or would it have remained a more segmented obligation at broker/bank/module boundaries?**

I think **that could genuinely have developed differently**.

And there's a really interesting irony in BASIC's 1970 memorandum: one of the arguments *against* two modules was specifically that **cross-module settlement and collateral lending would be harder**. ([SEC Historical Society][2]) Those same frictions might also have prevented some of the later seamless pooling/netting mechanisms that made it possible to keep trading and crediting customer accounts while an underlying delivery obligation remained outstanding. The 2010 SEC proxy-system release expressly notes that a broker normally credits the customer's account even where the broker itself has not actually received the securities. ([SEC][4])

[1]: https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions-8 "SEC.gov | Division of Trading and Markets:"
[2]: https://www.sechistorical.org/collection/papers/1980/1984_0401_BasicTeamwork_1.pdf "BASIC~ ~nterindustry Teamwork"
[3]: https://www.sec.gov/data-research/sec-markets-data/fails-deliver-data "SEC.gov | Fails-to-Deliver Data"
[4]: https://www.sec.gov/files/litigation/litreleases/2010/34-62495.pdf "Concept Release on the U.S. Proxy System"

this all just reinforecs teh ceililng arugmunut bucucaus it's so yssymeitaclly connectied tht there is no warirning faliliover forem the berokors haveing a problm inedepnedt of the banks. a birkebelm with eth eborkecs becames a probelm ofr the banks (basdid on the dontzer gov qute -upra) which neccessitties the Fed stopiing in Title II
