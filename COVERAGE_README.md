# Coverage Badge Integration

## Adding Coverage Badge to README

To add the coverage badge to your README.md, use one of these approaches:

### Option 1: Static Badge (Manual Update)
```markdown
![Coverage](https://img.shields.io/badge/coverage-99.3%25-brightgreen)
```

### Option 2: Dynamic Badge via Codecov
```markdown
[![codecov](https://codecov.io/gh/USERNAME/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USERNAME/REPO)
```

### Option 3: Dynamic Badge via Coveralls
```markdown
[![Coverage Status](https://coveralls.io/repos/github/USERNAME/REPO/badge.svg?branch=main)](https://coveralls.io/github/USERNAME/REPO?branch=main)
```

## Coverage Commands

### Quick Coverage Check
```bash
make test-cov
```

### Detailed Coverage Report with Badge
```bash
make test-cov-report
```

### View HTML Coverage Report
```bash
make test-cov-html
```

### Clean Coverage Files
```bash
make clean-cov
```

## Coverage Thresholds

- **Minimum Coverage**: 95%
- **Branch Coverage**: Enabled
- **Fail Under**: 95%

## Coverage Reports

The following coverage reports are generated:

1. **Terminal Report**: Displayed during test execution
2. **HTML Report**: `htmlcov/index.html` - Detailed interactive report
3. **XML Report**: `coverage.xml` - For CI/CD integration
4. **JSON Report**: `coverage.json` - For programmatic access
5. **Badge URL**: `coverage_badge.txt` - For README badges

## CI/CD Integration

The project includes GitHub Actions workflow for automated coverage reporting:

- Runs on push to main/develop branches
- Runs on pull requests to main
- Uploads coverage to Codecov and Coveralls
- Comments coverage results on pull requests
- Fails if coverage drops below 95%