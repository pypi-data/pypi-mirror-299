import re
from typing import List, Tuple


def find_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Find all the patterns like,
        - [some link]\(www.example.com)

    ## Examples
        Notebook: [Link](https://github.com/crimson206/filter/blob/main/example/finder/find_markdown_links.ipynb) to the notebook
    """

    pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)
