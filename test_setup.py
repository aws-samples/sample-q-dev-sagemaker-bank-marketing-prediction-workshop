"""Workshop environment check.

Verifies the Python version, the required workshop packages, the `.env` keys the labs
depend on, and live AWS connectivity. Exits non-zero if any check fails so it can be used
as a gate (e.g. in CI or a lifecycle script).
"""

import importlib
import os
import sys

from dotenv import load_dotenv

load_dotenv()

failures: list[str] = []

# --- Python version -------------------------------------------------------
python_version = sys.version_info
required_version = (3, 10)
print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
if python_version[:2] < required_version:
    failures.append(
        f"Python {required_version[0]}.{required_version[1]}+ required; found "
        f"{python_version.major}.{python_version.minor}.{python_version.micro}"
    )
else:
    print("Python version check passed!")

# --- Required packages ----------------------------------------------------
required_packages = ["sagemaker", "sagemaker_core", "boto3", "xgboost", "pandas", "jupyterlab"]
for pkg in required_packages:
    # jupyterlab imports as `jupyterlab`; sagemaker-core installs under sagemaker.core
    import_name = "sagemaker.core" if pkg == "sagemaker_core" else pkg
    try:
        importlib.import_module(import_name)
        print(f"Package check passed: {pkg}")
    except ImportError:
        failures.append(f"Required package not importable: {pkg} (did the .venv install requirements.txt?)")

# --- Required .env keys ----------------------------------------------------
required_env = [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_REGION",
    "SAGEMAKER_EXECUTION_ROLE",
    "S3_BUCKET_NAME",
]
missing_env = [k for k in required_env if not os.getenv(k)]
if missing_env:
    failures.append(f"Missing .env keys: {', '.join(missing_env)} (copy .env.example to .env and fill them in)")
else:
    print("All required .env keys are set!")
    print(f"Region: {os.getenv('AWS_REGION')}")

# --- Live AWS connectivity -------------------------------------------------
if not missing_env:
    try:
        import boto3

        account_info = boto3.client("sts").get_caller_identity()
        print("Successfully connected to AWS!")
        print(f"Account ID: {account_info['Account']}")
        print(f"User ARN: {account_info['Arn']}")
    except Exception as e:  # noqa: BLE001 — surface any auth/connectivity error to the participant
        failures.append(f"Could not connect to AWS with the provided credentials: {e}")

# --- Result ----------------------------------------------------------------
print()
if failures:
    print("Setup check FAILED:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print("Setup check passed — your environment is ready for the workshop.")
