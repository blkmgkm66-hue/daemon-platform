# Daemon Platform - Build Manual

**Version:** 1.0  
**Last Updated:** October 25, 2025  
**Status:** Phase 0: MVP Development - Infrastructure Setup Complete---

## Table of Contents

1. [Introduction](#introduction)
2. [Section 1: Full Vision](#section-1-full-vision)

3. [Development Progress Tracking](#development-progress-tracking)
4. [Section 2: Minimum Viable Product (MVP)](#section-2-minimum-viable-product-mvp)
5. [Section 3: High-Level Architecture](#section-3-high-level-architecture)
6. [Section 4: Build Phases](#section-4-build-phases)
7. [Appendix](#appendix)

## Development Progress Tracking

**Note:** This section serves as a living record of our development journey, tracking milestones, decisions, and progress as we build the Daemon platform.

### Current Status
- **Phase:** Phase 0 - MVP Development
- **Stage:** Infrastructure Setup Complete, Ready for Backend Development
- - **Last Updated:** October 25, 2025
  - 🔄 **Backend API Development - In Progress**
  - - Backend scaffolding complete (endpoints defined, Pydantic models created)
    - - Next: Implement Gemini/Vertex AI integration for /generate-workflow
      - - Next: Implement Secret Manager integration for /save-credential
        - - Next: Implement Cloud Run/Functions deployment for /deploy-workflow

### Milestones Achieved
✅ **October 25, 2025**
- Repository created (daemon-platform)
- BUILD_MANUAL.md established with complete vision, MVP definition, architecture, and phased roadmap
- Development team established: Human (oversight & decisions), Comet (implementation & automation), Gemini (AI expertise & architecture)
- Collaboration model defined: Lockstep development with continuous documentation
- Phase 0 detailed task breakdown completed (7 major components)
- - **GCP API setup script created** (`scripts/setup-gcp-apis.sh`) - Enables all 11 required APIs
- **Budget alert configured** - $10/month threshold with alerts at 50%, 90%, 100%
- **Cloud Run Admin API enabled** - First API activated (run.googleapis.com)
- **Strategic pivot** - Following Gemini's recommendation for highest-leverage approac
- - **All 11 GCP APIs enabled
  - - **Minimal Daemon SDK created** (`daemon_sdk/sdk.py`) - Core functions for MVP: get_trigger_data(), get_secret(), post_slack_message()
    - - **Backend API dependencies defined** (`backend/requirements.txt`) - FastAPI, GCP SDK libraries, Gemini AI integration packages
      - - **Backend API scaffolding complete** (`backend/main.py`) - Full FastAPI structure with logging, Pydantic models, and MVP endpoint stubs (/health, /generate-workflow, /save-credential, /deploy-workflow)** - Complete infrastructure foundation ready (Cloud Run, Functions, Pub/Sub, Firestore, Secret Manager, Storage, Vertex AI, API Gateway, Cloud Build, Resource Manager, IAM)h

### Ongoing Work
🔄 **Phase 0 Implementation Preparation*[[[### Ongoing Work
🔄 **Infrastructure Setup - In Progress*[☑️ **Infrastructure Setup - Complete**
- All 11 required GCP APIs successfully enabled](url)*
- GCP Project configured and ready for development
### Key Decisions Made
- **Repository Visibility:** Private during development phase
- **Development Approach:** MVP-first (Phase 0 complete before Phase 1)
- **Documentation Strategy:** BUILD_MANUAL.md as living document with continuous updates
- **Team Workflow:** Comet ↔ Gemini collaboration with user as human-in-the-loop

### Issues & Resolutions
*No issues encountered yet. This section will track any challenges faced during development and their solutions.*

### Next Steps
1. Get user approval for GCP Project Setu[[[[### Next Steps
1. ✅ **Complete API enablement** (in progress) - Enabling remaining 10 APIs through GCP Console
2. **Configure IAM roles and service accounts** - Set up least-privilege access for Cloud Run workers
3. **Initialize Backend API** - Create FastAPI project structure with initial endpoints
4. **Document architecture decisions** - Add infrastructure choices to BUILD_MANUAL.md](url)](url)](url)](url)p
5. **Validate MVP deployment** - Test the complete workflow end-to-end3. Set up billing and IAM roles
4. Begin Backend API development (FastAPI)

4. [Section 2: Minimum Viable Product (MVP)](#section-2-minimum-viable-product-mvp)
5. [Section 3: High-Level Architecture](#section-3-high-level-architecture)
6. [Section 4: Build Phases](#section-4-build-phases)
7. [Appendix](#appendix)

---

## Introduction

This document serves as the comprehensive guide for building **Daemon**, an AI-driven, developer-first automation platform on Google Cloud Platform. It outlines the complete vision, defines the MVP for initial validation, describes the technical architecture, and provides a phased roadmap from concept to production.

**Key Principles:**
- **MVP First, Then Expand:** Phase 0 (MVP) must be completed and validated before progressing to later phases
- **Risk Minimization:** Validate core concepts with minimal complexity before building full features
- **Incremental Delivery:** Each phase builds upon validated work from previous phases

---

## Section 1: Full Vision 🌟

### The Core Vision

**Daemon is the Operating System for Automated Business Logic.**

Daemon will be the definitive AI-driven, developer-first automation platform providing "Instant Infrastructure" on the Google Cloud Platform. Its fundamental purpose is to **eliminate the operational overhead** associated with building, deploying, scaling, and managing event-driven backend code (primarily Python), allowing developers to focus *solely* on writing the business logic that delivers value.

### What Does Using the Full Daemon Platform Look Like?

#### Example: Developer Workflow

Imagine a developer, Sarah, needs to build an automation for her company:

**1. The Interface:**  
Sarah logs into the Daemon web app and sees a prominent chat prompt: *"What automation do you need to build today?"*

**2. Building a Workflow (AI-First):**  
Sarah types:
> "When a new customer signs up in Stripe (webhook customer.created), enrich their email using Clearbit, check if their company size > 500. If yes, create a lead in Salesforce and send a high-priority alert to the #sales-large-deals Slack channel. If no, just add them to the 'SMB Welcome Sequence' list in Mailchimp."

**3. Daemon AI Response:**  
*"Got it. I'll need you to connect Stripe, Clearbit, Salesforce, Slack, and Mailchimp. I've drafted the Python code using our standard SDK. Take a look."*

**4. Split-Screen View:**  
Sarah sees:
- **Left:** A simple, readable logical flow summary
- **Right:** Clean, production-ready Python code implementing this logic using Daemon's built-in SDK

**5. Connection & Deployment:**  
Sarah clicks buttons to authorize the needed services (OAuth flows handled by Daemon), optionally tweaks the code, and clicks **"Deploy."**

**6. Behind the Scenes (Instantly):**
- Daemon registers the unique Stripe webhook URL
- Bundles Sarah's Python code
- Deploys to distributed execution engine
- Instantly live and ready to handle thousands of events

### User Experience & Key Features

**1. AI-Native Workflow Creation:**  
Primary interface is conversational. Developers describe their desired workflow in natural language to an integrated AI assistant (powered by Gemini via Vertex AI).

**2. Intelligent Code Generation:**  
The AI generates production-ready Python code, utilizing a robust "Daemon SDK" that simplifies interactions with triggers, credentials, logging, and potentially state management.

**3. Transparent Code & Logic:**  
A split-screen UI always shows both a human-readable "Logical Flow" summary and the actual generated Python code. Edits in one view reflect in the other, ensuring transparency and allowing developers to drop down to code level whenever needed. **Code is the source of truth.**

**4. Seamless Credential Management:**  
Connecting to third-party services (APIs, databases) is handled via a secure, centralized vault within Daemon. Developers connect an account once (via OAuth or providing keys), and the platform manages token refreshes and secure injection into the runtime environment via the SDK.

**5. One-Click Deployment:**  
Deploying a workflow takes a single click. Daemon handles packaging the code, configuring the necessary triggers (webhooks, schedules), and deploying it to its managed execution engine.

**6. Comprehensive Dashboard:**  
A unified dashboard provides visibility into all deployed workflows ("Daemons"). Developers can easily view:
- Status (running, failed, degraded)
- Detailed execution history and logs for each run
- Performance metrics (duration, resource usage, cost)
- Configuration settings

**7. Effortless Scaling:**  
Developers can adjust the performance characteristics (e.g., CPU, memory, concurrency/number of workers) allocated to a workflow via simple controls in the UI, without managing any underlying infrastructure.

**8. Integrated Observability:**  
Logs, metrics, and execution history are automatically captured, correlated, and easily accessible within the platform for debugging and monitoring. Alerting on failures or anomalies will be configurable.

### Broad Use Cases

Daemon will be capable of handling a wide array of backend automation tasks, including:

- **API integrations and data synchronization** between SaaS tools
- **Scheduled reporting and data processing jobs**
- **Real-time event processing** from message queues or IoT devices
- **Automated responses to infrastructure or application alerts**
- **File processing triggered by cloud storage events**
- **Orchestrating steps in CI/CD pipelines**
- **Building simple backend logic for internal tools** without managing a full server
- **Serving as the execution layer for AI/ML workflow steps** (e.g., data preprocessing, model inference calls)

### Ultimate Value Proposition

Daemon aims to be the **"Operating System for Automated Business Logic,"** acting as the central nervous system connecting a company's tools and services. It dramatically accelerates the development and deployment of reliable backend automation by providing the necessary infrastructure on demand, powered by an intuitive AI interface, **freeing developers from undifferentiated heavy lifting.**

---

## Section 2: Minimum Viable Product (MVP) 🚀

### MVP Goal

The absolute core goal of the MVP is to **prove that a developer can use an AI chat interface to generate a simple, event-triggered Python script and have Daemon successfully deploy and run it on GCP infrastructure.**

We need to validate the fundamental end-to-end flow:

**Describe → Generate → Deploy → Execute**

Getting this simple end-to-end flow working and tested is the **sole priority** of Phase 0.

### Minimal Features

**1. AI Interaction (Simplified):**  
A very basic chat interface where the user can describe **one specific type** of workflow.

**2. Code Generation (Basic):**  
The AI (Gemini via Vertex AI) generates Python code for that **one specific workflow**, using a barebones version of the Daemon SDK. No complex logic, just the core steps.

**3. Trigger Type:**  
Support for **only one** trigger type: **HTTP Webhook**. This is the best choice as it's common and easy to test externally.

**4. Action Type:**  
Support for **only one simple action** within the generated code. Sending a message to **Slack** is a good choice as it's a common integration and provides clear, visible output.

**5. Deployment (Simplified):**  
A single "Deploy" button. In the background, this will:
- Save the Python code to Cloud Storage
- Provision a unique API Gateway endpoint for the webhook
- Configure a **single, shared** Cloud Run service to receive trigger events (likely via Pub/Sub, even in the MVP, for better decoupling)

**6. Execution (Basic):**  
The shared Cloud Run service receives the trigger, fetches the code, and executes it using Python. No sophisticated isolation initially.

**7. Credentials (Manual Input):**  
For the MVP, **skip the complex OAuth UI**. The user will manually paste their Slack Bot Token into a simple input field, which the backend saves directly to Secret Manager.

**8. Observability (Minimal):**
- Display the unique Webhook URL to the user after deployment
- Show basic execution status (Success/Failure) retrieved from simple logs or a basic Firestore entry
- No detailed logs or history viewer in the UI yet; developers might need to check Cloud Logging directly if something breaks

### What the MVP Will NOT Include

It's crucial to be explicit about what we're intentionally leaving out to keep the scope minimal:

- **Multiple trigger types** (No scheduling, file triggers, etc.)
- **Multiple action types or complex SDK features**
- **Advanced AI features** (code editing sync, logical flow view)
- **UI for managing credentials** (OAuth)
- **Detailed observability dashboard** (logs, metrics, history)
- **Scalability controls**
- **Sophisticated error handling or automatic retries**
- **User accounts or authentication** (can be mocked or skipped initially)
- **Infrastructure as Code** (initial setup might be manual via GCP console/gcloud CLI)

### Technology Choices for MVP (Focus on Speed)

- **Frontend:** Simple static HTML + JavaScript, or a very basic React app (hosted perhaps directly on Cloud Storage or simple Cloud Run)
- **Backend API:** FastAPI on Cloud Run
- **AI:** Vertex AI (Gemini API)
- **Storage:** Cloud Storage (for code), Firestore (minimal metadata/status)
- **Trigger:** API Gateway → Pub/Sub
- **Execution:** Cloud Run (single shared service listening to Pub/Sub)
- **Credentials:** Secret Manager (manual input via backend)
- **Logging:** Basic Cloud Logging

### Why This MVP?

It tests the **riskiest, most novel parts of the idea** – the AI-to-deployed-code pipeline – with the **absolute minimum complexity**. It forces us to build the core execution flow end-to-end. Seeing a Slack message appear after hitting the generated webhook URL is the key validation.

---

## Section 3: High-Level Architecture 🏗️

### Overview

The Daemon platform uses a microservices-oriented architecture leveraging managed GCP services for scalability and reliability. This section provides a high-level view of the major components and how they interact.

**Note:** For extremely detailed component specifications, see `docs/ARCHITECTURE.md` (to be created).

### Main Components

**1. Frontend (Web UI)**
- **Technology:** React/Vue/Angular, containerized
- **Hosting:** Cloud Run
- **Purpose:** User interface for chat interaction, workflow management, viewing logs/history

**2. Backend API (Control Plane)**
- **Technology:** Python with FastAPI, containerized
- **Hosting:** Cloud Run
- **Database:** Firestore (user data, workflow metadata, execution history)
- **Purpose:** 
  - Manages user auth & workflow CRUD operations
  - Interfaces with Vertex AI for code generation
  - Manages OAuth flows and credentials (Secret Manager)
  - Initiates deployments and publishes trigger events

**3. AI Service (Vertex AI)**
- **Service:** Vertex AI Platform using Gemini Models
- **Integration:** Called via API from Backend API
- **Purpose:** Generate/modify Python code based on natural language prompts

**4. Workflow Definition Storage**
- **Metadata:** Firestore (workflow names, trigger types, schedules, status, etc.)
- **Code:** Cloud Storage (Python script files)

**5. Triggering System**
- **Webhooks:** API Gateway → Backend API → Pub/Sub topic
- **Schedules:** Cloud Scheduler → Pub/Sub topic
- **Future:** Cloud Storage events, other Pub/Sub topics

**6. Execution Engine (Data Plane)**
- **Technology:** Python runtime in Docker containers
- **Hosting:** Cloud Run Service(s) subscribed to Pub/Sub
- **Purpose:**
  - Receives trigger messages from Pub/Sub
  - Fetches Python code from Cloud Storage
  - Fetches credentials from Secret Manager
  - Executes user code in isolated environment
  - Logs to Cloud Logging, records results to Firestore

**7. Credential Management**
- **Service:** Secret Manager
- **Integration:** Backend writes/updates, Execution Workers read via IAM

**8. Observability Suite**
- **Logging:** Cloud Logging (structured JSON logs)
- **Metrics:** Cloud Monitoring (execution duration, error rates, custom metrics)
- **History:** Firestore (execution records for UI display)
- **Alerting:** Cloud Monitoring Alerts

### The Daemon SDK

A crucial Python library that abstracts platform complexities for user-generated code:

```python
import daemon_sdk as sdk

# Get trigger data
data = sdk.triggers.get_data()

# Access secrets securely
slack_token = sdk.secrets.get("slack_bot_token")

# Structured logging
sdk.log.info("Processing webhook")
sdk.log.error("Error occurred", extra={"details": "..."})

# Optional: state management, storage access, pre-configured GCP clients
```

---

## Section 4: Build Phases 📅

### Phased Development Approach

This roadmap outlines how to incrementally build Daemon from MVP to full vision. **Phase 0 must be completed and validated before progressing to later phases.**

### Phase 0: MVP Baseline (Completed First) ✅

**Goal:** Validate the core AI → Deploy → Execute flow

**Features:**
- Basic chat UI for ONE specific workflow (Webhook → Slack)
- AI (Gemini) generates Python code using minimal SDK
- Manual input for Slack credential (saved to Secret Manager)
- Single "Deploy" button
- Backend provisions API Gateway webhook URL, saves code to GCS, configures shared Cloud Run service via Pub/Sub trigger
- Shared Cloud Run service executes code
- Display webhook URL and basic success/failure status

**Outcome:** Successfully demonstrate that hitting a generated webhook URL results in a Slack message. **Core concept validated.*

**Detailed Implementation Tasks:**

**1. GCP Project Setup**
- Create new GCP project for Daemon
- Enable required APIs: Cloud Run, Cloud Functions, Pub/Sub, Firestore, Secret Manager, Cloud Storage, Vertex AI
- Set up billing account and enable billing for project
- Configure IAM roles and service accounts
- Set up Cloud Build for CI/CD

**2. Backend API (Control Plane)**
- Initialize FastAPI project structure
- Implement `/chat` endpoint for user interaction
  - Integrate with Vertex AI (Gemini) for natural language processing
  - Parse user intent and extract workflow parameters
- Implement `/save-credential` endpoint
  - Securely store credentials in Secret Manager
  - Validate credential format and permissions
- Implement `/deploy-workflow` endpoint
  - Generate Python code using AI based on user description
  - Save code to Cloud Storage
  - Create API Gateway webhook endpoint
  - Configure Cloud Run service
  - Set up Pub/Sub trigger connection
- Containerize API with Docker
- Deploy to Cloud Run with appropriate scaling configuration

**3. Daemon SDK (Minimal Python Library)**
- Create Python package structure
- Implement core SDK functions:
  - `sdk.triggers.get_data()` - Access trigger payload
  - `sdk.secrets.get(key)` - Retrieve secrets from Secret Manager
  - `sdk.log.info()` / `sdk.log.error()` - Structured logging
  - Optional: `sdk.storage.save()` / `sdk.storage.load()` - GCS access
- Package and publish to private/local PyPI or include in deployments
- Write basic SDK documentation

**4. Execution Worker (Data Plane)**
- Create Cloud Run service template
- Implement Pub/Sub message handler
- Set up code fetching from Cloud Storage
- Implement Python code execution environment
- Add error handling and logging
- Configure service to receive Pub/Sub messages
- Test with sample workflows

**5. Webhook Receiver (Trigger System)**
- Set up API Gateway
- Configure webhook endpoint routes
- Implement webhook-to-Pub/Sub bridge
- Add request validation and authentication
- Generate unique webhook URLs per workflow
- Test webhook reception and message publishing

**6. Frontend UI (Basic)**
- Create simple HTML/React application
- Implement chat interface component
  - Text input for workflow description
  - Message history display
  - AI response rendering
- Implement credential input form
  - Slack Bot Token field
  - Secure submission to backend
- Implement deploy button
  - Trigger workflow deployment
  - Display webhook URL after deployment
- Add basic success/failure status display
- Containerize and deploy to Cloud Run

**7. End-to-End Testing**
- Manual test workflow:
  1. User describes workflow: "When webhook is triggered, send message to Slack"
  2. User provides Slack Bot Token
  3. User clicks Deploy
  4. System generates code, creates webhook, configures Cloud Run
  5. User receives webhook URL
  6. User triggers webhook via curl/Postman
  7. Verify Slack message is sent
- Document test results and any issues
- Validate webhook URL accessibility
- Confirm logs appear in Cloud Logging
- Verify credential security (not exposed in logs or code)*

---

### Phase 1: Foundational Improvements & User Basics

**Goal:** Solidify the foundation and make the platform more usable

**Features:**
- **Multiple Trigger Types:** Add Cloud Scheduler (cron) support
- **Improved SDK:** Better error handling, more helper functions
- **Basic Observability UI:** Simple dashboard showing workflow list, execution history with timestamps/status
- **User Authentication:** Implement Firebase Auth or similar
- **Code Versioning:** Store multiple versions of workflow code

**Outcome:** A more robust MVP with basic user management and scheduling capability

---

### Phase 2: Core Platform Expansion

**Goal:** Build out core platform features for production use

**Features:**
- **OAuth UI for Credentials:** Proper OAuth2 flows for connecting services
- **Multiple Action Types:** Support for more integrations beyond Slack (email, databases, HTTP requests)
- **Split-Screen UI:** Implement logical flow view alongside code editor with sync
- **Enhanced Dashboard:** Detailed logs viewer, performance metrics, cost tracking
- **Retry Logic & Error Handling:** Configurable retry policies, dead-letter queues
- **Per-Workflow Isolation:** Separate Cloud Run instances or better isolation per workflow
- **Infrastructure as Code:** Terraform/Deployment Manager for reproducible infrastructure

**Outcome:** A production-ready platform suitable for team usage

---

### Phase 3: Enhance Developer Experience & Observability

**Goal:** Polish the developer experience and add advanced monitoring

**Features:**
- **Code Editor Improvements:** Syntax highlighting, autocomplete, inline documentation
- **AI Code Suggestions:** AI-powered code review, optimization suggestions, security scanning
- **Advanced Observability:** Detailed metrics dashboard, custom alerts, trace visualization
- **Team Collaboration:** Shared workflows, permissions, team workspaces
- **CLI Tool:** Command-line interface for managing workflows
- **Webhook Management:** Test webhook payloads, replay failed execution
- - **RAG System Integration:** Consider implementing standard RAG (Retrieval-Augmented Generation) to ground AI code generation in Daemon SDK documentation and relevant GCP/Python library docs for improved code quality and reliabilitys

**Outcome:** Enhanced developer productivity with enterprise-grade collaboration features

---

### Phase 4: Advanced Features & Ecosystem

**Goal:** Build ecosystem and advanced capabilities

**Features:**
- **Workflow Marketplace:** Share/reuse common Daemons or reusable Python functions/SDK extensions
- **Complex Orchestration:** Chain multiple Daemons, conditional branching managed by platform
- **Multi-Language Support:** Support for Node.js, Go (via Cloud Run)
- **State Management:** Built-in state persistence between workflow runs
- **Advanced Security:** VPC Service Controls, code scanning integrations (e.g., SonarQube via Cloud Build), more robust input validation
- **Cost Optimization:** Automatic resource optimization suggestions, budget controls

**Outcome:** A mature platform suitable for complex, mission-critical automations with a thriving ecosystem

---

### Ongoing Throughout All Phases

- **Testing:** Unit tests, integration tests, end-to-end tests
- **Documentation:** Comprehensive documentation for users and internal developers
- **Security Reviews & Hardening:** Regular security audits, dependency updates, vulnerability scanning
- **Performance Optimization:** Monitor GCP costs and resource usage, optimize queries, refine execution environments
- **User Feedback:** Continuously iterate on UI, AI interaction, and features based on actual usage

---

## Appendix

### Glossary

- **Daemon**: A deployed workflow/automation on the platform (also the platform name)
- **SDK**: Software Development Kit - the Python library provided to user code
- **Trigger**: An event that initiates workflow execution (webhook, schedule, etc.)
- **Control Plane**: Backend API and supporting services managing platform operations
- **Data Plane**: Execution engine that runs user code
- **GCP**: Google Cloud Platform
- **Vertex AI**: Google's AI platform (includes Gemini models)

### Non-Functional Requirements

- **Scalability:** Handled by Cloud Run, Pub/Sub, Firestore (managed, scalable services)
- **Security:** IAM (least privilege), Secret Manager, VPC Service Controls (advanced), input validation, code scanning
- **Reliability:** Decoupled architecture using Pub/Sub, automatic retries, Cloud Run's managed infrastructure
- **Cost-Effectiveness:** Serverless/managed services with pay-per-use pricing; requires cost monitoring
- **Developer Experience:** Simple UI, powerful AI, clear SDK, good documentation, fast deployments

### Future Documentation

- `docs/ARCHITECTURE.md`: Detailed technical specifications for each component
- `docs/SDK_REFERENCE.md`: Complete Daemon SDK API reference
- `docs/DEPLOYMENT_GUIDE.md`: Step-by-step deployment instructions
- `docs/SECURITY.md`: Security model and best practices
- `docs/CONTRIBUTING.md`: Guidelines for contributors

---

## Conclusion

This BUILD_MANUAL.md provides the comprehensive roadmap for building Daemon from concept to production. The key is to start with Phase 0 (MVP), validate the core concept, and then incrementally build out features phase by phase.

**Next Steps:**
1. Set up GCP project and initial infrastructure
2. Begin Phase 0 implementation
3. Create detailed task breakdown for Phase 0
4. Start building!

---

*This document is a living guide and will be updated as the project evolves.*
