# MCP Jenkins
![PyPI Version](https://img.shields.io/pypi/v/mcp-jenkins)
[![PyPI Downloads](https://static.pepy.tech/badge/mcp-jenkins)](https://pepy.tech/projects/mcp-jenkins)
[![test](https://github.com/lanbaoshen/mcp-jenkins/actions/workflows/test.yml/badge.svg)](https://github.com/lanbaoshen/mcp-jenkins/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/lanbaoshen/mcp-jenkins/branch/master/graph/badge.svg)](https://codecov.io/gh/lanbaoshen/mcp-jenkins)
![License](https://img.shields.io/github/license/lanbaoshen/mcp-jenkins)

The Model Context Protocol (MCP) is an open-source implementation that bridges Jenkins with AI language models following Anthropic's MCP specification. This project enables secure, contextual AI interactions with Jenkins tools while maintaining data privacy and security.

## Installation
Choose one of these installation methods:
```
# Using uv (recommended)
pip install uv
uvx mcp-jenkins

# Using pip
pip install mcp-jenkins
mcp-jenkins

# Docker
docker pull ghcr.io/lanbaoshen/mcp-jenkins:latest
docker run -p 9887:9887 --rm ghcr.io/lanbaoshen/mcp-jenkins:latest --transport streamable-http
```

## Line Arguments
When using command line arguments, you can specify the Jenkins server details as follows:

```shell
# Simple streamable-http example
uvx mcp-jenkins --transport streamable-http
```

| Argument                                                     | Description                                                                                                     | Required |
|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|----------|
| `--jenkins-url`                                              | The URL of the Jenkins server. (Http app can set it via headers `x-jenkins-url`)                                | No       |
| `--jenkins-username`                                         | The username for Jenkins authentication. (Http app can set it via headers `x-jenkins-username`)                 | No       |
| `--jenkins-password`                                         | The password or API token for Jenkins authentication. (Http app can set it via headers `x-jenkins-password`)    | No       |
| `--jenkins-timeout`                                          | Timeout for Jenkins API requests in seconds. Default is `5` seconds.                                            | No       |
| `--jenkins-verify-ssl/--no-jenkins-verify-ssl`               | Whether to verify SSL certificates when connecting to Jenkins. Default is to verify.                            | No       |
| `--jenkins-session-singleton/--no-jenkins-session-singleton` | Whether to use a singleton Jenkins client for all requests in the same session. Default is True.                | No       |
| `--read-only`                                                | Whether to enable read-only mode. Default is False                                                              | No       |
| `--transport`                                                | Transport method to use for communication. Options are `stdio`, `sse` or `streamable-http`. Default is `stdio`. | No       |
| `--host`                                                     | Host address for `streamable-http` transport. Default is `0.0.0.0`                                              | No       |
| `--port`                                                     | Port number for `streamable-http` transport. Default is `9887`.                                                 | No       |

### Environment Variables

You can also provide Jenkins credentials via environment variables:

- `jenkins_url` or `JENKINS_URL`
- `jenkins_username` or `JENKINS_USERNAME` or `JENKINS_USER`
- `jenkins_password` or `JENKINS_PASSWORD` or `JENKINS_TOKEN`
- `jenkins_timeout` or `JENKINS_TIMEOUT`
- `jenkins_verify_ssl` or `JENKINS_VERIFY_SSL`
- `JENKINS_CA_BUNDLE` (path to a custom CA bundle file)

`jenkins_verify_ssl` / `JENKINS_VERIFY_SSL` accepts `true` / `false`.
If `JENKINS_CA_BUNDLE` is set, that file path is used as Requests `verify` value.

## Configuration and Usage

### Jetbrains Github Copilot
1. Open Jetbrains Settings
2. Navigate to Github Copilot > MCP > Configure
3. Add the following configuration:
```json
{
  "servers": {
    "my-mcp-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "mcp-jenkins",
        "--jenkins-url=xxx",
        "--jenkins-username=xxx",
        "--jenkins-password=xxx"
      ]
    }
  }
}
```

### VSCode Copilot Chat
1. Create `.vscode` folder with `mcp.json` file in you workspace for local setup or edit `settings.json` trough settings menu.
2. Insert the following configuration:
- SSE mode
```json
{
    "servers": {
        "jenkins": {
            "url": "http://localhost:9887/sse",
            "type": "sse"
        }
    }
}
```
- Streamable-Http mode
```json
{
    "servers": {
        "mcp-jenkins-mcp": {
            "autoApprove": [],
            "disabled": false,
            "timeout": 60,
            "type": "streamableHttp",
            "url": "http://localhost:9887/mcp"
        }
    }
}
```

Run the Jenkins MCP server with the following command:
```shell
uvx mcp-jenkins \
  --jenkins-url xxx \
  --jenkins-username xxx  \
  --jenkins-password xxx \
  --transport sse
```

## Available Tools
| Tool                       | Description                                         |
|----------------------------|-----------------------------------------------------|
| `get_item`                 | Get a specific item by name. Supports `tree` for field selection. |
| `get_item_config`          | Get the configuration of a specific item.           |
| `get_item_parameters`      | Get the parameters of a specific item.              |
| `get_all_items`            | Get all items in Jenkins.                           |
| `query_items`              | Query items based on pattern.                       |
| `build_item`               | Build a item.                                       |
| `get_all_nodes`            | Get all nodes in Jenkins.                           |
| `get_node`                 | Get a specific node by name.                        |
| `get_node_config`          | Get the configuration of a specific node.           |
| `get_all_queue_items`      | Get all queue items in Jenkins.                     |
| `get_queue_item`           | Get a specific queue item by ID.                    |
| `cancel_queue_item`        | Cancel a specific queue item by ID.                 |
| `get_build`                | Get a specific build by job name and build number. Supports `tree` for field selection. |
| `get_build_scripts`        | Get scripts associated with a specific build.       |
| `get_build_console_output` | Get the console output of a specific build.         |
| `get_build_parameters`     | Get the parameters of a specific build.             |
| `get_build_test_report`    | Get the test report of a specific build. Supports `tree` for field selection. |
| `get_running_builds`       | Get all currently running builds in Jenkins.        |
| `stop_build`               | Stop a specific build by job name and build number. |
| `get_view`                 | Get a specific view by name.                        |
| `get_all_views`            | Get the configuration of a specific view.           |

### `tree` Parameter (Field Selection)

`get_item`, `get_build`, and `get_build_test_report` accept an optional `tree` parameter that maps directly to the [Jenkins REST API `?tree=` query parameter](https://www.jenkins.io/doc/book/using/remote-access-api/). It lets you select only the fields you need, which can reduce response sizes by an order of magnitude.

**Syntax:** comma-separated field names, with nested fields in `[]`.

| Use case | `tree` value |
|---|---|
| Test failures only | `suites[cases[name,status,errorDetails]]` |
| Build result + duration | `number,result,duration,timestamp` |
| Job name + last build status | `name,color,lastBuild[number,result]` |

**Example — fetch only failed test cases:**
```python
get_build_test_report(
    fullname="My_Job",
    tree="suites[cases[name,status,errorDetails]]"
)
```
Then filter locally:
```bash
jq '[.suites[].cases[] | select(.status == "FAILED") | {name, error: .errorDetails}]'
```

## Typical CI Flow (Using MCP Tools)

This is a common automation flow after pushing code:

1. Find the job:
   - `query_items(fullname_pattern=...)` or `get_item(fullname=...)`
   - Use `color_pattern="red"` on `query_items` to scope to failing jobs only
2. Trigger build:
   - `build_item(fullname=..., build_type='build')`
   - For parameterized jobs use `build_type='buildWithParameters'` with `params={...}`
3. Track queue:
   - `get_queue_item(id=<queue_id>)` until executable/build number is available
4. Track build:
   - `get_build(fullname=..., number=...)` until `building=false`
5. Inspect results:
   - `get_build_test_report(..., tree="suites[cases[name,status,errorDetails]]")` — returns only test names + failure details, avoiding megabyte-sized payloads
   - `get_build_console_output(..., pattern='(FAIL|ERROR|Exception)', limit=...)` for fast log triage

Notes:
- Some Jenkins endpoints are permission-gated (for example plugin manager APIs).
- On restricted roles, plugin tools may raise `JenkinsPermissionError` while regular job/build tools still work.

## Contributing
[CONTRIBUTING.md](CONTRIBUTING.md)

## License
Licensed under MIT - see [LICENSE](LICENSE) file. This is not an official Jenkins product.

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=lanbaoshen/mcp-jenkins&type=Date)](https://www.star-history.com/#lanbaoshen/mcp-jenkins&Date)
