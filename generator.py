import re

import cloudscraper

if __name__ == "__main__":
    PIXIV_BASE_URL = "https://www.pixiv.net"
    LATEST_USER_AGENT = (
        "https://raw.githubusercontent.com/fa0311/latest-user-agent/main/header.json"
    )

    session = cloudscraper.create_scraper()
    headers = session.get(LATEST_USER_AGENT).json()["chrome"]
    headers.update(
        {
            "host": None,
            "connection": None,
            "accept-encoding": None,
            "accept-language": "ja",
        }
    )

    response = session.get(PIXIV_BASE_URL, headers=headers)

    title = re.search(r"<title>(.*?)</title>", response.text)
    assert title is not None
    print(title.group(1))

    scripts: list[tuple[str, str]] = re.findall(
        r'<script src="(https://.*?/www/js/build/(.*?))" charset="utf8" crossorigin="anonymous"></script>',
        response.text,
    )
    common_path = next(filter(lambda x: x[1].startswith("common-path"), scripts))
    common_response = session.get(common_path[0], headers=headers)
    version: list[str] = re.findall(
        r'version:"([a-f0-9]+)"',
        common_response.text,
    )
    errortrace_release: list[str] = re.findall(
        r'release:"([a-f0-9]+)"',
        common_response.text,
    )
    assert len(version) == 1
    assert len(errortrace_release) == 1
    assert version == errortrace_release
    with open("version.txt", "w") as f:
        f.write(version[0])
