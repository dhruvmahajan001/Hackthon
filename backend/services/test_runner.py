import subprocess
from typing import Dict


def run_tests_in_docker(repo_path: str) -> Dict[str, object]:
    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{repo_path}:/app",
        "-w",
        "/app",
        "rift-test-image",
        "pytest",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        logs = (result.stdout or "") + (result.stderr or "")
        success = result.returncode == 0
        return {"success": success, "logs": logs}
    except subprocess.TimeoutExpired as exc:
        logs = (exc.stdout or "") + (exc.stderr or "")
        if not logs:
            logs = "Test run timed out after 60 seconds."
        return {"success": False, "logs": logs}
    except Exception as exc:
        return {"success": False, "logs": str(exc)}

