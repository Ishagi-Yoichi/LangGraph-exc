# git_sync.py
import sys
import subprocess

def main():
    # Capture everything after "uv run git-push" as the commit message
    # This correctly joins multi-word arguments if quotes are omitted by mistake
    commit_message = " ".join(sys.argv[1:])
    
    if not commit_message.strip():
        print("Error: Missing commit message.")
        print('Usage: uv run git-push "your commit message"')
        sys.exit(1)
        
    try:
        # 1. git add .
        print("Staging all changes...")
        subprocess.run(["git", "add", "."], check=True)

        # 2. git commit -m "your message"
        print(f"Committing changes: '{commit_message}'...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # 3. git push
        print("Pushing to remote repository...")
        subprocess.run(["git", "push"], check=True)
        
        print("Success! Changes deployed.")

    except subprocess.CalledProcessError as e:
        print(f"\nFailed executing Git command. Exit code: {e.returncode}")
        sys.exit(e.returncode)
