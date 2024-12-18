# pixiv-latest-version

Get pixiv version id every day at 21:00 UTC.

You can send a request without version, but it is more stable to include version.

```sh
version=$(curl -s https://raw.githubusercontent.com/fa0311/pixiv-latest-version/refs/heads/main/version.txt)  
curl -s "https://www.pixiv.net/ajax/user/11229342?full=0&lang=ja&version=$version"
```
