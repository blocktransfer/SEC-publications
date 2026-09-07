# Lost securityholder identity permanence

Source: https://github.com/JFWooten4/WhyDRS-Comments/issues/1

For the 17 CFR 240.17Ad-17 argument, develop the point that maintaining a permanent or mailing address has a materially higher ongoing cost than maintaining a blockchain address. Use that comparison to extend the concept from a "permanent address" toward a more persistent investor identity.

A blockchain address or public key can be treated as a durable identifier in the investor record and associated with the investor's Syndicate ID. Keep the example compact: at most one footnote showing an explicit public key recorded with, and cross-referenced to, its Syndicate ID.

Related dependency: migrate the paragraph (d) procedures into the open-source compliance website so the procedures can be cited directly in a footnote for self-reference, transparency, auditability, and education.

## Inactivity, contact failure, and escheatment

The existing public lost-investor procedures already implement this theory operationally. After three years without qualifying activity, the agent emails the owner to confirm continued engagement; on-chain activity associated with the user's public key counts as activity. This is better framed as a contact-risk trigger than as proof that an investor has disappeared. See https://github.com/blocktransfer/website/blob/main/compliance/team/lost-investor-searches.html.

Connect this to the prior Carvana example. In *Koeppen v. Carvana, LLC*, No. 21-cv-01951-TSH (N.D. Cal. Aug. 22, 2024), the settlement administrator began with the most recent mailing addresses in Carvana's records. Of 1,540 mailed notices, 220 were returned undeliverable; skip tracing found updated addresses for 175, while 45 ultimately remained undeliverable. The settlement also provided that checks returned as undeliverable or left uncashed for 180 days would be cancelled and the associated funds tendered to the California State Controller as unclaimed property in the class member's name. See https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_21-cv-01951/pdf/USCOURTS-cand-3_21-cv-01951-1.pdf#page=5 and https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_21-cv-01951/pdf/USCOURTS-cand-3_21-cv-01951-1.pdf#page=4.

The Carvana example is not a 17Ad-17 timing rule; it illustrates the operational consequence of stale physical contact information. A persistent public-key-linked identity can provide an additional durable activity signal and contact reference before ordinary address failure cascades into lost-owner searches and state unclaimed-property handling.
