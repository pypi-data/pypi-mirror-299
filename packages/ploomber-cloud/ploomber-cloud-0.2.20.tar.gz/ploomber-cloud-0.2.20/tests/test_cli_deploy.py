import os
import sys
from pathlib import Path
from unittest.mock import Mock, ANY
import zipfile

import pytest

from ploomber_core.exceptions import COMMUNITY

from ploomber_cloud.cli import cli
from ploomber_cloud import api, zip_, deploy, github
from ploomber_cloud.constants import (
    FORCE_INIT_MESSAGE,
    VALID_PROJECT_TYPES,
)
from ploomber_cloud.github import GITHUB_DOCS_URL
from ploomber_cloud.util import pretty_print

CMD_NAME = "ploomber-cloud"

COMMUNITY = COMMUNITY.strip()

CONFIGURE_WORKFLOW_MESSAGE = f"""You may create a GitHub workflow \
file for deploying your application by running 'ploomber-cloud github'.
To learn more about GitHub actions refer: \
{GITHUB_DOCS_URL}"""

UPDATE_WORKFLOW_MESSAGE = f""".github/workflows/ploomber-cloud.yaml \
seems outdated. You may update it by running 'ploomber-cloud github'.
To learn more about GitHub actions refer: \
{GITHUB_DOCS_URL}"""


def test_deploy_error_if_missing_key(monkeypatch, fake_ploomber_dir, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert (
        "Error: API key not found. Please run 'ploomber-cloud key YOURKEY', "
        "or set the key in environment variable 'PLOOMBER_CLOUD_KEY'\n"
        f"{COMMUNITY}" == capsys.readouterr().err.strip()
    )


def test_deploy(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={},
    )

    with zipfile.ZipFile("app-someuuid.zip") as z:
        mapping = {}
        for name in z.namelist():
            mapping[name] = z.read(name)

    assert mapping == {
        "Dockerfile": b"FROM python:3.11",
        "app.py": b"print('hello world')",
        "fake-ploomber-dir/stats/config.yaml": b"cloud_key: somekey",
    }

    assert "Deploying project with id: someid" in capsys.readouterr().out


def test_deploy_with_custom_config(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--config", "config.json"])

    Path("ploomber-cloud.json").write_text('{"id": "anotherid", "type": "panel"}')
    Path("config.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={},
    )


def test_deploy_configure_github_msg(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    Path(".git").mkdir()

    def requests_get(*args, **kwargs):
        return Mock(status_code=200, content=b"name: Ploomber Cloud updated")

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={},
    )
    out = capsys.readouterr().out
    assert "Deploying project with id: someid" in out
    assert CONFIGURE_WORKFLOW_MESSAGE.strip() in out


def test_deploy_configure_github_msg_workflow_file_outdated(
    monkeypatch, set_key, capsys
):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))
    monkeypatch.setattr(github.click, "confirm", Mock(side_effect=[True]))
    mock_requests_get = Mock(name="requests.get")

    Path(".git").mkdir()
    Path(".github", "workflows").mkdir(parents=True)

    Path(".github/workflows/ploomber-cloud.yaml").write_text(
        """
name: Ploomber Cloud
"""
    )

    def requests_get(*args, **kwargs):
        return Mock(status_code=200, content=b"name: Ploomber Cloud updated")

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    mock_requests_get.side_effect = requests_get

    monkeypatch.setattr(github.requests, "get", mock_requests_get)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={},
    )

    out = capsys.readouterr().out
    assert "Deploying project with id: someid" in out
    assert UPDATE_WORKFLOW_MESSAGE.strip() in out


PROJECT_NOT_FOUND_ERROR = f"""Error: An error occurred: \
project some-project-123 was not found
{FORCE_INIT_MESSAGE}
{COMMUNITY}"""


def test_deploy_when_not_found_response(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=False,
            status_code=404,
            json=Mock(
                return_value={"detail": "project some-project-123 was not found"}
            ),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={},
    )
    assert PROJECT_NOT_FOUND_ERROR.strip() in capsys.readouterr().err.strip()


@pytest.mark.parametrize(
    "separate_watch_command",
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    "pass_job_id",
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    "watch_option",
    [
        "--watch",
        "--watch-incremental",
    ],
)
@pytest.mark.parametrize(
    "job_status, expected_msg",
    [
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "finished"],
                    ["serving-traffic", "active"],
                ],
                "resources": {
                    "webservice": "http://someid.ploomberapp.io",
                    "is_url_up": True,
                },
                "status": "running",
            },
            """Deployment success.
View project dashboard: https://www.platform.ploomber.io/applications/someid/jobid
View your deployed app: http://someid.ploomberapp.io""",
        ),
        (
            {
                "summary": [
                    ["build-docker", "failed"],
                    ["deploy", "failed"],
                    ["webservice", "pending"],
                    ["serving-traffic", "pending"],
                ],
                "resources": {"is_url_up": False},
                "status": "docker-failed",
            },
            """Deployment failed.
View project dashboard: https://www.platform.ploomber.io/applications/someid/jobid""",
        ),
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "failed"],
                    ["serving-traffic", "failed"],
                ],
                "resources": {"is_url_up": False},
                "status": "infrastructure-failed",
            },
            """Deployment failed.
View project dashboard: https://www.platform.ploomber.io/applications/someid/jobid""",
        ),
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "finished"],
                    ["serving-traffic", "failed"],
                ],
                "resources": {"is_url_up": False},
                "status": "failed",
            },
            """Deployment failed.
View project dashboard: https://www.platform.ploomber.io/applications/someid/jobid""",
        ),
    ],
)
def test_deploy_watch(
    monkeypatch,
    set_key,
    capsys,
    separate_watch_command,
    pass_job_id,
    watch_option,
    job_status,
    expected_msg,
):
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # Configure file zipping
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return
        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    # Mock 'post' call for client.deploy()
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    # mock 'get' call to return project response in order to get job id
    project_response_mock = Mock(
        ok=True,
        json=Mock(
            return_value={"id": "someid", "type": "docker", "jobs": [{"id": "jobid"}]}
        ),
    )
    # Mock 'get' call to return different job status info in deploy._watch()
    job_status_mock = Mock(
        ok=True,
        json=Mock(return_value=job_status),
    )
    job_logs_mock = Mock(
        ok=True,
        json=Mock(return_value={"logs": {"build-docker": "", "webservice": ""}}),
    )
    if (separate_watch_command and pass_job_id) or not separate_watch_command:
        mock_requests_get = Mock(
            name="requests.get",
            side_effect=[job_status_mock, job_logs_mock],
        )
    else:
        # otherwise need to get job id from project response
        mock_requests_get = Mock(
            name="requests.get",
            side_effect=[project_response_mock, job_status_mock, job_logs_mock],
        )
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    # Call CLI
    if separate_watch_command:
        monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
        with pytest.raises(SystemExit):
            cli()
        if pass_job_id:
            args = [CMD_NAME, "watch", "--project-id", "someid", "--job-id", "jobid"]
        else:
            args = [CMD_NAME, "watch", "--project-id", "someid"]
        monkeypatch.setattr(
            sys,
            "argv",
            args,
        )
        with pytest.raises(SystemExit):
            cli()
    else:
        monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", watch_option])
        with pytest.raises(SystemExit):
            cli()

    # Assert success/fail message is displayed
    assert expected_msg in capsys.readouterr().out


@pytest.mark.parametrize(
    "separate_watch_command",
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    "pass_job_id",
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    "watch_option",
    [
        "--watch",
        "--watch-incremental",
    ],
)
def test_deploy_watch_timeout(
    monkeypatch, set_key, capsys, separate_watch_command, pass_job_id, watch_option
):
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))
    monkeypatch.setattr(deploy, "TIMEOUT_MINS", 0)
    monkeypatch.setattr(deploy, "INTERVAL_SECS", 0)

    # Configure file zipping
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return
        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    # Mock 'post' call for client.deploy()
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    # mock 'get' call to return project response in order to get job id
    project_response_mock = Mock(
        ok=True,
        json=Mock(
            return_value={"id": "someid", "type": "docker", "jobs": [{"id": "jobid"}]}
        ),
    )
    # Mock 'get' call to return different job status info in deploy._watch()
    job_status_mock = Mock(
        ok=True,
        json=Mock(return_value={"summary": [], "status": "pending"}),
    )
    job_logs_mock = Mock(
        ok=True,
        json=Mock(return_value={"logs": {"build-docker": "", "webservice": ""}}),
    )
    if (separate_watch_command and pass_job_id) or not separate_watch_command:
        mock_requests_get = Mock(
            name="requests.get",
            side_effect=[job_status_mock, job_logs_mock],
        )
    else:
        # otherwise need to get job id from project response
        mock_requests_get = Mock(
            name="requests.get",
            side_effect=[project_response_mock, job_status_mock, job_logs_mock],
        )
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    # Call CLI
    if separate_watch_command:
        monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
        with pytest.raises(SystemExit):
            cli()
        monkeypatch.setattr(
            sys,
            "argv",
            [CMD_NAME, "watch", "--project-id", "someid", "--job-id", "jobid"],
        )
        with pytest.raises(SystemExit):
            cli()
    else:
        monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", f"{watch_option}"])
        with pytest.raises(SystemExit):
            cli()

    assert "Timeout reached." in capsys.readouterr().out


@pytest.mark.parametrize(
    "separate_watch_command",
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    "pass_job_id",
    [
        True,
        False,
    ],
)
@pytest.mark.parametrize(
    "job, expected_logs,",
    [
        (
            {
                "summary": [
                    ["build-docker", "active"],
                    ["deploy", "pending"],
                    ["webservice", "pending"],
                    ["serving-traffic", "pending"],
                ],
                "status": "pending",
            },
            "These are docker logs",
        ),
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "pending"],
                    ["serving-traffic", "pending"],
                ],
                "status": "pending",
            },
            "These are webservice logs",
        ),
    ],
)
def test_deploy_watch_logs(
    monkeypatch,
    set_key,
    capsys,
    separate_watch_command,
    pass_job_id,
    job,
    expected_logs,
):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))
    monkeypatch.setattr(deploy, "TIMEOUT_MINS", 0.001)
    monkeypatch.setattr(deploy, "INTERVAL_SECS", 0.1)

    # Configure file zipping
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return
        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    # Mock 'post' call for client.deploy()
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    # mock 'get' call to return project response in order to get job id
    project_response_mock = Mock(
        ok=True,
        json=Mock(
            return_value={"id": "someid", "type": "docker", "jobs": [{"id": "jobid"}]}
        ),
    )
    # Mock 'get' call to return different job status info in deploy._watch()
    job_status_mock = Mock(
        ok=True,
        json=Mock(return_value=job),
    )
    job_logs_mock = Mock(
        ok=True,
        json=Mock(
            return_value={
                "logs": {
                    "build-docker": "These are docker logs",
                    "webservice": "These are webservice logs",
                }
            }
        ),
    )
    if (separate_watch_command and pass_job_id) or not separate_watch_command:
        mock_requests_get = Mock(
            name="requests.get",
            side_effect=[job_status_mock, job_logs_mock],
        )
    else:
        # otherwise need to get job id from project response
        mock_requests_get = Mock(
            name="requests.get",
            side_effect=[project_response_mock, job_status_mock, job_logs_mock],
        )

    # Mock 'get' call to return different job status info in deploy._watch()
    mock_requests_get = Mock(
        name="requests.get",
        side_effect=[
            Mock(
                ok=True,
                json=Mock(return_value=job),
            ),
            Mock(
                ok=True,
                json=Mock(
                    return_value={
                        "logs": {
                            "build-docker": "These are docker logs",
                            "webservice": "These are webservice logs",
                        }
                    }
                ),
            ),
        ],
    )
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    # Call CLI
    if separate_watch_command:
        monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
        with pytest.raises(SystemExit):
            cli()
        monkeypatch.setattr(
            sys,
            "argv",
            [CMD_NAME, "watch", "--project-id", "someid", "--job-id", "jobid"],
        )
        with pytest.raises(SystemExit):
            cli()
    else:
        monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch"])
        with pytest.raises(SystemExit):
            cli()

    # Assert success/fail message is displayed
    assert expected_logs in capsys.readouterr().out


@pytest.mark.parametrize(
    "job, expected_logs,",
    [
        (
            {
                "summary": [
                    ["build-docker", "active"],
                    ["deploy", "pending"],
                    ["webservice", "pending"],
                    ["serving-traffic", "pending"],
                ],
                "status": "pending",
            },
            "2024-04-30T07:46:31.460000 - INFO Retrieving image.",
        ),
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "pending"],
                    ["serving-traffic", "pending"],
                ],
                "status": "pending",
            },
            "2024-04-30T07:47:51.191000 - [2024-04-30 07:47:51 +0000] "
            "[1] [INFO] Listening at: http://0.0.0.0:80 (1)",
        ),
    ],
)
def test_deploy_watch_incremental_logs(
    monkeypatch,
    set_key,
    capsys,
    job,
    expected_logs,
):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))
    monkeypatch.setattr(deploy, "TIMEOUT_MINS", 0.001)
    monkeypatch.setattr(deploy, "INTERVAL_SECS", 0.1)

    # Configure file zipping
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return
        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    # Mock 'post' call for client.deploy()
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    # Mock 'get' call to return different job status info in deploy._watch()
    mock_requests_get = Mock(
        name="requests.get",
        side_effect=[
            Mock(
                ok=True,
                json=Mock(return_value=job),
            ),
            Mock(
                ok=True,
                json=Mock(
                    return_value={
                        "logs": {
                            "build-docker": "2024-04-30T07:46:31.460000 - "
                            "INFO Retrieving image.",
                            "webservice": "2024-04-30T07:47:51.191000 - "
                            "[2024-04-30 07:47:51 +0000] "
                            "[1] [INFO] Listening at: http://0.0.0.0:80 (1)",
                        }
                    }
                ),
            ),
        ],
    )
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch-incremental"])
    with pytest.raises(SystemExit):
        cli()

    assert expected_logs in capsys.readouterr().out


@pytest.mark.parametrize(
    "job, output",
    [
        (
            {
                "summary": [
                    ["build-docker", "active"],
                    ["deploy", "pending"],
                    ["webservice", "pending"],
                    ["serving-traffic", "pending"],
                ],
                "status": "build-docker",
            },
            """The deployment process started! \
Track its status at: https://www.platform.ploomber.io/applications/someid/jobid

Tracking deployment progress...

Stage: build-docker; Status: active

Showing build-docker logs:
2024-04-30T07:46:31.460000 - INFO Retrieving image.
Timeout reached.
For more details, go to: https://www.platform.ploomber.io/applications/someid/jobid""",
        ),
        (
            {
                "summary": [
                    ["build-docker", "finished"],
                    ["deploy", "finished"],
                    ["webservice", "active"],
                    ["serving-traffic", "pending"],
                ],
                "status": "provisioning",
            },
            """The deployment process started! \
Track its status at: https://www.platform.ploomber.io/applications/someid/jobid

Tracking deployment progress...

Stage: build-docker; Status: finished
Stage: deploy; Status: finished
Stage: webservice; Status: active

Showing webservice logs:
2024-04-30T07:47:51.191000 - [2024-04-30 07:47:51 +0000] [1] \
[INFO] Listening at: http://0.0.0.0:80 (1)
Timeout reached.
For more details, go to: https://www.platform.ploomber.io/applications/someid/jobid""",
        ),
    ],
)
def test_deploy_watch_incremental_status(monkeypatch, set_key, capsys, job, output):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))
    monkeypatch.setattr(deploy, "TIMEOUT_MINS", 0.001)
    monkeypatch.setattr(deploy, "INTERVAL_SECS", 0.1)

    # Configure file zipping
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return
        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)
    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    # Mock 'post' call for client.deploy()
    mock_requests_post = Mock(name="requests.post")

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    # Mock 'get' call to return different job status info in deploy._watch()
    mock_requests_get = Mock(
        name="requests.get",
        side_effect=[
            Mock(
                ok=True,
                json=Mock(return_value=job),
            ),
            Mock(
                ok=True,
                json=Mock(
                    return_value={
                        "logs": {
                            "build-docker": "2024-04-30T07:46:31.460000 - "
                            "INFO Retrieving image.",
                            "webservice": "2024-04-30T07:47:51.191000 - "
                            "[2024-04-30 07:47:51 +0000] "
                            "[1] [INFO] Listening at: http://0.0.0.0:80 (1)",
                        }
                    }
                ),
            ),
        ],
    )
    monkeypatch.setattr(api.requests, "get", mock_requests_get)

    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy", "--watch-incremental"])
    with pytest.raises(SystemExit):
        cli()

    assert output in capsys.readouterr().out


@pytest.mark.parametrize(
    "file_contents, error",
    (
        [
            '{"id": "someid", "type" "docker"}',
            f"""Error: Please add a valid ploomber-cloud.json file.
{FORCE_INIT_MESSAGE}
{COMMUNITY}
            """,
        ],
        [
            '{"id": "someid", "type": ""}',
            f"""Error: There are some issues with the ploomber-cloud.json file:
Missing value for key 'type'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid"}',
            f"""Error: There are some issues with the ploomber-cloud.json file:
Mandatory key 'type' is missing.

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": 123, "type": "docker"}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
Only str values allowed for key 'id'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "id": "duplicate", "type": "docker", '
            '"type": "streamlit"}',
            f"""
Error: Please add a valid ploomber-cloud.json file. \
Duplicate keys: 'id', and 'type'
{FORCE_INIT_MESSAGE}
{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "some-type", "some-key": "some-value"}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
Invalid type 'some-type'. Valid project types are: {pretty_print(VALID_PROJECT_TYPES)}
Invalid key: 'some-key'. \
Valid keys are: 'authentication', 'authentication_analytics', 'id', 'ignore', \
'labels', 'resources', 'secret-keys', 'template', and 'type'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", "resources": {"ram": 1, "gpu": 0}}',
            f"""Error: There are some issues with the ploomber-cloud.json file:
Mandatory key 'cpu' is missing.
To fix it, run 'ploomber-cloud resources --force'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", "resources": \
{"cpu": "invalid", "ram": 1, "gpu": 0}}',
            f"""Error: There are some issues with the ploomber-cloud.json file:
Only float values allowed for resource 'cpu'
To fix it, run 'ploomber-cloud resources --force'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", \
"resources": {"vcpu": 0.5, "ram": 1, "gpu": 0}}',
            f"""Error: There are some issues with the ploomber-cloud.json file:
Mandatory key 'cpu' is missing.
Invalid resource: 'vcpu'. Valid keys are: 'cpu', 'gpu', and 'ram'
To fix it, run 'ploomber-cloud resources --force'

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", "labels": "some-label"}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
'labels' must be a list of strings.

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", "labels": ["some-label", 123]}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
'labels' must be a list of strings. Found invalid label: 123.

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", "secret-keys": "invalid"}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
'secret-keys' must be a list of strings.

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", "secret-keys": ["some-key", 123]}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
'secret-keys' must be a list of strings. Found invalid key: 123.

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
        [
            '{"id": "someid", "type": "docker", "ignore":"invalid"}',
            f"""
Error: There are some issues with the ploomber-cloud.json file:
'ignore' must be a list of strings.

{FORCE_INIT_MESSAGE}

{COMMUNITY}
""",
        ],
    ),
    ids=[
        "invalid-json",
        "empty-type-value",
        "type-key-missing",
        "non-string-value",
        "duplicate-keys",
        "invalid-key-value-combination",
        "resource-missing",
        "invalid-resource-type",
        "invalid-resource-key",
        "invalid-labels-value",
        "invalid-label",
        "secret-keys-not-list",
        "invalid-secret-key-value",
        "invalid-ignore-value",
    ],
)
def test_deploy_error_if_invalid_json(
    monkeypatch, set_key, capsys, file_contents, error
):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(file_contents)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    out_error = capsys.readouterr().err.strip()

    assert excinfo.value.code == 1
    assert str(error.strip()) in str(out_error)


def test_deploy_sends_data_secrets(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])
    monkeypatch.setattr(zip_, "_generate_random_suffix", Mock(return_value="someuuid"))

    # so the zip file is not deleted
    def unlink(self):
        if str(self) == "app-someuuid.zip":
            return

        return os.remove(self)

    monkeypatch.setattr(zip_.Path, "unlink", unlink)

    Path("ploomber-cloud.json").write_text('{"id": "someid", "type": "docker"}')
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")
    Path(".env").write_text("TEST_SECRET=test_secret_value")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={
            "secrets": '[{"key": "TEST_SECRET", "value": "test_secret_value"}]',
        },
    )

    with zipfile.ZipFile("app-someuuid.zip") as z:
        mapping = {}
        for name in z.namelist():
            mapping[name] = z.read(name)

    assert mapping == {
        "Dockerfile": b"FROM python:3.11",
        "app.py": b"print('hello world')",
        "fake-ploomber-dir/stats/config.yaml": b"cloud_key: somekey",
        ".env": b"",  # Sends an empty .env file but sends secrets thru API
    }

    assert "Deploying project with id: someid" in capsys.readouterr().out


def test_deploy_sends_data_secrets_via_config(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", "secret-keys": ["key1"]}'
    )
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    monkeypatch.setenv("key1", "val1")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={
            "secrets": '[{"key": "key1", "value": "val1"}]',
        },
    )

    assert "Deploying project with id: someid" in capsys.readouterr().out


def test_deploy_secrets_via_config_error_env_exists(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", "secret-keys": ["key1"]}'
    )
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")
    Path(".env").write_text("some-key=some-val")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert (
        "Found 'secret-keys' section and '.env' file. "
        "Only one method for adding secrets may be used.\n"
        "Delete '.env' or remove 'secret-keys' from 'ploomber-cloud.json'."
    ) in capsys.readouterr().err


def test_deploy_secrets_via_config_error_value_not_set(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", "secret-keys": ["key1"]}'
    )
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post
    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 1
    assert (
        "Value for key 'key1' not found. "
        "Set the value using 'export key1=value' "
        "or remove it from 'secret-keys'"
    ) in capsys.readouterr().err


def test_deploy_sends_data_resources(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", \
"resources": {"cpu": 1.0, "ram": 1, "gpu": 0}}'
    )
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={"cpu": 1.0, "ram": 1, "gpu": 0},
    )


def test_deploy_sends_data_template(monkeypatch, set_key, capsys):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", \
"template": "node-auth0"}'
    )
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    Path(".env").touch()
    Path(".env").write_text(
        "AUTH_SECRET=some-secret\n"
        "AUTH_CLIENT_ID=some-client-id\n"
        "AUTH_ISSUER_BASE_URL=some-url"
    )

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={
            "secrets": (
                "["
                '{"key": "AUTH_SECRET", "value": "some-secret"}, '
                '{"key": "AUTH_CLIENT_ID", "value": "some-client-id"}, '
                '{"key": "AUTH_ISSUER_BASE_URL", "value": "some-url"}'
                "]"
            ),
            "template": "node-auth0",
        },
    )


def test_deploy_sends_data_labels(monkeypatch, set_key):
    monkeypatch.setattr(sys, "argv", [CMD_NAME, "deploy"])

    Path("ploomber-cloud.json").write_text(
        '{"id": "someid", "type": "docker", \
"labels": ["label-one", "label-two"]}'
    )
    Path("Dockerfile").write_text("FROM python:3.11")
    Path("app.py").write_text("print('hello world')")

    mock_requests_post = Mock(name="requests.post")

    with pytest.raises(SystemExit) as excinfo:
        cli()

    def requests_post(*args, **kwargs):
        return Mock(
            ok=True,
            json=Mock(return_value={"project_id": "someid", "id": "jobid"}),
        )

    mock_requests_post.side_effect = requests_post

    monkeypatch.setattr(api.requests, "post", mock_requests_post)

    with pytest.raises(SystemExit) as excinfo:
        cli()

    assert excinfo.value.code == 0
    mock_requests_post.assert_called_once_with(
        "https://cloud-prod.ploomber.io/jobs/webservice/docker?project_id=someid",
        headers={"accept": "application/json", "api_key": "somekey"},
        files={"files": ("app.zip", ANY, "application/zip")},
        data={
            "labels": '["label-one", "label-two"]',
        },
    )
