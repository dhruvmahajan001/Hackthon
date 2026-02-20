from __future__ import annotations


def generate_branch_name(team_name: str, leader_name: str) -> str:
    """
    Convert team_name and leader_name into a valid branch name.

    Rules:
    - Uppercase
    - Spaces replaced with underscores
    - Only letters, numbers, and underscores allowed
    - Ends with _AI_Fix
    """
    combined = f"{team_name} {leader_name}".upper()
    combined = combined.replace(" ", "_")


    sanitized = []
    for ch in combined:
        if ch.isalnum() or ch == "_":
            sanitized.append(ch)
    base = "".join(sanitized)

    suffix = "_AI_Fix"
    if not base.endswith(suffix):
        base = f"{base}{suffix}"

    return base

