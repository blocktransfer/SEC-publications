## Boni - Strategic fails 

final ver at least


The canonical reference URL is:
https://doi.org/10.1016/j.finmar.2005.11.001

cite as supra https://www.sec.gov/files/rules/petitions/2025/4865-petn-001.pdf n.6 link 1

---

there is a worknig apopr https://www.buyins.com/news/FailsPaperNov2004.pdf bit 

Yes — these are materially different versions of the same Boni paper, not just differently formatted copies.

* **Version/date:** `FailsPaperNov2004.pdf` is the November 13, 2004 working paper. The other is the published *Journal of Financial Markets* version, accepted November 8, 2005 and published as Vol. 9 (2006), pp. 1–26.  
* **Biggest addition:** the 2006 paper adds an entirely new research question: **why firms with fails-to-receive do not force delivery**. The draft says it has **three goals**; the published paper has **four**, with the new third goal devoted to this issue.  
* This becomes a new **Section 5, “Why clearing members do not force delivery,”** and adds **Tables 6 and 7**. Boni explicitly says the anonymous referee suggested examining this question. 
* The new theory is substantially stronger than the 2004 discussion of buy-ins. Boni tests four explanations and focuses especially on **reputation / reciprocity**: a firm may tolerate another firm's fail because it expects its own fails to be tolerated later — effectively a **quid pro quo**. She also tests whether underwriter relationships and geographic proximity explain tolerance of fails. 
* The resulting new empirical conclusion is that many firms allowing persistent fails are themselves failing elsewhere. Boni concludes firms may avoid becoming known for forcing delivery because they want reciprocal treatment. 
* **The main regression specification also changed.** In 2004, Table 4 is an **OLS robustness check** on fail age, with continuous variables standardized as z-scores.  In the published paper, Table 4 becomes a **Tobit regression**, which is more natural given the mass of observations censored at zero, and it adds an **unlisted-stock dummy**. 
* **Table 3 changes too.** The 2004 logits do not have an unlisted dummy. The published specification adds one because institutional-ownership data are unavailable for most unlisted stocks, so Boni wants to keep institutional ownership from inadvertently proxying for exchange-listing status. 
* That changes the interpretation of some results. The published model specifically finds that, controlling for the other variables, **unlisted stocks have older fails and are more likely to have small persistent fails, but are less likely to have threshold-sized persistent fails**. 
* There is also a noticeable **data-presentation correction**. The 2004 Table 2 reports unlisted institutional ownership as **1.3% overall / 1.6% among stocks with fails**.  The published Table 2 instead reports those cells as **NA**, explicitly explaining that institutional-ownership information is unavailable for most unlisted stocks. 
* The **headline descriptive findings barely change**: 42% of listed and 47% of unlisted issues have persistent fails of 5+ days; roughly 4% would meet the Reg SHO threshold criteria; and fails average about **5.7% of reported short interest** for listed stocks. Those conclusions survive into the published article.  
* Structurally, it goes from **four Roman-numeral sections** in the working paper to **six numbered sections** in the journal version, largely because the buy-in/goodwill analysis is promoted from a short institutional discussion into a full empirical contribution. The published introduction explicitly describes Sections 5 and 6 that did not exist separately in the draft. 

So the **important intellectual difference** is: **2004 = evidence that FTDs are strategic; 2006 = that same evidence, with improved econometrics, plus evidence that the *receiving side may also behave strategically* by tolerating FTDs as part of an informal reciprocal system.**

One odd PDF-specific difference: the 2004 file's embedded PDF **Title metadata is wrong** (`Industries, Analysts, and Price Momentum`), despite the visible document being Boni's *Strategic Delivery Failures*. The journal PDF's embedded Title is the DOI (`doi:10.1016/j.finmar.2005.11.001`).

se its a thorwaway at bost

[^boni-drafting-throwaway]: _See also_ darfting paper pubsihdd ther th eINeveisit of New Mexico as a worknig copy, AA https://www.buyins.com/news/FailsPaperNov2004.pdf


## Shapiro follow-up on Boni — concentration of fails and DTCC response

Robert J. Shapiro's March 2006 Sonecon report, *500 Million Shares of Stock Are Missing: A Report on the Impact of Allowing Stock Sales to Go Undelivered for Long Periods*, expressly builds on Boni's November 2004 work. Shapiro repeats Boni's estimate that on a typical day roughly **120–180 million listed shares** plus **300–420 million OTC/unlisted shares** had been sold but remained undelivered for at least three days, for an average of about **510 million shares**. He treats Boni as having established the breadth and persistence of FTDs, then asks a different question: **are those fails dispersed across thousands of issuers, or concentrated enough in particular issuers to matter for price formation?**

Shapiro analyzes threshold lists for three randomly selected dates — **February 15, March 22, and April 26, 2005** — together with SEC FOIA aggregate-fail data, trading volume, and short-interest data. Aggregate fails on those dates were **548.0 million, 526.8 million, and 490.4 million shares**, respectively.

His concentration estimates are striking but should be kept expressly qualified:

* about **50–80 actively traded NYSE/Nasdaq threshold securities** could account for as much as **95% of listed-company fails**, averaging about **1.5–2.0 million fails per security**;
* about **60–80 OTC threshold securities** could account for the great majority of OTC fails, averaging roughly **4.3–4.8 million fails per security**;
* his model estimated that **10 or fewer listed threshold securities might account for roughly two-thirds of listed fails**, and **20 or fewer for about three-quarters**;
* he estimated perhaps **15–33 listed companies** and **27–45 OTC companies** could each have more than **one million failed shares** on a given day;
* among the 30 listed threshold stocks with the highest estimated fails on February 15, **12 (40%)** were still threshold securities on both March 22 and April 26.

The major caveat is important for drafting: **Shapiro did not have issuer-by-issuer DTCC fail data and did not independently observe the cause of each fail.** His individual-company figures were modeled from aggregate SEC fail totals, trading volume, and short interest. Shapiro himself says the exact relationship cannot be established with certainty without more detailed security-level data and calls the quantitative estimates tentative. So this is much safer as evidence of **possible concentration and persistence of FTDs** than as proof that every failed share was a naked short.

### DTCC's contemporaneous response

A HedgeWorld article published March 16, 2006 reports that DTCC prepared a response on **March 15, 2006** identifying what it considered flaws in Shapiro's report. The surviving copy is a repost of the contemporary article, not a DTCC-primary-source webpage.

DTCC's principal responses were:

* **FTD is not synonymous with naked short.** DTCC said fails can arise from causes other than short selling, including customer-delivery and operational problems.
* **Buy-in authority:** DTCC rejected Shapiro's claim that it could simply cure extended fails by buying shares in and charging the failing broker, saying the SEC had repeatedly stated that DTCC did not possess the regulatory authority Shapiro attributed to it.
* **Regulation SHO:** DTCC said SHO had reduced outstanding fails, citing about a **10% reduction in aggregate fails** and a **32% reduction in fails involving threshold-list companies** during the first three months.
* **Causal data:** DTCC stated: **"While we have data on the volume of fails, we have no information on the underlying causes of those fails."** That distinction is useful: DTCC acknowledged security-level fail-volume information while disputing that those data alone identify whether a fail arose from a naked short, long sale, operational delay, or another cause.
* **Transparency:** DTCC also argued that fail data could be used for market manipulation and therefore defended limits on disclosure.
* **Shapiro's role:** DTCC pointed out that Shapiro was a paid consultant to law firms pursuing claims involving DTCC. That is relevant background but does not itself answer the empirical concentration analysis.

This makes the Shapiro/DTCC exchange useful as a direct extension of the Boni notes: **Boni documents persistent delivery failures; Shapiro tries to estimate whether they are concentrated; DTCC challenges both the naked-short causal inference and Shapiro's proposed remedy, while acknowledging that it has fail-volume data but not the underlying cause of each fail.**

### Sources

* Shapiro, *500 Million Shares of Stock Are Missing* (Sonecon, Mar. 2006):  
  https://nakedtruth.info/wp-content/uploads/2021/09/500-Million-Shares-of-Stock-Are-Missing-Robert-Shapiro-March-2006.pdf
* Contemporary HedgeWorld report reproducing DTCC's March 15, 2006 response:  
  https://investorshub.advfn.com/boards/read_msg.aspx?message_id=28318142
* Shapiro's later Sept. 14, 2006 Regulation SHO comment, File No. S7-12-06 (SEC-hosted):  
  https://www.sec.gov/comments/s7-12-06/rjshapiro5967.pdf
