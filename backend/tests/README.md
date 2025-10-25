# Backend Tests

Comprehensive test suite for the Daemon Platform backend API.

## Quick Start for Claude Code

### 1. Clone the Repository

```bash
git clone https://github.com/blkmgkm66-hue/daemon-platform.git
cd daemon-platform/backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest
```

### 3. Authenticate with GCP

```bash
gcloud auth application-default login
```

This authenticates your local environment to access GCP services (Vertex AI, Secret Manager, etc.)

### 4. Run Tests

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test file:**
```bash
pytest tests/test_generate_workflow.py -v
```

**Run a single test function:**
```bash
pytest tests/test_generate_workflow.py::test_generate_workflow_success -v
```

**Run with detailed output:**
```bash
pytest tests/ -v -s
```

## Test Files

### `test_generate_workflow.py`

Tests the `/generate-workflow` endpoint (Vertex AI integration).

**Test Coverage:**
- ✅ Health check endpoint
- ✅ Successful workflow code generation
- ✅ SDK function references in generated code
- ✅ Empty prompt error handling
- ✅ Different prompts generate unique workflow IDs

**Cost:** ~$0.01-0.02 per test run (Vertex AI API calls)

**Can also run directly:**
```bash
python tests/test_generate_workflow.py
```

### `test_save_credential.py` (Coming Soon)

Will test the `/save-credential` endpoint (Secret Manager integration).

### `test_deploy_workflow.py` (Coming Soon)

Will test the `/deploy-workflow` endpoint (Cloud Run deployment).

## Testing Strategy

We follow a **simplified incremental testing approach**:

1. **Test each component as we build it**
2. **Use real GCP services** (no mocking) to validate actual integrations
3. **Local testing** with FastAPI TestClient (no server needed)
4. **Minimal costs** by leveraging GCP free tiers
5. **Final manual end-to-end test** after deployment

See [BUILD_MANUAL.md - Testing Strategy](../../BUILD_MANUAL.md#testing-strategy) for full details.

## Expected Output

When tests pass, you'll see:

```
=================================================================== test session starts ====================================================================
platform darwin -- Python 3.x.x, pytest-x.x.x
collected 5 items

tests/test_generate_workflow.py::test_health_check PASSED                                                                                           [ 20%]
tests/test_generate_workflow.py::test_generate_workflow_success PASSED                                                                              [ 40%]
tests/test_generate_workflow.py::test_generate_workflow_with_sdk_functions PASSED                                                                   [ 60%]
tests/test_generate_workflow.py::test_generate_workflow_empty_prompt PASSED                                                                         [ 80%]
tests/test_generate_workflow.py::test_generate_workflow_different_prompts PASSED                                                                    [100%]

==================================================================== 5 passed in X.XXs =====================================================================
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'main'"

**Solution:** Run tests from the `backend/` directory:
```bash
cd backend
pytest tests/
```

### "google.auth.exceptions.DefaultCredentialsError"

**Solution:** Authenticate with GCP:
```bash
gcloud auth application-default login
```

### "ImportError: No module named 'pytest'"

**Solution:** Install pytest:
```bash
pip install pytest
```

### Tests failing with Vertex AI errors

**Possible causes:**
1. Vertex AI API not enabled → Enable in GCP Console
2. Wrong GCP project → Check `GCP_PROJECT_ID` in environment
3. Insufficient IAM permissions → Ensure your account has Vertex AI User role

## Cost Management

**Per test run costs:**
- `test_generate_workflow.py`: ~$0.01-0.02 (5 Vertex AI calls)
- `test_save_credential.py`: FREE (Secret Manager free tier: 10k ops/month)
- `test_deploy_workflow.py`: FREE (Cloud Run free tier: 2M requests/month)

**Total: ~$0.05-0.10 per full test suite run**

## Next Steps

1. **Run the existing test:** `pytest tests/test_generate_workflow.py -v`
2. **Share results** with the team
3. **If tests pass:** Mark testing milestone in BUILD_MANUAL.md
4. **If tests fail:** Report errors for debugging

## For More Information

- Full Testing Strategy: `../../BUILD_MANUAL.md#testing-strategy`
- Backend API Implementation: `../main.py`
- Requirements: `../requirements.txt`
