#!/bin/bash

# Daemon Platform - GCP API Setup Script
# This script enables all required Google Cloud APIs for the Daemon MVP
# 
# Prerequisites:
#   - gcloud CLI installed (https://cloud.google.com/sdk/docs/install)
#   - Authenticated with: gcloud auth login
#   - Project set: gcloud config set project PROJECT_ID
#
# Usage:
#   chmod +x scripts/setup-gcp-apis.sh
#   ./scripts/setup-gcp-apis.sh

set -e  # Exit on error

echo "========================================"
echo "Daemon Platform - GCP API Setup"
echo "========================================"
echo ""

# Get current project
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP project is set."
    echo "Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Project: $PROJECT_ID"
echo "🌍 Enabling required APIs..."
echo ""

# List of required APIs for Daemon Phase 0 (MVP)
APIS=(
    "run.googleapis.com"                  # Cloud Run - for containerized services
    "cloudfunctions.googleapis.com"       # Cloud Functions (future use)
    "pubsub.googleapis.com"               # Pub/Sub - for event-driven architecture
    "firestore.googleapis.com"            # Firestore - for workflow metadata storage
    "secretmanager.googleapis.com"        # Secret Manager - for credential storage
    "storage.googleapis.com"              # Cloud Storage - for code storage
    "aiplatform.googleapis.com"           # Vertex AI - for Gemini integration
    "apigateway.googleapis.com"           # API Gateway - for webhook endpoints
    "cloudbuild.googleapis.com"           # Cloud Build - for CI/CD
    "cloudresourcemanager.googleapis.com" # Resource Manager - for IAM management
    "iam.googleapis.com"                  # IAM - for service accounts
)

echo "APIs to enable:"
for api in "${APIS[@]}"; do
    echo "  • $api"
done
echo ""

# Confirm before proceeding
read -p "Do you want to enable these APIs? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted by user."
    exit 1
fi

echo ""
echo "⏳ Enabling APIs (this may take 2-3 minutes)..."
echo ""

# Enable all APIs
for api in "${APIS[@]}"; do
    echo "Enabling $api..."
    if gcloud services enable "$api" --project="$PROJECT_ID" 2>&1; then
        echo "  ✅ $api enabled"
    else
        echo "  ❌ Failed to enable $api"
    fi
done

echo ""
echo "========================================"
echo "✅ API Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Verify enabled APIs: gcloud services list --enabled"
echo "  2. Set up IAM roles and service accounts"
echo "  3. Begin Backend API development"
echo ""
echo "Region: Remember to set your default region"
echo "  Example: gcloud config set run/region us-east1"
echo ""
