# DTC's DRS machine interface: ICM, DRX1/DRX5, CCF, CCF-II, and MDH

## Bottom line

DTC did not merely describe the general idea of direct registration. It defined a DTC-specific machine implementation for transmitting DRS Profile instructions into its own systems.

By 2008, that implementation was documented as a fixed-record interface built around:

- the DRS Profile business function;
- the PTS function DRSP for terminal entry;
- DRX1 and DRX5 for automated machine input;
- an Interface Control Manager (ICM) transaction format;
- CCF and CCF-II batch file transmission between participant and DTC mainframes; and
- MDH for machine-to-machine transaction processing.

This is useful as an implementation boundary. The underlying DRS concept is direct, book-entry registration on the issuer/transfer-agent books. DTC's DRSP/DRX/ICM stack is one particular infrastructure for communicating a Profile transfer instruction to DTC.

## 2008 DRX1/DRX5 guide

DTC Important Notice 3463-08 included the "DRX1/DRX5 Function User's Guide," dated May 30, 2008.

The guide states that it describes the ICM file layout for DRS and that participants use the layout to transmit DRS Profile instructions to DTCC. It expressly characterizes DRX1/DRX5 as an automated alternative to entering those instructions through the PTS function DRSP.

The guide says the function was offered over CCF, CCF-II, and MDH.

The official PDF formerly lived at:

https://www.dtcc.com/-/media/Files/pdf/2008/5/29/3463-08.pdf

That URL currently returns 404. The document remains identifiable as DTCC Important Notice 3463-08, and its text is still indexed by web search.

Related SEC rulemaking describing the same 2008 Profile enhancement project:

https://www.sec.gov/files/rules/sro/dtc/2008/34-58292.pdf

## DRX1 and DRX5

DRX1 and DRX5 were the automated input functions for sending DRS Profile requests to DTC.

The 2008 guide maps the functions to the transport mechanism as follows:

| Function | Transport | Start | Cutoff |
| --- | --- | --- | --- |
| DRX1 | MDH | 03:00 | 17:30 |
| DRX5 | CCF / CCF-II | 03:00 | 17:30 |

The guide does not print a timezone in the operating-hours table.

The important architectural point is that DRX1 and DRX5 are not definitions of direct registration itself. They are DTC machine-entry points for DRS Profile requests.

## ICM records

ICM is DTC's Interface Control Manager transaction format.

The DRX1/DRX5 guide directs participants to a separate DTC document titled:

"Interface Control Manager CCF, CCF-II And MDH User's Guide For Transaction Input"

DTC says that the ICM document establishes standards for transaction processing through DTC's automated systems, including operation, error processing, and recovery for CCF, CCF-II, and MDH transmissions.

For DRX1 and DRX5, each input record is a fixed 500-byte record:

- 26-byte standard ICM transaction header
- 474-byte DRS application-detail area

The guide describes the 26-byte header as a standard transaction header for CCF, CCF-II, and MDH. Its fields include:

| Position | Length | Field | DRS use |
| --- | ---: | --- | --- |
| 1 | 1 | Feedback indicator | left blank on input; used for processing errors |
| 2 | 1 | Test/production indicator | T or P |
| 3-8 | 6 | Record type | DRSPRT |
| 9-10 | 2 | Record suffix | 01 for the single DRS input record |
| 11-12 | 2 | Version number | identifies the record-format version |
| 13-18 | 6 | User reference number | transmitting party's transaction identifier |
| 19-26 | 8 | Addressee | participant/entity on whose behalf the transaction is processed |

The application-detail portion then carries the DRS Profile instruction itself. Fields documented in the guide include:

- DTC participant number;
- CUSIP;
- the investor's DRS account identifier at the transfer agent;
- customer tax identification information;
- registration name/address lines;
- Profile surety information;
- broker-dealer customer account information;
- share quantity; and
- later Profile-enhancement fields such as the move-all instruction.

That structure is a classic fixed-position host message. The semantic instruction is encoded as terse values at predetermined byte offsets rather than as a self-describing modern API payload.

## Output / responses

The same 2008 Important Notice also documented automated response functions.

For MDH, the response function was DRSRTN.

For CCF/CCF-II, response files were DRSRT1, DRSRT2, and DRSRT3, made available at scheduled points during the day.

The response guide says these files let participants pick up responses to DRS Profile instructions as an automated alternative to viewing the responses through PTS DRSP.

This produces a fairly clear machine workflow:

1. construct a fixed-format DRS Profile ICM input record;
2. transmit it to DTC through DRX1 or DRX5;
3. DTC processes the Profile request;
4. retrieve the resulting response through the corresponding machine-output function.

So DTC's implementation was not merely a screen layered over DRS. It defined a host-to-host protocol and record model for expressing the instruction.

## CCF

CCF means Computer-to-Computer Facility.

DTC's Settlement Service Guide defines CCF/CCF II as:

"A batch transmission system for input/output based on various protocols between a participant's mainframe and DTC's mainframe."

Bobmahalo copy:

https://github.com/bobmahalo/DTCC/blob/main/PDF%20Manuals/Rules/Settlement.md

See the glossary around the "Computer-to-Computer Facility (CCF/CCF II)" entry.

DTC's Custody Service Guide makes the operational distinction especially clear: it describes CCF as "batch files" while contrasting MDH with "real-time transaction processing."

https://github.com/bobmahalo/DTCC/blob/main/PDF%20Manuals/Other/Custody.md

Accordingly, DRX5 was the DRS Profile input route when the participant was using DTC's CCF/CCF-II batch interface.

## CCF-II

CCF-II means Computer-to-Computer Facility II.

It is the later CCF file structure. Bobmahalo's DTCC documentation notes describe CCF-II as using a different record structure and adding header/trailer organization around the detailed records.

https://github.com/bobmahalo/DTCC/blob/main/CCFII.md

Historical DTC record-layout documentation also separately identifies CCF headers and CF2 header/trailer records:

https://github.com/bobmahalo/DTCC/blob/main/PDF%20Manuals/Other/DTFPART_05_11.md

Later DTC rulemaking says CCF and CCF-II files came to be referred to collectively as "CCF Files."

See SR-DTC-2019-003:

https://www.dtcc.com/-/media/Files/Downloads/legal/rule-filings/2019/DTC/SR-DTC-2019-003.pdf

## MDH

MDH means Mainframe Dual Host.

Unlike CCF's batch-file model, DTC documentation describes MDH as a real-time transaction-processing interface.

The Custody Service Guide states:

- CCF: batch files
- MDH: real-time transaction processing
- PTS/PBS: terminal/browser interface

Source:

https://github.com/bobmahalo/DTCC/blob/main/PDF%20Manuals/Other/Custody.md

Older DTC documentation includes dedicated "MDH Transmission User Guides" describing input and output requirements for records exchanged through DTC's Mainframe Dual Host system:

https://github.com/bobmahalo/DTCC/blob/main/PDF%20Manuals/Other/10PRELIM.md

Later DTC rulemaking describes MDH as a proprietary communications protocol and removes obsolete MDH references from service documentation after support ended.

See SR-DTC-2019-003:

https://www.dtcc.com/-/media/Files/Downloads/legal/rule-filings/2019/DTC/SR-DTC-2019-003.pdf

## What DTC implemented

The resulting architecture can be represented as:

direct registration
    -> DRS Profile business instruction
        -> DRSP in PTS/PBS for interactive entry
        -> DRX1 over MDH for automated host input
        -> DRX5 over CCF/CCF-II for automated batch input
            -> fixed 500-byte ICM transaction
                -> 26-byte DTC control header
                -> 474-byte DRS Profile detail record

The important distinction is between the business concept and DTC's implementation.

Direct registration is the condition in which the investor is registered in book-entry form directly on the issuer's books maintained by its transfer agent.

DTC's Profile infrastructure defines how a broker/participant and a FAST transfer agent communicate a movement between that directly registered position and a DTC participant position through DTC's systems.

A separate DTC FAST-agent guide confirms that the underlying communication/approval does not inherently require DRSP: it says a broker may inform the transfer agent through the DRS Profile Modification function in PTS/PBS "or by other means," and that the transfer agent may agree through DRSP "or by letter or fax."

Source:

https://github.com/bobmahalo/DTCC/blob/main/PDF%20Manuals/Other/as108_ctsspfastagents_20210811.md

That language is strong evidence that DRSP/DRX/ICM is DTC's implementation of the DRS transfer workflow, not the definition of direct registration itself.

## Working characterization

A useful characterization is:

DTC implemented DRS Profile as a proprietary host-processing layer on top of the broader direct-registration concept. Its automated version relied on fixed-position ICM transaction records transported through DTC's legacy participant-mainframe interfaces. CCF/CCF-II supplied batch host-to-host input/output, while MDH supplied transaction-oriented host processing. DRX1/DRX5 were the DRS-specific machine functions carried over those channels.

That is much closer to a mainframe transaction protocol than to a modern REST-style API: the operation is represented by a fixed function identifier, environment flag, participant/addressee, and application data placed at predetermined byte positions.
