import subprocess

def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"], check=True)