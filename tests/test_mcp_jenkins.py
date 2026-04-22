import os

from click.testing import CliRunner

from mcp_jenkins import main


def test_main_stdio(mocker):
    mocker.patch('mcp_jenkins.asyncio')
    mock_mcp = mocker.patch('mcp_jenkins.server.mcp')

    CliRunner().invoke(main, ['--transport', 'stdio'])

    mock_mcp.run_async.assert_called_once_with(transport='stdio')


def test_main_sse(mocker):
    mocker.patch('mcp_jenkins.asyncio')
    mock_mcp = mocker.patch('mcp_jenkins.server.mcp')

    CliRunner().invoke(main, ['--transport', 'sse', '--host', '127.0.0.1', '--port', '9887'])
    mock_mcp.run_async.assert_called_once_with(transport='sse', host='127.0.0.1', port=9887)


def test_main_streamable_http(mocker):
    mocker.patch('mcp_jenkins.asyncio')
    mock_mcp = mocker.patch('mcp_jenkins.server.mcp')

    CliRunner().invoke(
        main,
        ['--transport', 'streamable-http', '--host', '127.0.0.1', '--port', '9887'],
    )
    mock_mcp.run_async.assert_called_once_with(transport='streamable-http', host='127.0.0.1', port=9887)


def test_main(mocker):
    mocker.patch('mcp_jenkins.asyncio')
    mock_mcp = mocker.patch('mcp_jenkins.server.mcp')

    CliRunner().invoke(
        main,
        [
            '--transport',
            'stdio',
            '--jenkins-url',
            'https://example.com',
            '--jenkins-username',
            'username',
            '--jenkins-password',
            'password',
            '--jenkins-timeout',
            '30',
        ],
    )

    mock_mcp.run_async.assert_called_once_with(transport='stdio')


def test_main_does_not_shadow_uppercase_env_defaults(mocker, monkeypatch):
    mocker.patch('mcp_jenkins.asyncio')
    mock_mcp = mocker.patch('mcp_jenkins.server.mcp')

    monkeypatch.setenv('JENKINS_TIMEOUT', '13')
    monkeypatch.setenv('JENKINS_VERIFY_SSL', 'false')
    monkeypatch.setenv('JENKINS_SESSION_SINGLETON', 'false')
    monkeypatch.setenv('JENKINS_CA_BUNDLE', '/etc/ssl/certs/internal.pem')

    # Ensure lowercase aliases are unset before invoking CLI with defaults.
    monkeypatch.delenv('jenkins_timeout', raising=False)
    monkeypatch.delenv('jenkins_verify_ssl', raising=False)
    monkeypatch.delenv('jenkins_session_singleton', raising=False)

    CliRunner().invoke(main, ['--transport', 'stdio'])

    # Defaults should not be written into lowercase aliases.
    assert os.getenv('jenkins_timeout') is None
    assert os.getenv('jenkins_verify_ssl') is None
    assert os.getenv('jenkins_session_singleton') is None

    mock_mcp.run_async.assert_called_once_with(transport='stdio')


def test_main_sets_lowercase_env_when_flags_explicit(mocker, monkeypatch):
    mocker.patch('mcp_jenkins.asyncio')
    mock_mcp = mocker.patch('mcp_jenkins.server.mcp')

    monkeypatch.delenv('jenkins_timeout', raising=False)
    monkeypatch.delenv('jenkins_verify_ssl', raising=False)
    monkeypatch.delenv('jenkins_session_singleton', raising=False)

    CliRunner().invoke(
        main,
        [
            '--transport',
            'stdio',
            '--jenkins-timeout',
            '30',
            '--no-jenkins-verify-ssl',
            '--no-jenkins-session-singleton',
        ],
    )

    assert os.getenv('jenkins_timeout') == '30'
    assert os.getenv('jenkins_verify_ssl') == 'false'
    assert os.getenv('jenkins_session_singleton') == 'false'

    mock_mcp.run_async.assert_called_once_with(transport='stdio')
