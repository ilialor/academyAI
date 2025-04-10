# **AcademyOpenAI: Technical Documentation**

**Version:** 1.0
**Date:** [Current Date]

**Table of Contents:**

1.  [Introduction](#1-introduction)
    *   1.1. Project Vision & Goals
    *   1.2. Scope
    *   1.3. Target Audience (for this Documentation)
    *   1.4. Definitions & Glossary
2.  [System Overview](#2-system-overview)
    *   2.1. High-Level Concept
    *   2.2. Key Features & Capabilities (Refined)
    *   2.3. User Roles & Permissions
3.  [Requirements](#3-requirements)
    *   3.1. Functional Requirements (Use Cases)
    *   3.2. Non-Functional Requirements (NFRs)
    *   3.3. Data Requirements
4.  [System Architecture (C4 Model Approach)](#4-system-architecture-c4-model-approach)
    *   4.1. Level 1: System Context Diagram
    *   4.2. Level 2: Container Diagram (SotA Focus)
    *   4.3. Level 3: Component Diagram (Key Services)
    *   4.4. Technology Stack & Justification (SotA Choices)
5.  [Core Processing Pipelines](#5-core-processing-pipelines)
    *   5.1. Video-to-Interactive Course Pipeline
        *   5.1.1. Option A: Direct Generation (Gemini 2.5 Pro)
        *   5.1.2. Option B: Multi-Step Processing (SotA Components)
    *   5.2. Text-to-Interactive Course Pipeline
6.  [API Design & Specification](#6-api-design--specification)
    *   6.1. API Gateway (Kong) Configuration Overview
    *   6.2. Auth & Profile Service API (OpenAPI Spec)
    *   6.3. Courses Service API (OpenAPI Spec)
    *   6.4. Internal Service Communication (gRPC/REST)
7.  [Database Design](#7-database-design)
    *   7.1. Relational Database (PostgreSQL - Auth & Profile)
    *   7.2. Document Database (MongoDB - Courses & Content)
    *   7.3. (Optional) Vector Database (e.g., Weaviate/Pinecone - for Semantic Search/RAG)
8.  [Deployment Architecture & Strategy](#8-deployment-architecture--strategy)
    *   8.1. Containerization (Docker, Docker Compose)
    *   8.2. Orchestration (Kubernetes - Recommended for Scalability)
    *   8.3. Infrastructure as Code (Terraform/Pulumi)
    *   8.4. Environment Strategy (Dev, Staging, Prod)
9.  [CI/CD Pipeline](#9-cicd-pipeline)
    *   9.1. Source Control (Git - GitHub/GitLab)
    *   9.2. CI Server (GitHub Actions / GitLab CI)
    *   9.3. Pipeline Stages (Lint, Test, Build, Deploy)
10. [Development Environment & Standards](#10-development-environment--standards)
    *   10.1. Local Setup (Docker Compose)
    *   10.2. Package Management (UV / Poetry)
    *   10.3. Code Formatting & Linting (Ruff)
    *   10.4. Type Checking (MyPy / Pyright)
    *   10.5. Testing Strategy (Pytest, Coverage)
11. [Operations, Monitoring & Logging](#11-operations-monitoring--logging)
    *   11.1. Logging Strategy (Structured Logging -> Loki/ELK)
    *   11.2. Monitoring & Metrics (Prometheus, Grafana)
    *   11.3. Tracing (OpenTelemetry -> Tempo/Jaeger)
    *   11.4. Alerting (Alertmanager)
12. [Security Considerations](#12-security-considerations)
    *   12.1. Authentication & Authorization (JWT, Role-Based Access Control)
    *   12.2. Input Validation & Sanitization
    *   12.3. API Security (Rate Limiting, HTTPS via Kong)
    *   12.4. Dependency Management (Security Scanning)
    *   12.5. Secrets Management (HashiCorp Vault / K8s Secrets)
13. [Roadmap & Project Management](#13-roadmap--project-management)
    *   13.1. Phased Rollout (Aligned with Original Plan)
    *   13.2. Task Tracking (Jira/Notion/Trello Board Link)
    *   13.3. Communication & Reporting
14. [Risk Assessment & Mitigation](#14-risk-assessment--mitigation)
    *   (Expanded based on SotA choices)
15. [Appendices](#15-appendices)
    *   15.1. External API References (Gemini, STT, Translation)
    *   15.2. Key Configuration File Examples

---

## 1. Introduction

### 1.1. Project Vision & Goals
(As described in `main_doc_v01.md`, potentially refined)
**Vision:** To be the leading platform for rapidly converting English educational content (video/text) into engaging, interactive Russian-language courses.
**Goal:** Create a robust, scalable, containerized platform leveraging SotA AI and backend technologies for automated course generation, accessible via web and mobile.

### 1.2. Scope
**In Scope:**
*   User Authentication & Profile Management (Student, Teacher, Admin roles).
*   Video (English) upload and processing into interactive Russian text courses.
*   Text (English) upload/input and processing into interactive Russian text courses.
*   Automated generation of interactive elements (MCQs, summaries, keywords, self-reflection questions).
*   Web (React) and Mobile (React Native) clients for course consumption and content management (role-dependent).
*   Core platform deployment via containers.
*   API Gateway for unified access.
*   Basic course progress tracking for students.
**Out of Scope (Initially):**
*   Advanced Learning Analytics.
*   Real-time Collaboration features.
*   Support for languages other than English (input) and Russian (output).
*   Community features (forums, discussions).
*   Complex authoring tools beyond generated content editing.
*   Payment processing / Subscriptions.

### 1.3. Target Audience (for this Documentation)
*   Backend Developers
*   Frontend Developers
*   DevOps Engineers
*   QA Engineers
*   Project Managers
*   System Architects
*   (Future) Technical Support Personnel

### 1.4. Definitions & Glossary
*   **STT:** Speech-to-Text
*   **LLM:** Large Language Model
*   **SotA:** State-of-the-Art
*   **JWT:** JSON Web Token
*   **CRUD:** Create, Read, Update, Delete
*   **API:** Application Programming Interface
*   **CI/CD:** Continuous Integration / Continuous Deployment
*   **IaC:** Infrastructure as Code
*   **Interactive Element:** Quiz, Question, Summary, Keyword Definition, etc. within a course module.
*   **Pipeline:** The automated workflow for transforming input content into a course.

## 2. System Overview

### 2.1. High-Level Concept

### 2.2. Key Features & Capabilities (Refined)
*   **Multimodal Input:** Accepts English video files and text content.
*   **AI-Powered Transformation:** Utilizes SotA models for transcription, translation, and interactive content generation.
*   **Automated Course Structuring:** Generates logical modules/lessons from source material.
*   **Rich Interactivity:** Embeds quizzes (MCQ, T/F), reflection prompts, keyword definitions, and summaries.
*   **Role-Based Access:** Distinct interfaces and capabilities for Students, Teachers, and Admins.
*   **Cross-Platform Access:** Seamless experience via Web (React) and Mobile (React Native).
*   **Scalable Architecture:** Containerized microservices designed for growth.
*   **(Optional)** Manual Editing: Allows Teachers/Admins to refine automatically generated interactive elements.

### 2.3. User Roles & Permissions
*   **Student:** View published courses, interact with elements, track progress.
*   **Teacher:** Create/upload content, manage own courses (edit generated elements, publish/unpublish), view student progress on own courses.
*   **Admin:** Full system access - manage users, manage all courses, system configuration, view platform-wide analytics (future).

## 3. Requirements

### 3.1. Functional Requirements (Use Cases)
*   UC-AUTH-01: User Registration
*   UC-AUTH-02: User Login (JWT generation)
*   UC-AUTH-03: User Profile Management
*   UC-COURSE-01: Upload English Video (Teacher/Admin)
*   UC-COURSE-02: Process Video to Interactive Course (System - triggered by UC-COURSE-01) -> *Detail steps based on chosen pipeline*
*   UC-COURSE-03: Upload/Paste English Text (Teacher/Admin)
*   UC-COURSE-04: Process Text to Interactive Course (System - triggered by UC-COURSE-03)
*   UC-COURSE-05: View Course List (All Roles - filtered by publication status/ownership)
*   UC-COURSE-06: View Interactive Course Content (Student, Teacher, Admin)
*   UC-COURSE-07: Interact with Course Elements (e.g., Answer Quiz) (Student)
*   UC-COURSE-08: Edit Course Metadata (Title, Description) (Teacher/Admin)
*   UC-COURSE-09: Edit Generated Interactive Elements (Teacher/Admin - Optional)
*   UC-COURSE-10: Publish/Unpublish Course (Teacher/Admin)
*   UC-COURSE-11: Delete Course (Teacher/Admin)
*   UC-ADMIN-01: Manage Users (Admin)
*   ... (Add more as needed)

### 3.2. Non-Functional Requirements (NFRs)
*   **Performance:**
    *   API Response Time: < 500ms (p95) for standard CRUD operations.
    *   Course Processing Time: Target < TBD minutes for a 60-minute video (depends heavily on external APIs/models). Async processing required.
    *   Concurrent Users: Support at least [X] concurrent users during peak load.
*   **Scalability:** Architecture must support horizontal scaling of services.
*   **Availability:** Target 99.9% uptime for core services.
*   **Reliability:** Robust error handling and retries for external API calls (STT, Translation, LLM). Data backups for PostgreSQL and MongoDB.
*   **Security:** Adherence to OWASP Top 10, secure JWT handling, HTTPS enforced, input validation.
*   **Usability:** Intuitive UI/UX for both web and mobile platforms.
*   **Maintainability:** Clean code practices, comprehensive test coverage, modular design.
*   **Cost-Effectiveness:** Monitor and optimize usage of paid external APIs (Gemini, STT, Translation).

### 3.3. Data Requirements
*   User Data: Email, hashed password, role, profile info.
*   Course Metadata: Title, description, creator ID, status, timestamps.
*   Course Content: Original transcript (optional), translated text, structured modules, interactive elements (JSON/flexible format in MongoDB).
*   Source Files: Temporary storage for uploaded video/audio during processing.
*   Student Progress: Tracking which modules/elements are completed.

## 4. System Architecture (C4 Model Approach)

### 4.1. Level 1: System Context Diagram
*(Diagram showing users [Student, Teacher, Admin] interacting with the `AcademyOpenAI Platform`, and its interactions with external systems like `Email Service`, `External STT API`, `External Translation API`, `External LLM API (e.g., Google AI)`)*.
**(Tool: Mermaid, Structurizr DSL, or draw.io)**

```mermaid
graph TD
    subgraph "AcademyOpenAI Platform"
        direction LR
        WebApp[Web App (React)]
        MobileApp[Mobile App (React Native)]
        APIGateway[API Gateway (Kong)]
        AuthService[Auth & Profile Service (FastAPI)]
        CoursesService[Courses Service (FastAPI)]
        PipelineWorker[Pipeline Worker (Async - Celery/FastStream)]
        PostgresDB[(PostgreSQL)]
        MongoDB[(MongoDB)]
        FileStorage[(Object Storage / Local FS)]
    end

    User(User) -- HTTPS --> WebApp
    User -- HTTPS --> MobileApp
    WebApp -- HTTPS --> APIGateway
    MobileApp -- HTTPS --> APIGateway

    APIGateway -- Route --> AuthService
    APIGateway -- Route --> CoursesService

    AuthService -- CRUD --> PostgresDB
    CoursesService -- CRUD --> MongoDB
    CoursesService -- Trigger --> PipelineWorker
    CoursesService -- Read/Write --> FileStorage

    PipelineWorker -- Read --> FileStorage
    PipelineWorker -- CRUD Status --> MongoDB
    PipelineWorker -- Call --> External_STT[External STT API\n(e.g., Whisper)]
    PipelineWorker -- Call --> External_Translate[External Translation API\n(e.g., Google/DeepL)]
    PipelineWorker -- Call --> External_LLM[External LLM API\n(e.g., Gemini Pro/GPT-4)]

    AuthService -- Send Email --> EmailService[Email Service]

    %% Pipeline Option A (Simplified View)
    subgraph "Pipeline Option A Detail"
        direction TB
        PipelineWorker_A[Pipeline Worker] -- Call --> GeminiAPI[Google AI API\n(Gemini 2.5 Pro)]
        GeminiAPI -- Returns Structured Course --> PipelineWorker_A
    end

```
*(Note: Mermaid diagram above combines context and a hint of container view for illustration. Proper C4 would separate these.)*

### 4.2. Level 2: Container Diagram (SotA Focus)
*(Diagram showing the key deployable units/containers and their interactions)*
**(Tool: Mermaid, Structurizr DSL, or draw.io)**

*   **Containers:**
    *   `Frontend Web (React)`: Serves the SPA. Built using Vite/CRA.
    *   `Frontend Mobile (React Native)`: Native builds (iOS/Android).
    *   `API Gateway (Kong)`: Nginx-based. Handles TLS termination, routing, rate limiting, potentially JWT validation (or passes to services).
    *   `Auth & Profile Service (FastAPI)`: Python/FastAPI, Uvicorn/Gunicorn. Uses `asyncpg` for Postgres. Handles JWT creation/validation.
    *   `Courses Service (FastAPI)`: Python/FastAPI, Uvicorn/Gunicorn. Uses `Motor` for MongoDB. Manages course CRUD, triggers pipeline.
    *   `Pipeline Worker (Celery/FastStream/etc.)`: Python. Consumes tasks from a queue (RabbitMQ/Redis). Interacts with FFmpeg (binary/library), external APIs. Uses `aiohttp`/`httpx` for async API calls.
    *   `PostgreSQL Database`: Standard Postgres container.
    *   `MongoDB Database`: Standard MongoDB container.
    *   `Message Broker (RabbitMQ/Redis)`: For async task queuing between Courses Service and Pipeline Worker. `aio-pika` / `redis-py`.
    *   `(Optional) Vector Database (Weaviate/etc.)`: If needed for semantic features.
*   **Interactions:** Show HTTPS, TCP/IP connections, protocols (REST, AMQP/Redis Streams), data flows.

### 4.3. Level 3: Component Diagram (Key Services)
*(Diagram focusing on the internal components of `Auth Service` and `Courses Service` + `Pipeline Worker`)*
**(Tool: Mermaid, Structurizr DSL, or draw.io)**

*   **Auth Service Components:** API Endpoints (Router), Authentication Logic, User Profile Logic, Database Interface (SQLAlchemy Core/ORM + asyncpg), JWT Utilities.
*   **Courses Service Components:** API Endpoints (Router), Course Management Logic, Pipeline Trigger Logic, Database Interface (Motor), File Handling Logic.
*   **Pipeline Worker Components:** Task Consumer, State Manager, **Video Processor** (FFmpeg Interface), **STT Client**, **Translation Client**, **Course Generation Client (LLM Interface)**, Result Handler (Updates MongoDB).

### 4.4. Technology Stack & Justification (SotA Choices)

| Category             | Choice                                       | Justification                                                                                                                               |
| :------------------- | :------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| **Frontend (Web)**   | React (Vite) + TypeScript + TanStack Query   | Mature ecosystem, component-based UI, performance (Vite), type safety (TS), efficient data fetching/caching (TanStack Query).                 |
| **Frontend (Mobile)**| React Native + TypeScript + TanStack Query   | Code reuse with web (logic, state), native performance access, strong community. Same benefits for TS & TanStack Query.                       |
| **Backend Framework**| FastAPI (Python)                             | High performance (asyncio, Starlette, Pydantic), automatic docs (OpenAPI), built-in data validation, dependency injection (improved with Dishka). |
| **Package Mgmt**     | UV / Poetry                                  | Modern, fast, reliable dependency management and packaging for Python (UV is newer/faster, Poetry is very established).                        |
| **Linting/Format**   | Ruff                                         | Extremely fast Rust-based linter and formatter for Python, single tool replacing Flake8, isort, Black, etc. Consistent code style.           |
| **Type Checking**    | MyPy / Pyright                               | Static analysis for improved code quality and reliability in Python.                                                                        |
| **API Gateway**      | Kong                                         | Mature, feature-rich, plugin ecosystem, handles routing, security, rate limiting, observability. Nginx-based performance.                   |
| **Auth Database**    | PostgreSQL (asyncpg)                         | Robust, ACID compliant, mature relational database. `asyncpg` for high-performance async Python interaction.                                  |
| **Course Database**  | MongoDB (Motor)                              | Flexible schema ideal for evolving course structures and nested interactive elements. `Motor` for async Python interaction.                     |
| **Vector Database**  | Weaviate / Pinecone / ChromaDB (Optional)    | For potential future semantic search or RAG-based course enrichment features.                                                               |
| **Task Queue**       | RabbitMQ (aio-pika) / Redis Streams          | Decouples long-running pipeline tasks, improves responsiveness. RabbitMQ for robustness, Redis for simplicity/speed. Async libraries preferred. |
| **Video Processing** | FFmpeg (CLI or python-ffmpeg)                | De facto standard for audio/video manipulation. Reliable audio extraction.                                                                  |
| **STT Service**      | **Option A:** N/A (Gemini) <br> **Option B:** Whisper Large v3 / AssemblyAI / Google Speech-to-Text | **A:** Handled by multimodal model. <br> **B:** SotA accuracy (Whisper), enterprise features (AssemblyAI), GCP integration (Google).                |
| **Translation**      | **Option A:** N/A (Gemini) <br> **Option B:** Google Translate API / DeepL API            | **A:** Handled by multimodal model. <br> **B:** High-quality machine translation APIs.                                                              |
| **Course Gen LLM**   | **Option A:** Gemini 2.5 Pro <br> **Option B:** GPT-4 / Claude 3 / Fine-tuned Model        | **A:** SotA multimodal, large context, potential for direct structured output. <br> **B:** Powerful text generation, requires separate steps.           |
| **Containerization** | Docker                                       | Standard for packaging applications and dependencies.                                                                                       |
| **Orchestration**    | Kubernetes (K8s)                             | Industry standard for deploying, scaling, and managing containerized applications at scale.                                                   |
| **IaC**              | Terraform / Pulumi                           | Manage cloud infrastructure consistently and repeatably through code.                                                                       |
| **CI/CD**            | GitHub Actions / GitLab CI                   | Integrated with source control, automated workflows for testing and deployment.                                                             |
| **Monitoring**       | Prometheus + Grafana + OpenTelemetry         | SotA stack for metrics collection, visualization, and distributed tracing.                                                                  |
| **Logging**          | Loki / ELK Stack                             | Efficient log aggregation and querying (Loki pairs well with Prom/Grafana).                                                               |

## 5. Core Processing Pipelines

*(Detail the data flow and transformations for both input types, presenting the two video options clearly)*

### 5.1. Video-to-Interactive Course Pipeline

**Trigger:** `POST /courses/{course_id}/upload_video` request to Courses Service.

1.  **Upload & Initial Handling (Courses Service):**
    *   Receive video file via multipart/form-data.
    *   Validate file type and size (NFRs).
    *   Save file temporarily (e.g., Object Storage or shared volume accessible by workers).
    *   Update Course status in MongoDB to `PROCESSING_VIDEO`.
    *   Publish a task to the Message Broker (e.g., `process_video_task` with `course_id` and `file_path`).

#### 5.1.1. Option A: Direct Generation (Gemini 2.5 Pro) - SotA Multimodal

**(Pipeline Worker Executes This)**

2.  **Task Consumption:** Worker picks up `process_video_task`.
3.  **Gemini API Call:**
    *   Read video file from storage.
    *   Construct a prompt for the Gemini 2.5 Pro API (multimodal input).
        *   **Input:** Video data + Text Prompt.
        *   **Example Prompt:** "Analyze the provided English video lecture. Generate a structured interactive course in Russian based on its content. The course should include:
            *   Logical modules/sections with titles.
            *   Key takeaways/summaries for each module.
            *   Identification and definition of key technical terms (English and Russian).
            *   3-5 multiple-choice questions (MCQs) per module with correct answers indicated.
            *   1-2 open-ended questions for self-reflection per module.
            *   Output the result as a JSON object following this schema: `{ 'title': '...', 'modules': [ { 'module_title': '...', 'summary': '...', 'keywords': [{'term_en': '...', 'term_ru': '...', 'definition_ru': '...'}], 'mcqs': [{'question': '...', 'options': ['A', 'B', 'C'], 'answer': 'A'}], 'reflection_questions': ['...'] } ] }`"
    *   Send request to Google AI API. Handle potential errors (API limits, content filters).
4.  **Process Response:**
    *   Receive JSON response from Gemini.
    *   Validate the structure of the received JSON.
5.  **Update Course:**
    *   Update the corresponding Course document in MongoDB with the structured content (`modules` field).
    *   Change Course status to `PROCESSED` or `NEEDS_REVIEW`.
6.  **Cleanup:** Delete temporary video file.

#### 5.1.2. Option B: Multi-Step Processing (SotA Components)

**(Pipeline Worker Executes This)**

2.  **Task Consumption:** Worker picks up `process_video_task`.
3.  **Audio Extraction (FFmpeg):**
    *   Execute FFmpeg command: `ffmpeg -i <video_path> -vn -acodec pcm_s16le -ar 16000 -ac 1 <audio_output_path.wav>` (adjust params as needed).
4.  **Speech-to-Text (STT):**
    *   Send `audio_output_path.wav` to the chosen STT API (e.g., Whisper Large v3 API endpoint, AssemblyAI).
    *   Receive English transcription (with timestamps, ideally). Handle API errors/retries.
5.  **Translation:**
    *   Send the English transcript to the Translation API (e.g., Google Translate/DeepL).
    *   Receive Russian translation. Handle API errors/retries.
6.  **Course Structure & Interactivity Generation (LLM):**
    *   Take the Russian text.
    *   Construct a prompt for a powerful text-based LLM (e.g., GPT-4, Claude 3).
    *   **Example Prompt:** "Based on the following Russian text, which is a translation of an educational lecture, generate a structured interactive course. The course should include: [Same requirements as Gemini prompt, requesting JSON output]".
    *   Send request to the LLM API. Handle errors.
7.  **Process Response:**
    *   Receive JSON response from the LLM.
    *   Validate the structure.
8.  **Update Course:**
    *   Update the Course document in MongoDB with the structured content.
    *   Change Course status to `PROCESSED` or `NEEDS_REVIEW`.
9.  **Cleanup:** Delete temporary video and audio files.

### 5.2. Text-to-Interactive Course Pipeline

**Trigger:** `POST /courses/{course_id}/upload_text` request to Courses Service.

1.  **Upload & Initial Handling (Courses Service):**
    *   Receive text content (e.g., in request body).
    *   Validate input size.
    *   Update Course status in MongoDB to `PROCESSING_TEXT`.
    *   Publish a task to the Message Broker (e.g., `process_text_task` with `course_id` and `input_text`).

**(Pipeline Worker Executes This)**

2.  **Task Consumption:** Worker picks up `process_text_task`.
3.  **(Conditional) Translation:**
    *   *If* the input text is detected/flagged as English, send it to the Translation API (Google/DeepL). Receive Russian translation.
    *   *Else*, assume text is already Russian (or handle error).
4.  **Course Structure & Interactivity Generation (LLM):**
    *   Take the Russian text.
    *   Construct prompt for LLM (similar to step 6 in Video Pipeline Option B).
    *   Send request to LLM API. Handle errors.
5.  **Process Response:**
    *   Receive and validate JSON response.
6.  **Update Course:**
    *   Update Course document in MongoDB.
    *   Change Course status to `PROCESSED` or `NEEDS_REVIEW`.

## 6. API Design & Specification

### 6.1. API Gateway (Kong) Configuration Overview
*   Upstream services definitions (Auth, Courses).
*   Route definitions (e.g., `/auth/*` -> Auth Service, `/courses/*` -> Courses Service).
*   Plugin configuration (e.g., Rate Limiting, CORS, potentially JWT validation using `jwt-keycloak` or custom plugin/lambda).
*   HTTPS termination configuration (Certificates).

### 6.2. Auth & Profile Service API (OpenAPI Spec)
*   Generate using FastAPI's automatic OpenAPI documentation.
*   Key Endpoints:
    *   `POST /auth/register`
    *   `POST /auth/login`
    *   `GET /users/me` (Requires Auth)
    *   `PUT /users/me` (Requires Auth)
    *   `GET /admin/users` (Requires Admin Role) - Example admin endpoint
*   Define request/response schemas (Pydantic models).

### 6.3. Courses Service API (OpenAPI Spec)
*   Generate using FastAPI's automatic OpenAPI documentation.
*   Key Endpoints:
    *   `POST /courses` (Requires Teacher/Admin)
    *   `GET /courses` (Public/Authenticated - filtered)
    *   `GET /courses/{course_id}` (Public/Authenticated if published, Owner/Admin otherwise)
    *   `PUT /courses/{course_id}` (Requires Owner/Admin)
    *   `DELETE /courses/{course_id}` (Requires Owner/Admin)
    *   `POST /courses/{course_id}/upload_video` (Requires Owner/Admin)
    *   `POST /courses/{course_id}/upload_text` (Requires Owner/Admin)
    *   `POST /courses/{course_id}/publish` (Requires Owner/Admin)
    *   `GET /courses/{course_id}/status` (Requires Owner/Admin - for tracking processing)
*   Define request/response schemas (Pydantic models).

### 6.4. Internal Service Communication (gRPC/REST)
*   Primarily REST via API Gateway for external access.
*   Internal communication (e.g., if Courses needed to verify user details directly from Auth) could use REST or potentially gRPC for higher performance if needed, but adds complexity. Start with REST.
*   Async communication via Message Broker for decoupling pipeline tasks.

## 7. Database Design

### 7.1. Relational Database (PostgreSQL - Auth & Profile)
*   `users` table: `id (UUID PK)`, `email (TEXT UNIQUE NOT NULL)`, `hashed_password (TEXT NOT NULL)`, `role (VARCHAR ENUM('student', 'teacher', 'admin') NOT NULL)`, `created_at`, `updated_at`.
*   `profiles` table (optional, 1-to-1): `user_id (UUID FK REFERENCES users)`, `full_name (TEXT)`, `avatar_url (TEXT)`, `...other fields`.
*   Use Alembic for schema migrations.

### 7.2. Document Database (MongoDB - Courses & Content)
*   `courses` collection:
    ```json
    {
      "_id": "ObjectId(...)",
      "title": "String",
      "description": "String",
      "creator_id": "UUID", // Links to user in PostgreSQL
      "status": "String Enum('DRAFT', 'PROCESSING_VIDEO', 'PROCESSING_TEXT', 'PROCESSED', 'NEEDS_REVIEW', 'PUBLISHED', 'ERROR')",
      "source_type": "String Enum('VIDEO', 'TEXT')",
      "source_language": "String ('en')", // Initially fixed
      "target_language": "String ('ru')", // Initially fixed
      "original_content_ref": "String", // Optional ref to original transcript/text
      "processing_error_message": "String", // If status is ERROR
      "modules": [
        {
          "module_id": "UUID", // Or just use array index
          "module_title": "String",
          "module_order": "Int",
          "summary": "String",
          "keywords": [
            { "term_en": "String", "term_ru": "String", "definition_ru": "String" }
          ],
          "interactive_elements": [
             // Flexible array for different element types
             { "type": "MCQ", "question": "String", "options": ["String"], "correct_answer_index": "Int" },
             { "type": "REFLECTION", "question": "String" },
             { "type": "TEXT_BLOCK", "content": "String (translated text segment)"}
             // Add more types as needed
          ]
        }
      ],
      "created_at": "ISODate",
      "updated_at": "ISODate",
      "published_at": "ISODate" // Optional
    }
    ```
*   `student_progress` collection (example):
    ```json
    {
      "_id": "ObjectId(...)",
      "student_id": "UUID",
      "course_id": "ObjectId(...)",
      "completed_module_ids": ["UUID"],
      "completed_element_ids": ["UUID"], // Or more granular tracking
      "last_accessed": "ISODate"
    }
    ```
*   Use appropriate indexing (e.g., on `creator_id`, `status`).

### 7.3. (Optional) Vector Database (e.g., Weaviate/Pinecone)
*   If implementing semantic search for courses or using RAG:
    *   Store vectors representing course modules or text chunks.
    *   Schema would include vector embedding + metadata (course_id, module_id).

## 8. Deployment Architecture & Strategy

### 8.1. Containerization (Docker, Docker Compose)
*   `Dockerfile` for each service (FastAPI apps, potentially React build stage).
*   `docker-compose.yml` for local development and testing, linking services, databases, Kong, message broker.
*   Use multi-stage builds in Dockerfiles to keep final images small.

### 8.2. Orchestration (Kubernetes - Recommended for Scalability)
*   Define K8s manifests:
    *   `Deployment`: For each service (FastAPI, Workers, potentially Frontend).
    *   `Service`: To expose deployments internally (ClusterIP) or externally (LoadBalancer/NodePort).
    *   `Ingress`: To manage external access, routing via an Ingress controller (like Nginx Ingress or Traefik) which could replace or work with Kong.
    *   `ConfigMap`/`Secret`: To manage configuration and sensitive data.
    *   `PersistentVolumeClaim`: For databases and potentially file storage if not using external object storage.
    *   `StatefulSet`: For databases (Postgres, MongoDB, RabbitMQ) if running them within K8s.
*   Use Helm charts for easier management and deployment templating.

### 8.3. Infrastructure as Code (Terraform/Pulumi)
*   Manage cloud resources (Kubernetes cluster, databases if external, object storage, DNS) using IaC tools.
*   Ensures repeatable and version-controlled infrastructure setup.

### 8.4. Environment Strategy (Dev, Staging, Prod)
*   Separate environments (e.g., different K8s namespaces or clusters).
*   Use configuration management (ConfigMaps, Secrets, environment variables) to tailor deployments per environment (e.g., API keys, database endpoints).

## 9. CI/CD Pipeline

### 9.1. Source Control (Git - GitHub/GitLab)
*   Monorepo or separate repositories per service (discuss pros/cons).
*   Branching strategy (e.g., Gitflow, GitHub Flow).

### 9.2. CI Server (GitHub Actions / GitLab CI)
*   Define workflows in `.github/workflows` or `.gitlab-ci.yml`.

### 9.3. Pipeline Stages (Example for a Backend Service)
1.  **Trigger:** Push to `main`/`develop` branch or Pull Request.
2.  **Lint & Format:** Run `ruff check .` and `ruff format --check .`.
3.  **Type Check:** Run `mypy .` or `pyright .`.
4.  **Test:** Run `pytest` (unit, integration tests). Collect coverage report.
5.  **Build:** Build Docker image (`docker build ...`).
6.  **Push:** Push Docker image to container registry (Docker Hub, GHCR, GitLab Registry, ECR).
7.  **Deploy (Staging):** Automatically deploy to staging environment (e.g., `helm upgrade ...` or `kubectl apply ...`). Run smoke tests.
8.  **Deploy (Production):** Manual trigger or automatic after staging validation. Deploy to production environment.

## 10. Development Environment & Standards

### 10.1. Local Setup (Docker Compose)
*   Provide `docker-compose.yml` and instructions for easy local spin-up of all services.
*   Include hot-reloading for FastAPI and React during development.

### 10.2. Package Management (UV / Poetry)
*   Use `pyproject.toml` to define dependencies and project metadata.
*   Commands: `uv pip install`, `uv sync` or `poetry install`, `poetry add`.
*   Use lock files (`uv.lock` / `poetry.lock`) for reproducible builds.

### 10.3. Code Formatting & Linting (Ruff)
*   Define rules in `ruff.toml` or `pyproject.toml [tool.ruff]`.
*   Integrate with pre-commit hooks to enforce standards before commits.

### 10.4. Type Checking (MyPy / Pyright)
*   Configure in `mypy.ini` or `pyproject.toml`.
*   Aim for strict type checking where feasible.

### 10.5. Testing Strategy (Pytest, Coverage)
*   **Unit Tests:** Test individual functions/classes in isolation (mocking dependencies).
*   **Integration Tests:** Test interaction between components within a service (e.g., API endpoint -> logic -> database). Use test databases.
*   **End-to-End (E2E) Tests:** (Optional, complex) Test full user flows across services (e.g., using Cypress for frontend, or API-level tests).
*   Use `pytest` framework with plugins like `pytest-asyncio`, `pytest-cov`.
*   Target >80% test coverage.

## 11. Operations, Monitoring & Logging

### 11.1. Logging Strategy (Structured Logging -> Loki/ELK)
*   Use structured logging libraries (e.g., `structlog` for Python).
*   Log relevant context (request IDs, user IDs, course IDs).
*   Forward logs from containers (using Fluentd, Promtail) to Loki or ELK stack for aggregation and querying.

### 11.2. Monitoring & Metrics (Prometheus, Grafana)
*   Expose application metrics (request latency, error rates, queue sizes) using Prometheus client libraries (e.g., `prometheus-fastapi-instrumentator`).
*   Monitor infrastructure metrics (CPU, RAM, disk, network) using `node-exporter`.
*   Monitor database/broker metrics.
*   Visualize metrics in Grafana dashboards.

### 11.3. Tracing (OpenTelemetry -> Tempo/Jaeger)
*   Implement distributed tracing using OpenTelemetry SDKs in services.
*   Propagate trace context across service calls (including async tasks).
*   Send traces to Tempo or Jaeger for visualizing request flows and identifying bottlenecks.

### 11.4. Alerting (Alertmanager)
*   Define alerting rules in Prometheus based on metrics (e.g., high error rates, high latency, low disk space).
*   Use Alertmanager to handle deduplication, grouping, and routing of alerts (e.g., to Slack, PagerDuty).

## 12. Security Considerations

*(Expand significantly on the basic list)*
*   **Authentication:** Secure JWT implementation (short-lived access tokens, refresh tokens), strong password hashing (bcrypt/argon2).
*   **Authorization:** Enforce RBAC rigorously at the API Gateway and service levels. Check ownership for resource modifications (e.g., course editing).
*   **Input Validation:** Use Pydantic in FastAPI for strict request validation. Sanitize any user-generated content displayed in HTML. Protect against prompt injection in LLM calls.
*   **API Security:** HTTPS everywhere, rate limiting, potentially WAF (Web Application Firewall).
*   **Dependency Scanning:** Use tools like `pip-audit` or GitHub Dependabot/Snyk to find vulnerabilities in dependencies.
*   **Secrets Management:** Use K8s Secrets mounted as volumes/env vars, or a dedicated solution like HashiCorp Vault. Do not commit secrets to Git.
*   **Container Security:** Scan container images for vulnerabilities (e.g., Trivy, Clair). Run containers as non-root users.
*   **Data Security:** Encrypt sensitive data at rest (database encryption) and in transit (HTTPS).

## 13. Roadmap & Project Management

### 13.1. Phased Rollout
*(Align with the 4 phases from `main_doc_v01.md`, but detail tasks based on the SotA tech stack)*
*   **Phase 1:** Infra Setup (Docker, K8s basics, Kong), Auth Service (FastAPI, Postgres, JWT), Basic CI/CD.
*   **Phase 2:** Courses Service (FastAPI, MongoDB, CRUD), Integrate Auth, Message Broker Setup.
*   **Phase 3:** Pipeline Implementation (**Choose Option A or B, or build both for comparison**), Worker Service (Celery/FastStream), FFmpeg/API integrations, Update Course logic.
*   **Phase 4:** Frontend Web (React, Auth flow, Course list/view, Upload UI), Frontend Mobile (React Native, Core viewing), Connect to Backend via Kong.
*   **Phase 5:** Monitoring/Logging Setup, Testing Refinement, Security Hardening, Documentation Finalization, Initial Deployment (Staging -> Prod).

### 13.2. Task Tracking
*   Link to the chosen tool (Jira, Notion, Trello): `[Link to Board]`
*   Use epics for phases, stories for features/use cases, tasks for implementation details.

### 13.3. Communication & Reporting
*   Daily Standups (optional, depending on team).
*   Weekly Sync Meetings (Progress, Blockers, Planning).
*   Sprint Reviews/Demos (at end of iterations/phases).
*   Use Slack/Teams for regular communication.

## 14. Risk Assessment & Mitigation

*(Expand on original list, adding SotA specifics)*

| Risk                                      | Likelihood | Impact | Mitigation Strategies                                                                                                                                                              |
| :---------------------------------------- | :--------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **External API Downtime/Limits (STT/Translate/LLM)** | Medium     | High   | Implement retries with exponential backoff. Monitor usage quotas. Have fallback options (e.g., alternative provider) ready if possible. Cache results where appropriate. |
| **External API Cost Overruns**            | Medium     | Medium | Set budget alerts on cloud provider/API accounts. Optimize prompts/requests. Implement strict rate limiting per user/tenant. Consider fine-tuning smaller models (Option B). |
| **LLM Hallucination / Inaccuracy**        | Medium     | High   | Implement thorough prompt engineering. Allow manual review/editing by Teachers. Use RAG (Retrieval-Augmented Generation) if needed for factuality. Version control prompts.      |
| **Poor Quality Output (Bad Source/AI)**   | Medium     | High   | Set input quality guidelines (audio clarity). Allow manual editing. Potentially add content scoring/flagging mechanism. User feedback loop.                                    |
| **Video Processing Timeouts/Failures**    | Medium     | Medium | Use robust async processing (queues). Implement timeouts and failure handling logic. Monitor worker resources. Set reasonable file size/duration limits.                          |
| **Vendor Lock-in (Specific LLM/API)**     | Medium     | Medium | Abstract API interactions behind internal clients/interfaces. Design prompts to be relatively model-agnostic where possible. Prioritize Option B for more control.              |
| **Infrastructure Complexity (K8s, etc.)** | Low-Medium | High   | Use managed K8s services (EKS, GKE, AKS). Leverage Helm charts. Invest in training/expertise. Start simpler if team lacks experience.                                           |
| **Data Privacy/Security Breach**          | Low-Medium | High   | Implement robust security measures (Sec 12). Regular security audits/scans. Adhere to relevant privacy regulations (GDPR, etc.).                                                 |
| **Scalability Bottlenecks**               | Medium     | Medium | Load testing. Horizontal scaling configuration (K8s HPA). Monitor resource utilization closely. Optimize database queries/indexes.                                               |
| **Dependency Vulnerabilities**            | High       | Medium | Regular dependency scanning (CI/CD). Prompt patching schedule. Use tools like `pip-audit`.                                                                                       |

## 15. Appendices

### 15.1. External API References
*   Google AI (Gemini): [Link to Docs]
*   Google Speech-to-Text: [Link to Docs]
*   Google Translate: [Link to Docs]
*   DeepL API: [Link to Docs]
*   AssemblyAI: [Link to Docs]
*   OpenAI API (Whisper, GPT): [Link to Docs]
*   Anthropic API (Claude): [Link to Docs]

### 15.2. Key Configuration File Examples
*   `.ruff.toml`
*   `pyproject.toml` (UV/Poetry structure)
*   `docker-compose.yml` (local development)
*   Example Kubernetes Deployment/Service YAML
*   Example Kong Configuration snippet

---

This structure provides a comprehensive, SotA-aware documentation plan covering all critical aspects of the AcademyOpenAI project, including the specific pipeline variations requested. Remember to keep this documentation living and updated throughout the project lifecycle.