# Scripts Directory

This directory contains utility scripts for the backend project.

## Available Scripts

### `run_tests.sh`
Runs the complete test suite with coverage reporting.

**Usage:**
```bash
./scripts/run_tests.sh
```

**Features:**
- Runs all tests with verbose output
- Generates coverage reports (terminal and HTML)
- Sets proper environment variables for testing
- Uses Poetry for dependency management

**For detailed testing information, see:**
- [Tests README](../tests/README.md) - Comprehensive testing guide
- [Coverage Configuration](../.coveragerc) - Coverage settings

### `start.sh`
Starts the development server.

### `build.sh`
Builds the project.

## Notes

- All scripts are executable and should be run from the `backend/` directory
- The test runner uses Poetry to ensure proper dependency management
- Coverage reports are generated in `htmlcov/index.html`
