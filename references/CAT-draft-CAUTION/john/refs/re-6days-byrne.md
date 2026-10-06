from https://patentimages.storage.googleapis.com/00/42/44/8382cc8b4b0898/US20160234026A1.pdf
per https://discord.com/channels/1102309240145707049/1102309241026515066/1516201737256697877

---

Direct quotes from the patent regarding FIX:

**General role of FIX, ¶ 23:**

> “For example, one protocol is the Financial Information eXchange protocol or ‘FIX’ protocol.”

> “Messages in the FIX protocol are used in many examples in the present disclosure.”

> “However, the Crypto Integration Platform can receive and transform messages in protocols other than the FIX protocol to be consummated using cryptographic techniques.” 

**Broker-dealer orders, ¶ 31:**

> “The orders sent by broker-dealer(s) 115 may use the FIX protocol or other protocols and/or formats.” 

**Translation by the Crypto Adapter, ¶ 33:**

> “The orders are received by Crypto Adapter 130 in a conventional protocol/format commonly used by broker-dealer(s) 115 (e.g., FIX messages).”

> “Crypto Adapter 130 translates the orders into cryptographic transactions...” 

**Linking the FIX order to the customer’s crypto authorization, ¶ 33:**

> “[The Crypto Adapter] verifies that the cryptographic transaction is authorized by the same customer authorizing the FIX order.” 

**ATS use, ¶ 36:**

> “ATS(s) 150 receive digitally signed FIX orders from Crypto Integration Platform 125, find potential buy/sell order matches to trade digital assets, and contain a state of the order book which records the state of the orders.” 

**Broker workflow shown in Figure 5:**

> “Receive Order from Customer”
> “Send FIX Order To Crypto Integration Platform”
> “Receive Execution Reports” 

**Comparing FIX and blockchain signatures, ¶ 82:**

> “By verifying that the FIX order transaction was signed by the same party as the crypto committed transaction, the Crypto Integration Platform can provide certainty that the FIX order transaction is associated with the committed transaction and therefore that the asset is available for the transaction.” 

**Execution report after acceptance, ¶ 83:**

> “The Crypto Adapter maps the order identifier to the crypto commitment transaction hash.”

> “Next, assuming success … the Crypto Adapter creates an execution report indicating that the order is pending and issues the execution report to the broker-dealer.” 

So FIX remains the **broker/ATS order and reporting protocol**. The platform adds signatures, wallet commitments, ledger transactions, and hashes behind that conventional FIX workflow.
