"""Tests for /deploy-workflow endpoint with mocked GCS Storage and Firestore.

These tests mock the Storage and Firestore clients to avoid creating
real GCS objects or Firestore documents during testing, following
Gemini's guidance for the MVP testing approach.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)


def test_deploy_workflow_success():
    """Test successful workflow deployment with mocked GCS and Firestore."""
    with patch('main.storage.Client') as mock_storage, \
         patch('main.firestore.Client') as mock_firestore:
        
        # Mock GCS Storage client
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage.return_value.bucket.return_value = mock_bucket
        
        # Mock Firestore client
        mock_db = MagicMock()
        mock_doc = MagicMock()
        mock_db.collection.return_value.document.return_value = mock_doc
        mock_firestore.return_value = mock_db
        
        response = client.post(
            "/deploy-workflow",
            json={
                "workflow_id": "test-workflow-123",
                "generated_code": "print('Hello from workflow')"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Workflow deployed successfully."
        assert "webhook_url" in data
        assert "test-workflow-123" in data["webhook_url"]
        
        # Verify GCS blob upload was called
        mock_blob.upload_from_string.assert_called_once_with(
            "print('Hello from workflow')",
            content_type='text/x-python'
        )
        
        # Verify Firestore document was created
        mock_doc.set.assert_called_once()
        call_args = mock_doc.set.call_args[0][0]
        assert call_args['workflow_id'] == 'test-workflow-123'
        assert call_args['status'] == 'deployed'


def test_deploy_workflow_gcs_error():
    """Test error handling when GCS upload fails."""
    with patch('main.storage.Client') as mock_storage:
        # Mock GCS to raise an exception
        mock_storage.return_value.bucket.side_effect = Exception("GCS connection failed")
        
        response = client.post(
            "/deploy-workflow",
            json={
                "workflow_id": "test-workflow-456",
                "generated_code": "print('Test code')"
            }
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to deploy workflow" in data["detail"]


def test_deploy_workflow_firestore_error():
    """Test error handling when Firestore write fails."""
    with patch('main.storage.Client') as mock_storage, \
         patch('main.firestore.Client') as mock_firestore:
        
        # Mock GCS to succeed
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage.return_value.bucket.return_value = mock_bucket
        
        # Mock Firestore to fail
        mock_firestore.return_value.collection.side_effect = Exception("Firestore write failed")
        
        response = client.post(
            "/deploy-workflow",
            json={
                "workflow_id": "test-workflow-789",
                "generated_code": "print('Test')"
            }
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to deploy workflow" in data["detail"]


def test_deploy_workflow_validates_workflow_id():
    """Test that workflow_id is properly used in paths and metadata."""
    with patch('main.storage.Client') as mock_storage, \
         patch('main.firestore.Client') as mock_firestore:
        
        # Mock GCS Storage client
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage.return_value.bucket.return_value = mock_bucket
        
        # Mock Firestore client
        mock_db = MagicMock()
        mock_doc = MagicMock()
        mock_db.collection.return_value.document.return_value = mock_doc
        mock_firestore.return_value = mock_db
        
        workflow_id = "my-special-workflow"
        
        response = client.post(
            "/deploy-workflow",
            json={
                "workflow_id": workflow_id,
                "generated_code": "# Test code"
            }
        )
        
        assert response.status_code == 201
        
        # Verify correct path was used for GCS blob
        mock_bucket.blob.assert_called_once_with(f"{workflow_id}/main.py")
        
        # Verify correct document ID was used in Firestore
        mock_db.collection.assert_called_once_with('workflows')
        mock_db.collection.return_value.document.assert_called_once_with(workflow_id)


# Standalone execution
if __name__ == "__main__":
    print("Running /deploy-workflow endpoint tests with mocked GCS and Firestore...")
    print("\nTest 1: Deploy workflow (success)...")
    test_deploy_workflow_success()
    print("✓ PASSED")
    
    print("\nTest 2: Deploy workflow (GCS error)...")
    test_deploy_workflow_gcs_error()
    print("✓ PASSED")
    
    print("\nTest 3: Deploy workflow (Firestore error)...")
    test_deploy_workflow_firestore_error()
    print("✓ PASSED")
    
    print("\nTest 4: Deploy workflow (workflow_id validation)...")
    test_deploy_workflow_validates_workflow_id()
    print("✓ PASSED")
    
    print("\nAll /deploy-workflow tests passed! ✓")
    print("\nNote: These tests use mocked GCS Storage and Firestore clients.")
    print("No actual GCS objects or Firestore documents were created.")
