# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 1. **DO NOT** create a public GitHub issue
Security vulnerabilities should be reported privately to avoid potential exploitation.

### 2. Report the vulnerability
Please email us at [your-email@example.com] with the following information:
- A clear description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Suggested fix (if any)

### 3. What to expect
- We will acknowledge receipt within 48 hours
- We will investigate and provide updates on our progress
- We will work with you to coordinate disclosure
- We will credit you in our security advisory (unless you prefer to remain anonymous)

### 4. Responsible disclosure timeline
- **Initial response**: Within 48 hours
- **Status update**: Within 1 week
- **Fix development**: 1-4 weeks (depending on complexity)
- **Public disclosure**: After fix is available

## Security Best Practices

When using this tool, please follow these security guidelines:

### AWS Credentials
- Use IAM roles with minimal required permissions
- Never commit AWS credentials to version control
- Use AWS Secrets Manager or environment variables for sensitive data
- Regularly rotate access keys

### Input Validation
- Validate all SRT files before processing
- Be cautious with files from untrusted sources
- Monitor for unusual API usage patterns

### Network Security
- Use HTTPS for all API communications
- Consider using VPC endpoints for AWS services
- Monitor network traffic for anomalies

## Security Features

This tool includes several security features:
- Input sanitization for SRT files
- Secure AWS credential handling
- Rate limiting for API calls
- Comprehensive error handling without information disclosure

## Updates and Patches

- Security updates will be released as patch versions (e.g., 1.0.1, 1.0.2)
- Critical security fixes may be backported to previous versions
- Always update to the latest version for best security

## Contact Information

For security-related issues, please contact:
- Email: [your-email@example.com]
- PGP Key: [if you have one]

---

Thank you for helping keep this project secure! 🔒 
