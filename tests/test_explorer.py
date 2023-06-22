import subprocess
from unittest.mock import patch

from fondant.explorer import (
    DEFAULT_CONTAINER,
    DEFAULT_PORT,
    DEFAULT_TAG,
    run_explorer_app,
)


def test_run_data_explorer_default():
    """Test that the data explorer can be run with default arguments."""
    with patch("subprocess.call") as mock_call:
        run_explorer_app()
        mock_call.assert_called_once_with(
            [
                "docker",
                "run",
                "--name",
                "fondant-explorer",
                "--rm",
                "-p",
                "8501:8501",
                "ghcr.io/ml6team/data_explorer:latest",
            ],
            stdout=-1,
        )


def test_run_data_explorer_with_data_dir():
    """Test that the data explorer can be run with a data directory."""
    data_directory = "/path/to/source"
    args = {
        "data_directory": data_directory,
    }

    with patch("subprocess.call") as mock_call:
        run_explorer_app(**args)

        mock_call.assert_called_once_with(
            [
                "docker",
                "run",
                "--name",
                "fondant-explorer",
                "--rm",
                "-p",
                f"{DEFAULT_PORT}:8501",
                "-v",
                f"{data_directory}:/artifacts",
                f"{DEFAULT_CONTAINER}:{DEFAULT_TAG}",
            ],
            stdout=subprocess.PIPE,
        )


def test_run_data_explorer_with_credentials():
    """Test that the data explorer can be run with a credentials file."""
    credentials = "/path/to/credentials"
    args = {
        "credentials": credentials,
    }

    with patch("subprocess.call") as mock_call:
        run_explorer_app(**args)

        mock_call.assert_called_once_with(
            [
                "docker",
                "run",
                "--name",
                "fondant-explorer",
                "--rm",
                "-p",
                "8501:8501",
                "-v",
                "/path/to/credentials:ro",
                "ghcr.io/ml6team/data_explorer:latest",
            ],
            stdout=-1,
        )


def test_run_data_explorer_full_option():
    """Test that the data explorer can be run with all options."""
    credentials = "/path/to/credentials"
    data_directory = "/path/to/source"
    container = "ghcr.io/ml6team/data_explorer_test"
    tag = "earliest"
    port = 1234

    with patch("subprocess.call") as mock_call:
        run_explorer_app(
            credentials=credentials,
            data_directory=data_directory,
            container=container,
            tag=tag,
            port=port,
        )

        mock_call.assert_called_once_with(
            [
                "docker",
                "run",
                "--name",
                "fondant-explorer",
                "--rm",
                "-p",
                "1234:8501",
                "-v",
                "/path/to/credentials:ro",
                "-v",
                "/path/to/source:/artifacts",
                "ghcr.io/ml6team/data_explorer_test:earliest",
            ],
            stdout=-1,
        )