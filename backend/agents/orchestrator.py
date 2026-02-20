import os
import time
import json
from typing import Dict, List, Optional


from agents.analyzer_agent import FailureAnalyzerAgent
from agents.fix_agent import FixGeneratorAgent
from agents.validator_agent import PreCommitValidatorAgent
from agents.git_agent import GitAgent
from services.test_runner import run_tests_in_docker
from services.ci_monitor import CIMonitor
from services.scoring_engine import ScoringEngine




DEFAULT_MAX_RETRY = int(os.getenv("MAX_RETRY", 5))



class Orchestrator:
    def __init__(
        self,
        repo_path: str,
        team_name: str,
        leader_name: str,
        max_retry: Optional[int] = None,
    ):
        self.repo_path = repo_path
        self.team_name = team_name
        self.leader_name = leader_name
        self.max_retry = max_retry or DEFAULT_MAX_RETRY

        # Multi-agent architecture
        self.analyzer = FailureAnalyzerAgent()
        self.fix_agent = FixGeneratorAgent()
        self.validator = PreCommitValidatorAgent()
        self.git_agent = GitAgent(repo_path)

        # CI Monitor (requires GITHUB_TOKEN env)
        github_token = os.getenv("GITHUB_TOKEN")
        self.ci_monitor = CIMonitor(github_token) if github_token else None

        self.fixes_applied: List[Dict] = []

    # =====================================================
    # MAIN ENTRY
    # =====================================================

    def run(self) -> Dict:
        start_time = time.time()
        ci_status = "NOT_TRIGGERED"

        branch_name = self.git_agent.generate_branch_name(
            self.team_name,
            self.leader_name,
        )

        self.git_agent.create_and_checkout_branch(branch_name)

        iteration = 0

        # Initial docker test run
        result = run_tests_in_docker(self.repo_path)
        logs = result.get("logs", "")
        previous_failure_count = self._count_failures(logs)
        initial_failure_count = previous_failure_count 

        # =====================================================
        # Retry Loop
        # =====================================================

        while (
            iteration < self.max_retry
            and previous_failure_count > 0
        ):
            iteration += 1

            failures = self.analyzer.analyze_failures(logs)

            if not failures:
                break

            for bug in failures:
                file_relative_path = bug.get("file")
                if not file_relative_path:
                    continue

                file_path = os.path.join(
                    self.repo_path,
                    file_relative_path,
                )

                if not os.path.exists(file_path):
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    original_content = f.read()

                fixed_content = self.fix_agent.generate_fix(
                    file_relative_path,
                    bug,
                    original_content,
                )

                if fixed_content and fixed_content != original_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(fixed_content)

                    self.fixes_applied.append(bug)

            # Validate via Docker sandbox
            is_valid, new_failure_count, logs = (
                self.validator.validate_fix(
                    self.repo_path,
                    previous_failure_count,
                    run_tests_in_docker,
                )
            )

            if not is_valid:
                break

            # Commit & push
            self.git_agent.commit_changes(
                f"Iteration {iteration} automated fixes"
            )
            self.git_agent.push_branch(branch_name)

            # Trigger & monitor CI if configured
            if self.ci_monitor:
                try:
                    repo_full_name = self._extract_repo_full_name()
                    ci_status = self.ci_monitor.wait_for_ci(
                        repo_full_name,
                        branch_name,
                    )
                except Exception:
                    ci_status = "CI_MONITOR_FAILED"

            previous_failure_count = new_failure_count

        end_time = time.time()

        final_status = (
            "PASSED" if previous_failure_count == 0 else "FAILED"
        )

        result_data = {
            "repo_path": self.repo_path,
            "branch": branch_name,
            "iterations": iteration,
            "max_retry": self.max_retry,
            "initial_failure_count": initial_failure_count,
            "final_failure_count": previous_failure_count,
            "status": final_status,
            "ci_status": ci_status,
            "fixes_applied": self.fixes_applied,
            "total_time_seconds": round(
                end_time - start_time,
                2,
            ),
        }
        scoring_engine = ScoringEngine()
        score_data = scoring_engine.calculate_score(result_data)

        result_data["score"] = score_data


        self._write_results(result_data)

        return result_data

    # =====================================================
    # HELPERS
    # =====================================================

    def _count_failures(self, logs: str) -> int:
        failure_count = 0

        for line in logs.splitlines():
            line = line.strip().lower()
            if " failed" in line:
                parts = line.split()
                for i, token in enumerate(parts):
                    if token == "failed":
                        try:
                            failure_count += int(parts[i - 1])
                        except Exception:
                            pass

        return failure_count

    def _extract_repo_full_name(self) -> str:
        """
        Returns owner/repo format.
        Requires env variable GITHUB_USERNAME.
        """
        repo_name = os.path.basename(self.repo_path)
        github_username = os.getenv("GITHUB_USERNAME")

        if not github_username:
            raise RuntimeError(
                "GITHUB_USERNAME environment variable not set."
            )

        return f"{github_username}/{repo_name}"

    def _write_results(self, data: Dict) -> None:
        backend_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
            )
        )

        results_dir = os.path.join(
            backend_dir,
            "results",
        )

        os.makedirs(results_dir, exist_ok=True)

        results_path = os.path.join(
            results_dir,
            "results.json",
        )

        with open(
            results_path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=4)
