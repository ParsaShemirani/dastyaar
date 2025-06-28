#!/usr/bin/env bash
set -euo pipefail

# Configuration
LOCAL_DIR="/Users/parsashemirani/Main/dastyaar"
REMOTE_USER="parsa"
REMOTE_HOST="192.168.1.4"
REMOTE_DIR="~/dastyaar"
ARCHIVE_NAME="dastyaar_deploy.zip"

# Step 0: Activate local virtual environment
cd "$LOCAL_DIR"
if [ -f ".venv/bin/activate" ]; then
  echo "Activating local virtual environment..."
  source ".venv/bin/activate"
else
  echo "Error: .venv not found. Exiting."
  exit 1
fi

# Step 1: Generate requirements.txt
echo "Generating requirements.txt..."
pip freeze > "$LOCAL_DIR/requirements.txt" 2>/dev/null

# Step 2: Package project into zip, excluding .venv
echo "Creating archive $ARCHIVE_NAME..."
zip -r "$ARCHIVE_NAME" . -x ".venv/*" > /dev/null 2>&1

# Step 3: Transfer archive to remote server
echo "Transferring archive..."
scp "$ARCHIVE_NAME" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/" > /dev/null 2>&1

# Step 4: Remote setup
echo "Setting up project on remote server..."
ssh "$REMOTE_USER@$REMOTE_HOST" bash -s <<EOF
set -euo pipefail
cd $REMOTE_DIR

echo "Removing old deployment..."
rm -rf src requirements.txt venv > /dev/null 2>&1

echo "Unpacking new archive..."
unzip -o $ARCHIVE_NAME > /dev/null 2>&1
rm $ARCHIVE_NAME > /dev/null 2>&1

echo "Creating virtual environment..."
python3 -m venv venv > /dev/null 2>&1
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

echo "Deployment complete."
EOF

# Step 5: Local cleanup
echo "Cleaning up local archive..."
rm "$LOCAL_DIR/$ARCHIVE_NAME" > /dev/null 2>&1

echo "Done."
