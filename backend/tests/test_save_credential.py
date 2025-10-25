"""Tests for /save-credential endpoint with mocked Secret Manager.

These tests mock the SecretManagerServiceClient to avoid creating
real secrets in GCP, following Gemini's guidance for testing approach.
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


def test_save_credential_new_secret():
    """Test saving credential when secret doesn't exist yet (creates new secret)."""
    with patch('main.secretmanager.SecretManagerServiceClient') as mock_sm:
        # Mock the client instance
        mock_client = MagicMock()
        mock_sm.return_value = mock_client
        
        # First call to add_secret_version will fail (secret doesn't exist)
        mock_client.add_secret_version.side_effect = [
            Exception("NOT_FOUND: Secret not found"),
            MagicMock(name="projects/test-project/secrets/daemon-mvp-slack-token/versions/1")
        ]
        
        # Mock create_secret to succeed
        mock_secret = MagicMock()
        mock_secret.name = "projects/test-project/secrets/daemon-mvp-slack-token"
        mock_client.create_secret.return_value = mock_secret
        
        response = client.post(
            "/save-credential",
            json={
                "credential_name": "slack_token",
                "secret_value": "xoxb-test-token-12345"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Credential saved successfully."
        assert "secret_version_id" in data
        
        # Verify create_secret was called
        mock_client.create_secret.assert_called_once()
        # Verify add_secret_version was called twice (fail, then succeed)
        assert mock_client.add_secret_version.call_count == 2


def test_save_credential_existing_secret():
    """Test saving credential when secret already exists (adds new version)."""
    with patch('main.secretmanager.SecretManagerServiceClient') as mock_sm:
        # Mock the client instance
        mock_client = MagicMock()
        mock_sm.return_value = mock_client
        
        # Mock add_secret_version to succeed on first call
        mock_version = MagicMock()
        mock_version.name = "projects/test-project/secrets/daemon-mvp-slack-token/versions/2"
        mock_client.add_secret_version.return_value = mock_version
        
        response = client.post(
            "/save-credential",
            json={
                "credential_name": "slack_token",
                "secret_value": "xoxb-updated-token-67890"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Credential saved successfully."
        assert data["secret_version_id"] == "2"
        
        # Verify add_secret_version was called once
        mock_client.add_secret_version.assert_called_once()
        # Verify create_secret was NOT called (secret already exists)
        mock_client.create_secret.assert_not_called()


def test_save_credential_other_error():
    """Test error handling when a non-NotFound error occurs."""
    with patch('main.secretmanager.SecretManagerServiceClient') as mock_sm:
        # Mock the client instance
        mock_client = MagicMock()
        mock_sm.return_value = mock_client
        
        # Mock add_secret_version to fail with permission error
        mock_client.add_secret_version.side_effect = Exception("PERMISSION_DENIED: Insufficient permissions")
        
        response = client.post(
            "/save-credential",
            json={
                "credential_name": "slack_token",
                "secret_value": "xoxb-test-token"
            }
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to save credential" in data["detail"]


def test_save_credential_create_fails():
    """Test error handling when creating a new secret fails."""
    with patch('main.secretmanager.SecretManagerServiceClient') as mock_sm:
        # Mock the client instance
        mock_client = MagicMock()
        mock_sm.return_value = mock_client
        
        # First call to add_secret_version will fail (secret doesn't exist)
        mock_client.add_secret_version.side_effect = Exception("NOT_FOUND: Secret not found")
        
        # Mock create_secret to fail
        mock_client.create_secret.side_effect = Exception("PERMISSION_DENIED: Cannot create secret")
        
        response = client.post(
            "/save-credential",
            json={
                "credential_name": "slack_token",
                "secret_value": "xoxb-test-token"
            }
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "Failed to create secret" in data["detail"]


def test_save_credential_empty_value():
    """Test that endpoint accepts empty string as valid secret value."""
    with patch('main.secretmanager.SecretManagerServiceClient') as mock_sm:
        # Mock the client instance
        mock_client = MagicMock()
        mock_sm.return_value = mock_client
        
        # Mock add_secret_version to succeed
        mock_version = MagicMock()
        mock_version.name = "projects/test-project/secrets/daemon-mvp-slack-token/versions/1"
        mock_client.add_secret_version.return_value = mock_version
        
        response = client.post(
            "/save-credential",
            json={
                "credential_name": "slack_token",
                "secret_value": ""
            }
        )
        
        # Should succeed - empty string is technically valid
        assert response.status_code == 201


# Standalone execution
if __name__ == "__main__":
    print("Running Secret Manager tests with mocked client...")
    print("\nTest 1: Save credential (new secret)...")
    test_save_credential_new_secret()
    print("✓ PASSED")
    
    print("\nTest 2: Save credential (existing secret)...")
    test_save_credential_existing_secret()
    print("✓ PASSED")
    
    print("\nTest 3: Error handling (other error)...")
    test_save_credential_other_error()
    print("✓ PASSED")
    
    print("\nTest 4: Error handling (create fails)...")
    test_save_credential_create_fails()
    print("✓ PASSED")
    
    print("\nTest 5: Empty secret value...")
    test_save_credential_empty_value()
    print("✓ PASSED")
    
    print("\nAll Secret Manager tests passed! ✓")
    print("\nNote: These tests use mocked Secret Manager client.")
    print("No actual secrets were created in GCP.")
