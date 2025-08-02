#!/bin/bash

# navigate to absolute backend path
cd /Users/maxharsh/Desktop/Coding Projects/matchnet/backend || exit 1

# Initialize Conda for bash shell (only needed if running via cron or non-login shell)
source /opt/anaconda3/etc/profile.d/conda.sh

# Activate your Conda environment
conda activate matchnet

# Run the Python file
python3 app/routers/trigger_pipeline_router.py