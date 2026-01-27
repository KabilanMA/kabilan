import subprocess
import sys

# --- CONFIGURATION ---
# Your university username and server address
REMOTE_USER = "kabilan"
REMOTE_HOST = "rlogin.cs.vt.edu"

# The FULL path on the server where files should go
# WARNING: 'rsync --delete' will wipe this directory to match your local site.
REMOTE_PATH = "/web/people/kabilan/"

# Local directory to push
LOCAL_DIR = "_site/"

def run_command(command):
    """Runs a shell command and exits if it fails."""
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error running: {command}")
        sys.exit(1)

def main():
    print(f"🚀 Starting deployment to {REMOTE_HOST}...")

    # Step 1: Clean and Build Jekyll
    print("🔨 Building Jekyll site...")
    # 'JEKYLL_ENV=production' ensures optimized assets
    run_command("bundle exec jekyll build")

    # Step 2: Push files using rsync
    # -a: archive mode (keeps permissions/dates)
    # -v: verbose
    # -z: compress during transfer (faster)
    # --delete: removes files on server that you deleted locally (keeps it clean)
    print("📤 Pushing files to server...")
    
    rsync_cmd = (
        f"rsync -avz --delete "
        f"{LOCAL_DIR} {REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}"
    )
    
    run_command(rsync_cmd)

    print("✅ Deployment Complete!")

if __name__ == "__main__":
    main()