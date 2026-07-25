# BrandPilot Architecture

## Overview
BrandPilot is a SaaS platform that provides an autonomous AI-powered digital marketing team. The platform helps businesses create, approve, publish, analyze, and optimize marketing content across multiple social media platforms.

## Technology Choices Explained

### Backend: Python 3.14 with Django 5.x
- **Why Django?**: 
  - Batteries-included ORM, admin interface, and authentication system accelerate development.
  - Mature ecosystem with extensive packages (django-allauth, django-storages, Celery, Channels).
  - Explicit over implicit philosophy aligns with our need for clarity and maintainability.
  - Django 5.x provides async views and improved performance.
- **Why Python 3.14?**: Latest performance improvements and type hinting enhancements.

### Django REST Framework (DRF)
- Used for API endpoints that might be consumed by frontend (though we're primarily using Django templates + HTMX, DRF provides flexibility for future mobile/api needs).
- Consistent data serialization and validation.

### Database: PostgreSQL
- Chosen for its reliability, advanced features (JSONB for agent state), and scalability.
- Hosted on Railway or Hostinger for managed service benefits.

### Background Processing: Celery + Redis
- Celery handles asynchronous tasks (content generation, publishing, analytics pulls).
- Redis as broker and result backend for its speed and simplicity.
- Enables horizontal scaling of worker nodes.

### Real-time Updates (Optional): Django Channels
- For live agent activity updates and notifications via WebSockets.
- Will be implemented in later milestones when real-time feedback becomes critical.

### Frontend: Django Templates + Bootstrap 5 + HTMX + Alpine.js
- **Why not React/Next.js?**:
  - Faster initial development with Django's templating system.
  - HTMX allows AJAX-like behavior with minimal JavaScript, keeping stack simple.
  - Alpine.js provides reactive components without the overhead of a full SPA framework.
  - Bootstrap 5 provides responsive design.
- **Custom CSS**: We'll extend Bootstrap with custom styles to avoid the "default Bootstrap" look and create a premium aesthetic.

### Authentication: Django Auth + django-allauth
- Django's built-in auth is secure and well-tested.
- django-allauth extends it to handle OAuth for social platforms (Facebook, Instagram, etc.) and provides account management views.
- Custom providers for platforms not covered by allauth (TikTok, Threads).

### Storage: Django Storages + S3-compatible
- For storing generated media (images, videos) and user-uploaded assets.
- S3-compatible services (like AWS S3, DigitalOcean Spaces, or Hostinger's storage) offer scalability and reliability.
- Separates media from application code and database.

### AI Layer: LangGraph + PydanticAI + OpenAI SDKs
- **LangGraph**: For orchestrating multi-agent workflows (stateful, cyclic graphs). Perfect for our complex content pipeline with feedback loops.
- **PydanticAI**: Ensures type-safe agent inputs/outputs, reducing integration errors.
- **OpenAI SDKs**: Access to latest LLMs (GPT-4o, GPT-4o-mini) for text, DALL-E 3 for images, and Sora or similar for video (when available).
- Agents run as Python logic inside Celery tasks, decoupled from web framework.

## System Architecture

### High-Level Components
1. **Web Interface** (Django): Handles user requests, serves templates, processes form submissions.
2. **API Layer** (DRF): Optional REST/WebSocket endpoints for frontend interactions.
3. **Worker Nodes** (Celery): Execute background tasks (agent operations, publishing, analytics).
4. **Message Broker** (Redis): Facilitates communication between web interface and workers.
5. **Database** (PostgreSQL): Stores all persistent data (users, businesses, content, agent states, etc.).
6. **Object Storage** (S3-compatible): Stores generated media and user uploads.
7. **AI Services** (OpenAI): External LLMs and generative models invoked by agents.

### Core Domains (Django Apps)
Each Django app represents a bounded context:
- `accounts`: Custom user profiles, teams, memberships, authentication extensions.
- `businesses`: Business profiles, onboarding data, brand assets.
- `connections`: Social media platform connections and OAuth token management.
- `agents`: Agent definitions, configurations, and state management.
- `content`: Content calendar, drafts, scheduled posts, assets.
- `publishing`: Logic for scheduling and posting to social platforms.
- `analytics`: Metrics collection, storage, and reporting.
- `optimization`: A/B testing, performance analysis, and recommendation engine.
- `support`: Customer support agent and ticketing system.
- `billing`: Subscription plans, invoices, payment processing.

### Multi-Agent System Details
Each agent is implemented as:
- A LangGraph node that can maintain state and make decisions.
- A PydanticAI agent for structured communication with LLMs.
- A Celery task for asynchronous execution.
- A PostgreSQL-backed memory table for conversation history and learning.

#### Agent Responsibilities
1. **CEO Agent**: Orchestrates the overall marketing strategy, delegates to other agents, and approves final plans.
2. **Brand Research Agent**: Analyzes the business, website, and brand assets to understand voice and positioning.
3. **Competitor Analysis Agent**: Researches competitors' content strategies and performance.
4. **Trend Detection Agent**: Monitors industry trends, hashtags, and viral content.
5. **Content Strategy Agent**: Creates monthly content calendars based on research and goals.
6. **Copywriter Agent**: Generates engaging text copy for posts.
7. **Image Generation Agent**: Creates visuals using AI image models.
8. **Video Generation Agent**: Produces short-form videos (template-based initially, evolving to AI-generated).
9. **Approval Agent**: Routes content for human review and manages approval workflows.
10. **Publishing Agent**: Schedules and publishes content to connected social platforms.
11. **Analytics Agent**: Collects performance metrics from platforms and stores them.
12. **Optimization Agent**: Analyzes performance data to recommend improvements and A/B tests.
13. **Customer Support Agent**: Handles user inquiries and escalates complex issues.

### Data Flow Example: Content Creation Pipeline
1. User onboards a business (stored in `businesses` app).
2. CEO Agent triggers the pipeline via a Celery task.
3. Brand Research Agent analyzes the business (fetching website data, etc.).
4. Competitor Analysis Agent researches top competitors.
5. Trend Detection Agent identifies relevant trends.
6. Content Strategy Agent synthesizes inputs into a monthly calendar.
7. For each content item in the calendar:
   - Copywriter Agent generates text.
   - Image Generation Agent creates visuals.
   - Video Generation Agent produces video (if applicable).
   - Assets are stored in S3-compatible storage.
   - Content is saved as a draft in the `content` app.
   - Approval Agent notifies relevant stakeholders (via email/in-app).
   - Upon approval, Publishing Agent schedules the post.
   - At scheduled time, Publishing Agent posts to connected platforms.
   - Analytics Agent pulls metrics periodically.
   - Optimization Agent analyzes metrics and feeds insights back to strategy.

### Security Considerations
- **Authentication**: Secure password handling, session management, and OAuth flows.
- **Authorization**: Role-based access control (team owners, admins, members).
- **Data Protection**: Encryption at rest (database, backups) and in transit (HTTPS).
- **Input Validation**: Django forms and DRF serializers prevent injection attacks.
- **Rate Limiting**: Protect APIs from abuse.
- **Secrets Management**: Environment variables for API keys, database credentials, etc.
- **Regular Updates**: Dependency scanning and updates.

### Scalability Strategies
- **Horizontal Scaling**: 
  - Web layer: Multiple Django instances behind a load balancer.
  - Worker layer: Multiple Celery worker nodes.
  - Database: PostgreSQL read replicas for analytics queries.
  - Cache: Redis for frequent computations (can be clustered).
- **Asynchronous Processing**: Long-running tasks (AI generation, API calls) offloaded to workers.
- **Database Optimization**: Proper indexing, connection pooling, and query optimization.
- **Static Assets**: Served via CDN (integrated with django-storages).

### Observability
- **Logging**: Structured logging (JSON format) to stdout/stderr, aggregated by external service (e.g., ELK stack).
- **Metrics**: Prometheus metrics exposed via Django Prometheus endpoint.
- **Error Tracking**: Sentry integration for real-time error alerting.
- **Health Checks**: Endpoints for monitoring service availability.
- **Performance Monitoring**: Django Debug Toolbar in development, custom middleware in production.

### Development Principles Applied
- **Clean Architecture**: Separation of concerns with distinct layers (domain, services, agents, apps).
- **Type Safety**: Python type hints throughout, Pydantic models for agent I/O.
- **Incremental Delivery**: Each milestone delivers user-facing value.
- **Maintainability**: Clear documentation, consistent code style (ruff/pre-commit hooks), comprehensive tests.
- **Extensibility**: Plugin-like agent system; new agents can be added without modifying core pipeline.

## Future Enhancements
- Integration with additional social platforms (Snapchat, Reddit).
- Advanced AI capabilities: multimodal agents, fine-tuned models for brand voice.
- Predictive analytics for trend forecasting.
- Collaborative features: team commenting, version approval workflows.
- Marketplace for custom agent templates and content themes.