# Secure CI/CD Demo

This repository is a small Python API used to demonstrate a security-focused CI/CD pipeline with GitHub Actions.

The application itself is intentionally simple. The purpose of the project is to show a clean, repeatable pipeline that can test, scan, build, and publish a deployable artifact while applying basic security controls.

## Application Overview

The app is a minimal HTTP API built with the Python standard library.

Available endpoints:

- `GET /` - Returns a basic service status message.
- `GET /health` - Returns a health check response.
- `GET /security-summary` - Returns a summary of the security controls represented in the project.

The runtime application intentionally avoids third-party Python dependencies. This reduces supply-chain risk and keeps the deployable artifact small.

## Running Locally

Create and activate a virtual environment:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

Install development dependencies:

~~~bash
pip install -r requirements-dev.txt
~~~

Run the app:

~~~bash
python -m app.main
~~~

Test the health endpoint:

~~~bash
curl http://127.0.0.1:8000/health
~~~

Expected response:

~~~json
{"status": "healthy"}
~~~

## Running with Docker

Build the image:

~~~bash
docker build -t secure-cicd-demo .
~~~

Run the container:

~~~bash
docker run --rm -p 8000:8000 secure-cicd-demo
~~~

Test the health endpoint:

~~~bash
curl http://127.0.0.1:8000/health
~~~

## CI/CD Pipeline

This repository includes two GitHub Actions workflows.

### CI Security Checks

File: `.github/workflows/ci.yml`

This workflow runs on pushes and pull requests to `main`.

It performs:

- Unit tests with `pytest`
- Linting with `ruff`
- Static security analysis with `bandit`
- Dependency vulnerability auditing with `pip-audit`

The workflow uses read-only repository permissions:

~~~yaml
permissions:
  contents: read
~~~

This follows the principle of least privilege by only granting the workflow access needed to read the repository contents.

### Container Build, Scan, and Publish

File: `.github/workflows/container.yml`

This workflow runs on pushes to `main` and can also be manually triggered.

It performs:

- Docker Buildx setup
- GitHub Container Registry authentication
- Container image build
- Container vulnerability scanning with Trivy
- Container image publishing to GitHub Container Registry

The image is published to:

~~~text
ghcr.io/sagewater1283/secure-cicd-demo
~~~

The workflow grants package write access only where needed to publish the container image.

## Security Choices

### Minimal Runtime Dependencies

The app uses only the Python standard library at runtime. This was an intentional design choice to reduce third-party dependency risk.

Development and scanning tools are separated into `requirements-dev.txt`.

### Dependency Auditing

`pip-audit` checks the runtime dependency file for known vulnerabilities. Since the production dependency footprint is intentionally minimal, the runtime dependency audit currently reports no known vulnerabilities.

### Static Application Security Testing

`bandit` scans the application code for common Python security issues.

During development, Bandit flagged binding to all interfaces as a risky default. The app was updated to bind to `127.0.0.1` by default and only bind externally when explicitly configured through environment variables.

### Container Vulnerability Scanning

`trivy` scans the final container image. This matters because the deployable artifact includes the base image and operating system packages, not just application code.

During development, Trivy identified vulnerabilities in the Debian-based Python image. The project was updated to use a smaller Alpine-based Python image to reduce the container attack surface.

### Least-Privilege Workflow Permissions

Workflow permissions are explicitly defined. The CI workflow is read-only. The container workflow grants package write access only because it publishes to GitHub Container Registry.

## Production Hardening Ideas

If this project were being taken further, I would add:

- Branch protection rules requiring pull requests and passing checks before merge
- Required code review for changes to workflows and application code
- Dependabot updates for GitHub Actions and development dependencies
- GitHub secret scanning and push protection
- Container image signing with Sigstore/Cosign
- SBOM generation for published images
- OIDC-based cloud deployment instead of long-lived credentials
- Environment-specific deployments with approval gates
- More complete application logging and monitoring
- Versioned releases instead of only `latest` and commit SHA tags

## AI Usage

AI assistance was used for planning the repository structure, reviewing GitHub Actions syntax, troubleshooting scanner findings, and improving documentation clarity. All code, workflow behavior, scanner results, and final implementation decisions were reviewed and validated manually.
