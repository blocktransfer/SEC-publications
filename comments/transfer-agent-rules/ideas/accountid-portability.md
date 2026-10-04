# Cross-agent AccountID portability

[Response 8](../../../examinations/response-8/README.md), note `[^psnause]`, already records the intended distinction between organization-scoped identity-provider identifiers and a portable `AccountID`. It explains that Persona IDs are unique within an organization's Persona instance and therefore cannot be easily shared between transfer agents, unlike an `AccountID`.

Use this as a basis for the transfer-agent rulemaking argument that investor identity should not be trapped inside each agent's proprietary onboarding stack. A portable account identifier could let multiple transfer agents reference the same investor identity record while each agent continues to maintain its own books, permissions, holdings, and compliance records.

The current repositories establish the intended cross-agent portability of `AccountID`, but do not yet appear to state a formal global-uniqueness rule. Any proposal should distinguish those two points: portability is already part of the design; generation, collision resistance, verification, governance, and whether an `AccountID` is globally unique across all participating agents still need an explicit interoperable standard.
