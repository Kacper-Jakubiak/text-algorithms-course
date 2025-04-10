import re

def extract_links(html: str) -> list[dict[str, str]]:
    url_pattern = r"<a href=\"(?P<url>[^\"]*)\""
    # url jest zawsze na początku, traktujemy url jako dowolne znaki oprócz [\"]
    title_pattern = r"(?: title=\"(?P<title>[^\"]*)\")?"
    # 1 lub 0 dopasowań tytułu, znaki jak powyżej
    text_pattern = r">(?P<link_text>[^<>]*)</a>"
    # text tylko między <a> </a>, więc brak znaków [<>] w text_pattern
    pattern = url_pattern + title_pattern + text_pattern

    links = []
    for link in re.finditer(pattern, html):
        links.append({
            "url": link.group("url"),
            "title": link.group("title"),
            "text": link.group("link_text"),
        })
        # konstrukcja struktury links zgodnie z poleceniem
    return links