#!/bin/bash
# Deployment script for Ha-WakeWord-LU on Unraid
# This script deploys the Luxembourgish wake word detector to Unraid

set -e

echo "=================================="
echo "Ha-WakeWord-LU Deployment Script"
echo "=================================="
echo ""

# Configuration
UNRAID_HOST="192.168.10.100"
UNRAID_USER="root"
UNRAID_PASSWORD="Gx4GG_lom23822"
DEPLOY_PATH="/mnt/user/appdata/ai/Ha-WakeWord-LU"
MODELS_PATH="/mnt/user/appdata/ai/roberto-models"

echo "Target: $UNRAID_USER@$UNRAID_HOST:$DEPLOY_PATH"
echo ""

# Create deployment directories on Unraid
echo "[1/5] Creating directories on Unraid..."
sshpass -p "$UNRAID_PASSWORD" ssh "$UNRAID_USER@$UNRAID_HOST" "mkdir -p $DEPLOY_PATH $MODELS_PATH"

# Copy project files to Unraid
echo "[2/5] Copying project files..."
sshpass -p "$UNRAID_PASSWORD" scp -r \
    docker-compose.yml \
    docker-compose-training.yml \
    training \
    README.md \
    "$UNRAID_USER@$UNRAID_HOST:$DEPLOY_PATH/"

# Copy trained models if they exist
if [ -d "training/models" ] && [ "$(ls -A training/models/*.tflite 2>/dev/null)" ]; then
    echo "[3/5] Copying trained models..."
    sshpass -p "$UNRAID_PASSWORD" scp training/models/*.tflite "$UNRAID_USER@$UNRAID_HOST:$MODELS_PATH/"
else
    echo "[3/5] No trained models found - skipping model copy"
    echo "     You'll need to train the model first using docker-compose-training.yml"
fi

# Deploy the container
echo "[4/5] Deploying wake word service..."
sshpass -p "$UNRAID_PASSWORD" ssh "$UNRAID_USER@$UNRAID_HOST" "cd $DEPLOY_PATH && docker-compose up -d"

# Check deployment status
echo "[5/5] Checking deployment status..."
sshpass -p "$UNRAID_PASSWORD" ssh "$UNRAID_USER@$UNRAID_HOST" "docker ps | grep ha-wakeword-lu"

echo ""
echo "=================================="
echo "Deployment complete!"
echo "=================================="
echo ""
echo "Service available at: tcp://192.168.106.20:10400"
echo ""
echo "Next steps:"
echo "1. If you haven't trained the model yet:"
echo "   - SSH to Unraid: ssh $UNRAID_USER@$UNRAID_HOST"
echo "   - Navigate to: cd $DEPLOY_PATH"
echo "   - Run training: docker-compose -f docker-compose-training.yml up"
echo ""
echo "2. Configure Home Assistant:"
echo "   - Add Wyoming integration"
echo "   - Host: 192.168.106.20"
echo "   - Port: 10400"
echo ""
echo "3. View logs: ssh $UNRAID_USER@$UNRAID_HOST 'docker logs -f ha-wakeword-lu'"
