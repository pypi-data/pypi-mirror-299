from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from git import Repo, InvalidGitRepositoryError, GitCommandError

from extended_data_types.file_data_type import (
    get_parent_repository,
    get_repository_name,
    clone_repository_to_temp,
    get_tld,
    match_file_extensions,
    get_encoding_for_file_path,
    file_path_depth,
    file_path_rel_to_root,
    FilePath,
)


@pytest.fixture
def valid_file_path() -> Path:
    """Provides a valid file path for testing.

    Returns:
        Path: A valid file path.
    """
    return Path("/path/to/file.txt")


@pytest.fixture
def valid_repo_data() -> dict:
    """Provides valid data for testing repository functions.

    Returns:
        dict: A dictionary with the repository owner, name, token, and branch.
    """
    return {
        "repo_owner": "owner",
        "repo_name": "repo",
        "github_token": "token123",
        "branch": "main",
    }


def test_get_parent_repository(mocker) -> None:
    """Tests retrieving the parent Git repository of a file or directory.

    Uses mock to simulate the Repo object and invalid cases.

    Asserts:
        The result of get_parent_repository is either a valid Repo object or None if invalid.
    """
    # Mock the Repo constructor to return a mock Repo instance
    mock_repo_constructor = mocker.patch("extended_data_types.file_data_type.Repo")
    mock_repo_instance = mocker.Mock(spec=Repo)
    mock_repo_constructor.return_value = mock_repo_instance

    # Test for a valid repository path
    result = get_parent_repository("/valid/repo")
    assert result is mock_repo_instance

    # Test for an invalid repository path
    mock_repo_constructor.side_effect = InvalidGitRepositoryError
    result_invalid = get_parent_repository("/invalid/repo")
    assert result_invalid is None


def test_get_repository_name(mocker) -> None:
    """Tests retrieving the name of a Git repository.

    Uses mock to simulate the Repo object with a valid remote URL.

    Asserts:
        The result of get_repository_name matches the expected repository name.
    """
    # Create a mock Repo instance
    mock_repo = mocker.Mock(spec=Repo)
    mock_remote = mocker.Mock()
    mock_remote.urls = ["https://github.com/owner/repo.git"]
    mock_repo.remotes = [mock_remote]

    # Test with a valid remote URL
    assert get_repository_name(mock_repo) == "repo"

    # Test case where remote URL is not available
    mock_repo.remotes = []
    assert get_repository_name(mock_repo) is None


def test_clone_repository_to_temp(mocker, valid_repo_data: dict) -> None:
    """Tests cloning a GitHub repository to a temporary directory.

    Uses mock to simulate the Repo object cloning process.

    Args:
        valid_repo_data (dict): The valid repository data provided by the fixture.

    Asserts:
        The result of clone_repository_to_temp matches the expected temp directory and repo.
    """
    # Mock the Repo.clone_from method to return a mock Repo instance
    mock_clone_from = mocker.patch("extended_data_types.file_data_type.Repo.clone_from")
    mock_repo_instance = mocker.Mock(spec=Repo)
    mock_clone_from.return_value = mock_repo_instance

    # Call the function under test
    temp_dir, repo = clone_repository_to_temp(**valid_repo_data)

    # Assert that temp_dir is a Path instance and repo is the mocked Repo instance
    assert isinstance(temp_dir, Path)
    assert repo is mock_repo_instance

    # Test cloning with errors
    mock_clone_from.side_effect = GitCommandError("Error", "git")
    with pytest.raises(EnvironmentError, match="Git command error occurred"):
        clone_repository_to_temp(**valid_repo_data)


def test_get_tld(mocker) -> None:
    """Tests retrieving the top-level directory of a Git repository.

    Uses mock to simulate the Repo object and its working directory.

    Asserts:
        The result of get_tld matches the expected top-level directory or None if not a repository.
    """
    # Mock get_parent_repository to return a mock Repo instance
    mock_get_parent_repo = mocker.patch("extended_data_types.file_data_type.get_parent_repository")
    mock_repo_instance = mocker.Mock(spec=Repo)
    mock_repo_instance.working_tree_dir = "/valid/repo"
    mock_get_parent_repo.return_value = mock_repo_instance

    # Test for a valid repository
    result = get_tld("/valid/repo/file.txt")
    assert result == Path("/valid/repo")

    # Test for an invalid repository
    mock_get_parent_repo.return_value = None
    result_invalid = get_tld("/invalid/repo")
    assert result_invalid is None


@pytest.mark.parametrize(
    "p, allowed, denied, expected",
    [
        ("/path/file.txt", [".txt"], None, True),
        ("/path/file.txt", None, [".txt"], False),
        ("/path/file.txt", [".md"], None, False),
        ("/path/file.txt", None, None, True),
    ],
)
def test_match_file_extensions(
        p: FilePath, allowed: list[str] | None, denied: list[str] | None, expected: bool
) -> None:
    """Tests matching allowed or denied file extensions.

    Args:
        p (FilePath): The file path to check.
        allowed (list[str] | None): The allowed file extensions.
        denied (list[str] | None): The denied file extensions.
        expected (bool): The expected result.

    Asserts:
        The result of match_file_extensions matches the expected boolean value.
    """
    assert match_file_extensions(p, allowed, denied) == expected


@pytest.mark.parametrize(
    "file_path, expected_encoding",
    [
        ("/path/to/file.yaml", "yaml"),
        ("/path/to/file.json", "json"),
        ("/path/to/file.tf", "hcl"),
        ("/path/to/file.unknown", "raw"),
    ],
)
def test_get_encoding_for_file_path(file_path: FilePath, expected_encoding: str) -> None:
    """Tests retrieving the file encoding based on file extension.

    Args:
        file_path (FilePath): The file path to check.
        expected_encoding (str): The expected file encoding.

    Asserts:
        The result of get_encoding_for_file_path matches the expected encoding.
    """
    assert get_encoding_for_file_path(file_path) == expected_encoding


@pytest.mark.parametrize(
    "file_path, expected_depth",
    [
        ("/path/to/file.txt", 3),
        ("/", 0),
        ("/single_directory/", 1),
    ],
)
def test_file_path_depth(file_path: FilePath, expected_depth: int) -> None:
    """Tests retrieving the depth of a file path.

    Args:
        file_path (FilePath): The file path to check.
        expected_depth (int): The expected depth.

    Asserts:
        The result of file_path_depth matches the expected depth value.
    """
    assert file_path_depth(file_path) == expected_depth


@pytest.mark.parametrize(
    "file_path, expected_rel_to_root",
    [
        ("/path/to/file.txt", "../../.."),
        ("/", ""),
        ("/single_directory/", ".."),
    ],
)
def test_file_path_rel_to_root(file_path: FilePath, expected_rel_to_root: str) -> None:
    """Tests generating the relative path to the root directory.

    Args:
        file_path (FilePath): The file path to check.
        expected_rel_to_root (str): The expected relative path to the root.

    Asserts:
        The result of file_path_rel_to_root matches the expected relative path.
    """
    assert file_path_rel_to_root(file_path) == expected_rel_to_root
