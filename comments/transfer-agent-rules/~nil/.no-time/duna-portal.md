# WhyDRS DUNA retro-comp portal

## References

- Existing WhyDRS identity/compensation registry baseline: https://github.com/WhyDRS/DUNA-docs/blob/main/registry.md
- Stellar application-security/custody guidance: https://developers.stellar.org/docs/build/apps/application-design-considerations#application-security
- Freighter/dapp wallet-connect reference: https://developers.stellar.org/docs/build/guides/dapps/frontend-guide#interacting-with-the-stellar-network

## Goal

Build the final public WhyDRS DUNA retro-comp launch site around retroactive awards, identity proof, member accounts, balances, and onward retro-granting. It is not a job board or bounty board. The system should make completed work and the public reasoning around compensation easy to inspect, then give the recipient a direct path to authenticate, join, and claim.

The smart contract that ultimately custody/allocates awarded assets lives in a separate repository. This site should integrate with it, display its state, and initiate authenticated claim/signing flows, but should not contain the contract implementation.

## Public surface

### Completed vote / award pages

Every passed proposal should have a permanent public page. The recipient is the primary subject of the page.

The page should show:

- recipient name/handle and profile photo where available;
- award amount and awarded asset/value;
- proposal title and full proposal text;
- an embedded rendering of the actual proposal vote and final result;
- a direct link to the Discord thread/conversation for the proposal;
- linked public identities used for the recipient record, shown as recognizable badge icons;
- award/claim status;
- a prominent claim/authentication action for the recipient.

Where GitHub is one of the linked identities, use the public GitHub avatar when available. Other providers may supply a profile image through their public/OAuth profile data where permitted.

### Votes in progress

Votes that have not yet closed should also have public pages using nearly the same layout:

- proposal and requested amount;
- current embedded vote;
- recipient/proposed recipient identity card;
- attachments;
- Discord discussion link;
- current status and timing.

The public page should clearly distinguish a vote still in progress from a completed award.

### Homepage

The homepage should explain the retro-comp model, current/public votes, completed awards, and how identity claiming works. It should also expose the normal signup/login path directly, so users do not need an award link to become members.

## Identity and recipient claiming

Assume many recipients first arrive without being DUNA members. They may initially be known only through Discord, GitHub, X, or another public identity used in the proposal/vote.

A recipient claim should work as follows:

1. Open the public award page.
2. Choose one of the linked identity providers.
3. Complete that provider's OAuth flow.
4. Verify that the authenticated provider account matches the identity recorded on the award.
5. Continue into the ordinary member signup flow if the recipient is not already a member.
6. Associate the verified external identity with the member profile.
7. Require wallet/public-key control before any on-chain withdrawal.

OAuth is evidence that the person controls the linked social account; it is not a substitute for proving control of the Stellar account used to receive assets.

For external recipient records with multiple public profiles, preserve the profiles as separate identity proofs. Grants up to $200 may be claimed through an independently listed profile. If the recipient record intentionally aggregates multiple profiles for one person, require OAuth proof of a majority of the listed profiles before releasing the award.

## Member account and key model

The canonical account identifier is the member's Stellar public key.

At signup, the client should generate the member's key material and present an 18-word recovery mnemonic.

Security requirements:

- generate entropy only with a cryptographically secure random number generator;
- for a browser implementation, use the platform CSPRNG such as Web Crypto `crypto.getRandomValues`; never use `Math.random` or a home-grown PRNG;
- an 18-word BIP-39 mnemonic corresponds to 192 bits of entropy plus checksum and is acceptable for the requested recovery flow;
- generate and derive keys client-side;
- never send the mnemonic, raw entropy, Stellar secret seed, or derived private key to the application server;
- never persist them in the application database, logs, analytics, crash reports, cookies, local storage, indexed DB, or caches;
- keep secret material only transiently in memory for the generation/confirmation flow and clear references as soon as practical;
- show the mnemonic once and require a confirmation step before completion;
- store only the public key and the user's chosen public profile/account metadata.

The portal should not become a hot wallet. Normal signing should happen later through an external wallet/browser extension or, preferably, a cold/hardware wallet.

For wallet authentication, use a short-lived, single-use challenge that is signed by the wallet controlling the registered public key. The challenge should be domain-separated for this site and unusable as a transaction or authorization for any unrelated action.

## Profiles and linked accounts

Every member has a public profile.

The profile should include:

- Stellar public key as the canonical identifier;
- display name;
- profile image;
- optional bio/profile metadata;
- linked GitHub, Discord, X, and other supported identities;
- linked-account badges beside the member name;
- public awards and retro-grants;
- current claimable/retained balance where public by design.

OAuth-linked providers should be usable both to prove ownership and to fill profile data. GitHub can be the default source for a profile image when available.

## Proposal creation and voting

Authenticated members can create proposals.

Proposal composition should support:

- Markdown entry;
- plain-text entry;
- attachments up to 50 MB each;
- selection of an existing person from the member registrar;
- creation of an external proposed recipient using one or more public social profiles;
- requested award amount/asset;
- reasoning for the retroactive award;
- a Discord discussion/thread link.

Markdown rendering must be sanitized, with unsafe raw HTML/scripts disabled. Uploaded files should be handled as untrusted content.

A proposal should always be framed around completed contribution/value. The interface should not encourage "do this work and receive X" bounty behavior.

## Passed awards, balances, and claims

After a passed vote results in an allocation, the site should display the resulting award/balance from the separate contract integration.

A logged-in member should be able to:

- see each award contributing to their balance;
- see which assets their balance currently represents;
- authenticate control of their registered wallet/public key;
- claim/withdraw available assets from the contract to their wallet;
- leave assets in the contract/account balance instead of withdrawing.

The contract itself is out of scope for this repository.

## Balance asset choice

A member can choose what asset their retained balance is denominated/held in, including options such as:

- USDC;
- tokenized Treasury assets;
- supported crypto assets;
- other approved assets exposed by the contract/integration.

The member may change that choice once every 39 days.

Any investment gain or loss from the chosen asset belongs only to that member's retained balance. The UI should therefore show:

- current asset selection;
- current value;
- cost/reference basis used by the portal;
- gain/loss attributable to the account;
- the next date on which the member may change the selected asset.

## Member-funded retro-grants without a DUNA vote

A member may use their own retained balance to create a retroactive grant for another person without a DUNA vote or approval.

The flow should allow the member to:

- choose an existing registered member;
- choose/create an external recipient from public social profiles;
- enter an amount;
- enter the reason for the retroactive grant;
- submit the grant directly from their available balance.

The resulting public notice page should subtly but clearly distinguish:

- a DUNA allocation produced by a community vote; and
- an individual member's retroactive grant funded from that member's own balance.

External recipients should receive the same public identity/claim page pattern and can join the DUNA through the same claim -> OAuth -> signup -> wallet-control flow.

## Tax/document center

Authenticated users should have a document area that can generate/export records needed for tax and accounting purposes, including award/claim history and relevant asset/value information.

The exact tax forms and thresholds should remain configurable rather than hard-coded into the UI until the accounting/tax treatment is finalized.

## Navigation and account controls

The authenticated portal should include at minimum:

- Home/dashboard;
- Public votes;
- Awards;
- New proposal;
- Balance/claims;
- Member directory/profiles;
- Documents/tax;
- Account/linked identities;
- Logout;
- day/night theme toggle.

## UX principle

The public side should make governance inspectable without requiring an account. Authentication should only become necessary when a person wants to vote/create proposals, manage a profile, prove an identity, receive/claim an award, or manage a balance.

For a new recipient, the shortest intended path is:

`public award page -> verify familiar social account -> create/join member account -> register public key -> authenticate wallet -> claim or retain award`.

## Voting-threshold WhyDRS email accounts

Members who reach a DUNA-defined voting-power threshold should be entitled to a WhyDRS email account. Keep the exact threshold and eligibility rules configurable rather than fixing a number here.

Provisioning and mailbox access should be integrated into the same member portal and wallet-authenticated sign-in used for other DUNA account functions. An eligible member should be able to use their registered Stellar public key and wallet-signed authentication challenge instead of maintaining a separate email password where technically practical.

Explore taking wallet-based signing down to the mail-protocol authentication layer itself: an IMAP-compatible authentication bridge or gateway could verify a wallet-signed challenge for mailbox access, with equivalent support for SMTP submission when sending mail. IMAP does not natively define Stellar-wallet signing, so this would require an explicit authentication integration rather than assuming ordinary IMAP supports it. Keep wallet secrets client-side and never disclose them to the mail server.

Email eligibility is a voting-threshold benefit, not a prerequisite for basic DUNA membership, voting, or claiming retroactive awards.
