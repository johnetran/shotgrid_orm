---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

Steps to reproduce the behavior:

1. Initialize SGORM with '...'
2. Call method '...'
3. Execute query '...'
4. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

## Error Messages

If applicable, paste the complete error message and stack trace:

```
Paste error message here
```

## Environment

Please complete the following information:

- **OS:** [e.g., macOS 13.0, Ubuntu 22.04, Windows 11]
- **Python Version:** [e.g., 3.11.5]
- **shotgrid_orm Version:** [e.g., 0.1.0]
- **SQLAlchemy Version:** [e.g., 2.0.22]
- **Database:** [e.g., SQLite, PostgreSQL 15, MySQL 8.0]

## Code Sample

Please provide a minimal code sample that reproduces the issue:

```python
from shotgrid_orm import SGORM, SchemaType

# Your code here
```

## Schema Information (if applicable)

If the bug is schema-related, please provide:

- Number of entities in schema: [e.g., 50]
- Specific entity types affected: [e.g., Shot, Asset]
- Custom field types involved: [e.g., entity, multi_entity]

## Connection Type

Which schema source are you using?

- [ ] `SchemaType.JSON_FILE`
- [ ] `SchemaType.JSON_TEXT`
- [ ] `SchemaType.SG_USER`
- [ ] `SchemaType.SG_SCRIPT`
- [ ] `SchemaType.SG_CONNECTION`

## Additional Context

Add any other context about the problem here:

- Does this happen consistently or intermittently?
- Did this work in a previous version?
- Are there any workarounds?
- Screenshots (if applicable)

## Possible Solution (Optional)

If you have ideas on how to fix the bug, please share them here.

## Checklist

- [ ] I have searched existing issues to ensure this is not a duplicate
- [ ] I have provided all requested information
- [ ] I have included a minimal code sample
- [ ] I have included the complete error message
- [ ] I have verified this occurs in the latest version
