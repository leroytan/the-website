# Pre-commit Setup Guide

This guide explains how to set up and use pre-commit hooks for this project.

## What is Pre-commit?

Pre-commit is a framework that manages pre-commit hooks for Git. It runs automated checks before each commit to ensure code quality and consistency.

## Current Hooks

This project has pre-commit hooks configured for both backend and frontend:

### Backend Hooks
1. **Backend Tests** - Runs all backend tests to ensure code quality
2. **Export Requirements** - Exports Poetry dependencies to `requirements.txt`

### Frontend Hooks
*Coming soon - will include linting, type checking, and tests*

## Initial Setup

### Prerequisites

- Python 3.12+ (for backend)
- Node.js (for frontend)
- Poetry installed (for backend)
- npm/yarn (for frontend)
- pre-commit installed globally
- Git repository initialized

### Global Setup

1. **Install pre-commit globally:**
   ```bash
   pip install pre-commit
   ```

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install the pre-commit hooks:**
   ```bash
   pre-commit install
   ```

3. **Verify installation:**
   ```bash
   pre-commit run --all-files
   ```

### Frontend Setup

*Coming soon - will include setup instructions for frontend pre-commit hooks*

## Usage

### Automatic Execution

Once installed, pre-commit hooks run automatically on every `git commit`. If any hook fails, the commit will be blocked until the issues are resolved.

### Manual Execution

#### From Root Directory
```bash
# Run backend pre-commit hooks
cd backend && ./scripts/run_precommit.sh

# Run frontend pre-commit hooks (when available)
cd frontend && npm run pre-commit
```

#### From Backend Directory
```bash
./scripts/run_precommit.sh
# OR
pre-commit run --all-files
```

#### From Frontend Directory
```bash
npm run pre-commit
```

#### Run Specific Hooks

**Backend:**
```bash
# Run only tests
pre-commit run backend-tests

# Run only export requirements
pre-commit run export-requirements
```

**Frontend:**
```bash
# Run only linting (when available)
npm run lint

# Run only type checking (when available)
npm run type-check
```

## Hook Details

### Backend Tests Hook
- **Purpose**: Ensures all backend tests pass before commit
- **Command**: `./scripts/run_tests.sh`
- **Behavior**: Runs pytest with coverage and detailed output
- **Failure**: Commit blocked if any tests fail

### Export Requirements Hook
- **Purpose**: Keeps `requirements.txt` in sync with `pyproject.toml`
- **Command**: `./scripts/export-requirements.sh`
- **Behavior**: Exports Poetry dependencies to requirements.txt
- **Note**: This hook will "fail" when it modifies files (this is expected)

## Troubleshooting

### Hook Fails on First Run
If hooks fail on the first run, try:
```bash
cd backend
poetry run pre-commit run --all-files
```

### Export Hook "Fails"
The export-requirements hook may show as "failed" even when successful. This is normal behavior when the hook modifies files. Check that `requirements.txt` was updated.

### Poetry Not Found
Ensure you're running commands from the `backend` directory where `pyproject.toml` is located.

### Permission Issues
Make sure scripts are executable:
```bash
chmod +x scripts/*.sh
```

## Configuration Files

- **`.pre-commit-config.yaml`** - Main configuration file (root directory)
- **`backend/scripts/run_tests.sh`** - Backend test runner script
- **`backend/scripts/export-requirements.sh`** - Backend requirements export script
- **`backend/scripts/run_precommit.sh`** - Backend pre-commit runner script
- **`frontend/package.json`** - Frontend dependencies and scripts (when pre-commit is added)

## Adding New Hooks

To add new pre-commit hooks:

1. Edit `.pre-commit-config.yaml`
2. Add your hook configuration
3. Reinstall hooks: `cd backend && poetry run pre-commit install`
4. Test: `poetry run pre-commit run --all-files`

## Best Practices

- Always run pre-commit hooks before pushing code
- Fix any hook failures before committing
- Keep the `requirements.txt` file in version control
- Use the manual scripts for testing during development

## Common Commands

```bash
# Install hooks
cd backend && pre-commit install

# Run all hooks manually (from backend directory)
./scripts/run_precommit.sh

# Run all hooks manually (from root directory)
cd backend && ./scripts/run_precommit.sh

# Run specific hook
cd backend && pre-commit run <hook-id>

# Update hook versions
cd backend && pre-commit autoupdate

# Skip hooks (use with caution)
git commit --no-verify
```

## Shell Scripts

### `backend/scripts/run_precommit.sh`

This script provides a convenient way to run all pre-commit hooks manually. It's useful for:

- Testing hooks before committing
- Running hooks during development
- CI/CD integration

**Usage:**
```bash
# From backend directory
./scripts/run_precommit.sh

# From root directory
cd backend && ./scripts/run_precommit.sh
```

**Features:**
- Runs all configured pre-commit hooks
- Provides clear output and status messages
- Handles the export-requirements hook "failure" gracefully
- Can be easily integrated into other scripts or CI/CD pipelines

## Support

If you encounter issues:
1. Check that all prerequisites are installed
2. Ensure you're in the correct directory
3. Verify Poetry environment is activated
4. Check the troubleshooting section above
