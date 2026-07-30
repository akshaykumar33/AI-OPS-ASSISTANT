import os
import subprocess
import sys

def main():
    env = os.environ.copy()
    
    # Load .env variables cleanly
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    env[k] = v

    # Remove stale temporary session tokens
    env.pop('AWS_SESSION_TOKEN', None)

    # Force standard Docker V2 Schema 2 manifests compatible with AWS Lambda
    env['BUILDX_NO_DEFAULT_ATTESTATIONS'] = '1'
    env['DOCKER_DEFAULT_PLATFORM'] = 'linux/amd64'

    print(f"Deploying with AWS_ACCESS_KEY_ID: {env.get('AWS_ACCESS_KEY_ID')}")
    
    cmd = "npx serverless@3 deploy --stage prod --region ap-south-1"
    res = subprocess.run(cmd, cwd=r"d:\pro\ai-ops-assistant", env=env, shell=True)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
