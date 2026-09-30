this was for the end of the school year to the pub date. i really dont think it coeldve been more tahn 3 weeks


| Function | TAD2 | ERC-3643 |
|---|---|---|
| ERC-20-like security token | yes | yes |
| Transfers conditional on regulatory eligibility | `validTransfer(from,to)` | `isVerified` + `canTransfer` |
| Separate identity/eligibility contract | `MasterVerification` | `IdentityRegistry` |
| Both sender and recipient checked | yes | yes |
| Global transfer halt | `freeze()` / `unfreeze()` | `pause()` / `unpause()` |
| Forced transfer | `forceRedact()` | `forcedTransfer()` |
| Lost-key remediation | explicit key-loss workflow + forced movement | `recoveryAddress()` |
| Issuance | `allocateNewShares()` | `mint()` |
| Cancellation | `cancelShares()` | `burn()` |
| Administrative/operator roles | `peer_BT` plus compliance/onboarding/support/etc. | owner + agents |
| Address compliance state | numeric status in `MasterVerification` | Identity Registry + ONCHAINID claims |


