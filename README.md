# Microservices Online Retail Store

A comprehensive event-driven microservices architecture for an online retail store built with Python backend, React frontend, and deployed on AWS using CDK.

## Architecture Overview

This application implements a microservices architecture with the following services:
- **Product Catalog Service**: Manages product information and inventory
- **Shopping Cart Service**: Handles cart operations and session management
- **Order Management Service**: Processes orders and manages order lifecycle
- **User Management Service**: Handles authentication, authorization, and user profiles
- **Notification Service**: Manages email/SMS notifications
- **Payment Service**: Processes payments (mock implementation)

## Technology Stack

### Backend
- **Language**: Python 3.11
- **Framework**: FastAPI
- **Database**: DynamoDB (NoSQL for scalability)
- **Message Queue**: Amazon SQS
- **Event Bus**: Amazon EventBridge
- **Authentication**: JWT tokens
- **Containerization**: Docker
- **Deployment**: AWS Fargate

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit
- **HTTP Client**: Axios
- **Authentication**: JWT with refresh tokens

### Infrastructure
- **IaC**: AWS CDK (TypeScript)
- **Container Registry**: Amazon ECR
- **Load Balancer**: Application Load Balancer
- **API Gateway**: Amazon API Gateway
- **Monitoring**: CloudWatch
- **Security**: AWS WAF, Security Groups

## Project Structure

```
retail-store/
├── backend/
│   ├── services/
│   │   ├── product-catalog/
│   │   ├── shopping-cart/
│   │   ├── order-management/
│   │   ├── user-management/
│   │   ├── notification/
│   │   └── payment/
│   └── shared/
├── frontend/
├── infrastructure/
├── docs/
└── docker-compose.yml
```

## Getting Started

1. **Prerequisites**
   - Docker and Docker Compose
   - Node.js 18+
   - Python 3.11+
   - AWS CLI configured
   - AWS CDK CLI

2. **Local Development**
   ```bash
   # Start all services
   docker-compose up -d
   
   # Start frontend
   cd frontend && npm start
   ```

3. **AWS Deployment**
   ```bash
   cd infrastructure
   npm install
   cdk deploy --all
   ```

## Features

- User registration and authentication
- Product browsing and search
- Shopping cart management
- Order placement and tracking
- Real-time notifications
- Admin panel for product management
- Responsive design for mobile and desktop

## Cost Analysis (MVP - 20 Users)

Estimated Annual Recurring Revenue (ARR) for hosting on AWS: **$2,400 - $3,600**

See detailed cost breakdown in `docs/cost-analysis.md`

## Documentation

- [Technical Architecture Document (TAD)](docs/technical-architecture.md)
- [API Documentation](docs/api-documentation.md)
- [Database Schema](docs/database-schema.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Cost Analysis](docs/cost-analysis.md)