# BrandPilot

An autonomous AI-powered digital marketing team that creates, approves, publishes, analyzes, and continuously optimizes marketing content across multiple platforms.

## Overview

BrandPilot is a SaaS platform designed to act as an autonomous AI-powered digital marketing team for businesses. It handles the entire content lifecycle from strategy creation to publishing and optimization across multiple social media platforms.

## Technology Stack

- **Backend**: Python 3.14 with Django 5.x
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Background Processing**: Celery + Redis
- **Authentication**: Django Auth + django-allauth
- **Storage**: Django Storages + S3-compatible
- **AI Layer**: LangGraph + PydanticAI + OpenAI SDKs
- **Frontend**: Django Templates + Bootstrap 5 + HTMX + Alpine.js

## Key Features

1. **Authentication & Teams** - User registration, login, team workspaces
2. **Business Onboarding** - Business profiles, website analysis, brand setup
3. **Social Platform Connections** - OAuth integrations with major platforms
4. **Multi-Agent System** - Specialized AI agents for different marketing functions
5. **Content Pipeline** - End-to-end content creation, approval, publishing, and optimization
6. **Comprehensive Dashboards** - Analytics, content calendar, billing, and more

## Project Structure

- `accounts/` - User profiles, teams, authentication
- `businesses/` - Business profiles and onboarding data
- `connections/` - Social media platform connections
- `agents/` - AI agent definitions and configurations
- `content/` - Content calendar, drafts, assets
- `publishing/` - Content scheduling and publishing logic
- `analytics/` - Metrics collection and reporting
- `optimization/` - A/B testing and performance optimization
- `support/` - Customer support systems
- `billing/` - Subscription and payment processing

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `.env.example`)
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Start development server: `python manage.py runserver`

## Architecture Decisions

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed explanations of technology choices and system architecture.

## Development Principles

- Clean Architecture with separation of concerns
- Type-safe Python with hints and Pydantic models
- Incremental delivery - each milestone provides user-facing value
- Extensible agent system for easy addition of new capabilities
- Premium UI/UX with custom Bootstrap styling and micro-interactions

## License

Proprietary - All rights reserved