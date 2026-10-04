# SEC-related Gmail emails

Scanned **28,972** messages from the complete Gmail archive. Originally copied **24** matching messages without changing the originals; **23** are retained. The Login.gov notification (`000707`) was removed, and its metadata remains in the index for provenance. Each copy matches its enriched EML in the complete archive and preserves the original message bytes and attachments. Added `X-Original-Mbox-*` headers retain the original archive metadata.

- Direct correspondence: **10** messages with `sec.gov` or its subdomains in From, Sender, To, Cc, or Bcc email addresses.
- Related references: **14** additional messages mentioning `sec.gov`, the full Commission name, or the uppercase acronym `SEC` / `S.E.C.` in their subject or decoded plain-text/HTML body.

Brokerage and financial-app emails, promotional newsletters, and forwarded personal account notices are excluded from related references, including Wealthfront, Webull, SoFi, Moomoo/Futu, Robinhood, and tZERO. An SEC mention in a regulatory footer does not make these emails relevant. Direct SEC correspondence is retained regardless of brokerage involvement. Remaining reference matches may include quoted or forwarded SEC material and require human review. Attachment contents were not searched, though attachments remain in the copied EMLs. Dates are shown in UTC when parseable; missing timezones are interpreted as UTC. `SHA256SUMS` records checksums of the copied EML files.

## Formats

- `eml/` preserves the 23 retained original email files without changing their bytes.
- `md/` contains 23 readable Markdown conversions. The removed Login.gov notification has no retained email file or Markdown copy.

Markdown copies include message headers and the preferred plain-text body, falling back to decoded HTML text when needed. Repeated URLs appear as a single link per document; subsequent occurrences use numbered text references. Attachments are extracted into `md/` and linked from the message copies. The five image parts are byte-identical and share one extracted image. Original EMLs retain all MIME parts, HTML formatting, attachments, and archive metadata.

## Message index

The message index is chronological, oldest first, using each email’s existing `Date` header. File numbers retain the original archive order. Messages with unparseable dates appear last.

| Date | From | Recipients | Subject | Match reasons | EML | Markdown |
| --- | --- | --- | --- | --- | --- | --- |
| 2021-02-09T19:42:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com | REJECTED FORM TYPE ID-NEWCIK (9999999996-21-007841) | From SEC, sec.gov reference, Commission name, SEC acronym | [026346.eml](eml/026346.eml) | [Read](md/026346.md) |
| 2021-02-10T11:57:14+00:00 | John Wooten &lt;jfwooten4@gmail.com&gt; | jwooten31@gatech.edu | patent ip | SEC acronym | [026387.eml](eml/026387.eml) | [Read](md/026387.md) |
| 2021-02-12T14:57:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com | ACCEPTED FORM TYPE ID-NEWCIK (9999999996-21-008493) | From SEC, sec.gov reference, Commission name, SEC acronym | [026389.eml](eml/026389.eml) | [Read](md/026389.md) |
| 2021-07-20T10:08:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, sec@blocktransfer.io | SUSPENDED FORM TYPE XXXXXXXXXX (0001846058-21-000001) | From SEC, sec.gov reference, Commission name, SEC acronym | [025526.eml](eml/025526.eml) | [Read](md/025526.md) |
| 2021-07-21T15:45:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, sec@blocktransfer.io | SUSPENDED FORM TYPE XXXXXXXXXX (0001846058-21-000003) | From SEC, sec.gov reference, Commission name, SEC acronym | [025510.eml](eml/025510.eml) | [Read](md/025510.md) |
| 2021-07-21T15:50:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, sec@blocktransfer.io | SUSPENDED FORM TYPE XXXXXXXXXX (0001846058-21-000004) | From SEC, sec.gov reference, Commission name, SEC acronym | [025536.eml](eml/025536.eml) | [Read](md/025536.md) |
| 2021-07-22T14:37:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, sec@blocktransfer.io | SUSPENDED FORM TYPE XXXXXXXXXX (0001846058-21-000005) | From SEC, sec.gov reference, Commission name, SEC acronym | [025470.eml](eml/025470.eml) | [Read](md/025470.md) |
| 2021-07-22T14:39:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, sec@blocktransfer.io | SUSPENDED FORM TYPE XXXXXXXXXX (0001846058-21-000006) | From SEC, sec.gov reference, Commission name, SEC acronym | [025413.eml](eml/025413.eml) | [Read](md/025413.md) |
| 2021-08-20T14:36:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, sec@blocktransfer.io | ACCEPTED FORM TYPE TA-1 (0001846058-21-000002) | From SEC, sec.gov reference, Commission name, SEC acronym | [025255.eml](eml/025255.eml) | [Read](md/025255.md) |
| 2022-01-28T14:03:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, sec@blocktransfer.io | ACCEPTED FORM TYPE TA-2 (0001846058-22-000001) | From SEC, sec.gov reference, Commission name, SEC acronym | [022447.eml](eml/022447.eml) | [Read](md/022447.md) |
| 2022-06-05T23:01:36+00:00 | John Wooten &lt;john@blocktransfer.io&gt; | jfwooten4 &lt;jfwooten4@gmail.com&gt; | Fwd: Example, $1B lost in 2 weeks | SEC acronym | [019482.eml](eml/019482.eml) | [Read](md/019482.md) |
| 2022-06-05T23:02:10+00:00 | John Wooten &lt;john@blocktransfer.io&gt; | jfwooten4 &lt;jfwooten4@gmail.com&gt; | Fwd: Example, $1B lost in 2 weeks | SEC acronym | [019481.eml](eml/019481.eml) | [Read](md/019481.md) |
| 2022-07-03T17:27:17+00:00 | John Wooten &lt;jfwooten4@gmail.com&gt; | John Wooten &lt;jfwooten4@gmail.com&gt; | Re: | sec.gov reference | [019118.eml](eml/019118.eml) | [Read](md/019118.md) |
| 2022-07-27T19:50:00+00:00 | edgar-postmaster@sec.gov | jfwooten4@gmail.com, compliance@blocktransfer.io | ACCEPTED FORM TYPE TA-1/A (0001846058-22-000002) | From SEC, sec.gov reference, Commission name, SEC acronym | [018785.eml](eml/018785.eml) | [Read](md/018785.md) |
| 2022-10-21T13:58:40+00:00 | John Wooten &lt;jfwooten4@gmail.com&gt; | &quot;Flynn, Kelley&quot; &lt;Kelley.Flynn@lseg.com&gt; | Re: SIC(R) Web Site - Comments | sec.gov reference | [017544.eml](eml/017544.eml) | [Read](md/017544.md) |
| 2022-10-21T14:09:08+00:00 | &quot;Flynn, Kelley&quot; &lt;Kelley.Flynn@lseg.com&gt; | John Wooten &lt;jfwooten4@gmail.com&gt; | RE: SIC(R) Web Site - Comments | sec.gov reference | [017543.eml](eml/017543.eml) | [Read](md/017543.md) |
| 2022-10-21T14:36:27+00:00 | John Wooten &lt;jfwooten4@gmail.com&gt; | &quot;Flynn, Kelley&quot; &lt;Kelley.Flynn@lseg.com&gt; | Re: SIC(R) Web Site - Comments | sec.gov reference | [017542.eml](eml/017542.eml) | [Read](md/017542.md) |
| 2024-01-23T09:39:53+00:00 | John Wooten &lt;jfwooten4@gmail.com&gt; | john.wooten@blocktransfer.com | Securrency Ex | sec.gov reference | [010541.eml](eml/010541.eml) | [Read](md/010541.md) |
| 2024-03-06T21:16:14+00:00 | Stellar Community Fund &lt;noreply@dashboard.communityfund.stellar.org&gt; | jfwooten4 &lt;jfwooten4@gmail.com&gt; | SCF Submission Update | SEC acronym | [010189.eml](eml/010189.eml) | [Read](md/010189.md) |
| 2024-03-07T00:46:52+00:00 | John Wooten &lt;jfwooten4@gmail.com&gt; | john.wooten@blocktransfer.com | Fwd: SCF Submission Update | SEC acronym | [010188.eml](eml/010188.eml) | [Read](md/010188.md) |
| 2024-03-18T12:00:39+00:00 | John Wooten &lt;john.wooten@blocktransfer.com&gt; | jfwooten4@gmail.com | Following up Tues discord | SEC acronym | [010004.eml](eml/010004.eml) | [Read](md/010004.md) |
| 2025-03-12T12:33:21+00:00 | Google Alerts &lt;googlealerts-noreply@google.com&gt; | jfwooten4@gmail.com | Google Alert - &quot;BlockTrans Syndicate&quot; | SEC acronym | [008146.eml](eml/008146.eml) | [Read](md/008146.md) |
| 2025-09-09T11:01:08+00:00 | Google Alerts &lt;googlealerts-noreply@google.com&gt; | jfwooten4@gmail.com | Google Alert - &quot;BlockTrans Syndicate&quot; | SEC acronym | [005727.eml](eml/005727.eml) | [Read](md/005727.md) |
| 2026-08-20T10:16:39+00:00 | &quot;Login.gov&quot; &lt;no-reply@login.gov&gt; | jfwooten4@gmail.com | You connected your account to SEC’s Public Access Link | SEC acronym | Removed (`000707.eml`) | Not retained due to JWT |
