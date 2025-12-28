"""
GitHub Repository Cloning Script
Clones the PhonePe Pulse repository using GitPython
"""

import os
import logging
from git import Repo
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

REPO_URL = "https://github.com/PhonePe/pulse.git"
RAW_DATA_DIR = os.path.join("data", "raw")
REPO_DIR = os.path.join(RAW_DATA_DIR, "pulse")


def clone_repository():
    """
    Clone the PhonePe Pulse repository to data/raw/pulse directory.
    If repository already exists, pull latest changes.
    """
    try:
        # Create directory if it doesn't exist
        Path(RAW_DATA_DIR).mkdir(parents=True, exist_ok=True)
        
        repo_path = Path(REPO_DIR)
        
        if repo_path.exists() and (repo_path / ".git").exists():
            logger.info(f"Repository already exists at {REPO_DIR}. Pulling latest changes...")
            repo = Repo(REPO_DIR)
            origin = repo.remotes.origin
            origin.pull()
            logger.info("Repository updated successfully")
        else:
            logger.info(f"Cloning repository from {REPO_URL}...")
            Repo.clone_from(REPO_URL, REPO_DIR)
            logger.info(f"Repository cloned successfully to {REPO_DIR}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error cloning repository: {e}")
        return False


if __name__ == "__main__":
    success = clone_repository()
    if success:
        logger.info("Repository cloning completed successfully!")
    else:
        logger.error("Repository cloning failed!")
        exit(1)

