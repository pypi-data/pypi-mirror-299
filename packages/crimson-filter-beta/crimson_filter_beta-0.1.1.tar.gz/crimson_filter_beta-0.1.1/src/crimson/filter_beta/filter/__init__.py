import re
import fnmatch
from typing import List, Union

ReFlag = Union[re.RegexFlag, int]


def re_filter(
    texts: List[str],
    include: List[str] = [],
    exclude: List[str] = [],
    flags: List[ReFlag] = [re.IGNORECASE],
) -> List[str]:
    # Combine flags using bitwise OR
    combined_flags = 0
    for flag in flags:
        combined_flags |= flag

    # Compile include and exclude patterns
    include_patterns = [re.compile(pattern, combined_flags) for pattern in include] if include else []
    exclude_patterns = [re.compile(pattern, combined_flags) for pattern in exclude]

    filtered_texts = []

    for text in texts:
        # If include is empty, consider all texts
        include_match = not include or any(pattern.search(text) for pattern in include_patterns)
        # Check if no exclude pattern matches
        exclude_match = any(pattern.search(text) for pattern in exclude_patterns)
        
        if include_match and not exclude_match:
            filtered_texts.append(text)

    return filtered_texts


def fnmatch_filter(
    texts: List[str],
    include: List[str] = [],
    exclude: List[str] = []
) -> List[str]:
    def matches_any(path, patterns):
        return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

    filtered_paths = []
    for text in texts:
        # If include is empty, consider all texts
        include_match = not include or matches_any(text, include)
        exclude_match = matches_any(text, exclude)
        
        if include_match and not exclude_match:
            filtered_paths.append(text)

    return filtered_paths