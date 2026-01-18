# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

**Note:** As this is currently a beta release (0.1.x), we recommend always using the latest version.

## Reporting a Vulnerability

We take the security of Shotgrid ORM Generator seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Please do not report security vulnerabilities through public GitHub issues, discussions, or pull requests.

### 2. Report Privately

Send your vulnerability report via email to:

**Email:** johnemtran@gmail.com

Include the following information in your report:

- **Type of vulnerability** (e.g., SQL injection, credential exposure, etc.)
- **Full description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** of the vulnerability
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up questions

### 3. Encryption (Optional)

For highly sensitive reports, you may request a PGP key by emailing the address above.

## Response Timeline

You can expect the following timeline for security reports:

- **Initial Response:** Within 48 hours of your report
- **Status Update:** Within 7 days with an assessment of the vulnerability
- **Fix Timeline:** Depends on severity
  - **Critical:** Patch within 7 days
  - **High:** Patch within 14 days
  - **Medium:** Patch within 30 days
  - **Low:** Patch in next regular release

## Security Update Process

When a security vulnerability is confirmed:

1. We will work on a fix in a private repository
2. We will create a security advisory (if applicable)
3. We will release a patched version
4. We will publish a security advisory with details after users have had time to update

## Security Best Practices for Users

When using Shotgrid ORM Generator, follow these security best practices:

### 1. Protect Credentials

**Never** commit Shotgrid API credentials to version control:

```bash
# Bad - Don't do this
sg_orm = SGORM(sg_schema_type=SchemaType.SG_SCRIPT,
               sg_schema_source={"url": "https://studio.shotgunstudio.com",
                                "script": "my_script",
                                "api_key": "abc123xyz"})

# Good - Use environment variables
import os
sg_orm = SGORM(sg_schema_type=SchemaType.SG_SCRIPT,
               sg_schema_source={"url": os.getenv("SG_URL"),
                                "script": os.getenv("SG_SCRIPT"),
                                "api_key": os.getenv("SG_API_KEY")})
```

Always use:
- Environment variables
- `.env` files (ensure they're in `.gitignore`)
- Secret management systems (AWS Secrets Manager, HashiCorp Vault, etc.)

### 2. Validate Input

When using dynamically generated ORM models, validate user input:

```python
# Sanitize user input before using in queries
user_input = sanitize(user_input)
shot = session.execute(select(Shot).where(Shot.code == user_input)).scalar_one_or_none()
```

### 3. Database Connection Security

Use secure database connection strings:

```python
# Use encrypted connections for production databases
engine = create_engine("postgresql+psycopg2://user:pass@host/db?sslmode=require")
```

### 4. Keep Dependencies Updated

Regularly update dependencies to get security patches:

```bash
pip install --upgrade shotgrid_orm
```

### 5. Limit Database Permissions

When using generated ORM models in production:
- Use read-only database users for reporting/BI use cases
- Apply principle of least privilege
- Don't use database admin accounts in application code

### 6. Network Security

When connecting to Shotgrid:
- Use HTTPS endpoints only
- Verify SSL certificates
- Don't disable SSL verification in production

## Known Security Considerations

### 1. SQL Injection

While SQLAlchemy's ORM layer provides protection against SQL injection, be cautious when:
- Building raw SQL queries
- Using `text()` constructs
- Concatenating user input into queries

**Always use parameterized queries:**

```python
# Safe - parameterized
session.execute(select(Shot).where(Shot.id == user_id))

# Unsafe - string concatenation
session.execute(text(f"SELECT * FROM Shot WHERE id = {user_id}"))  # DON'T DO THIS
```

### 2. Schema Information Disclosure

The generated ORM models reveal your Shotgrid schema structure. Consider:
- Not exposing generated model files publicly
- Sanitizing schema dumps before sharing
- Using access controls on systems with ORM models

### 3. Credential Storage

This tool requires Shotgrid API credentials for live connections. Ensure:
- Credentials are never hardcoded
- API keys have minimal required permissions
- Credentials are rotated regularly
- `.env` files are in `.gitignore`

### 4. Data Integrity

This tool disables foreign key constraints by design. When using in production:
- Implement application-level data validation
- Use database triggers if referential integrity is critical
- Validate data before insertion

## Scope

This security policy applies to:
- The `shotgrid_orm` Python package
- Code in the `shotgrid_orm` GitHub repository
- Official documentation and examples

This policy does **not** cover:
- Vulnerabilities in third-party dependencies (report to respective projects)
- Shotgrid/Flow Production Tracking platform itself (report to Autodesk)
- User-specific implementations or custom code

## Security Advisories

Security advisories will be published at:
- GitHub Security Advisories: https://github.com/johnetran/shotgrid_orm/security/advisories
- Release notes when applicable

## Contact

For security concerns or questions about this policy:
- **Email:** johnemtran@gmail.com
- **GitHub Issues:** https://github.com/johnetran/shotgrid_orm/issues (non-security issues only)

---

Thank you for helping keep Shotgrid ORM Generator secure!
