# MLForge Design Playbook

This document is the living design memory of the project.

It records:
- what we changed
- why we changed it
- how the code works
- how modules connect
- the product and UI theory behind each decision

Use this file to learn the system as it evolves.

## How To Read This File

Each module entry follows the same structure:

1. Goal
2. User problem
3. Design choices
4. Code structure
5. Connections
6. Theory notes
7. Print snapshot
8. Future improvements

## Project Design Principles

### 1. Core Value First
We design the module that proves the product's main value before supporting modules.

### 2. Trust Over Decoration
For an ML research assistant, confidence, evidence, and clarity matter more than flashy visuals.

### 3. Visible System Thinking
The UI should help the user understand what the assistant is doing, not just show outputs.

### 4. Modular Growth
Each module should be strong alone and also fit naturally into the larger workflow.

### 5. Learn Through the Build
Every design choice should be documented in both code terms and theory terms.

---

# Frontend Architecture Snapshot

## Current Frontend Scope
The frontend now covers four product modules inside one React application:
- Research Query Workspace
- Document Intake
- Evidence Explorer
- Conversation Memory

## Primary Frontend File
### `frontend/src/App.jsx`
This file now acts as the orchestration shell for the interactive product surface.

Responsibilities:
- manages local React state
- coordinates the module components
- connects to backend routes with `fetch`
- provides local fallback behavior when backend services are unavailable

## Primary Styling File
### `frontend/src/index.css`
This file now holds:
- the visual language of the product
- layout systems for each module
- responsive behavior
- print styles for exporting the design anytime

## Component Refactor Snapshot
The frontend has now been refactored into component and data layers.

### Component files
- `frontend/src/components/HeroBanner.jsx`
- `frontend/src/components/QueryWorkspace.jsx`
- `frontend/src/components/ModuleSidebar.jsx`
- `frontend/src/components/DocumentIntakeSection.jsx`
- `frontend/src/components/EvidenceExplorer.jsx`
- `frontend/src/components/ConversationPanel.jsx`
- `frontend/src/components/ConfidenceMeter.jsx`

### Shared support files
- `frontend/src/config/api.js`
- `frontend/src/data/appContent.js`

### Why this refactor matters
This separates:
- orchestration logic in `App.jsx`
- reusable UI sections in `components/`
- configuration in `config/`
- static content and seed data in `data/`

This is the first major step from prototype-grade structure toward production-grade maintainability.

## Backend Connections Used By The Frontend
- `POST /query`
- `POST /upload_documents`
- `POST /conversation`

## Frontend Strategy
The frontend is intentionally built as:
- backend-aware where routes already exist
- resilient when services are offline
- educational in how it explains the product

This means the UI does not collapse if the backend is unavailable. Instead, it keeps the workflow visible with local fallback states.

---

# Module 01: Research Query Workspace

## Status
Applied

## Goal
Create the first product surface where a user can ask a research question, receive a response, and judge whether the response is trustworthy.

## Why This Module Comes First
This module sits directly on the product's core promise:
the user asks a research question and the assistant responds.

This decision is supported by the backend architecture:
- `backend/routes/query.py` already exposes `/query`
- later modules depend on this question-answer loop

## User Problem
A researcher needs to:
- ask a focused technical question
- receive an answer quickly
- estimate whether the answer is trustworthy
- understand whether the system is useful before doing more setup

## Module Responsibilities
This module is responsible for:
- collecting the research question
- calling the query backend when available
- showing the primary answer
- showing a confidence signal
- giving a useful fallback if the backend is unavailable

## Code Structure

### In `frontend/src/App.jsx`
Key parts:
- `question`
- `queryResult`
- `queryStatus`
- `isQuerying`
- `handleQuerySubmit`
- `ConfidenceMeter`

### Flow
1. The user enters a question.
2. The frontend sends a request to `POST /query`.
3. The backend returns `answer` and `confidence`.
4. The UI updates the answer card and the confidence meter.
5. If the request fails, the UI shows a fallback answer and a status message.

## Design Choices And Theory

### Why confidence is shown next to the answer
Research users need support for judgment, not only generation. A confidence signal helps position the model as an assistant rather than an oracle.

### Why the query area is large and central
The main task of the system begins with intent capture. That makes the question input the strongest visual anchor.

### Why fallback behavior matters
While the backend is still growing, the frontend should remain teachable and reviewable. A dead screen teaches nothing.

## Connections

### Connected backend route
- `POST /query`

### Connected frontend neighbors
- Evidence Explorer uses the current question and answer as context.
- Conversation Memory extends this single-turn workflow into a session.

## Print Snapshot
This module prints cleanly because:
- the answer and confidence are separate cards
- the module has a clear heading and narrative
- interactive controls can be hidden in print styles

## Future Improvements
- loading skeletons
- richer error messaging
- cited evidence from the backend
- query presets by research task

---

# Module 02: Document Intake

## Status
Applied

## Goal
Create the upload and ingestion surface that turns research documents into retrievable knowledge.

## Why This Module Comes Next
After the query workspace, the next important problem is knowledge acquisition.
A research assistant is only as strong as the documents it can parse, index, and retrieve from.

This codebase supports that direction through:
- `backend/routes/upload_documents.py`

## User Problem
A researcher needs to:
- add PDFs and papers easily
- understand whether ingestion is working
- know what stage a document is in
- trust that uploaded content will become searchable later

## Module Responsibilities
This module is responsible for:
- document upload entry
- ingestion progress visibility
- recent document awareness
- explaining the path from file to retrieval

## Code Structure

### In `frontend/src/App.jsx`
Key parts:
- `documents`
- `selectedFile`
- `uploadState`
- `isUploading`
- `ingestionStages`
- `handleUploadSubmit`

### Flow
1. The user chooses a file.
2. The frontend sends the file to `POST /upload_documents`.
3. If the backend accepts it, a new document entry is added to the list.
4. If the backend fails, the UI still adds a local placeholder item so the workflow remains visible.

## Design Choices And Theory

### Why the ingestion pipeline is visible
This is not a simple storage uploader. It is a knowledge-ingestion system. Showing parse, clean, chunk, embed, and index helps the user build a mental model of the platform.

### Why recent documents are shown beside upload
Upload without feedback creates uncertainty. A visible list confirms system receipt and reinforces progress.

### Why stats are summarized
Researchers need to know scale and readiness quickly. Small stats create operational confidence without requiring a dedicated admin screen.

## Connections

### Connected backend route
- `POST /upload_documents`

### Connected frontend neighbors
- Evidence Explorer uses uploaded documents to frame possible sources.
- Query quality improves as the library grows.

## Print Snapshot
This module prints well because:
- the upload narrative remains readable without interaction
- the ingestion pipeline is represented in text
- document and stats cards collapse into a clean document layout

## Future Improvements
- drag-and-drop upload states
- progress bars
- failure and retry states
- document filters
- metadata editing

---

# Module 03: Evidence Explorer

## Status
Applied as a UI prototype

## Goal
Create a module that explains why the system answered the way it did by surfacing evidence-oriented source cards.

## Why This Module Matters
Research workflows depend on verification. Users must be able to inspect why the model responded in a certain way, especially when retrieval is part of the architecture.

## User Problem
A researcher needs to:
- inspect likely sources behind an answer
- see which themes drove retrieval
- understand where confidence should come from

## Module Responsibilities
This module is currently responsible for:
- visualizing evidence cards
- showing approximate source relevance
- connecting the current question and answer to candidate documents

This module is not yet responsible for:
- exact chunk citations
- token-level provenance
- click-through to original PDF pages

## Code Structure

### In `frontend/src/App.jsx`
Key parts:
- `EvidenceExplorer`
- evidence card generation derived from `question`, `answer`, and `documents`

### Flow
1. The current question is tokenized into meaningful terms.
2. The uploaded document list is used as the current source pool.
3. The UI generates evidence cards that preview how retrieval inspection will work.

## Design Choices And Theory

### Why prototype evidence before the backend is ready
Evidence is central to trust. Designing it early prevents the product from turning into a plain answer box that is hard to retrofit later.

### Why cards are used
At this stage, cards communicate source identity, matching strength, and explanation more clearly than a dense table.

## Connections

### Current frontend inputs
- query question
- query answer
- uploaded documents

### Future backend connections
- retrieval traces
- chunk citations
- reranker scores

## Print Snapshot
This module prints clearly because each evidence card is a standalone explanation block.

## Future Improvements
- real citations
- chunk previews
- source highlighting
- confidence attribution by source

---

# Module 04: Conversation Memory

## Status
Applied

## Goal
Create a multi-turn workspace that lets users continue the research process after the first answer.

## Why This Module Comes After Query And Intake
Conversation is valuable only after the user has something worth discussing.
The earlier modules establish that foundation:
- query proves answer generation
- intake grows the knowledge base
- evidence increases trust

Then conversation extends the workflow across time.

## User Problem
A researcher needs to:
- ask follow-up questions
- compare ideas over multiple turns
- maintain continuity in the investigation

## Module Responsibilities
This module is responsible for:
- showing a session thread
- accepting a new turn
- calling the conversation backend route when available
- preserving flow with a local fallback response if needed

## Code Structure

### In `frontend/src/App.jsx`
Key parts:
- `messages`
- `conversationDraft`
- `isSending`
- `ConversationPanel`
- `handleConversationSubmit`

### Flow
1. The user writes a follow-up turn.
2. The frontend appends the user message to the thread.
3. The frontend sends a request to `POST /conversation`.
4. If the backend returns a reply, it is added to the thread.
5. If the backend fails, the UI inserts a fallback assistant message.

## Design Choices And Theory

### Why the thread uses separate user and assistant cards
Research conversations need role clarity. Distinct card treatments make the thread easier to scan.

### Why local fallback is kept
Conversation should remain explorable even while backend logic is still placeholder-level.

## Connections

### Connected backend route
- `POST /conversation`

### Connected frontend neighbors
- conversation naturally grows from the question workflow
- future evidence can be attached per conversation turn

## Print Snapshot
This module prints cleanly because each message is a separate content block and buttons are removed in print mode.

## Future Improvements
- session history
- turn grouping by topic
- citations attached to turns
- exportable research briefs

---

# Print Strategy

## Why The Frontend Is Printable
The project now supports printability in two ways:

### 1. Documentation printability
This file is structured so it can be exported or printed as a clean learning document.

### 2. UI printability
`frontend/src/index.css` now contains `@media print` rules that:
- remove interactive-only controls
- flatten multi-column layouts into single-column print layouts
- remove glass and shadow effects
- keep module sections readable on paper

This means the frontend and the theory document can both be printed at any time.

---

# Update Log

## 2026-03-18
- Initialized the playbook structure
- Applied Module 01 query workspace
- Applied Module 02 document intake
- Applied Module 03 evidence explorer as a UI prototype
- Applied Module 04 conversation memory
- Added backend-aware frontend behavior with local fallbacks
- Added print-friendly frontend styling
- Refactored the frontend into reusable components and shared data/config files
- Upgraded backend routes into a route-plus-service structure
- Replaced placeholder ingestion internals with real parsing, chunking, and metadata extraction
- Added persistent document and chunk storage in SQLite
- Added persistent FAISS storage and persistent BM25 corpus storage
- Wired uploads into persistence and shared retrieval state
- Added Hugging Face-backed baseline generation with safe fallback generation
- Added fine-tuning dataset preparation, evaluation, and QLoRA training scaffolding
- Promoted query responses to include evidence, plan summaries, and revision signals
- Connected the frontend Evidence Explorer and conversation flow to backend evidence payloads
- Added backend integration tests for rich query and conversation responses
