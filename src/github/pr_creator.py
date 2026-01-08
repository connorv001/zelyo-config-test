"""GitHub PR Creator for GitOps remediation."""

import os
from typing import Optional
from datetime import datetime
from github import Github, GithubException
from src.llm.prompts import PR_DESCRIPTION_TEMPLATE


class GitHubPRCreator:
    """Creates PRs in GitHub for remediation fixes."""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        
        self.repo_name = os.getenv("GITHUB_REPO")
        if not self.repo_name:
            raise ValueError("GITHUB_REPO environment variable is required (format: org/repo)")
        
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        self.github = Github(self.token)
        self.repo = self.github.get_repo(self.repo_name)
    
    def create_remediation_pr(
        self,
        control_id: str,
        description: str,
        resource_id: str,
        severity: str,
        yaml_patch: str,
        fix_strategy: str,
        risk_summary: str,
        file_path: Optional[str] = None,
    ) -> dict:
        """
        Create a PR with the remediation fix.
        
        Args:
            control_id: Kubescape control ID
            description: Finding description
            resource_id: Affected resource
            severity: Severity level
            yaml_patch: YAML content to add/modify
            fix_strategy: Description of the fix approach
            risk_summary: Analysis of the risk
            file_path: Target file path in repo (auto-generated if None)
            
        Returns:
            dict with pr_url, pr_number, branch_name
        """
        # Generate branch name
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"zelyo/{control_id.lower()}-{timestamp}"
        
        # Generate file path if not provided
        if not file_path:
            # Create in a remediation folder
            resource_safe = resource_id.replace("/", "-").replace(":", "-")[:50]
            file_path = f"remediations/{control_id}/{resource_safe}.yaml"
        
        # Get base branch ref
        base_ref = self.repo.get_branch(self.base_branch)
        
        # Create new branch
        self.repo.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=base_ref.commit.sha
        )
        
        # Create/update file with the fix
        commit_message = f"fix({control_id}): Remediate {description[:50]}"
        
        try:
            # Try to get existing file
            existing_file = self.repo.get_contents(file_path, ref=branch_name)
            self.repo.update_file(
                path=file_path,
                message=commit_message,
                content=yaml_patch,
                sha=existing_file.sha,
                branch=branch_name,
            )
        except GithubException:
            # File doesn't exist, create it
            self.repo.create_file(
                path=file_path,
                message=commit_message,
                content=yaml_patch,
                branch=branch_name,
            )
        
        # Generate PR description
        pr_body = PR_DESCRIPTION_TEMPLATE.format(
            control_id=control_id,
            description=description,
            resource_id=resource_id,
            severity=severity,
            risk_summary=risk_summary,
            strategy=fix_strategy,
        )
        
        # Create PR
        pr_title = f"[Zelyo] {control_id}: {description[:60]}"
        pr = self.repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base=self.base_branch,
        )
        
        # Add labels if they exist
        try:
            pr.add_to_labels("zelyo", "security", "auto-generated")
        except GithubException:
            pass  # Labels might not exist
        
        return {
            "pr_url": pr.html_url,
            "pr_number": pr.number,
            "branch_name": branch_name,
            "file_path": file_path,
        }
    
    def create_escalation_issue(
        self,
        control_id: str,
        description: str,
        resource_id: str,
        severity: str,
        escalation_reason: str,
    ) -> dict:
        """
        Create an issue for findings that require human escalation.
        
        Args:
            control_id: Kubescape control ID
            description: Finding description
            resource_id: Affected resource
            severity: Severity level
            escalation_reason: Why this needs human review
            
        Returns:
            dict with issue_url, issue_number
        """
        issue_title = f"[Zelyo Escalation] {control_id}: {description[:50]}"
        
        issue_body = f"""## 🚨 Security Finding Requires Human Review

**Control:** `{control_id}` - {description}
**Resource:** `{resource_id}`
**Severity:** {severity}

---

### Why Escalation is Needed
{escalation_reason}

---

### Recommended Actions
1. Review the finding in your cluster
2. Assess the impact of potential fixes
3. Implement the fix manually if needed

---

*Created by Zelyo Config Guardian - Human-in-the-Loop Escalation*
"""
        
        issue = self.repo.create_issue(
            title=issue_title,
            body=issue_body,
            labels=["zelyo", "escalation", "security"],
        )
        
        return {
            "issue_url": issue.html_url,
            "issue_number": issue.number,
        }
