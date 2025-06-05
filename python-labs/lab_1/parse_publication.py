import re
from typing import Optional


def parse_publication(reference: str) -> Optional[dict]:
    authors_year_pattern = r"(?:\w+, \w\., )*\w+, \w. \((?P<year>\d+)\)\. "
    title_journal_pattern = r"(?P<title>\w+[ \w]*)\. (?P<journal>\w+[ \w]*), "
    volume_issue_pattern = r"(?P<volume>\d+)(?:\((?P<issue>\d+)\))?, "
    pages_pattern = r"(?P<first_page>\d+)-(?P<end_page>\d+)\."
    # po kolei dopasowania do podanego wzorca
    # zgodnie z przykładem

    full_pattern = authors_year_pattern + title_journal_pattern + volume_issue_pattern + pages_pattern

    match = re.match(full_pattern, reference)
    if match is None:
        return None
    # jak nie ma dopasowania, zwracamy None

    authors_list = []
    author_pattern = r"(?P<last_name>(\w+)), (?P<initial>\w)\."
    # ten sam pattern co w authors_year_pattern, tylko z nazwami grup

    for author in re.finditer(author_pattern, reference):
        authors_list.append({"last_name": author.group("last_name"), "initial": author.group("initial")})

    result = {
        "authors": authors_list,
        "year": int(match.group("year")),
        "title": match.group("title"),
        "journal": match.group("journal"),
        "volume": int(match.group("volume")),
        "issue": int(match.group("issue")) if match.group("issue") else None,
        "pages": {"start": int(match.group("first_page")), "end": int(match.group("end_page"))}
    }
    return result
