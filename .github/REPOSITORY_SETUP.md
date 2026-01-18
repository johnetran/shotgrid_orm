# GitHub Repository Configuration Guide

This guide covers the manual configuration steps needed for the GitHub repository. These settings should be configured through the GitHub web interface.

## Repository Settings

### Basic Information

Navigate to **Settings** → **General**:

1. **Description**:
   ```
   SQLAlchemy ORM Generator for Autodesk Flow Production Tracking (Shotgrid)
   ```

2. **Website**: Add if you host documentation:
   ```
   https://github.com/johnetran/shotgrid_orm
   ```

3. **Topics/Tags**: Add the following topics (in Settings → General):
   - `shotgrid`
   - `shotgun`
   - `sqlalchemy`
   - `orm`
   - `autodesk`
   - `python`
   - `data-warehouse`
   - `flow-production-tracking`
   - `reporting`
   - `analytics`

4. **Features**:
   - ✅ Issues
   - ✅ Projects (optional)
   - ✅ Wiki (optional)
   - ✅ Discussions (optional - for community support)
   - ✅ Sponsorships (optional)

## Branch Protection Rules

Navigate to **Settings** → **Branches** → **Add rule**:

### Rule for `main` branch:

**Branch name pattern**: `main`

**Protect matching branches**:
- ✅ Require a pull request before merging
  - ✅ Require approvals: 1
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  - ✅ Require review from Code Owners (if you create a CODEOWNERS file)

- ✅ Require status checks to pass before merging
  - ✅ Require branches to be up to date before merging
  - **Required checks** (add these as they appear from CI):
    - `test (3.7)` through `test (3.13)` (from test.yml workflow)
    - Any other CI checks you've configured

- ✅ Require conversation resolution before merging

- ✅ Require linear history (optional - keeps history clean)

- ✅ Include administrators (recommended - admins also follow rules)

- ✅ Allow force pushes: **No one**

- ✅ Allow deletions: **Disabled**

## Secrets Configuration

Navigate to **Settings** → **Secrets and variables** → **Actions**:

### Required Secrets for Publishing:

1. **PYPI_API_TOKEN**
   - Go to https://pypi.org/manage/account/token/
   - Create a new API token
   - Scope: "Entire account" or "Project: shotgrid_orm"
   - Copy the token (starts with `pypi-`)
   - Add as repository secret: `PYPI_API_TOKEN`

2. **CODECOV_TOKEN** (if using Codecov):
   - Go to https://codecov.io/ and sign in with GitHub
   - Add your repository
   - Copy the upload token
   - Add as repository secret: `CODECOV_TOKEN`

## GitHub Pages (Optional)

If you want to host documentation via GitHub Pages:

Navigate to **Settings** → **Pages**:

1. **Source**: Deploy from a branch
2. **Branch**: `gh-pages` or `main` (depending on your docs setup)
3. **Folder**: `/docs` or `/` (root)
4. **Custom domain**: Optional

## Social Preview Image

Navigate to **Settings** → **General** → **Social preview**:

1. Click **Edit**
2. Upload an image (1280x640 pixels recommended)
3. Suggested content:
   - Project logo or name
   - Tagline: "Shotgrid ORM Generator"
   - Visual: Database/schema diagram
   - Tech stack icons (Python, SQLAlchemy, Shotgrid)

You can use the existing `doc/ShotgridORM.png` or create a new one.

## Collaborators and Teams (Optional)

Navigate to **Settings** → **Collaborators and teams**:

Add collaborators or teams who should have access to the repository.

## Security

Navigate to **Settings** → **Security**:

### Code security and analysis:

- ✅ **Dependabot alerts**: Enabled (automatically enabled)
- ✅ **Dependabot security updates**: Enabled
- ✅ **Dependabot version updates**: Enabled (via dependabot.yml)
- ✅ **Secret scanning**: Enabled
- ✅ **Code scanning**: Configure CodeQL (optional)

### Security policy:

Ensure `SECURITY.md` exists (already created).

## Project Boards (Optional)

Navigate to **Projects**:

Create project boards for:
- Roadmap
- Bug tracking
- Release planning

## Discussions (Optional)

Navigate to **Settings** → **General** → **Features**:

Enable **Discussions** if you want:
- Q&A section
- General discussions
- Announcements
- Show and Tell

Categories to create:
- 📣 Announcements
- 💬 General
- 💡 Ideas
- 🙏 Q&A
- 🐛 Bug Reports (if not using Issues)

## Webhooks (Optional)

Navigate to **Settings** → **Webhooks**:

Add webhooks if you want to integrate with:
- Slack/Discord notifications
- CI/CD systems
- Other automation tools

## GitHub Actions Settings

Navigate to **Settings** → **Actions** → **General**:

**Actions permissions**:
- ✅ Allow all actions and reusable workflows

**Workflow permissions**:
- ✅ Read and write permissions (needed for releases)
- ✅ Allow GitHub Actions to create and approve pull requests

## Checklist

Use this checklist when setting up a new repository:

- [ ] Set repository description and website
- [ ] Add topics/tags
- [ ] Configure branch protection for `main`
- [ ] Add `PYPI_API_TOKEN` secret
- [ ] Add `CODECOV_TOKEN` secret (if using)
- [ ] Upload social preview image
- [ ] Enable Dependabot alerts and security updates
- [ ] Verify GitHub Actions permissions
- [ ] Enable Discussions (optional)
- [ ] Create project boards (optional)
- [ ] Invite collaborators (if applicable)

## Next Steps After Configuration

1. Push code to `main` branch
2. Verify CI/CD workflows run successfully
3. Test pull request workflow
4. Verify branch protection rules work
5. Test release workflow (on a test branch first)
6. Monitor Dependabot for security updates

## Support

For issues with repository configuration, contact the repository owner or see GitHub's documentation:
- https://docs.github.com/en/repositories
- https://docs.github.com/en/actions
