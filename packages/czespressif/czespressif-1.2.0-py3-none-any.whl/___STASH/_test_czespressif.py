from __future__ import annotations

import pytest

from commitizen.changelog import Metadata
from commitizen.commands.changelog import Changelog
from commitizen.config import BaseConfig
from commitizen.exceptions import DryRunExit
from syrupy.extensions.single_file import SingleFileSnapshotExtension
from syrupy.extensions.single_file import WriteMode


# Using Syrupy to compare markdown snapshots
class MarkdownSnapshotExtension(SingleFileSnapshotExtension):
    _file_extension = 'md'
    _write_mode = WriteMode.TEXT


@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(MarkdownSnapshotExtension)


def render_changelog(config, gitcommits, tags, capsys, mocker, incremental: bool) -> str:
    mocker.patch('commitizen.git.get_commits', return_value=gitcommits[:4] if incremental else gitcommits)
    mocker.patch('commitizen.git.get_tags', return_value=tags)

    kwargs = {'dry_run': True, 'incremental': incremental, 'unreleased_version': True}
    cmd = Changelog(config, kwargs)

    mocker.patch.object(cmd.changelog_format, 'get_metadata').return_value = Metadata(latest_version='1.3.0')
    capsys.readouterr()

    try:
        cmd()
    except DryRunExit:
        pass

    return capsys.readouterr().out


@pytest.mark.parametrize('incremental', [False, True])
def test_changelog(snapshot, incremental, mocker, gitcommits, tags, capsys):
    # Create config for changelog
    config = BaseConfig()
    config.settings.update({'name': 'czespressif'})

    # Render the changelog using the provided fixture
    changelog = render_changelog(config, gitcommits, tags, capsys, mocker, incremental)

    # Compare the output with the markdown snapshot (Syrupy automatically handles snapshot naming)
    assert changelog == snapshot
