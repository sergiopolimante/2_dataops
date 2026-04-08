# DataOps Demo — DevOps Extended for Data Pipelines

This project demonstrates how **DataOps** extends **DevOps** best practices
to data pipelines. It uses **Databricks Asset Bundles** for deployment and
**GitHub Actions** for CI/CD.

## What is DataOps?

DataOps applies DevOps principles to data engineering:

| DevOps (what you know)         | DataOps (the extension)                          |
|-------------------------------|--------------------------------------------------|
| Unit tests (pytest)           | Data quality tests (on the platform)             |
| Deploy code to servers        | Deploy notebooks/jobs to Databricks              |
| Test in staging before prod   | Run data pipeline in staging, validate output    |
| Rollback on failure           | Destroy failed deployment automatically          |
| Branch protection             | Block merge if data tests fail on Databricks     |

## Project Structure

```
2_dataops/
├── src/                          # Python source code
│   ├── calculator.py             #   Arithmetic operations
│   └── string_utils.py          #   String helper functions
├── tests/                        # Unit tests (DevOps)
│   ├── test_calculator.py       #   Calculator tests
│   └── test_string_utils.py     #   String utils tests
├── notebooks/                    # Databricks notebooks (DataOps)
│   ├── main_pipeline.py         #   Main data pipeline
│   └── test_pipeline.py         #   Data quality tests
├── resources/                    # Databricks job definitions
│   └── dataops_jobs.yml         #   Pipeline + test job configs
├── .github/workflows/
│   └── test.yml                 #   CI/CD pipeline (4 stages)
├── databricks.yml               # Databricks Asset Bundle config
├── requirements.txt
└── README.md
```

## CI/CD Pipeline — 4 Stages

The GitHub Actions workflow (`.github/workflows/test.yml`) runs a 4-stage pipeline:

```
┌─────────────────────┐     ┌──────────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Stage 1            │     │  Stage 2             │     │  Stage 3         │     │  Stage 4        │
│  Unit Tests         │────▶│  Deploy & Test on    │────▶│  Quality Gate    │────▶│  Deploy to      │
│  (DevOps)           │     │  Databricks (DataOps)│     │  (Blocks merge)  │     │  Production     │
│                     │     │                      │     │                  │     │                 │
│  - pytest           │     │  - Deploy to dev     │     │  - Checks all    │     │  - Only after   │
│  - Python 3.10-3.12 │     │  - Run test notebook │     │    stages passed │     │    merge to     │
│                     │     │  - Rollback if fails │     │  - Required in   │     │    main         │
│                     │     │                      │     │    branch rules  │     │                 │
└─────────────────────┘     └──────────────────────┘     └──────────────────┘     └─────────────────┘
                                      │
                                      │ On failure:
                                      ▼
                              ┌────────────────┐
                              │   ROLLBACK     │
                              │  Destroy dev   │
                              │  deployment    │
                              └────────────────┘
```

## Demo Flow for Students

```bash
# 1. Start on main (production code)
git checkout main

# 2. Create a feature branch
git checkout -b feature/my-change

# 3. Make a change (e.g., edit a notebook or source file)
#    ... edit files ...

# 4. Commit and push
git add .
git commit -m "my change"
git push -u origin feature/my-change

# 5. Open a PR on GitHub: feature/my-change → main
#    → Stages 1, 2, 3 run automatically
#    → PR is BLOCKED from merging until Stage 3 (Quality Gate) passes

# 6. Merge the PR on GitHub
#    → Stage 4 runs automatically and deploys to production
```

## Getting Started

### 1. Install dependencies locally

```bash
pip install -r requirements.txt
```

### 2. Run unit tests locally

```bash
pytest tests/ -v
```

### 3. Deploy to Databricks manually (optional)

```bash
# Deploy to dev
databricks bundle deploy -t dev

# Run the test job
databricks bundle run test_job -t dev

# Deploy to production
databricks bundle deploy -t prod
```

## Setup Requirements

### 1. GitHub Secrets

Create an environment called `dev` in your GitHub repo (Settings → Environments)
and add these secrets:

| Secret              | Value                                            |
|---------------------|--------------------------------------------------|
| `DATABRICKS_HOST`   | Your workspace URL (e.g., `https://dbc-xxx.cloud.databricks.com`) |
| `DATABRICKS_TOKEN`  | A Databricks Personal Access Token               |

### 2. Branch Protection Rule (blocks merge if tests fail)

Go to: **Settings → Rules → Rulesets → New ruleset**

1. Name: `Protect main`
2. Target branches: add `main`
3. Check **Require status checks to pass**
4. Add required check: **`Stage 3: Quality Gate`**
5. Save

This ensures PRs can only be merged when unit tests AND Databricks data
tests have passed.

### 3. Databricks Workspace

- Serverless compute must be enabled, **or** uncomment the cluster config
  in `resources/dataops_jobs.yml`
- The user associated with the token needs permissions to create jobs
  and run notebooks

## Key Concepts for Students

1. **Unit Tests (DevOps)**: Test your Python code locally with pytest
2. **Bundle Deploy (DataOps)**: Package and deploy notebooks + jobs to Databricks
3. **Data Quality Tests (DataOps)**: Run assertions on actual Spark data
4. **Quality Gate**: A single check that blocks merging if anything failed
5. **Gated Promotion**: Only deploy to prod after ALL tests pass
6. **Automatic Rollback**: Destroy failed deployments — bad code never stays live
