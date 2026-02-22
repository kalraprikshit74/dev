import subprocess

def run_git_command(command):
    """Runs a git command and handles errors."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error during Git operation:", e)

def git_checkin(branch_name, commit_message, remote="origin"):
    """Creates a new branch, checks out, commits changes, and pushes."""

    # Ensure repository is initialized
    run_git_command(["git", "init"])

    # Create and switch to the new branch
    run_git_command(["git", "checkout", "-b", branch_name])

    # Add all changes
    run_git_command(["git", "add", "."])

    # Commit changes
    run_git_command(["git", "commit", "-m", commit_message])

    # Push the branch to the remote repository
    run_git_command(["git", "push", remote, branch_name])

    print(f"Check-in completed for branch '{branch_name}'.")

# Example usage
git_checkin("branch1", "First commit on branch1")
git_checkin("branch2", "Second commit on branch2")
