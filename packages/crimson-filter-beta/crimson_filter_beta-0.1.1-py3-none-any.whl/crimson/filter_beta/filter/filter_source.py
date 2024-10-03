import os
import re
from crimson.filter_beta.filter import re_filter, fnmatch_filter
from typing import List, Union

ReFlag = Union[re.RegexFlag, int]


def re_filter_source(
    source_dir: str,
    include: List[str] = [],
    exclude: List[str] = [],
    flags: List[ReFlag] = [re.IGNORECASE],
) -> List[str]:
    """
    Filter files in a source directory based on include and exclude regex patterns.

    Args:
        source_dir (str): Path to the source directory.
        include (List[str]): List of regex patterns to include.
        exclude (List[str]): List of regex patterns to exclude.
        flags (List[ReFlag]): List of regex flags to use. Default is [re.IGNORECASE].

    Returns:
        List[str]: Filtered list of file paths relative to source_dir.
    """
    all_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), source_dir)
            all_files.append(rel_path)

    return re_filter(all_files, include, exclude, flags)


def fnmatch_filter_source(
    source_dir: str, include: List[str] = [], exclude: List[str] = [],
) -> List[str]:
    """
    Filter files in a source directory based on include and exclude patterns using fnmatch.

    Args:
        source_dir (str): Path to the source directory.
        include (List[str]): List of patterns to include.
        exclude (List[str]): List of patterns to exclude.

    Returns:
        List[str]: Filtered list of file paths relative to source_dir.
    """
    all_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), source_dir)
            all_files.append(rel_path)

    return fnmatch_filter(all_files, include, exclude)
