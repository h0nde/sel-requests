from .models import Request, Response
from . import exceptions
from selenium import webdriver
import selenium.common
import os
import signal

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
with open(__file__ + "/../" + "js/request.js") as f:
    js_request_template = f.read()

def create_chrome_options(proxy_url=None, user_agent=None):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--disable-web-security")
    if proxy_url:
        options.add_argument(f"--proxy-server={proxy_url}")
    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")
    return options

class Session:
    def __init__(self, proxy_url=None, user_agent=None, timeout=10, headers=None):
        self.user_agent = user_agent or user_agent
        self.proxy_url = proxy_url
        self.timeout = timeout
        self.headers = headers or {}
        self._webdriver = None
        try:
            self._setup()
        except Exception as exc:
            self.__exit__(exc, 0, 0)
            raise

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        self.close()

    def _setup(self):
        self._webdriver = webdriver.Chrome(
            options=create_chrome_options(self.proxy_url, self.user_agent),
            service_log_path="NUL"
        )
        self._webdriver.set_script_timeout(self.timeout)

    def close(self):
        """
        Closes the webdriver instance.
        """
        if self._webdriver:
            self._webdriver.quit()

    def set_origin(self, url: str, title: str=None):
        """
        Sets the webdriver's current page URL, useful for setting referer/origin/sec-fetch headers.

        :param url: URL to be used as window location
        :param title: Text to be used as window title
        """
        self._webdriver.execute_script(
            "history.replaceState(null, arguments[1], arguments[0])",
            url,
            title
        )

    def send(self, request: Request) -> Response:
        """
        Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param request: :class:`Request`
        :rtype: selrequests.Response
        """
    
        headers = dict(self.headers)
        headers.update(request.headers)

        try:
            resp = Response(**self._webdriver.execute_script(
                js_request_template,
                request.method,
                request.url,
                request.data,
                headers
            ))
        
        except selenium.common.exceptions.JavascriptException as err:
            raise exceptions.RequestException(err.msg)
    
        except selenium.common.exceptions.TimeoutException as err:
            raise exceptions.Timeout(err.msg)
    
        return resp

    def request(self, method: str, url: str, data: (dict, str)=None,
            json: (dict, list, str, int)=None, headers: dict=None):
        """
        Creates request object and passes it to .send.

        :param method:
        :param url:
        :param data:
        :param json:
        :param headers:
        """

        req = Request(method, url, data, json, headers)
        resp = self.send(req)
        return resp

    def get(self, url: str, **kwargs):
        r"""
        Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: selrequests.Response
        """
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs):
        r"""
        Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: selrequests.Response
        """
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs):
        r"""
        Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: selrequests.Response
        """
        return self.request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs):
        r"""
        Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: selrequests.Response
        """
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs):
        r"""
        Sends a DELETE request. Returns :class:`Response` object.
        
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: selrequests.Response
        """
        return self.request("DELETE", url, **kwargs)
