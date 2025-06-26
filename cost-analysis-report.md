# Retail Store Infrastructure (MVP - 20 Users) Cost Analysis Estimate Report

## Service Overview

Retail Store Infrastructure (MVP - 20 Users) is a fully managed, serverless service that allows you to This project uses multiple AWS services.. This service follows a pay-as-you-go pricing model, making it cost-effective for various workloads.

## Pricing Model

This cost analysis estimate is based on the following pricing model:
- **ON DEMAND** pricing (pay-as-you-go) unless otherwise specified
- Standard service configurations without reserved capacity or savings plans
- No caching or optimization techniques applied

## Assumptions

- MVP deployment with 20 concurrent users
- Standard ON DEMAND pricing model for all services
- US East (N. Virginia) region pricing
- 1 ECS Fargate task running 24/7 with 1 vCPU and 2GB memory
- DynamoDB Pay-per-Request billing mode
- Estimated 10,000 API calls per month per user (200,000 total)
- Average 1KB request/response size
- Basic monitoring and logging enabled
- No reserved instances or savings plans
- Standard data transfer rates apply

## Limitations and Exclusions

- Domain name registration and SSL certificate costs
- Development and testing environment costs
- CI/CD pipeline infrastructure costs
- Third-party integrations and services
- Support plan costs
- Data backup and disaster recovery beyond basic point-in-time recovery
- Advanced monitoring and alerting tools
- Custom domain and advanced CDN configurations
- Multi-region deployment costs
- Professional services and consulting fees

## Cost Breakdown

### Unit Pricing Details

| Service | Resource Type | Unit | Price | Free Tier |
|---------|--------------|------|-------|------------|
| AWS Fargate | Cpu | vCPU-second | $0.000011244 | No free tier for Fargate |
| AWS Fargate | Memory | GB-second | $0.000001235 | No free tier for Fargate |
| Amazon API Gateway | Api Calls | million API calls | $3.50 | 1M REST API calls per month for 12 months |
| Amazon API Gateway | Data Transfer | GB | $0.09 | 1M REST API calls per month for 12 months |
| Amazon CloudFront | Data Transfer | GB (first 10TB) | $0.085 | 1TB data transfer and 10M requests per month for 12 months |
| Amazon CloudFront | Requests | 10,000 requests | $0.0075 | 1TB data transfer and 10M requests per month for 12 months |
| Amazon CloudWatch | Custom Metrics | metric per month | $0.30 | 10 custom metrics and 5GB log ingestion for 12 months |
| Amazon CloudWatch | Log Ingestion | GB | $0.50 | 10 custom metrics and 5GB log ingestion for 12 months |
| Amazon CloudWatch | Log Storage | GB per month | $0.03 | 10 custom metrics and 5GB log ingestion for 12 months |
| Amazon DynamoDB | Read Requests | read request unit | $0.00000025 | 25GB storage and 25 WCU/RCU (200M requests/month) for 12 months |
| Amazon DynamoDB | Storage | GB-month | $0.25 | 25GB storage and 25 WCU/RCU (200M requests/month) for 12 months |
| Amazon DynamoDB | Write Requests | write request unit | $0.00000125 | 25GB storage and 25 WCU/RCU (200M requests/month) for 12 months |
| Amazon EventBridge | Custom Events | million events | $1.00 | No free tier for custom event bus |
| Amazon S3 | Requests | 1,000 requests | $0.0004 | 5GB storage and 20,000 GET requests for 12 months |
| Amazon S3 | Storage | GB-month | $0.023 | 5GB storage and 20,000 GET requests for 12 months |
| Amazon SQS | Requests | million requests | $0.40 | 1M requests per month permanently free |
| Application Load Balancer | Alb Hours | hour | $0.0225 | No free tier for ALB |
| Application Load Balancer | Lcu Hours | LCU-hour | $0.008 | No free tier for ALB |
| VPC and Networking | Nat Data Processing | GB | $0.045 | No free tier for NAT Gateway |
| VPC and Networking | Nat Gateway | hour | $0.045 | No free tier for NAT Gateway |

### Cost Calculation

| Service | Usage | Calculation | Monthly Cost |
|---------|-------|-------------|-------------|
| AWS Fargate | 1 task running 24/7 with 1 vCPU, 2GB memory, Linux/x86 (Cpu Hours: 744 hours/month × 1 vCPU = 744 vCPU-hours, Memory Hours: 744 hours/month × 2GB = 1,488 GB-hours) | CPU: $0.000011244 × 2,678,400 seconds = $30.12, Memory: $0.000001235 × 5,356,800 seconds = $6.62, Total: $36.74 | $36.50 |
| Amazon API Gateway | 200,000 REST API calls per month with 1KB average response size (Api Calls: 200,000 calls/month, Data Transfer: 0.2GB/month) | API calls covered by free tier for first 12 months, Data transfer: 0.2GB × $0.09 = $0.02 | $0.70 |
| Amazon CloudFront | CDN for frontend with 10GB data transfer and 100,000 requests per month (Data Transfer: 10GB/month, Requests: 100,000 requests/month) | Covered by free tier for first 12 months | $1.20 |
| Amazon CloudWatch | Basic monitoring with 10 custom metrics and log retention (Custom Metrics: 10 metrics, Log Ingestion: 2GB/month, Log Storage: 10GB) | Mostly covered by free tier, estimated $2-5 for additional usage | $5.00 |
| Amazon DynamoDB | 6 tables with Pay-per-Request billing, estimated 500,000 read/write requests per month (Read Requests: 250,000 read requests/month, Storage: 5GB estimated, Write Requests: 250,000 write requests/month) | Writes: 250,000 × $0.00000125 = $0.31, Reads: 250,000 × $0.00000025 = $0.06, Storage: 5GB × $0.25 = $1.25, Total: $1.62 (covered by free tier for first 12 months) | $0.63 |
| Amazon EventBridge | Custom event bus with 50,000 events per month (Events: 50,000 events/month) | 50,000 × $1.00/million = $0.05 | $0.05 |
| Amazon S3 | Frontend hosting with 1GB storage and 10,000 requests per month (Requests: 10,000 requests/month, Storage: 1GB) | Covered by free tier for first 12 months | $0.25 |
| Amazon SQS | 3 queues with 100,000 messages per month (Requests: 100,000 requests/month) | Covered by permanent free tier | $0.04 |
| Application Load Balancer | 1 ALB running 24/7 with 200,000 requests per month (Alb Hours: 744 hours/month, Lcu Hours: Estimated 1 LCU × 744 hours) | ALB: 744 × $0.0225 = $16.74, LCU: 744 × $0.008 = $5.95, Total: $22.69 | $18.50 |
| VPC and Networking | VPC with NAT Gateway, Internet Gateway, and data transfer (Data Processing: 10GB/month, Nat Hours: 744 hours/month) | NAT Gateway: 744 × $0.045 = $33.48, Data processing: 10GB × $0.045 = $0.45, Total: $33.93 | $45.00 |
| **Total** | **All services** | **Sum of all calculations** | **$107.87/month** |

### Free Tier

Free tier information by service:
- **AWS Fargate**: No free tier for Fargate
- **Amazon API Gateway**: 1M REST API calls per month for 12 months
- **Amazon CloudFront**: 1TB data transfer and 10M requests per month for 12 months
- **Amazon CloudWatch**: 10 custom metrics and 5GB log ingestion for 12 months
- **Amazon DynamoDB**: 25GB storage and 25 WCU/RCU (200M requests/month) for 12 months
- **Amazon EventBridge**: No free tier for custom event bus
- **Amazon S3**: 5GB storage and 20,000 GET requests for 12 months
- **Amazon SQS**: 1M requests per month permanently free
- **Application Load Balancer**: No free tier for ALB
- **VPC and Networking**: No free tier for NAT Gateway

## Cost Scaling with Usage

The following table illustrates how cost estimates scale with different usage levels:

| Service | Low Usage | Medium Usage | High Usage |
|---------|-----------|--------------|------------|
| AWS Fargate | $18/month | $36/month | $73/month |
| Amazon API Gateway | $0/month | $0/month | $1/month |
| Amazon CloudFront | $0/month | $1/month | $2/month |
| Amazon CloudWatch | $2/month | $5/month | $10/month |
| Amazon DynamoDB | $0/month | $0/month | $1/month |
| Amazon EventBridge | $0/month | $0/month | $0/month |
| Amazon S3 | $0/month | $0/month | $0/month |
| Amazon SQS | $0/month | $0/month | $0/month |
| Application Load Balancer | $9/month | $18/month | $37/month |
| VPC and Networking | $22/month | $45/month | $90/month |

### Key Cost Factors

- **AWS Fargate**: 1 task running 24/7 with 1 vCPU, 2GB memory, Linux/x86
- **Amazon API Gateway**: 200,000 REST API calls per month with 1KB average response size
- **Amazon CloudFront**: CDN for frontend with 10GB data transfer and 100,000 requests per month
- **Amazon CloudWatch**: Basic monitoring with 10 custom metrics and log retention
- **Amazon DynamoDB**: 6 tables with Pay-per-Request billing, estimated 500,000 read/write requests per month
- **Amazon EventBridge**: Custom event bus with 50,000 events per month
- **Amazon S3**: Frontend hosting with 1GB storage and 10,000 requests per month
- **Amazon SQS**: 3 queues with 100,000 messages per month
- **Application Load Balancer**: 1 ALB running 24/7 with 200,000 requests per month
- **VPC and Networking**: VPC with NAT Gateway, Internet Gateway, and data transfer

## Projected Costs Over Time

The following projections show estimated monthly costs over a 12-month period based on different growth patterns:

Base monthly cost calculation:

| Service | Monthly Cost |
|---------|-------------|
| AWS Fargate | $36.50 |
| Amazon API Gateway | $0.70 |
| Amazon CloudFront | $1.20 |
| Amazon CloudWatch | $5.00 |
| Amazon DynamoDB | $0.63 |
| Amazon EventBridge | $0.05 |
| Amazon S3 | $0.25 |
| Amazon SQS | $0.04 |
| Application Load Balancer | $18.50 |
| VPC and Networking | $45.00 |
| **Total Monthly Cost** | **$107** |

| Growth Pattern | Month 1 | Month 3 | Month 6 | Month 12 |
|---------------|---------|---------|---------|----------|
| Steady | $107/mo | $107/mo | $107/mo | $107/mo |
| Moderate | $107/mo | $118/mo | $137/mo | $184/mo |
| Rapid | $107/mo | $130/mo | $173/mo | $307/mo |

* Steady: No monthly growth (1.0x)
* Moderate: 5% monthly growth (1.05x)
* Rapid: 10% monthly growth (1.1x)

## Detailed Cost Analysis

### Pricing Model

ON DEMAND


### Exclusions

- Domain name registration and SSL certificate costs
- Development and testing environment costs
- CI/CD pipeline infrastructure costs
- Third-party integrations and services
- Support plan costs
- Data backup and disaster recovery beyond basic point-in-time recovery
- Advanced monitoring and alerting tools
- Custom domain and advanced CDN configurations
- Multi-region deployment costs
- Professional services and consulting fees

### Recommendations

#### Immediate Actions

- Take advantage of AWS Free Tier benefits for the first 12 months to significantly reduce costs
- Monitor DynamoDB usage patterns and consider switching to Provisioned Capacity if usage becomes predictable
- Implement CloudWatch cost monitoring and set up billing alerts
- Use AWS Cost Explorer to track spending patterns and identify optimization opportunities
- Consider using Fargate Spot for development/testing environments to save up to 70%
#### Best Practices

- Implement auto-scaling for ECS services to optimize resource utilization
- Use DynamoDB on-demand billing initially, then evaluate provisioned capacity after establishing usage patterns
- Leverage CloudFront caching to reduce origin server load and data transfer costs
- Implement proper resource tagging for cost allocation and tracking
- Set up AWS Budgets with alerts to prevent unexpected cost overruns
- Consider AWS Savings Plans or Reserved Instances after 6-12 months of stable usage
- Regularly review and clean up unused resources
- Use AWS Trusted Advisor for cost optimization recommendations



## Cost Optimization Recommendations

### Immediate Actions

- Take advantage of AWS Free Tier benefits for the first 12 months to significantly reduce costs
- Monitor DynamoDB usage patterns and consider switching to Provisioned Capacity if usage becomes predictable
- Implement CloudWatch cost monitoring and set up billing alerts

### Best Practices

- Implement auto-scaling for ECS services to optimize resource utilization
- Use DynamoDB on-demand billing initially, then evaluate provisioned capacity after establishing usage patterns
- Leverage CloudFront caching to reduce origin server load and data transfer costs

## Conclusion

By following the recommendations in this report, you can optimize your Retail Store Infrastructure (MVP - 20 Users) costs while maintaining performance and reliability. Regular monitoring and adjustment of your usage patterns will help ensure cost efficiency as your workload evolves.