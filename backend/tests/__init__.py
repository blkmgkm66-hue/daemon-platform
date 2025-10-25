"""Backend Tests Package

This package contains tests for the Daemon Platform backend API.

Test files:
- test_generate_workflow.py: Tests for /generate-workflow endpoint (Vertex AI integration)
- test_save_credential.py: Tests for /save-credential endpoint (Secret Manager integration)
- test_deploy_workflow.py: Tests for /deploy-workflow endpoint (Cloud Run deployment)

Setup Instructions:
1. Install dependencies: pip install pytest
2. Authenticate with GCP: gcloud auth application-default login
3. Run tests: pytest tests/ -v

For detailed testing strategy, see BUILD_MANUAL.md - Testing Strategy section.
"""
