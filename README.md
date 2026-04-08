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

## Project Structure

```
2_dataops/
├── src/                          # Python source code
│   ├── calculator.py             #   Arithmetic operations
│   └── string_utils.py           #   String helper functions
├── tests/                        # Unit tests (DevOps)
│   ├── test_calculator.py        #   Calculator tests
│   └── test_string_utils.py      #   String utils tests
├── notebooks/                    # Databricks notebooks (DataOps)
│   ├── main_pipeline.py          #   Main data pipeline
│   └── test_pipeline.py          #   Data quality tests
├── resources/                    # Databricks job definitions
│   └── dataops_jobs.yml          #   Pipeline + test job configs
├── .github/workflows/
│   └── test.yml                  #   CI/CD pipeline (3 stages)
├── databricks.yml                # Databricks Asset Bundle config
├── requirements.txt
└── README.md
```

## CI/CD Pipeline — 3 Stages

The GitHub Actions workflow (`.github/workflows/test.yml`) runs a 3-stage pipeline:

```
┌─────────────────────┐     ┌──────────────────────────┐     ┌─────────────────────┐
│  Stage 1: Unit Tests│────▶│ Stage 2: Deploy & Test   │────▶│ Stage 3: Deploy     │
│  (DevOps)           │     │ on Databricks (DataOps)  │     │ to Production       │
│                     │     │                          │     │ (DataOps)           │
│  - pytest           │     │  - Deploy to dev target  │     │  - Deploy to prod   │
│  - Python 3.10-3.12 │     │  - Run test notebook     │     │  - Only on main     │
│                     │     │  - Rollback if fails     │     │  - After all gates  │
└─────────────────────┘     └──────────────────────────┘     └─────────────────────┘
                                      │
                                      │ On failure:
                                      ▼
                              ┌────────────────┐
                              │   ROLLBACK     │
                              │  Destroy dev   │
                              │  deployment    │
                              └────────────────┘
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

### GitHub Secrets

Add these secrets in your GitHub repo (Settings → Secrets → Actions):

| Secret              | Value                                            |
|---------------------|--------------------------------------------------|
| `DATABRICKS_HOST`   | Your workspace URL (e.g., `https://dbc-xxx.cloud.databricks.com`) |
| `DATABRICKS_TOKEN`  | A Databricks Personal Access Token               |

### Databricks Workspace

- Serverless compute must be enabled, **or** uncomment the cluster config
  in `resources/dataops_jobs.yml`
- The user associated with the token needs permissions to create jobs
  and run notebooks

## Key Concepts for Students

1. **Unit Tests (DevOps)**: Test your Python code locally with pytest
2. **Bundle Deploy (DataOps)**: Package and deploy notebooks + jobs to Databricks
3. **Data Quality Tests (DataOps)**: Run assertions on actual Spark data
4. **Gated Promotion**: Only deploy to prod after ALL tests pass
5. **Automatic Rollback**: Destroy failed deployments — bad code never stays live
