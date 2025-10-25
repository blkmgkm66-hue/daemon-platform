"""Tests for /generate-workflow endpoint

This file tests the Vertex AI integration for the /generate-workflow endpoint.

Setup Required:
1. Install pytest: pip install pytest
2. Authenticate with GCP: gcloud auth application-default login
3. Ensure Vertex AI API is enabled in your GCP project

Usage:
    pytest tests/test_generate_workflow.py -v

Note: This test calls the REAL Vertex AI API and will incur small costs (~$0.01-0.02)
"""

import sys
import os

# Add parent directory to path to import main module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


def test_generate_workflow_success():
    """Test successful workflow generation with a simple prompt"""
    response = client.post("/generate-workflow", json={
        "prompt": "Create a workflow that posts 'Hello World' to Slack"
    })
    
    # Check status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    
    # Check response structure
    data = response.json()
    assert "generated_code" in data, "Response missing 'generated_code' field"
    assert "workflow_id" in data, "Response missing 'workflow_id' field"
    
    # Verify generated code is not empty
    assert len(data["generated_code"]) > 0, "Generated code is empty"
    
    # Verify workflow_id follows expected format (wf-<hash>)
    assert data["workflow_id"].startswith("wf-"), f"Workflow ID doesn't start with 'wf-': {data['workflow_id']}"
    assert len(data["workflow_id"]) == 15, f"Workflow ID wrong length: {data['workflow_id']}"  # wf- + 12 char hash
    
    # Verify generated code contains Python-like syntax
    code = data["generated_code"]
    assert "def" in code or "import" in code or "post_slack_message" in code, \
        "Generated code doesn't appear to contain valid Python"
    
    print(f"\n✅ Test passed!")
    print(f"   Workflow ID: {data['workflow_id']}")
    print(f"   Generated code length: {len(code)} characters")
    print(f"   First 100 chars: {code[:100]}...")


def test_generate_workflow_with_sdk_functions():
    """Test that generated code references SDK functions"""
    response = client.post("/generate-workflow", json={
        "prompt": "Create a workflow that reads trigger data, retrieves a secret, and posts to Slack"
    })
    
    assert response.status_code == 200
    data = response.json()
    code = data["generated_code"]
    
    # Check if SDK functions are referenced
    # Note: AI might use different function names, so we check for common patterns
    has_trigger = "trigger" in code.lower() or "get_trigger_data" in code
    has_secret = "secret" in code.lower() or "get_secret" in code
    has_slack = "slack" in code.lower() or "post_slack_message" in code
    
    # At least 2 out of 3 SDK concepts should be present
    sdk_count = sum([has_trigger, has_secret, has_slack])
    assert sdk_count >= 2, f"Generated code doesn't reference enough SDK functions. Code: {code[:200]}"
    
    print(f"\n✅ Test passed!")
    print(f"   SDK function references: trigger={has_trigger}, secret={has_secret}, slack={has_slack}")


def test_generate_workflow_empty_prompt():
    """Test error handling for empty prompt"""
    response = client.post("/generate-workflow", json={
        "prompt": ""
    })
    
    # Should either return 422 (validation error) or 500 (server handles it)
    assert response.status_code in [422, 500], f"Unexpected status code: {response.status_code}"
    
    print(f"\n✅ Test passed! Empty prompt correctly rejected with status {response.status_code}")


def test_generate_workflow_different_prompts():
    """Test that different prompts generate different workflow IDs"""
    response1 = client.post("/generate-workflow", json={
        "prompt": "Post 'Morning update' to Slack"
    })
    response2 = client.post("/generate-workflow", json={
        "prompt": "Post 'Evening summary' to Slack"
    })
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    workflow_id1 = response1.json()["workflow_id"]
    workflow_id2 = response2.json()["workflow_id"]
    
    # Different prompts should generate different workflow IDs
    assert workflow_id1 != workflow_id2, "Different prompts generated same workflow ID"
    
    print(f"\n✅ Test passed!")
    print(f"   Workflow ID 1: {workflow_id1}")
    print(f"   Workflow ID 2: {workflow_id2}")


def test_health_check():
    """Test that the health check endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print(f"\n✅ Health check passed!")


if __name__ == "__main__":
    # Allow running this file directly for quick testing
    print("Running tests...\n")
    print("=" * 70)
    
    try:
        test_health_check()
        print("\n" + "=" * 70)
        
        test_generate_workflow_success()
        print("\n" + "=" * 70)
        
        test_generate_workflow_with_sdk_functions()
        print("\n" + "=" * 70)
        
        test_generate_workflow_empty_prompt()
        print("\n" + "=" * 70)
        
        test_generate_workflow_different_prompts()
        print("\n" + "=" * 70)
        
        print("\n🎉 All tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
