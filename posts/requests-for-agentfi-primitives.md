Date: 2026 May 20
# Requests for AgentFi primitives: Building a better stack

<img src="/images/agentfi-primitives-cover.png" alt="Requests for AgentFi primitives" />

There's a multi-million dollar opportunity in the answer to this question: how can you actually trust an AI agent to manage your money? Every conversation about agentic finance (AgentFi) covers the same topics: wallets, stablecoins, and payment rails. But there's a glaring problem: decision makers still don't have the tools they need to *trust* agents.

I noticed this problem most clearly a couple of weeks ago, when I went to the AI & Blockchain Redefining Markets event at Cornell Tech in NYC. More than a hundred people attended, among them wealth managers, corporate finance leaders, founders, and researchers. The main topic was the convergence of AI and blockchain. Crypto OGs were the minority in the room, something that would've been hard to imagine at a crypto event 10 years ago.

In what I can only describe as a far cry from crypto's highly scrutinized "shady" origins, I watched every executive on stage agree that crypto rails are the inevitable future of finance, and predict that agents moving money is the end state. That said, nobody complained about capital or TVL; each institutional question circled about UX, identity, regulation, standards, and compliance.

## What institutions actually ask for

The initial [adoption phase](https://www.cambrian.org/blog/agentic-finance-landscape-q1-2026#growth-metrics) of agentic finance products, particularly those focused on yield-seeking agents like [Sail](https://x.com/SaildotMoney) and [Zyfai](https://x.com/Zyfai_), has been driven by early retail customers, those Innovators with small amounts of capital. These users are typically the first wave, characterized by a higher tolerance for risk and the inherent issues of being early adopters.

<img src="/images/product-adoption-curve.png" alt="Product adoption curve for agentic finance" />

However, institutional investors operate under different considerations and risk frames, and significant progress is still required to achieve widespread adoption within the AgentFi segment. Institutions have spent 50+ years answering the following question: Should I trust this counterparty with capital? This question won't go away when the counterparty is an agent. We need to build the stack that helps answer that question.

There are still big structural issues we need to address to make AgentFi safe for institutions and welcome big waves of capital. Among them are identity, permissioned execution by agents, and a verifiable track record. We need to build a trust layer for agents that scales without intermediaries. Alongside regulation clarity that will come, marked by the GENIUS Act and CLARITY Act combo, bootstrapping innovation at scale in the US.

## The AgentFi primitives every agent will need

I still remember my 18yo self going to the bank to ask for a credit card. The bank representative looked at me and almost laughed. That day, I learned that I needed to build a reputation before they would trust me to give me a credit card.

The lesson for me came from this very early experience, but you probably know that every time someone wants to interact with the traditional finance world, there are three key questions every institution wants to answer before they trust you:

- *Who are you?* (identity, beneficial ownership, jurisdiction)
- *What do you (provably) do?* (audit trails, recordkeeping)
- *What's your history with money?* (track record, references, ODD)

The same questions we need to be able to answer for agents before we expect real-world adoption. Who is this agent? What did this agent do in the past? Does it have a good reputation? What is his history and stack? How does this agent custody users' funds?

### Identity

A traditional [KYC](https://en.wikipedia.org/wiki/Know_your_customer) process in the US requires a named legal person or entity, verification using "reliable, independent source documents", adherence to specific data points, and continuous re-verification with 5-year recordkeeping. In the same way, [KYB](https://stripe.com/en-pt/resources/more/know-your-business-kyb) requires a chain of beneficial ownership terminating in natural persons.

Verifiable, portable, and persistent identity is a key challenge to be addressed in order to bootstrap AgentFi adoption. Here is where blockchain technology stops being optional and becomes the most rational alternative to build on top.

### Permissioned execution

We have seen a lot of crazy stories about [agents deleting entire critical pieces of code](https://x.com/Osint613/status/2048888305874264484?s=20), and this won't be an exception in AgentFi if we don't have the right stack to scope their permissions. An agent should be able to execute some actions with scoped permissions.

In traditional finance, fund managers operate under an investment mandate, a set of rules that lay out how a pool of assets should be invested. Mandates might include priorities, goals, benchmarks, risks, and types of funds to be either chosen or avoided. In AgentFi, we can leverage blockchain technology to enforce a mandate with code, enabling *permissioned execution*.

Permissioned execution is the ability for an agent to act within a bounded authority that was explicitly granted by someone who has the right to grant it, and that can be verified, scoped, revoked, and audited. This can happen in two primary ways: offchain enforcement evaluates the mandate inside a vendor's infrastructure before signing, either through a policy engine like @privy_io or inside a hardware-isolated [TEE](https://en.wikipedia.org/wiki/Trusted_execution_environment) like @turnkeyhq; onchain enforcement encodes the mandate directly in smart contracts via modular accounts ([ERC-4337](https://docs.erc4337.io/index.html), [ERC-7579](https://eips.ethereum.org/EIPS/eip-7579)) and module providers like @rhinestonewtf, meaning the policy is verifiable by any counterparty, on every transaction, without trusting an intermediary.

There should also be a verifiable chain of authority. The user should be able to prove who delegated the capital, what was delegated exactly, when it happened, and the scope within which the agent can operate. Auditability should be a key feature of any agentic system that manages capital.

### Verifiable track record

Following [Resnick & Zeckhauser's framework](https://rzeckhauser.scholars.harvard.edu/sites/g/files/omnuum4441/files/rzeckhauser/files/reputation_systems.pdf), a well-designed reputation system should be able to collect, distribute, and aggregate feedback about participants' past behavior. It should have three key properties:

1. Persistence that it is tied to a stable identity
2. Observability among counterparties
3. Predictability of future behaviors based on previous ones

Track record is where traditional finance (TradFi) has the most complete and mature stack to triangulate different pieces of information to predict future behavior. If we want institutions to trust agents, we need to provide them with the information needed to answer similar questions and predict agents' trust levels based on past behavior. This includes, but is not limited to, policy adherence, volatility behavior, tail-risk exposure, operational consistency, and performance during stressed markets.

The good news is that every action an agent takes onchain is already auditable in a way no fund manager's track record is. The problem to solve isn't in recording the data, it's in building the system on top of it that packages this information for trustworthiness.

## The emerging stack

Onchain activity is already more auditable than most fund managers, but it's not yet packaged in a way compliance teams can use. Closing this gap is what the next wave of AgentFi infrastructure is being built to do. New standards, primitives, and tools are constantly being developed. I will just cover a few in this section.

### ERC-8004 — Identity and reputation

Co-authored by Coinbase, Metamask, Google, and the Ethereum Foundation, the [ERC-8004](https://www.8004.org/learn) is one of the most solid identity and reputation standards released to date and serves as an agent discovery and trust protocol.

This open protocol lets participants register agents and APIs, making them visible and portable, enabling others (either humans or agents) to discover them and decide which ones to use based on feedback from previous clients and third-party validation.

[AgentScan](https://agentscan.info/agents) reports 140k+ registered agents on the ERC-8004 protocol (72.2k active ones) and 200k+ total feedback submissions that happened onchain. For example, [Dackie](https://agentscan.info/agents/aeec9610-029c-49fc-b702-a88ce8532512) is one of the most used agents on Base. If you enter this agent's profile, you can see the owner's address, 1.5k+ reviews of this agent, a trust score derived from the available information, and more.

### ERC-4337

The key introduction behind the [ERC-4337](https://docs.erc4337.io/index.html) is account abstraction (AA). This Ethereum standard allows traditional wallets (EOAs) to behave like smart contracts, with enforced rules that allow wallets to run arbitrary logic.

EOAs can't enforce mandates because they can't run arbitrary code. ERC-4337 is what makes "the wallet refuses to sign anything that violates the policy" technically possible, enabling a whole new world of innovation with policy enforcement happening fully onchain.

An interesting point to note is that a companion standard, [ERC-7702](https://eip7702.io/), extends this further by allowing existing EOAs to temporarily adopt smart contract behavior.

### ENS — Naming layer

With ~3.5 million .eth domains, ENS (Ethereum Name Service) is the most popular and established naming layer for crypto. It maps human-readable names to addresses, content hashes, text records, and now agents' identities.

Integrated into PayPal, Venmo, Gemini, Coinbase, and the Coinbase Base App for payments, ENS is now extending its naming infrastructure to agents via [ENSIP-25](https://ens.domains/blog/post/ensip-25) and [ENSIP-26](https://discuss.ens.domains/t/ensip-26-ens-native-ai-identity/21968). ENSIP-25 introduces a standardized way to verify that an agent registered in an onchain registry like ERC-8004 is genuinely associated with an ENS name. ENSIP-26 standardizes agent context and endpoint discovery, making it composable and resolvable across different chains, enabling identity support for multichain agents.

### Agentic wallets

Acquired by Stripe in June 2025, Privy launched [Agentic wallets](https://docs.privy.io/recipes/agent-integrations/agentic-wallets) designed to enable developers to create wallets for agents with strict policy controls and security guardrails.

Agentic Wallets are promising for use cases where agents need to have the ability to transact without human intervention but under permissioned execution. Clear use cases are trading agents, portfolio managers, and automated market makers.

Under the most common policies applied to agents, we can find the following ones: transfer limits, allowlisted contracts, time-based controls, and action-specific rules.

Privy supports two primary models for agentic wallets: 1) agent-controlled, developer-owned wallets and; 2) user-owned wallets with agent signers.

### Virtuals' ACP

@virtuals_io is the largest production agent platform with onchain commerce and reputation enabled by blockchain technology. Virtuals is best known for its [Agent Commerce Protocol](https://app.virtuals.io/acp/scan) (ACP), which enables agent-to-agent commerce on Base and Solana.

With more than 400M USDC processed, ACP serves as a blockchain-enabled protocol to enable collaboration of interconnected and specialized agent clusters. Composed by an agent registry that lets developers register specialized agents plus standardized APIs and contracts that define how agents collaborate, ACP was designed to enable agents to coordinate, transact and negotiate at scale.

## The bridge is data

*Every layer of the stack we walked through together in this article depends on one thing: structured, machine-readable data that accurately captures what is happening onchain.*

The agents that get to operate with institutional scale will be the ones whose identity and track record are exposed in a language compliance teams can read. Capital was never the bottleneck, reputation and identity were, and they run on data.

Once agents have identity, permissions, and history, the missing layer is normalized data.

Fast, accurate, comprehensive, institutional-grade data that can be used by humans and agents to make accurate decisions is the foundation that will serve as the bridge to deploy capital in AgentFi at scale.

I'm proud to be working on a new data layer for humans and agents alike at @CambrianNetwork. If you want to connect, please don't hesitate to email me at [me@0xpili.xyz](mailto:me@0xpili.xyz).

---

*Special thanks to @aadopico ([@SaildotMoney](https://x.com/SaildotMoney)), @Beler, @bermchain ([@CambrianNetwork](https://x.com/CambrianNetwork)), @0xEulersID ([@gizatechxyz](https://x.com/gizatechxyz)), @0xrhota ([@CambrianNetwork](https://x.com/CambrianNetwork)) for the feedback and discussions.*
