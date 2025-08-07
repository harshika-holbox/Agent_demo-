# CrewAI Document Intelligence Agent - ECS Fargate Deployment

## 🚀 **Deployment Overview**

This deployment solution provides a **production-ready, scalable CrewAI Document Intelligence Agent** using **AWS ECS Fargate** - perfect for AWS Marketplace integration.

### **Why Fargate over Lambda?**

| Feature | Lambda (Original) | **ECS Fargate (Recommended)** |
|---------|------------------|--------------------------------|
| **Processing Time** | 15min limit ❌ | Unlimited ✅ |
| **Memory** | 10GB max ❌ | 30GB max ✅ |
| **Cold Start** | 5-10s delay ❌ | Always warm ✅ |
| **Agent Persistence** | Stateless ❌ | Persistent ✅ |
| **Cost** | Pay per invoke | Pay for running time |
| **Scaling** | Limited concurrency | Auto-scaling ✅ |
| **AWS Marketplace** | Complex integration | Native support ✅ |

---

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Internet       │    │  Application    │    │  ECS Fargate    │
│  Gateway        │────┤  Load Balancer  │────┤  Tasks          │
│                 │    │  (ALB)          │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       ▼
         │                       │              ┌─────────────────┐
         │                       │              │  CrewAI Agent   │
         │                       │              │  • FastAPI      │
         │                       │              │  • Gradio UI    │
         │                       │              │  • Multi-Agent  │
         │                       │              └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│  Route 53       │    │  CloudWatch     │
│  (Optional)     │    │  Monitoring     │
└─────────────────┘    └─────────────────┘
```

**Features:**
- ✅ **2 vCPU, 8GB RAM** per task (scalable)
- ✅ **Auto-scaling** 2-10 instances
- ✅ **Load balancer** with health checks
- ✅ **Container registry** (ECR)
- ✅ **Monitoring** with CloudWatch
- ✅ **S3 bucket** for document storage
- ✅ **IAM roles** with minimal permissions

---

## 📋 **Prerequisites**

### **1. Tools Installation**
```bash
# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# jq (JSON processor)
sudo apt-get install jq  # Ubuntu/Debian
brew install jq          # macOS
```

### **2. AWS Configuration**
```bash
# Configure AWS CLI
aws configure
# Enter: Access Key ID, Secret Access Key, Region (e.g., us-east-1)

# Verify configuration
aws sts get-caller-identity
```

### **3. Enable AWS Services**
- ✅ **AWS Bedrock** access in your region
- ✅ **ECR** (Elastic Container Registry) 
- ✅ **ECS** (Elastic Container Service)
- ✅ **VPC** permissions
- ✅ **IAM** role creation permissions

---

## 🚀 **Quick Deployment**

### **Method 1: Automated Script (Recommended)**

```bash
# Clone and navigate
git clone <your-repo>
cd Agent_demo-/fargate-deployment/

# Run deployment script
python3 deploy.py
```

The script will:
1. 🔍 Check prerequisites
2. 🐳 Create ECR repository 
3. 🏗️ Build and push Docker image
4. 🚀 Deploy CloudFormation stack
5. ⏳ Wait for completion
6. 🧪 Test endpoints
7. 📋 Show summary with URLs

### **Method 2: Manual Deployment**

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name crewai-document-agent

# 2. Get login token and login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

# 3. Build and push image
docker build -t crewai-document-agent .
docker tag crewai-document-agent:latest <account>.dkr.ecr.us-east-1.amazonaws.com/crewai-document-agent:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/crewai-document-agent:latest

# 4. Deploy infrastructure
aws cloudformation deploy \
    --template-file template.yaml \
    --stack-name crewai-document-agent \
    --parameter-overrides \
        Environment=prod \
        ImageURI=<account>.dkr.ecr.us-east-1.amazonaws.com/crewai-document-agent:latest \
    --capabilities CAPABILITY_NAMED_IAM \
    --region us-east-1
```

---

## 🔗 **API Endpoints**

After deployment, you'll get a load balancer URL like: `http://crewai-alb-xxx.us-east-1.elb.amazonaws.com`

### **Core Endpoints for AWS Marketplace**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/process` | POST | **Main processing endpoint** |
| `/api/upload` | POST | File upload endpoint |
| `/api/capabilities` | GET | Agent capabilities |
| `/api/pricing` | GET | Pricing information |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive API docs |

### **Request/Response Format**

```json
// POST /api/process
{
  "input_text": "Your document text here...",
  "user_query": "Summarize the key points and extract action items"
}

// Response
{
  "status": "success",
  "agent_response": "Based on the document analysis...",
  "source": "Direct text input",
  "user_query": "Summarize the key points",
  "agent_info": {
    "crew_type": "summarization",
    "complexity": "simple",
    "agents_used": ["Content Summarization Specialist"]
  },
  "processing_time_ms": 2350,
  "input_length": 456,
  "timestamp": "2025-01-07T10:30:00Z"
}
```

### **File Upload Support**

```bash
# Upload file for processing
curl -X POST http://your-endpoint/api/upload \
  -F "file=@document.pdf" \
  -F "query=Extract key insights from this document"

# Base64 encoded file
curl -X POST http://your-endpoint/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "file_content": "base64_encoded_content_here",
    "filename": "document.pdf",
    "user_query": "Analyze this document"
  }'
```

---

## 📊 **Monitoring & Management**

### **CloudWatch Metrics**
- ✅ CPU/Memory utilization
- ✅ Request count and latency
- ✅ Error rates
- ✅ Container health

### **Scaling Configuration**
```yaml
Auto Scaling:
  Min Capacity: 2 instances
  Max Capacity: 10 instances  
  Target CPU: 70%
  Scale up: +1 instance if CPU > 70% for 2 minutes
  Scale down: -1 instance if CPU < 50% for 5 minutes
```

### **Health Checks**
```bash
# ECS health check
curl http://your-endpoint/health

# Load balancer health check
# Endpoint: /
# Interval: 30s
# Timeout: 5s
# Healthy threshold: 2
# Unhealthy threshold: 5
```

---

## 💰 **Cost Optimization**

### **Pricing Breakdown (us-east-1)**
```
ECS Fargate (2 vCPU, 8GB RAM):
├── CPU: 2 vCPU × $0.04048/hour = $0.08096/hour
├── Memory: 8GB × $0.004445/hour = $0.03556/hour
└── Total per hour: ~$0.12/hour

Monthly cost (2 instances, 24/7):
├── Base infrastructure: ~$172/month
├── Data transfer: ~$10-50/month
├── Load balancer: ~$16/month
└── Total: ~$200-240/month
```

### **Cost Optimization Tips**
- ✅ Use **Savings Plans** (up to 50% savings)
- ✅ Scale down during low usage
- ✅ Use **Spot instances** for non-critical workloads
- ✅ Monitor and optimize resource usage

---

## 🛒 **AWS Marketplace Integration**

### **Required Information for Listing**

```yaml
Product Information:
  Name: "CrewAI Document Intelligence Agent"
  Category: "AI/ML Services"
  Pricing Model: "Pay-per-request"
  
Technical Details:
  API Endpoint: "http://your-load-balancer/api/process"
  Authentication: "None (can add API keys)"
  Rate Limits: "1000 requests/hour (configurable)"
  SLA: "99.9% availability"
  
Supported Formats:
  - PDF documents
  - Images (PNG, JPG, GIF, etc.)
  - Word documents (DOCX, DOC)
  - Excel files (XLSX, XLS)
  - CSV files
  - Text files (TXT, MD, RTF)
```

### **Integration Testing**
```bash
# Test all capabilities
curl http://your-endpoint/api/capabilities

# Test health check
curl http://your-endpoint/health

# Test document processing
curl -X POST http://your-endpoint/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Sample document for testing",
    "user_query": "Summarize this document"
  }'

# Test file upload
curl -X POST http://your-endpoint/api/upload \
  -F "file=@test_document.pdf" \
  -F "query=Extract key information"
```

---

## 🔧 **Configuration & Customization**

### **Environment Variables**
```dockerfile
ENV AWS_DEFAULT_REGION=us-east-1
ENV S3_BUCKET_NAME=your-documents-bucket
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO
```

### **Resource Scaling**
Update `template.yaml`:
```yaml
ECSTaskDefinition:
  Cpu: '4096'      # 4 vCPU (for heavy workloads)
  Memory: '16384'  # 16 GB RAM
  
ServiceScalingTarget:
  MinCapacity: 1   # Minimum instances
  MaxCapacity: 20  # Maximum instances
```

### **Custom Domain (Optional)**
```yaml
# Add to template.yaml parameters
DomainName: "api.yourdomain.com"
CertificateArn: "arn:aws:acm:region:account:certificate/cert-id"
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Container fails to start**
   ```bash
   # Check ECS logs
   aws logs describe-log-streams --log-group-name /ecs/crewai-document-agent
   
   # Check container health
   aws ecs describe-services --cluster crewai-document-agent --services crewai-document-agent-service
   ```

2. **High memory usage**
   ```bash
   # Increase task memory
   aws ecs update-service --cluster crewai-document-agent \
     --service crewai-document-agent-service \
     --task-definition crewai-document-agent:2
   ```

3. **Load balancer health check failures**
   ```bash
   # Check target group health
   aws elbv2 describe-target-health --target-group-arn <target-group-arn>
   ```

### **Performance Optimization**

1. **Optimize Docker image**
   - Use multi-stage builds
   - Remove unnecessary dependencies
   - Use Alpine Linux base image

2. **Tune CrewAI settings**
   - Reduce agent verbosity in production
   - Optimize memory usage
   - Use caching for repeated requests

---

## 📋 **Next Steps**

1. **✅ Deploy the infrastructure** using the automated script
2. **🧪 Test all endpoints** thoroughly
3. **📊 Set up monitoring** and alerting
4. **🔐 Add authentication** if required
5. **🏪 Submit to AWS Marketplace**
6. **📈 Monitor usage** and optimize costs
7. **📚 Update documentation** with actual URLs
8. **🎯 Scale based on demand**

---

## 📞 **Support**

For deployment issues or questions:
- 📧 **Email**: support@yourdomain.com
- 📚 **Documentation**: Your deployed endpoint `/docs`
- 🐛 **Issues**: GitHub repository issues
- 💬 **Community**: AWS Community forums

---

**🎉 Your CrewAI Document Intelligence Agent is now ready for AWS Marketplace!**
