# XColos - The AI Colosseum

**AI-Powered Game Orchestration Platform: Benchmarking, Hybrid Play, & Human-in-the-Loop Coaching**

> This document is the author's original project overview, preserved as written.
> Design discussion and technical decisions live in separate documents under `design/`.

---

## 1. Executive Summary & Product Vision

This document details the high-level architecture and system specification for a developer-centric AI game runtime engine designed for extensible social deduction and strategy simulations. The platform prioritizes Plug-and-Play AI integration and robust human-in-the-loop coaching capabilities.

By strictly decoupling game state management from agent cognition, the system enables developers to swap arbitrary LLM endpoints—cloud-hosted, local open-weights, or custom webhooks—while providing supervisors with real-time monitoring and intervention tools to guide agent behavior in games like Mafia and Werewolf.

## 2. Primary Use Cases

### Use Case 1: Automated AI Benchmarks & Model Tournaments

Researchers and developers configure games via YAML (e.g., 7-Player Secret Hitler) and assign different models (GPT-4o, Claude 3.5 Sonnet, DeepSeek, Llama 3) to each seat. The engine executes matches at high speed in headless mode to benchmark model reasoning, deception, and negotiation abilities.

### Use Case 2: Hybrid Human-AI Social Gaming

Casual players or content streamers launch a lobby where 1 human player plays alongside 4 AI agents configured with custom personas (e.g., "Aggressive Accuser", "Quiet Logician"). The UI handles multi-channel chat while simulating natural AI typing pacing.

### Use Case 3: Rule Prototyping & Custom Game Modding

Game designers design and balance custom game mechanics without modifying backend code. By writing a new YAML configuration (e.g., adding a custom "Serial Killer" or "Assassin" role), designers run 100 fast AI-vs-AI simulation matches locally to analyze win-rate balances.

### Use Case 4: Online BYO-AI (Bring Your Own AI) Multiplayer

AI enthusiasts and model tuners register their self-hosted model's HTTP Webhook URL in an online lobby. The game server dispatches sanitized action requests over Webhooks whenever it is the agent's turn to speak, vote, or execute a skill.

## 3. Core Architectural Principles

**Zero Information Leakage:** Hidden role information (e.g., Mafia role identities, Detective investigation results) is strictly stripped by an authoritative backend event bus before event payloads reach non-authorized agents or human players.

**Declarative Rule Engine:** Game rules, phases, win conditions, and action types are defined in human-readable YAML configurations and executed via standard atomic system primitives, eliminating the need to recompile engine code to create game variations.

**Decoupled Agent Context Management:** Models do not share memory or context buffers directly. Each player seat operates an isolated Context Manager that maintains working memory, compresses historical chat logs, and tracks a private belief state.

**Model-Agnostic Transport Gateway:** The platform translates game actions into standardized tool/function-calling schemas, enabling seamless swapping between OpenAI, Anthropic, local open-weights, and user-hosted webhook endpoints.

**Human-in-the-Loop Observability:** The system provides native hooks for human supervisors to pause simulations, inspect latent reasoning logs, and steer AI logic via real-time overrides during live gameplay.

## 4. High-Level System Architecture

**Client Layer (Web / Desktop):** Manages multi-channel UI, human actions, and real-time visualization.

*Data Flow: WSS / Local Event Bus ↓*

**Core Processing Engine:**
- YAML Rule Engine: Executes finite state machine runtime based on configurations.
- State Sanitizer & Bus: Performs per-seat view filtering to enforce information boundaries.

*Data Flow: Sanitized Event Streams ↓*

**Per-Seat Context Managers:** Maintains short-term history buffers and epistemic belief graphs for each player.

*Data Flow: Context-Aware Prompts ↓*

**Agent Gateway Layer:**
- Local Model Adapters: Connects to OpenAI, Claude, or local Ollama instances.
- BYO-AI / Remote Gateway: Handles external webhook receivers and gRPC endpoints.

## 5. Core System Orchestration & Subsystems

### A. AI-Driven Game Orchestrator

The Central Game Orchestrator acts as the system's command hub and primary interface for human intervention. It interprets YAML configurations to manage game flow while allowing human coaches to dispatch manual overrides, inject guidance into agent prompts, and modulate the game loop state for monitoring purposes.

### B. YAML Rule Engine & State Machine

The game engine executes games as finite state machines. It parses declarative YAML configuration files into active game phases, player attributes, role assignment constraints, communication channels, and victory condition trees.

- **State Lifecycle Execution:** Controls sequential phase progression (e.g., NIGHT_PHASE → DAY_DISCUSSION → DAY_VOTING).
- **Phase Rules:** Defines duration timers, channel access restrictions, permitted player actions, and phase transition triggers.

### C. State Sanitizer & Event Bus

The Sanitizer sits between the authoritative game state and the agent network layer.

- **Role View Generator:** Intercepts system events and generates customized, role-filtered state perspectives for each seat.
- **Visibility Filtering:** Strips secret state parameters (e.g., night action targets or private faction chat logs) from public event broadcasts.

### D. Per-Seat Context Management Engine

To keep token usage efficient and prevent model reasoning contradictions across multi-turn games, each player seat manages its own context pipeline.

- **Working Memory Buffer:** Stores recent raw uncompressed chat messages for the active round.
- **Epistemic Belief Graph:** Maintains persistent structured records tracking public role claims, suspicion levels, vote histories, and confirmed facts.
- **Context Summarization:** Compresses historical turns when approaching context window limits while preserving key logical beliefs.

### E. Agent Gateway & Model Routing System

Acts as the transport bridge between game primitive calls and LLM endpoints.

- **Standardized Action Adapter:** Converts system action requests into structured function-calling/tool-calling schemas for target models.
- **Multi-Provider Support:** Translates payloads into OpenAI, Anthropic, or OpenAI-compatible formats (vLLM, Ollama, LM Studio).
- **BYO-AI Webhook Handler:** Dispatches HTTP/gRPC action requests to user-hosted external agent servers.

### F. Client Presentation Layer

Provides the user-facing interface for both players and spectators.

- **Multi-Channel UI:** Dynamically displays separate chat tabs based on player visibility permissions (Public Town Chat, Faction Night Channels, Private Whispers).
- **Human Action Interceptor:** Replaces model API requests with interactive UI controls (e.g., drop-down target selectors, voting buttons) when a human player occupies a seat.
- **Real-Time Spectator Feed:** Displays complete, unmasked game states, reasoning logs, and model internal monologues for audience view.

## 6. System Primitive Categories

Game definitions orchestrate game mechanics by composing standard atomic primitives:

- **State Primitives:** Update hidden or public player variables (`set_player_attribute`), transition phase states (`set_phase`), and eliminate players (`eliminate_player`).
- **Communication Primitives:** Instantiate dynamic chat groups (`create_channel`), transmit messages (`send_message`), and broadcast system events (`broadcast_event`).
- **Selection & Action Primitives:** Solicit structured tool actions from agents or human UIs (`prompt_action`), compute vote results (`resolve_majority_vote`), and evaluate team counters (`count_matching_players`).

## 7. End-to-End Operational Walkthrough

The AI-Driven Game Orchestrator initiates the session by parsing the YAML configuration, initializing the lobby, and managing all phase transitions, decision dispatching, and message routing.

Consider a 5-Player Mafia Game session with the following seats:

| Seat | Role | Agent |
|---|---|---|
| Seat 1 | Villager | Human Player (Web UI) |
| Seat 2 | Mafia | GPT-4o (Cloud Adapter) |
| Seat 3 | Mafia | User Model (BYO-AI Webhook) |
| Seat 4 | Detective | Claude 3.5 Sonnet (Cloud Adapter) |
| Seat 5 | Villager | Llama-3 (Local Ollama) |

**Phase 1: Night Phase**

- *Orchestrator Role:* Initiates the phase, instantiates private role channels based on YAML rules, and coordinates secret action prompts while holding others in a waiting state.
- *Scenario Walkthrough:* Seats 2 & 3 access the `mafia_night` channel to target Seat 4, while Seat 4 receives a private investigation result on Seat 2.

**Phase 2: Day Discussion**

- *Orchestrator Role:* Drives the transition, processes hidden night actions, broadcasts public notification events, and opens the public chat channel for all players.
- *Scenario Walkthrough:* The engine eliminates Seat 4 (Detective) and notifies the town. Seat 2 (GPT-4o) initiates a turn by accusing Seat 5 in the public chat.

**Phase 3: Synchronous Voting**

- *Orchestrator Role:* Solicits structured elimination targets from all surviving player seats and interfaces with the engine to resolve the majority vote and update status variables.
- *Scenario Walkthrough:* Seats 1, 2, and 3 vote for Seat 5. The Orchestrator resolves this 3-vote majority and removes Seat 5 from the game.

**Phase 4: Game Termination Check**

- *Orchestrator Role:* Evaluates win conditions, manages the final transition, unmasks hidden roles, and routes final results to all participants and spectators.
- *Scenario Walkthrough:* The engine detects the Evil team count (2) is ≥ the Good team count (1). The game halts and broadcasts a Mafia victory.

## 8. Multi-Milestone Roadmap

**Milestone 1: Local AI Engine (LLM vs LLM Playground)**
- Headless game loop & YAML interpreter
- Per-seat State Sanitizer & local Context Managers
- Direct LLM adapters (OpenAI, Claude, local Ollama)

**Milestone 2: Human-in-the-Loop Integration**
- Web UI with multi-channel chat & action controls
- Human turn interceptor & secret masking
- Simulated typing delays & turn timing controls

**Milestone 3: Online Multiplayer & BYO-AI Network**
- Distributed WebSocket lobby & room management
- Authenticated BYO-AI webhook gateway for external models
- Spectator views & automated tournament matchmaker

---

## Addenda from discussion

These clarify or supersede parts of the text above. They are recorded here so the overview stays the single source of intent.

**Turn-taking and the absence of a public channel.** There is no broadcast channel that every seat observes. The orchestrator sends a directed message to the next speaking agent over a dedicated turn dispatch channel, which is a special control-plane construct. References to "broadcast" in sections 3, 5C, and 7 should be read as "recorded with an audience set and delivered at each recipient's next dispatch."

**Belief graph demoted.** The epistemic belief graph in section 5D is not a default component. Engine-derived facts such as vote history, public claims, and deaths ship as an always-on deterministic record. Model-authored suspicion scoring becomes an opt-in experiment.

**Record and replay added.** Every move and the full detail of every agent decision is logged in a structured, append-only format sufficient to replay a match exactly.
