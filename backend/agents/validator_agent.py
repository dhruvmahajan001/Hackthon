from typing import Any, Callable, Tuple


class PreCommitValidatorAgent:
    def validate_fix(
        self,
        repo_path: str,
        previous_failure_count: int,
        test_runner_function: Callable[[str], dict],
    ) -> Tuple[bool, int, str]:
        try:
            result: dict[str, Any] = test_runner_function(repo_path)
        except Exception as exc:
            logs = f"Test runner crashed: {exc}"
            return False, previous_failure_count, logs

        logs = str(result.get("logs", ""))

        new_failure_count = self._count_failures_from_logs(logs)

        # ✅ Accept fix if it improves or keeps failure count same
        if new_failure_count <= previous_failure_count:
            return True, new_failure_count, logs

        # ❌ Reject only if worse
        return False, new_failure_count, logs

    def _count_failures_from_logs(self, logs: str) -> int:
        """
        Counts pytest failures more reliably by parsing summary lines.
        """
        failure_count = 0

        for line in logs.splitlines():
            line = line.strip().lower()

            # Look for pytest summary pattern like:
            # "=== 2 failed, 1 passed in 0.03s ==="
            if " failed" in line:
                parts = line.split()
                for i, token in enumerate(parts):
                    if token == "failed":
                        try:
                            failure_count += int(parts[i - 1])
                        except Exception:
                            pass

        return failure_count
