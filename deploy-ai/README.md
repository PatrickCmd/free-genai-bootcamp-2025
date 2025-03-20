# AI and GenAI Deployment

## How Top Companies Deploy AI in 2025

Here is a summary of the transcript from the provided youtube video: [Link](https://www.youtube.com/watch?v=pLjCc6yZuJo&list=PLBfufR7vyJJ69c9MNlOKtO2w2KU5VzLJV&index=31)

**Title**: AI Deployment Patterns for Enterprises

**Introduction**:
- Deploying AI, especially generative AI, requires a strategic approach.
- This presentation explores common deployment patterns used by enterprises to integrate and manage AI applications securely and efficiently.
- The video will discuss the top 5 AI deployment patterns for enterprises.

**Pattern 1: API Integration**
- **API-Driven Access**:
    - Enterprises often integrate AI models via REST APIs.
    - API calls pass through internal gateways for security and monitoring.
    - This pattern is ideal for quick experimentation and basic tasks.
- **Security Considerations**:
    - Ensure Strict Access Controls and secure your AI Model API keys.
    - Use authentication mechanisms like OAuth to validate requests and prevent unauthorized access.
    - Only approved data types are allowed to be sent to the LLM Model for data security.
    - Applications run in private VPCs with strict network policies.
    - API calls route through internal API gateways for monitoring and governance.
- **Diagram Elements**:
    - Private VPCs (Network Security, Data Privacy)
    - Internal API Gateways (Monitoring, Governance)
    - AI Microservices App
    - OpenAI's Hosted API (Secure API Keys, Access Controls)

**Pattern 2: Containerized Deployments**
- Microservices architecture allows for modularity and scalability.
- Deploy containers using Kubernetes platforms like EKS, AKS, or GKE.
- Each container encapsulates a specific function (API handling, prompt management, response processing, security filtering).
- This enables independent development and deployment.
- Utilize Role-Based Access Control (RBAC) to restrict access to sensitive resources and prevent unauthorized operations.

**Pattern 3: Serverless Architecture**
- **Cloud Functions**:
    - Lambda or Cloud Functions handle API requests.
    - Allows for efficient resource utilization and automatic scaling.
- **Security**:
    - Use a Web Application Firewall (WAF) to protect against common attacks.
    - Employ encryption and access control mechanisms for data stored in S3 or Blob storage.
- **Asynchronous Processing**:
    - Leverage services like SQS or EventBridge for asynchronous processing, improving performance and handling large workloads.
- **Diagram Elements**:
    - API Gateway (Cloud)
    - Functions
    - Events
    - Database
    - Storage Services
    - Function by Fan-out/In

**Pattern 4: Private Endpoint or VNet Integration**
- Private endpoints or VNet integrations ensure data never leaves the secure network.
- This pattern is vital for regulated industries that demand data isolation.
- Utilize virtual private networks (VPNs) and secure network configurations to create a secure and isolated environment for AI applications.
- **Diagram Elements**:
    - Endpoints
    - AI Model
    - Enterprise
    - Secure Network (Lock icon)

**Pattern 5: Hybrid Model Hosting**
- **On-Premises**:
    - Maintain partial models on-premises for data locality or compliance requirements.
- **Cloud**:
    - Leverage cloud infrastructure for large-scale training or fine-tuning, taking advantage of its scalability and resources.
- This pattern is a hybrid approach utilizing both on-premises and cloud capabilities for AI model hosting.

**Next Steps (Conclusion & Remarks)**
- **Top AI Security Risk**: Assess your organization's needs, security requirements, and technical infrastructure.
- **Pilot for Security by Design**: Start with a pilot project to test and refine your chosen deployment pattern.
- **Monitor and Optimize**: Continuously monitor performance, security, and efficiency, making adjustments as needed.
- The presenter recommends considering top AI security risks before building or piloting AI applications.
- Security considerations for Identity and Data are crucial across all deployment patterns.

**Remark from Transcript**:
- The presenter recommends watching another video about top AI security risks to consider before building or piloting AI applications.
- The presenter emphasizes that understanding these patterns is crucial for enterprises deploying AI applications securely and efficiently.


## Top Risks & Deployment Patterns for GenAI Applications on Public Cloud

- [Youtube Link](https://www.youtube.com/watch?v=Q0x3ZtwYI9Y&list=PLBfufR7vyJJ69c9MNlOKtO2w2KU5VzLJV&index=74)

This video guides deploying Generative AI applications on public clouds like AWS, Azure, and GCP, exploring key risks, deployment patterns for OpenAI Enterprise Edition, and essential security checkpoints.

### 1. Data Exposure & Privacy

*   **Data is the fuel for AI**, making data exposure the biggest risk.
*   **Enterprise Risk**: Proprietary data may be exposed during inference or fine-tuning processes.
*   **User Risk**: Personal data requires strict protection standards.
*   **Protection Tools**: Utilize AWS Key Management Service, Azure Key Vault, or GCP’s Cloud KMS.
*   **Privacy Policy**: Be mindful of the privacy policy of the LLM being used, whether it's free, open-source, or paid.
*   **Recommendation**: Keep sensitive data away from LLMs and aim to keep LLMs as "dumb" as possible. Send instructions, get responses, but avoid sharing sensitive data if feasible.

### 2. Model Misuse & Hallucination

*   **Model Misuse**: Common with open-source versions downloaded from platforms like Hugging Face, potentially leading to unexpected outputs.
*   **Unexpected Outputs & Hallucinations**: GenAI models can produce misleading information called "hallucinations," leading to bad decisions.
*   **Implement Guardrails**: Add content filters to prevent inaccurate responses.
*   **Continuous Monitoring**: Apply validation layers before serving outputs to end-users.

### 3. Compliance & Regulatory Requirements

*   Crucial for large organizations, especially those handling private data (PII).
*   **Steps for Compliance**:
    *   **Identify Regulations**: Determine applicable regulations like HIPAA, GDPR, etc., to your data.
    *   **Configure Services**: Use cloud compliance toolkits and configure services appropriately.
    *   **Maintain Audit Logs**: Keep detailed records of all data access and processing.
    *   **Follow Retention Policies**: Implement appropriate data retention and deletion schedules.

### 4. Intellectual Property & Licensing

*   **Legal Risks**: Potential lawsuits due to the use of copyrighted material for training LLMs.
*   **Pre-trained Models**: Check licensing terms for third-party models.
*   **Commercial Use**: Some models restrict commercial applications.
*   **OpenAI Terms**: Review Enterprise Edition usage limitations.
*   **Attribution**: Some licenses require proper attribution even for usage.

### Common Deployment Patterns

*   **API Integration**:
    *   Utilize OpenAI's hosted API for quick experimentation.
    *   Secure API keys and enforce access controls.
*   **Private Endpoint**:
    *   Set up VNet integrations to keep data within your secure network.
    *   Essential for regulated industries to maintain data locality.
*   **Hybrid Model Hosting**:
    *   Maintain partial models on-premises while using the cloud for training.
    *   Balances data locality with flexibility.
    *   API integration and Private endpoints are very common deployment patterns.

### Top 3 Security Application Review Checkpoints

*   **Identity & Access Management**:
    *   Configure roles and policies in AWS IAM, Azure RBAC, or GCP IAM.
    *   Ensure only authorized access to data and AI infrastructure.
*   **Encryption & Key Management**:
    *   Encrypt data at rest and in transit.
    *   Rotate keys frequently using cloud key management services.
*   **Network Configuration & Monitoring**:
    *   Restrict public access with VPCs and firewall rules.
    *   Monitor logs for unusual patterns and potential threats.
    *   Conduct regular penetration tests.

### Conclusion Summary

To securely deploy GenAI applications on public clouds, it is vital to understand and mitigate risks related to data exposure, model misuse, compliance, and intellectual property. Common deployment patterns like API integration and private endpoints offer different balances of flexibility and security. Implementing robust security checkpoints focusing on identity management, encryption, and network security is crucial for building safe AI applications.


## Summary of "TOP 2 AI Security Mistakes to Avoid in 2025"

- [Youtube - Link](https://www.youtube.com/watch?v=bSg_rj2-aN0&list=PLBfufR7vyJJ69c9MNlOKtO2w2KU5VzLJV&index=43)

This video discusses the two main ways to look at AI security and emphasizes the importance of considering both to avoid being vulnerable to attacks. The speaker divides AI security into two categories based on the CI/CD pipeline for AI applications: **Shift Left** (pre-deployment) and **Shift Right** (runtime/post-deployment).

### 1. Shift Left (Pre-deployment Security)

This side focuses on security measures taken during the development and deployment phases of AI applications. These are security practices that have been traditionally applied to software development but are now crucial for AI as well.

*   **OWASP Top 10 LLM:** Understanding and mitigating the top 10 vulnerabilities specific to Large Language Models.
*   **DevSecOps:** Integrating security practices into the DevOps pipeline for AI applications.
*   **Cloud Security:** Ensuring the security of the cloud infrastructure where AI applications are built and deployed.
*   **Detection Controls:** Implementing controls to detect potential security issues early in the development process.
*   **Application Security:** Applying standard application security measures to AI applications.
*   **LLM Privacy:** Protecting the privacy of data used in LLM models.
*   **LLM License:**  Addressing licensing and compliance issues related to LLMs.
*   **Open Source LLM:** Securing the use of open-source LLMs, considering their unique security challenges.

### 2. Shift Right (Runtime Security)

This side addresses security concerns that arise once AI applications are in production and running. This is particularly important for AI due to its unique runtime behaviours.

*   **AI Prompt Attacks:** Protecting against attacks that manipulate AI models through crafted prompts.
*   **Shadow AI:** Identifying and securing AI applications that are deployed without proper oversight.
*   **Data Leakage:** Preventing sensitive data from being leaked through AI applications.
*   **AI Output Validation:** Validating the outputs of AI models to ensure they are secure and not manipulated.
*   **Prevention Controls:** Implementing controls to prevent runtime security incidents in AI applications.
*   **3rd Party Security:**  Securing integrations with third-party AI services and models.

### Conclusion Summary

The video emphasizes that to effectively secure AI applications, organizations need to consider both **pre-deployment (Shift Left)** and **runtime (Shift Right)** security measures. Focusing on only one aspect can leave significant security gaps. For organizations already running AI applications in production, runtime security becomes a primary concern, focusing on threats like prompt attacks and data leakage.  For those in the development phase, a comprehensive approach covering the entire pipeline, including OWASP Top 10 for LLM and application security, is critical.

### Remark from Transcript

The speaker ends the video by asking, "Is there a third way to secure AI?". This question encourages viewers to think beyond the two categories discussed and potentially consider other emerging aspects of AI security. The speaker invites viewers to leave comments if they want a deeper dive into any of these topics.