# -*- coding: utf-8 -*-

"""Tests dict input objects for `tackle.providers.github.hooks` modules."""
import os
from tackle.main import tackle
import pytest
from tackle.utils.paths import rmtree


@pytest.fixture()
def clean_outputs():
    yield
    paths = ['services', 'foo', 'tackle-pypackage']
    for p in paths:
        if os.path.isdir(p):
            rmtree(p)


def test_provider_git_hooks_repos(change_dir, clean_outputs):
    """Verify hook."""
    tackle('.', context_file='repo.yaml')
    assert os.path.isdir('tackle-pypackage')


def test_provider_git_hooks_meta(change_dir, clean_outputs):
    """Verify hook."""
    tackle('.', context_file='meta.yaml', no_input=True)
    assert os.path.isdir(os.path.join('foo', 'bar', 'thing', 'docs'))
    assert os.path.isdir(os.path.join('foo', 'bar', 'gh', 'docs'))
    assert os.path.isdir(os.path.join('foo', 'bar', 'gh-branch', 'docs'))
    assert os.path.isdir(os.path.join('foo', 'bar', 'main', 'docs'))
    assert os.path.isdir(os.path.join('services', 'users', 'docs'))
    assert os.path.isdir(os.path.join('services', 'thing', 'docs'))
