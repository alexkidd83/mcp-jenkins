class JenkinsPermissionError(Exception):
    """Jenkins denied access to an API endpoint (HTTP 401/403)."""

