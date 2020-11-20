# sel-requests
A selenium-based requests-like module for evading TLS fingerprinting, until a better solution is available for Python.

## Pros
- Bypass JA3 fingerprinting
- Uses `fetch()` to send requests, thus no page rendering is done

## Cons
- Relatively long init times
- No control over cookies
- No control over redirects
- All other limits of fetch(), except for CORS/SOP

# Setup
```bash
pip install -U git+https://github.com/h0nde/sel-requests.git
```

# Usage
```python3
import selrequests

with selrequests.Session() as s:
  resp = s.get("https://ja3er.com/json")
  print(resp.json())
```

# Documentation

(Do not forget to set a user_agent, else it'll use HeadlessChrome by default)
### Session(proxy_url=None, user_agent=None, timeout=10, headers=None)
Creates a requests-like session

### Session.set_origin(url)
Sets the instance's current page url, useful for setting Referer/Origin/Sec-Fetch headers.

### Session.request(method, url, data=None, json=None, headers=None, mode="same-origin", credentials="include")

### Session.get, .post, .put, .patch, .delete

### Session.close()
Closes the selenium instance.

## Exceptions

### exceptions.RequestException
All other exceptions are based on this.

### exceptions.HTTPError

### exceptions.Timeout
