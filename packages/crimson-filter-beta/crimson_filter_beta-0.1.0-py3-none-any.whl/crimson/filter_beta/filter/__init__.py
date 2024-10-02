import re
import fnmatch
from typing import List, Union

ReFlag = Union[re.RegexFlag, int]


def re_filter(
    texts: List[str],
    include: List[str],
    exclude: List[str],
    flags: List[ReFlag] = [re.IGNORECASE],
) -> List[str]:
    """
    Filter a list of texts based on include and exclude regex patterns.

    Args:
        texts (List[str]): List of strings to filter.
        include (List[str]): List of regex patterns to include.
        exclude (List[str]): List of regex patterns to exclude.
        flags (List[ReFlag]): List of regex flags to use. Default is an empty list.
                            Can include any of the re module flags, e.g.:
                            - re.IGNORECASE: Case-insensitive matching
                            - re.MULTILINE: '^' and '$' match at the beginning and end of each line
                            - re.DOTALL: '.' matches any character including newline

    Returns:
        List[str]: Filtered list of strings.

    ## Examples
        Notebook: [Link](https://github.com/crimson206/filter/blob/main/example/filter/re_filter.ipynb) to the notebook
    """
    # Combine flags using bitwise OR
    combined_flags = 0
    for flag in flags:
        combined_flags |= flag

    # Compile include and exclude patterns
    include_patterns = [re.compile(pattern, combined_flags) for pattern in include]
    exclude_patterns = [re.compile(pattern, combined_flags) for pattern in exclude]

    filtered_texts = []

    for text in texts:
        # Check if any include pattern matches
        if any(pattern.search(text) for pattern in include_patterns):
            # Check if no exclude pattern matches
            if not any(pattern.search(text) for pattern in exclude_patterns):
                filtered_texts.append(text)

    return filtered_texts


def fnmatch_filter(
    texts: List[str], include: List[str], exclude: List[str]
) -> List[str]:
    """
    Filter a list of paths based on include and exclude patterns using fnmatch.

    Args:
        paths (List[str]): List of paths to filter.
        include (List[str]): List of patterns to include.
        exclude (List[str]): List of patterns to exclude.

    Returns:
        List[str]: Filtered list of paths.

    """

    def matches_any(path, patterns):
        return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

    filtered_paths = []
    for text in texts:
        if matches_any(text, include) and not matches_any(text, exclude):
            filtered_paths.append(text)

    return filtered_paths
