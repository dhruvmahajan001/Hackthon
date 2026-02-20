from typing import Dict


class ScoringEngine:
    def calculate_score(self, result_data: Dict) -> Dict:
        iterations = result_data.get("iterations", 0)
        final_failures = result_data.get("final_failure_count", 0)

        base_score = 100

        # Retry penalty
        retry_penalty = max(iterations - 1, 0) * 5

        # Commit penalty (optional logic)
        commit_penalty = len(result_data.get("fixes_applied", [])) * 2

        final_score = base_score - retry_penalty - commit_penalty

        if final_failures > 0:
            final_score -= 20

        if final_score < 0:
            final_score = 0

        return {
            "final_score": final_score,
            "retry_penalty": retry_penalty,
            "commit_penalty": commit_penalty,
        }

