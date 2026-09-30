this was for the end of the school year to the pub date. i really dont think it coeldve been more tahn 3 weeks

## Timeline

- 2021-02-12 - Tokeny had a public T-REX standards draft on GitHub, then labeled EIP-42/ ERC-42. [Draft commit](https://github.com/TokenySolutions/EIP3643/commit/ba586663292abc41f81874330e6352d7454bc763)
- 2021-06-22 - BlockTransfer's TAD2 repository existed on GitHub; the substantive Solidity contracts and whitepaper were uploaded that morning. [Initial commit](https://github.com/blocktransfer/TAD2/commit/f93481d15123871a4245d1ca8652569e8a65e4de) [Code and whitepaper upload](https://github.com/blocktransfer/TAD2/commit/4f633fda38667a9c87c6d3f3aa68588d9c2659ed)
- 2021-07-09 - ERC-3643 was formally submitted to the Ethereum EIP process as PR #3643. [EIP PR #3643](https://github.com/ethereum/EIPs/pull/3643)
- 2023-12-12 - ERC-3643 moved to Final status. [Final-status commit](https://github.com/ethereum/ERCs/commit/4b8674884dfc8ba8ede9c5e7e39ef9ab7e766c1a)

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

