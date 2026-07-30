import subprocess
import sys

def main():
    print("Staging changes...")
    subprocess.run(["git", "add", "."], cwd=r"d:\pro\ai-ops-assistant")
    
    print("Committing changes...")
    subprocess.run(["git", "commit", "-m", "Deploy AWS Lambda Container Image and S3 CloudFront frontend pipeline"], cwd=r"d:\pro\ai-ops-assistant")
    
    print("Pushing to origin main...")
    res = subprocess.run(["git", "push", "origin", "main"], cwd=r"d:\pro\ai-ops-assistant")
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
