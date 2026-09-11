# Findings


I. Deficiencies

A. 

## physical address not  current

Form TA-1 - Application for Registration of Transfer Agents

Rule 17Ac2-1(a) under the Exchange Act states that an application for registration, pursuant tosection 17A(c) of the [Exchange] Act, of a transfer agent for which the Commission is theappropriate regulatory agency, as defined in section 3(a)(34)(B) of the Act, shall be filed with theCommission on Form TA-1, in accordance with the instructions contained therein.

Rule 17Ac2-1(c) under the Exchange Act requires that a registrant file an amendment to FormTA-1 within sixty days following the date on which the information in the submitted Form TA-1becomes inaccurate, misleading, or incomplete.

The instructions for Form TA-1 disclose that a filer should “State in Question 3.c. the full address ofthe registrant’s principal office where transfer agent activities are, or will be, performed.”BlockTrans’s current Form TA-1/A, dated September 25, 2023, reflects a principal office address of99 Wall Street #4640, New York, NY 10005 (“99 Wall Street”). The Staff’s discussions with theRegistrant revealed that the 99 Wall Street address is the location of a virtual business addressservice, PhysicalAddress.com (“PhysicalAddress”), that receives/handles mail for clients.
BlockTrans does not maintain any personnel at that location. Likewise, it does not appear thatBlockTrans performs any transfer agent activities at that location.

Consequently, it appears that BlockTrans’s Form TA-1/A dated September 25, 2023, contained inaccurate information as to the Registrant’s principal office and the Registrant failed to file an amendment within the timeframe specified by the Rule.

As such, BlockTrans is not in compliance with Rule 17Ac2-1(c) under the Exchange Act




## MSF Items


B. Maintenance of Master Securityholder File

Rule 17Ad-10(a)(1) under the Exchange Act states that every recordkeeping transfer agent shall promptly and accurately post to the master securityholder file debit and credits containing minimumand appropriate certificate detail representing every security transferred, purchased, redeemed orissued[^1]

[^1]: can do a good usbsection here with IL and cede setup]


Rule 17Ad-10(b) under the Exchange Act states that every recordkeeping transfer agent shall maintain and keep current an accurate master securityholder file and subsidiary files. If such transferagent has any record difference, its master securityholder file and subsidiary files must accuratelyrepresent all relevant debits and credits until the record differences is resolved. The recordkeeping transfer agent shall exercise diligent and continuous attention to resolve all record differences.

The Staff discovered the following exceptions during its review of the Laylor Corporation (“Laylor”) master securityholder file for the period of September 2023 through April 2025:


1. First Last (“Investor A”): In an email dated September 28, 2023, Laylor’s President, authorized the issuance of 100,000 shares to Investor A. While some of the certificate detail required under Rule 17Ad-9(a)(2) and (5) under the Exchange Act appears in the Legacy Database, as evidenced in the excel spreadsheet of its output, BlockTrans did not post the credit of 100,000 shares to the blockchain portion of the Master Securityholder File (“MSF”) for the issuance to this securityholder.

Pursuant to Rule 17Ad-10(a)(2)(i) under the Exchange Act, recordkeeping transfer agentsmust post credits containing minimum and appropriate certificate detail within 30 days after issuance. As the authorization for the issuance of Investor A’s shares is dated September 28, 2023, BlockTrans should have posted the credit of 100,000 shares to the MSF by October 28, 2023.

In addition, the Staff’s review of the information maintained on the Legacy Database for Investor A disclosed that the data populating the “from” column (column J) reflected the Memo (HASH) from the transaction issuing another investor’s 300,000 shares. As a result, it appears that this data was mistakenly linked to Investor A’s certificate detail.[^2]

[^2]: subsubsection with start of issue auth convo...]



2. First Last (“Investor B”): This securityholder’s 1 million shares were revoked/cancelled on December 8, 2023, as a result of the clawback by the issuer. The shares were subsequently re-issued to Investor B pursuant to an email authorization from Laylor to BlockTrans on February 26, 2024. However, the Staff’s review of the information maintained on the Legacy Database for Investor B disclosed that the issue date (“aqAt”), reflected in “holdings” column (column k) corresponded to the original establishment of the cancelled position on September 11, 2023, not February 26, 2024 (authorization date) or March 21, 2024 (date of transaction on the Stellar blockchain)[^3]

[^3]: DB design and good catch on the blockchain side..]




Therefore, BlockTrans is not in compliance with Rule 17Ad-10(a) under the Exchange Act for failing to post the credit of 100,000 shares to the blockchain for the issuance to Investor A within the 30-day time frame, as well as for posting inaccurate certificate detail to the MSF for both Investors A and B.

Moreover, BlockTrans is not in compliance with Rule 17Ad-10(b) under the Exchange Act sincethese discrepancies caused BlockTrans’s MSF for Laylor to be inaccurate during the period of September 2023 through April 2025.


## control book items

C. Maintenance of Control Book

Rule 17Ad-10(e) under the Exchange Act states that every recordkeeping transfer agent shallmaintain and keep current an accurate control book for each issue of securities. A change in the control book shall not be made except upon written authorization from a duly authorized agent of the issuer. Rule 17Ad-9(d) under the Exchange Act defines a control book as a record or other document that shows the total number of shares authorized and issued by the issuer.

As noted above, the issuer's email of September 28, 2023, authorized the issuance of 100,000 shares to Investor A. The Registrant’s failure to post a credit for these shares to the blockchain portion of  the MSF resulted in understatement of Laylor’s issued share amount by 100,000 shares. Consequently, Laylor’s issued amount reflected on its Control Book was understated by 100,000 shares during the period of October 2023 through April 2025.

Therefore, BlockTrans is not in compliance with Rule 17Ad-10(e) under the Exchange Act for failing to maintain and keep current an accurate control book for Laylor.



# II. Weaknesses in Internal Controls, Supervisory Procedures, and Operational
Processes

## A. Written Procedures

### chacnged / neww identity  provider

Anti-Money Laundering (AML) Policy – BlockTrans’s AML Policy reflects the use ofthe Persona platform in its Client Identity Verification process. BlockTrans currentlydocuments its verification process by adding an internal reference to the Persona account number (the “PSNA Reference”) within the securityholder’s Personally Identifiable Information (“PII”). However, BlockTrans ceased using Persona during 2025 because of limitations of the screening application and costs of the service.

 Therefore, BlockTrans should update its AML Policy to reflect its new process for performing and documenting client identity verification


### Cancellation and Destruction of Securities Certificates

BlockTrans does not currently have written procedures pertaining to the cancellation and/or destruction of securities certificates. Rule 17Ad-19(b) under the Exchange Act requires every transfer agent involved in the handling, processing, or storage of securities certificates to establish and implement written procedures for the cancellation, storage, transportation, destruction, or other disposition of securities certificate. While the Registrant’s business model focuses on uncertificated shares, the Agreement for Transfer Services between BlockTrans and Laylor, dated June 30, 2023, instructed investors to mail prior physical stock certificates to BlockTrans for destruction. Even though BlockTrans did not receive any securities certificates during the Staff’s review period, it should establish written procedures for the cancellation and/or destruction of securities certificates in accordance with the Rule in the event that it does receive them. 



### Lost Securityholder Search Evidence

The Staff’s review of BlockTrans’s Unresponsive orLost User Policy disclosed that it does not require BlockTrans to maintain evidence of the specific search terms, search results, or screenshots/summaries of reports generated by
the search engines used. As a result, BlockTrans did not maintain such documentation.

Consequently, BlockTrans’s written procedures did not appear to be adequately designed to demonstrate compliance with the requirements of the Rule. During the examination, the Registrant took steps to update its written procedures for Unresponsive or Lost User to incorporate requirements to document each search with comprehensive screenshots orgenerated reports that include the search date, search terms, and U.S. - based personal
identifiers


### Mail Handling (Safeguarding of Securities) 

The Staff’s discussions with BlockTransdisclosed that it currently uses PhysicalAddress for receipt and handling of its mail. PhysicalAddress scans envelopes received at the 99 Wall Street address for the Registrant and posts them on its platform for review by BlockTrans. The Registrant will then instruct PhysicalAddress on how to handle the item (i.e., forward, open/scan to pdf, or shred). However, BlockTrans has not established written procedures to define what category/type of mail should receive which treatment.

Rule 17Ad-12(a) under the Exchange Act states that any registered transfer agent that hascustody or possession of any funds or securities related to its transfer agent activities shall assure that (1) all such securities are held in safekeeping and handled, in light of all facts and circumstances, in a manner reasonably free from risk of theft, loss or destruction. As noted above, securityholders had been instructed to mail physical stock certificates to BlockTrans.


Although the Registrant has not received any physical certificates at the 99 Wall Street address, BlockTrans’ failure to have a documented methodology for handling different categories/types of mail received at a virtual business address appears to be an internal control weakness.


## B. MSF Certificate Detail


### Securities  Cancellation Dates

This information is required as part of the minimum certificate detail pursuant to Rule 17Ad-9(a) under the Exchange Act. Cancellation dates are reflected on the Stellar blockchain and for securityholders who opened Accounts/Wallets on Stellar (the “Stellar Accounts”) are readily obtainable. However, for those securityholders without Stellar Accounts whose shares are held in the “Distribution Account”, there is no clear audit trail that records the number of shares cancelled by securityholder or the date of cancellation. To obtain this information on a securityholder level, BlockTrans would have to review several sources to determine the number of shares cancelled and the cancel date.

As a result, BlockTrans does not maintain or have readily accessible the cancellation dates or share amounts for cancelled securities of securityholders allocating to the Distribution Account.


### Deleted Certificate Detail

#### backups in CRON and pen...

For those securityholders who don’t maintain StellarAccounts, the Registrant will manually delete certificate detail for cancelled securities. At present, deleted certificate detail for these securityholders would be reflected in backup files maintained by BlockTrans. However, the Registrant does not have a process to back-up and maintain the certificate detail for these securityholders which resides in the Legacy Database.

Rule 17Ad-10(f) under the Exchange Act states that every recordkeeping transfer agentshall retain a record of all certificate detail deleted from the master securityholder file for a period of six years from the date of deletion. In lieu of maintaining a hard copy, a recordkeeping transfer agent may comply with this paragraph by complying with §240.17Ad-7(f) or §240.17Ad-7(g).

BlockTrans’ failure to establish a process to ensure that back-up files of the Legacy Database are maintained is an internal control weakness, as such process could ensure that BlockTrans maintains a record of certificate detail deleted from the MSF as required by Rule 17Ad-10(f) under the Exchange Act.



## OFAC Searches

C. U.S. Department of Treasury – Office of Foreign Assets Control (“OFAC”) –

BlockTrans Does Not Maintain or Implement Written Procedures Related to Its OFAC Searches



Every person or business in the U.S., including all securities transfer agents, must monitor transactions to blocked countries, and to certain identified individuals, by comparing and matching information against current lists (www.treas.gov/ofac) maintained by OFAC.

The Staff’s review of BlockTrans’s procedures revealed that the Registrant does not address OFAC compliance. However, the Registrant verbally disclosed that it utilized the Persona platform for screening against OFAC’s list of specially designated nationals (“SDNs”), which was evidenced by adding a PSNA Reference within the securityholder’s PII. However, the Staff’s review of the output from the Legacy Database disclosed two securityholders, Investors C and D, whose PII did not include a PSNA Reference, indicating they had not been screened.
Further, based on the Staff’s conversations with BlockTrans, it appears that these screenings were performed only at the time a securityholder was onboarded, rather than periodically which would be more prudent for a dynamic list like OFAC’s SDNs.

Therefore, BlockTrans’ failure to maintain written procedures addressing OFAC regulations, and to conduct OFAC searches for these two securityholders is an internal control weakness.

BlockTrans could consult OFAC’s website at http://home.treasury.gov/policy-issues/office-of-foreign-assets-control-sanctions-programs-and-information to review its obligations underOFAC’s mandate and make any changes deemed by the Firm to be necessary for compliance.


