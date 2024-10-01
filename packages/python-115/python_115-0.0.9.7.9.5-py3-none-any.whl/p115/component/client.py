#!/usr/bin/env python3
# encoding: utf-8

from __future__ import annotations

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__all__ = [
    "AVAILABLE_APPMAP", "CLIENT_API_MAP", "check_response", "P115Client", "P115Url", 
    "ExportDirStatus", "PushExtractProgress", "ExtractProgress", 
]

import errno
import posixpath

from asyncio import create_task, to_thread, Lock as AsyncLock
from base64 import b64encode
from binascii import b2a_hex, crc32
from collections.abc import (
    AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, Callable, Coroutine, 
    Generator, ItemsView, Iterable, Iterator, Mapping, Sequence, 
)
from concurrent.futures import Future
from contextlib import asynccontextmanager
from datetime import date, datetime
from email.utils import formatdate
from functools import cached_property, partial
from hashlib import md5, sha1
from hmac import digest as hmac_digest
from http.cookiejar import Cookie, CookieJar
from http.cookies import Morsel
from inspect import isawaitable, iscoroutinefunction
from itertools import chain, count, takewhile
from os import fsdecode, fspath, fstat, isatty, stat, PathLike
from os import path as ospath
from pathlib import PurePath
from re import compile as re_compile, MULTILINE
from socket import getdefaulttimeout, setdefaulttimeout
from _thread import start_new_thread
from threading import Condition, Lock, Thread
from time import sleep, strftime, strptime, time
from typing import (
    cast, overload, Any, Final, Literal, NotRequired, Self, TypedDict, TypeVar, 
)
from urllib.parse import quote, urlencode, urlsplit
from uuid import uuid4
from warnings import warn
from xml.etree.ElementTree import fromstring

from asynctools import as_thread, async_chain, ensure_aiter, ensure_async
from cookietools import cookies_str_to_dict, create_cookie
from Crypto.Hash.MD4 import MD4Hash
from dictattr import AttrDict
from filewrap import (
    Buffer, SupportsRead, 
    bio_chunk_iter, bio_chunk_async_iter, 
    bio_skip_iter, bio_skip_async_iter, 
    bytes_iter_skip, bytes_async_iter_skip, 
    bytes_iter_to_async_reader, bytes_iter_to_reader, 
    bytes_to_chunk_iter, bytes_to_chunk_async_iter, 
    progress_bytes_iter, progress_bytes_async_iter, 
)
from hashtools import HashObj, file_digest, file_mdigest, file_digest_async, file_mdigest_async
from http_request import encode_multipart_data, encode_multipart_data_async, SupportsGeturl
from http_response import get_content_length, get_filename, get_total_length, is_chunked, is_range_request
from httpfile import HTTPFileReader
from httpx import AsyncClient, Client, Cookies, AsyncHTTPTransport, HTTPTransport
from httpx_request import request
from iterutils import (
    through, async_through, run_gen_step, run_gen_step_iter, wrap_iter, wrap_aiter, 
    Yield, YieldFrom, 
)
from multidict import CIMultiDict
from orjson import dumps, loads
from qrcode import QRCode # type: ignore
from startfile import startfile, startfile_async # type: ignore
from urlopen import urlopen
from yarl import URL

from .cipher_fast import (
    rsa_encode, rsa_decode, ecdh_aes_encode, ecdh_aes_decode, ecdh_encode_token, MD5_SALT, 
)
from .exception import AuthenticationError, LoginError, MultipartUploadAbort


if getdefaulttimeout() is None:
    setdefaulttimeout(30)

# 所有的可用登录设备和对应的 ssoent
AVAILABLE_APPMAP: Final[dict[str, str]] = {
    "web": "A1", 
    "desktop": "A1", 
    "ios": "D1", 
    "115ios": "D3", 
    "android": "F1", 
    "115android": "F3", 
    #"ipad": "H1", 
    "115ipad": "H3", 
    "tv": "I1", 
    "qandroid": "M1", 
    #"qios": "N1", 
    "windows": "P1", 
    "mac": "P2", 
    "linux": "P3", 
    "wechatmini": "R1", 
    "alipaymini": "R2", 
    "harmony": "S1", 
}
# 所有已封装的 115 接口以及对应的方法名
CLIENT_API_MAP: Final[dict[str, str]] = {}

T = TypeVar("T")
CRE_SHARE_LINK_search = re_compile(r"/s/(?P<share_code>\w+)(\?password=(?P<receive_code>\w+))?").search
CRE_SET_COOKIE = re_compile(r"[0-9a-f]{32}=[0-9a-f]{32}.*")
CRE_CLIENT_API_search: Final = re_compile("^ +((?:GET|POST) .*)", MULTILINE).search

APP_VERSION: Final = "99.99.99.99"
MD4_EMPTY_HASH = b"1\xd6\xcf\xe0\xd1j\xe91\xb7<Y\xd7\xe0\xc0\x89\xc0"

parse_json = lambda _, content: loads(content)
httpx_request = partial(request, timeout=(5, 60, 60, 5))


def to_base64(s: bytes | str, /) -> str:
    if isinstance(s, str):
        s = bytes(s, "utf-8")
    return str(b64encode(s), "ascii")


def convert_digest(digest, /):
    if isinstance(digest, str):
        if digest == "crc32":
            digest = lambda: crc32
        elif digest == "ed2k":
            digest = Ed2kHash()
    return digest


class Ed2kHash:

    def __init__(self, b: Buffer = b"", /):
        self.block_hashes = bytearray()
        self._last_hashobj: MD4Hash = MD4Hash()
        self._remainder = 0
        self.update(b)

    def update(self, b: Buffer, /):
        size = len(b)
        if not size:
            return
        block_size = 1024 * 9500
        block_hashes = self.block_hashes
        remainder = self._remainder
        last_hashobj = self._last_hashobj
        m = memoryview(b)
        start = 0
        if remainder:
            start = block_size - remainder
            last_hashobj.update(m[:start])
            block_hashes[-16:] = last_hashobj.digest()
        if start < size: 
            for start in range(start, size, block_size):
                last_hashobj = MD4Hash(m[start:start+block_size])
                block_hashes += last_hashobj.digest()
        self._remainder = (size - start) % block_size
        self._last_hashobj = last_hashobj

    def digest(self, /) -> bytes:
        block_hashes: Buffer = self.block_hashes
        if not self._remainder:
            block_hashes = block_hashes + MD4_EMPTY_HASH
        return MD4Hash(block_hashes).digest()

    def hexdigest(self, /) -> str:
        return self.digest().hex()


def ed2k_hash(file: Buffer | SupportsRead[bytes]) -> tuple[int, str]:
    block_size = 1024 * 9500
    if hasattr(file, "getbuffer"):
        file = file.getbuffer()
    if isinstance(file, Buffer):
        chunk_iter = bytes_to_chunk_iter(file, chunksize=block_size)
    else:
        chunk_iter = bio_chunk_iter(file, chunksize=block_size, can_buffer=True)
    block_hashes = bytearray()
    filesize = 0
    for chunk in chunk_iter:
        block_hashes += MD4Hash(chunk).digest()
        filesize += len(chunk)
    if not filesize % block_size:
        block_hashes += MD4_EMPTY_HASH
    return filesize, MD4Hash(block_hashes).hexdigest()


async def ed2k_hash_async(file: Buffer | SupportsRead[bytes]) -> tuple[int, str]:
    block_size = 1024 * 9500
    if hasattr(file, "getbuffer"):
        file = file.getbuffer()
    if isinstance(file, Buffer):
        chunk_iter = bytes_to_chunk_async_iter(file, chunksize=block_size)
    else:
        chunk_iter = bio_chunk_async_iter(file, chunksize=block_size, can_buffer=True)
    block_hashes = bytearray()
    filesize = 0
    async for chunk in chunk_iter:
        block_hashes += MD4Hash(chunk).digest()
        filesize += len(chunk)
    if not filesize % block_size:
        block_hashes += MD4_EMPTY_HASH
    return filesize, MD4Hash(block_hashes).hexdigest()


@overload
def check_response(resp: dict, /) -> dict:
    ...
@overload
def check_response(resp: Coroutine[Any, Any, dict], /) -> Awaitable[dict]:
    ...
def check_response(resp: dict | Coroutine[Any, Any, dict], /) -> dict | Awaitable[dict]:
    """检测 115 的某个接口的响应，如果成功则直接返回，否则根据具体情况抛出一个异常
    """
    def check(resp: dict) -> dict:
        if resp.get("state", True):
            return resp
        if "errno" in resp:
            match resp["errno"]:
                # {"state": false, "errno": 99, "error": "请重新登录", "request": "/app/uploadinfo", "data": []}
                case 99:
                    raise AuthenticationError(resp)
                # {"state": false, "errno": 911, "errcode": 911, "error_msg": "请验证账号"}
                case 911:
                    raise AuthenticationError(resp)
                # {"state": false, "errno": 20004, "error": "该目录名称已存在。", "errtype": "war"}
                case 20004:
                    raise FileExistsError(errno.EEXIST, resp)
                # {"state": false, "errno": 20009, "error": "父目录不存在。", "errtype": "war"}
                case 20009:
                    raise FileNotFoundError(errno.ENOENT, resp)
                # {"state": false, "errno": 90008, "error": "文件（夹）不存在或已经删除。", "errtype": "war"}
                case 90008:
                    raise FileNotFoundError(errno.ENOENT, resp)
                # {"state": false, "errno": 91002, "error": "不能将文件复制到自身或其子目录下。", "errtype": "war"}
                case 91002:
                    raise OSError(errno.ENOTSUP, resp)
                # {"state": false, "errno": 91004, "error": "操作的文件(夹)数量超过5万个", "errtype": "war"}
                case 91004:
                    raise OSError(errno.ENOTSUP, resp)
                # {"state": false, "errno": 91005, "error": "空间不足，复制失败。", "errtype": "war"}
                case 91005:
                    raise OSError(errno.ENOSPC, resp)
                # {"state": false, "errno": 231011, "error": "文件已删除，请勿重复操作","errtype": "war"}
                case 231011:
                    raise FileNotFoundError(errno.ENOENT, resp)
                # {"state": false, "error": "404 Not Found", "errno": 980006, "request": "<api>", "data": []}
                case 980006:
                    raise OSError(errno.ENOSYS, resp)
                # {"state": false, "errno": 990009, "error": "删除[...]操作尚未执行完成，请稍后再试！", "errtype": "war"}
                # {"state": false, "errno": 990009, "error": "还原[...]操作尚未执行完成，请稍后再试！", "errtype": "war"}
                # {"state": false, "errno": 990009, "error": "复制[...]操作尚未执行完成，请稍后再试！", "errtype": "war"}
                # {"state": false, "errno": 990009, "error": "移动[...]操作尚未执行完成，请稍后再试！", "errtype": "war"}
                case 990009:
                    raise OSError(errno.EBUSY, resp)
                # {"state": false, "errno": 990023, "error": "操作的文件(夹)数量超过5万个", "errtype": ""}
                case 990023:
                    raise OSError(errno.ENOTSUP, resp)
                # {"state": 0, "errno": 40100000, "code": 40100000, "error": "参数错误！", "message": "参数错误！", "data": {}}
                case 40100000:
                    raise OSError(errno.EINVAL, resp)
                # {"state": 0, "errno": 40101004, "code": 40101004, "error": "IP登录异常,请稍候再登录！", "message": "IP登录异常,请稍候再登录！"}
                case 40101004:
                    raise LoginError(resp)
                # {"state": 0, "errno": 40101032, "code": 40101032, "data": {}, "message": "请重新登录", "error": "请重新登录"}
                case 40101032:
                    raise AuthenticationError(resp)
        elif "errNo" in resp:
            match resp["errNo"]:
                case 990001:
                    raise AuthenticationError(resp)
        elif "errcode" in resp:
            match resp["errcode"]:
                case 911:
                    raise AuthenticationError(resp)
        elif "code" in resp:
            match resp["code"]:
                case 99:
                    raise AuthenticationError(resp)
        raise OSError(errno.EIO, resp)
    if isinstance(resp, dict):
        return check(resp)
    else:
        async def check_await() -> dict:
            return check(await resp)
        return check_await()


class P115Url(str):

    def __new__(cls, url="", /, *args, **kwds):
        return super().__new__(cls, url)

    def __init__(self, url="", /, *args, **kwds):
        self.__dict__.update(*args, **kwds)

    def __delitem__(self, key, /):
        del self.__dict__[key]

    def __getitem__(self, key, /):
        return self.__dict__[key]

    def __setitem__(self, key, val, /):
        self.__dict__[key] = val

    def __repr__(self, /) -> str:
        return f"{type(self).__qualname__}({str(self)!r}, {self.__dict__})"

    def get(self, key, /, default=None):
        return self.__dict__.get(key, default)

    def geturl(self, /) -> str:
        return str(self)

    url = property(geturl)


class MultipartResumeData(TypedDict):
    bucket: str
    object: str
    upload_id: str
    callback: dict
    partsize: int
    filesize: NotRequired[int]


class P115Client:
    """115 的客户端对象

    :param cookies: 115 的 cookies，要包含 UID、CID 和 SEID，如果为 None，则会要求人工扫二维码登录
    :param check_for_relogin: 网页请求抛出异常时，判断是否要重新登录并重试
        - 如果为 False，则不重试
        - 如果为 True，则自动通过判断 HTTP 响应码为 405 时重新登录并重试
        - 如果为 Callable，则调用以判断，当返回值为 True 时重新登录并重试
    :param app: 人工扫二维码后绑定的 app
    :param console_qrcode: 在命令行输出二维码，否则在浏览器中打开

    设备列表如下：

    | No.    | ssoent  | app        | description            |
    |-------:|:--------|:-----------|:-----------------------|
    |     01 | A1      | web        | 网页版                 |
    |     02 | A2      | ?          | 未知: android          |
    |     03 | A3      | ?          | 未知: iphone           |
    |     04 | A4      | ?          | 未知: ipad             |
    |     05 | B1      | ?          | 未知: android          |
    |     06 | D1      | ios        | 115生活(iOS端)         |
    |     07 | D2      | ?          | 未知: ios              |
    |     08 | D3      | 115ios     | 115(iOS端)             |
    |     09 | F1      | android    | 115生活(Android端)     |
    |     10 | F2      | ?          | 未知: android          |
    |     11 | F3      | 115android | 115(Android端)         |
    |     12 | H1      | ipad       | 未知: ipad             |
    |     13 | H2      | ?          | 未知: ipad             |
    |     14 | H3      | 115ipad    | 115(iPad端)            |
    |     15 | I1      | tv         | 115网盘(Android电视端) |
    |     16 | M1      | qandriod   | 115管理(Android端)     |
    |     17 | N1      | qios       | 115管理(iOS端)         |
    |     18 | O1      | ?          | 未知: ipad             |
    |     19 | P1      | windows    | 115生活(Windows端)     |
    |     20 | P2      | mac        | 115生活(macOS端)       |
    |     21 | P3      | linux      | 115生活(Linux端)       |
    |     22 | R1      | wechatmini | 115生活(微信小程序)    |
    |     23 | R2      | alipaymini | 115生活(支付宝小程序)  |
    |     24 | S1      | harmony    | 115(Harmony端)         |
    """
    def __init__(
        self, 
        /, 
        cookies: None | str | Mapping[str, str] | Cookies | Iterable[Mapping | Cookie | Morsel] | PurePath = None, 
        check_for_relogin: bool | Callable[[BaseException], bool | int] = False, 
        app: str = "web", 
        console_qrcode: bool = True, 
    ):
        self.__dict__.update(
            headers = CIMultiDict({
                "Accept": "application/json, text/plain, */*", 
                "Accept-Encoding": "gzip, deflate", 
                "Connection": "keep-alive", 
                "User-Agent": "Mozilla/5.0 AppleWebKit/600 Safari/600 Chrome/124.0.0.0 115disk/" + APP_VERSION, 
            }), 
            cookies = Cookies(), 
        )
        if isinstance(cookies, PurePath) and hasattr(cookies, "open"):
            self.cookies_path = cookies
            cookies = self._read_cookies_from_path()
        if cookies is None:
            resp = self.login_with_qrcode(app, console_qrcode=console_qrcode)
            cookies = resp["data"]["cookie"]
        if cookies:
            setattr(self, "cookies", cookies)
        if check_for_relogin is True:
            def check_for_relogin(e: BaseException) -> bool:
                status = getattr(e, "status", None) or getattr(e, "code", None) or getattr(e, "status_code", None)
                if status is None and hasattr(e, "response"):
                    response = e.response
                    status = getattr(response, "status", None) or getattr(response, "code", None) or getattr(response, "status_code", None)
                return status == 405
        setattr(self, "check_for_relogin", check_for_relogin)
        setattr(self, "_request_lock", Lock())
        setattr(self, "_request_alock", AsyncLock())

    def __del__(self, /):
        self.close()

    def __eq__(self, other, /) -> bool:
        try:
            return type(self) is type(other) and self.user_id == other.user_id
        except AttributeError:
            return False

    @cached_property
    def session(self, /) -> Client:
        """同步请求的 session
        """
        ns = self.__dict__
        session = Client(transport=HTTPTransport(retries=5), verify=False)
        session._headers = ns["headers"]
        session._cookies = ns["cookies"]
        return session

    @cached_property
    def async_session(self, /) -> AsyncClient:
        """异步请求的 session
        """
        ns = self.__dict__
        session = AsyncClient(transport=AsyncHTTPTransport(retries=5), verify=False)
        session._headers = ns["headers"]
        session._cookies = ns["cookies"]
        return session

    @property
    def cookiejar(self, /) -> CookieJar:
        return self.__dict__["cookies"].jar

    @property
    def cookies(self, /) -> str:
        """115 登录的 cookies，包含 UID, CID 和 SEID 这 3 个字段
        """
        cookies = self.__dict__["cookies"]
        return "; ".join(f"{key}={val}" for key in ("UID", "CID", "SEID") if (val := cookies.get(key, domain=".115.com")))

    @cookies.setter
    def cookies(self, cookies: None | str | Mapping[str, str] | Cookies | Iterable[Mapping | Cookie | Morsel], /):
        """更新 cookies
        """
        ns = self.__dict__
        old_cookies = self.cookies
        if cookies is None:
            self.cookiejar.clear()
            if old_cookies:
                self._write_cookies_to_path("")
            return
        elif isinstance(cookies, str):
            cookies = cookies.strip()
            if not cookies:
                return
            cookies = cookies_str_to_dict(cookies.strip())
        set_cookie = ns["cookies"].jar.set_cookie
        if isinstance(cookies, Mapping):
            if not cookies:
                return
            for key, val in ItemsView(cookies):
                set_cookie(create_cookie(key, val, domain=".115.com"))
        else:
            if isinstance(cookies, Cookies):
                cookies = cookies.jar
            for cookie in cookies:
                set_cookie(create_cookie("", cookie))
        cookies = self.cookies
        if cookies != old_cookies:
            ns.pop("user_id", None)
            ns.pop("user_key", None)
            self._write_cookies_to_path(cookies)

    @property
    def cookies_all(self, /) -> str:
        """所有和 115 有关的 cookie 值
        """
        return "; ".join(f"{cookie.name}={cookie.value}" for cookie in self.cookiejar if cookie.domain.endswith(".115.com"))

    @property
    def headers(self, /) -> CIMultiDict:
        """请求头，无论同步还是异步请求都共用这个请求头
        """
        return self.__dict__["headers"]

    @headers.setter
    def headers(self, headers, /):
        """替换请求头，如果需要更新，请用 <client>.headers.update
        """
        headers = CIMultiDict(headers)
        default_headers = self.headers
        default_headers.clear()
        default_headers.update(headers)

    def _read_cookies_from_path(
        self, 
        /, 
        encoding: str = "latin-1", 
    ) -> None | str:
        cookies_path = getattr(self, "cookies_path", None)
        if not cookies_path:
            return None
        try:
            self.cookies_mtime = cookies_path.stat().st_mtime
        except OSError:
            self.cookies_mtime = 0
        try:
            with cookies_path.open("rb") as f:
                return str(f.read(), encoding)
        except OSError:
            return None

    def _write_cookies_to_path(
        self, 
        cookies: str, 
        /, 
        encoding: str = "latin-1", 
    ):
        cookies_path = getattr(self, "cookies_path", None)
        if not cookies_path:
            return
        with cookies_path.open("wb") as f:
            f.write(bytes(cookies, encoding))
        try:
            self.cookies_mtime = cookies_path.stat().st_mtime
        except OSError:
            self.cookies_mtime = 0

    def close(self, /) -> None:
        """删除 session 和 async_session，如果它们未被引用，则会被自动清理
        """
        ns = self.__dict__
        ns.pop("session", None)
        ns.pop("async_session", None)

    def request(
        self, 
        /, 
        url: str, 
        method: str = "GET", 
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ):
        """帮助函数：可执行同步和异步的网络请求
        """
        check_for_relogin = getattr(self, "check_for_relogin", None)
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            request_kwargs["session"] = self.async_session if async_ else self.session
            do_request = partial(
                httpx_request, 
                url=url, 
                method=method, 
                async_=async_, 
                **request_kwargs, 
            )
        else:
            cookies = "; ".join(f"{c.name}={c.value}" for c in self.cookiejar)
            if (headers := request_kwargs.get("headers")):
                request_kwargs["headers"] = {**self.headers, **headers, "Cookie": cookies}
            else:
                request_kwargs["headers"] = {**self.headers, "Cookie": cookies}
            do_request = partial(
                request, 
                url=url, 
                method=method, 
                **request_kwargs, 
            )
        if callable(check_for_relogin):
            if async_:
                async def wrap():
                    while True:
                        try:
                            return await do_request()
                        except BaseException as e:
                            res = check_for_relogin(e)
                            if not res if isinstance(res, bool) else res != 405:
                                raise
                            cookies = self.cookies
                            cookies_mtime = getattr(self, "cookies_mtime", 0)
                            async with getattr(self, "_request_alock"):
                                cookies_new = self.cookies
                                cookies_mtime_new = getattr(self, "cookies_mtime", 0)
                                if cookies == cookies_new:
                                    warn("relogin to refresh cookies")
                                    if not cookies_mtime_new or cookies_mtime == cookies_mtime_new:
                                        await self.login_another_app(replace=True, async_=True)
                                    else:
                                        setattr(self, "cookies", self._read_cookies_from_path())
                return wrap()
            else:
                while True:
                    try:
                        return do_request()
                    except BaseException as e:
                        res = check_for_relogin(e)
                        if not res if isinstance(res, bool) else res != 405:
                            raise
                        cookies = self.cookies
                        cookies_mtime = getattr(self, "cookies_mtime", 0)
                        with getattr(self, "_request_lock"):
                            cookies_new = self.cookies
                            cookies_mtime_new = getattr(self, "cookies_mtime", 0)
                            if cookies == cookies_new:
                                warn("relogin to refresh cookies")
                                if not cookies_mtime_new or cookies_mtime == cookies_mtime_new:
                                    self.login_another_app(replace=True)
                                else:
                                    setattr(self, "cookies", self._read_cookies_from_path())
        else:
            return do_request()

    ########## Login API ##########

    @overload
    def login_status(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bool:
        ...
    @overload
    def login_status(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bool]:
        ...
    def login_status(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bool | Coroutine[Any, Any, bool]:
        """检查是否已登录
        GET https://my.115.com/?ct=guide&ac=status
        """
        api = "https://my.115.com/?ct=guide&ac=status"
        def parse(resp, content: bytes) -> bool:
            try:
                return loads(content)["state"]
            except:
                return False
        request_kwargs["parse"] = parse
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def login_check(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def login_check(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def login_check(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """检查当前用户的登录状态
        GET https://passportapi.115.com/app/1.0/web/1.0/check/sso
        """
        api = "https://passportapi.115.com/app/1.0/web/1.0/check/sso"
        return self.request(url=api, async_=async_, **request_kwargs)

    @property
    def login_ssoent(self, /) -> None | str:
        cookie_uid = self.__dict__["cookies"].get("UID")
        if cookie_uid:
            return cookie_uid.split("_")[1]
        else:
            return None

    @overload
    def login_app(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> None | str:
        ...
    @overload
    def login_app(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, None | str]:
        ...
    def login_app(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> None | str | Coroutine[Any, Any, None | str]:
        def gen_step():
            ssoent = self.login_ssoent
            if ssoent is None:
                return None
            for app, v in AVAILABLE_APPMAP.items():
                if v == ssoent:
                    return app
            device = yield self.login_device(async_=async_, **request_kwargs)
            if device is None:
                return None
            return device["icon"]
        return run_gen_step(gen_step, async_=async_)

    @overload
    def login_device(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> None | dict:
        ...
    @overload
    def login_device(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, None | dict]:
        ...
    def login_device(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> None | dict | Coroutine[Any, Any, None | dict]:
        """获取当前的登录设备的信息，如果为 None，则说明登录失效
        """
        def parse(resp, content: bytes) -> None | dict:
            login_devices = loads(content)
            if not login_devices["state"]:
                return None
            return next(d for d in login_devices["data"]["list"] if d["is_current"])
        request_kwargs["parse"] = parse
        return self.login_devices(async_=async_, **request_kwargs)

    @overload
    def login_devices(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def login_devices(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def login_devices(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取所有的已登录设备的信息，不过当前必须未登录失效
        GET https://passportapi.115.com/app/1.0/web/1.0/login_log/login_devices
        """
        api = "https://passportapi.115.com/app/1.0/web/1.0/login_log/login_devices"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def login_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def login_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def login_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取登录信息
        GET https://proapi.115.com/pc/user/login_info
        """
        api = "https://proapi.115.com/pc/user/login_info"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def login_log(
        self, 
        payload: dict = {}, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def login_log(
        self, 
        payload: dict = {}, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def login_log(
        self, 
        payload: dict = {}, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取登录信息
        GET https://passportapi.115.com/app/1.0/web/1.0/login_log/log
        payload:
            - start: int = 0
            - limit: int = 100
        """
        api = "https://passportapi.115.com/app/1.0/web/1.0/login_log/log"
        payload = {"start": 0, "limit": 100, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def login_online(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def login_online(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def login_online(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """当前登录的设备总数和最近登录的设备
        GET https://passportapi.115.com/app/1.0/web/1.0/login_log/login_online
        """
        api = "https://passportapi.115.com/app/1.0/web/1.0/login_log/login_online"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def login(
        self, 
        /, 
        app: str, 
        console_qrcode: bool,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> Self:
        ...
    @overload
    def login(
        self, 
        /, 
        app: str, 
        console_qrcode: bool,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, Self]:
        ...
    def login(
        self, 
        /, 
        app: str = "web", 
        console_qrcode: bool = True,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> Self | Coroutine[Any, Any, Self]:
        """扫码二维码登录，如果已登录则忽略
        app 至少有 24 个可用值，目前找出 14 个：
            - web
            - ios
            - 115ios
            - android
            - 115android
            - 115ipad
            - tv
            - qandroid
            - windows
            - mac
            - linux
            - wechatmini
            - alipaymini
            - harmony
        还有几个备选（暂不可用）：
            - bios
            - bandroid
            - ipad（登录机制有些不同，暂时未破解）
            - qios（登录机制有些不同，暂时未破解）
            - desktop（就是 web，但是用 115 浏览器登录）

        设备列表如下：

        | No.    | ssoent  | app        | description            |
        |-------:|:--------|:-----------|:-----------------------|
        |     01 | A1      | web        | 网页版                 |
        |     02 | A2      | ?          | 未知: android          |
        |     03 | A3      | ?          | 未知: iphone           |
        |     04 | A4      | ?          | 未知: ipad             |
        |     05 | B1      | ?          | 未知: android          |
        |     06 | D1      | ios        | 115生活(iOS端)         |
        |     07 | D2      | ?          | 未知: ios              |
        |     08 | D3      | 115ios     | 115(iOS端)             |
        |     09 | F1      | android    | 115生活(Android端)     |
        |     10 | F2      | ?          | 未知: android          |
        |     11 | F3      | 115android | 115(Android端)         |
        |     12 | H1      | ipad       | 未知: ipad             |
        |     13 | H2      | ?          | 未知: ipad             |
        |     14 | H3      | 115ipad    | 115(iPad端)            |
        |     15 | I1      | tv         | 115网盘(Android电视端) |
        |     16 | M1      | qandriod   | 115管理(Android端)     |
        |     17 | N1      | qios       | 115管理(iOS端)         |
        |     18 | O1      | ?          | 未知: ipad             |
        |     19 | P1      | windows    | 115生活(Windows端)     |
        |     20 | P2      | mac        | 115生活(macOS端)       |
        |     21 | P3      | linux      | 115生活(Linux端)       |
        |     22 | R1      | wechatmini | 115生活(微信小程序)    |
        |     23 | R2      | alipaymini | 115生活(支付宝小程序)  |
        |     24 | S1      | harmony    | 115(Harmony端)         |
        """
        def gen_step():
            status = yield partial(
                self.login_status, 
                async_=async_, 
                **request_kwargs
            )
            if not status:
                resp = yield partial(
                    self.login_with_qrcode, 
                    app, 
                    console_qrcode=console_qrcode, 
                    async_=async_, 
                    **request_kwargs, 
                )
                self.cookies = resp["data"]["cookie"]
        return run_gen_step(gen_step, async_=async_)

    @overload
    @classmethod
    def login_with_qrcode(
        cls, 
        /, 
        app: str, 
        console_qrcode: bool,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @classmethod
    def login_with_qrcode(
        cls, 
        /, 
        app: str, 
        console_qrcode: bool,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @classmethod
    def login_with_qrcode(
        cls, 
        /, 
        app: str = "web", 
        console_qrcode: bool = True,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """扫码二维码登录，获取响应（如果需要更新此 client 的 cookies，请直接用 login 方法）
        app 至少有 24 个可用值，目前找出 14 个：
            - web
            - ios
            - 115ios
            - android
            - 115android
            - 115ipad
            - tv
            - qandroid
            - windows
            - mac
            - linux
            - wechatmini
            - alipaymini
            - harmony
        还有几个备选（暂不可用）：
            - bios
            - bandroid
            - ipad（登录机制有些不同，暂时未破解）
            - qios（登录机制有些不同，暂时未破解）
            - desktop（就是 web，但是用 115 浏览器登录）

        设备列表如下：

        | No.    | ssoent  | app        | description            |
        |-------:|:--------|:-----------|:-----------------------|
        |     01 | A1      | web        | 网页版                 |
        |     02 | A2      | ?          | 未知: android          |
        |     03 | A3      | ?          | 未知: iphone           |
        |     04 | A4      | ?          | 未知: ipad             |
        |     05 | B1      | ?          | 未知: android          |
        |     06 | D1      | ios        | 115生活(iOS端)         |
        |     07 | D2      | ?          | 未知: ios              |
        |     08 | D3      | 115ios     | 115(iOS端)             |
        |     09 | F1      | android    | 115生活(Android端)     |
        |     10 | F2      | ?          | 未知: android          |
        |     11 | F3      | 115android | 115(Android端)         |
        |     12 | H1      | ipad       | 未知: ipad             |
        |     13 | H2      | ?          | 未知: ipad             |
        |     14 | H3      | 115ipad    | 115(iPad端)            |
        |     15 | I1      | tv         | 115网盘(Android电视端) |
        |     16 | M1      | qandriod   | 115管理(Android端)     |
        |     17 | N1      | qios       | 115管理(iOS端)         |
        |     18 | O1      | ?          | 未知: ipad             |
        |     19 | P1      | windows    | 115生活(Windows端)     |
        |     20 | P2      | mac        | 115生活(macOS端)       |
        |     21 | P3      | linux      | 115生活(Linux端)       |
        |     22 | R1      | wechatmini | 115生活(微信小程序)    |
        |     23 | R2      | alipaymini | 115生活(支付宝小程序)  |
        |     24 | S1      | harmony    | 115(Harmony端)         |
        """
        def gen_step():
            resp = yield cls.login_qrcode_token(
                async_=async_, 
                **request_kwargs, 
            )
            qrcode_token = resp["data"]
            qrcode = qrcode_token.pop("qrcode")
            if console_qrcode:
                qr = QRCode(border=1)
                qr.add_data(qrcode)
                qr.print_ascii(tty=isatty(1))
            else:
                url = "https://qrcodeapi.115.com/api/1.0/web/1.0/qrcode?uid=" + qrcode_token["uid"]
                if async_:
                    yield partial(startfile_async, url)
                else:
                    startfile(url)
            while True:
                try:
                    resp = yield cls.login_qrcode_status(
                        qrcode_token, 
                        async_=async_, 
                        **request_kwargs, 
                    )
                except Exception:
                    continue
                match resp["data"].get("status"):
                    case 0:
                        print("[status=0] qrcode: waiting")
                    case 1:
                        print("[status=1] qrcode: scanned")
                    case 2:
                        print("[status=2] qrcode: signed in")
                        break
                    case -1:
                        raise LoginError("[status=-1] qrcode: expired")
                    case -2:
                        raise LoginError("[status=-2] qrcode: canceled")
                    case _:
                        raise LoginError(f"qrcode: aborted with {resp!r}")
            return (yield cls.login_qrcode_result(
                {"account": qrcode_token["uid"], "app": app}, 
                async_=async_, 
                **request_kwargs, 
            ))
        return run_gen_step(gen_step, async_=async_)

    @overload
    def login_another_app(
        self, 
        /, 
        app: None | str = None, 
        replace: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> Self:
        ...
    @overload
    def login_another_app(
        self, 
        /, 
        app: None | str = None, 
        replace: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, Self]:
        ...
    def login_another_app(
        self, 
        /, 
        app: None | str = None, 
        replace: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> Self | Coroutine[Any, Any, Self]:
        """登录某个设备（同一个设备最多同时一个在线，即最近登录的那个）
        :param app: 要登录的 app，如果为 None，则用同一登录设备
        :param replace: 替换当前 client 对象的 cookie，否则返回新的 client 对象

        设备列表如下：

        | No.    | ssoent  | app        | description            |
        |-------:|:--------|:-----------|:-----------------------|
        |     01 | A1      | web        | 网页版                 |
        |     02 | A2      | ?          | 未知: android          |
        |     03 | A3      | ?          | 未知: iphone           |
        |     04 | A4      | ?          | 未知: ipad             |
        |     05 | B1      | ?          | 未知: android          |
        |     06 | D1      | ios        | 115生活(iOS端)         |
        |     07 | D2      | ?          | 未知: ios              |
        |     08 | D3      | 115ios     | 115(iOS端)             |
        |     09 | F1      | android    | 115生活(Android端)     |
        |     10 | F2      | ?          | 未知: android          |
        |     11 | F3      | 115android | 115(Android端)         |
        |     12 | H1      | ipad       | 未知: ipad             |
        |     13 | H2      | ?          | 未知: ipad             |
        |     14 | H3      | 115ipad    | 115(iPad端)            |
        |     15 | I1      | tv         | 115网盘(Android电视端) |
        |     16 | M1      | qandriod   | 115管理(Android端)     |
        |     17 | N1      | qios       | 115管理(iOS端)         |
        |     18 | O1      | ?          | 未知: ipad             |
        |     19 | P1      | windows    | 115生活(Windows端)     |
        |     20 | P2      | mac        | 115生活(macOS端)       |
        |     21 | P3      | linux      | 115生活(Linux端)       |
        |     22 | R1      | wechatmini | 115生活(微信小程序)    |
        |     23 | R2      | alipaymini | 115生活(支付宝小程序)  |
        |     24 | S1      | harmony    | 115(Harmony端)         |
        """
        def gen_step():
            nonlocal app
            if app is None:
                app = yield self.login_app(async_=async_, **request_kwargs)
                if app is None:
                    raise LoginError("can't determine app")
            uid = check_response((yield self.login_qrcode_token(
                async_=async_, 
                **request_kwargs, 
            )))["data"]["uid"]
            check_response((yield self.login_qrcode_scan(
                uid, 
                async_=async_, 
                **request_kwargs, 
            )))
            check_response((yield self.login_qrcode_scan_confirm(
                uid, 
                async_=async_, 
                **request_kwargs, 
            )))
            cookies = check_response((yield self.login_qrcode_result(
                {"account": uid, "app": app}, 
                async_=async_, 
                **request_kwargs, 
            )))["data"]["cookie"]
            if replace:
                self.cookies = cookies
                return self
            elif async_:
                return (yield partial(to_thread, type(self), cookies))
            else:
                return type(self)(cookies)
        return run_gen_step(gen_step, async_=async_)

    @overload
    def login_qrcode_scan(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def login_qrcode_scan(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def login_qrcode_scan(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """扫描二维码，payload 数据取自 `login_qrcode_token` 接口响应
        GET https://qrcodeapi.115.com/api/2.0/prompt.php
        payload:
            - uid: str
        """
        api = "https://qrcodeapi.115.com/api/2.0/prompt.php"
        if isinstance(payload, str):
            payload = {"uid": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def login_qrcode_scan_confirm(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def login_qrcode_scan_confirm(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def login_qrcode_scan_confirm(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """确认扫描二维码，payload 数据取自 `login_qrcode_scan` 接口响应
        GET https://hnqrcodeapi.115.com/api/2.0/slogin.php
        payload:
            - key: str
            - uid: str
            - client: int = 0
        """
        api = "https://hnqrcodeapi.115.com/api/2.0/slogin.php"
        if isinstance(payload, str):
            payload = {"key": payload, "uid": payload, "client": 0}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    @staticmethod
    def login_qrcode_scan_cancel(
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def login_qrcode_scan_cancel(
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def login_qrcode_scan_cancel(
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """确认扫描二维码，payload 数据取自 `login_qrcode_scan` 接口响应
        GET https://hnqrcodeapi.115.com/api/2.0/cancel.php
        payload:
            - key: str
            - uid: str
            - client: int = 0
        """
        api = "https://hnqrcodeapi.115.com/api/2.0/cancel.php"
        if isinstance(payload, str):
            payload = {"key": payload, "uid": payload, "client": 0}
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            return httpx_request(url=api, params=payload, async_=async_, **request_kwargs)
        else:
            return request(url=api, params=payload, **request_kwargs)

    @overload
    @staticmethod
    def login_qrcode_status(
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def login_qrcode_status(
        payload: dict, 
        /, 
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def login_qrcode_status(
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取二维码的状态（未扫描、已扫描、已登录、已取消、已过期等），payload 数据取自 `login_qrcode_token` 接口响应
        GET https://qrcodeapi.115.com/get/status/
        payload:
            - uid: str
            - time: int
            - sign: str
        """
        api = "https://qrcodeapi.115.com/get/status/"
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            return httpx_request(url=api, params=payload, async_=async_, **request_kwargs)
        else:
            return request(url=api, params=payload, **request_kwargs)

    @overload
    @staticmethod
    def login_qrcode_result(
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def login_qrcode_result(
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def login_qrcode_result(
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取扫码登录的结果，包含 cookie
        POST https://passportapi.115.com/app/1.0/{app}/1.0/login/qrcode/
        payload:
            - account: int | str
            - app: str = "web"
        """
        if isinstance(payload, (int, str)):
            payload = {"account": payload}
            app = "web"
        else:
            payload = {"app": "web", **payload}
            app = payload.pop("app")
            if app == "desktop":
                app = "web"
        api = f"https://passportapi.115.com/app/1.0/{app}/1.0/login/qrcode/"
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            return httpx_request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)
        else:
            return request(url=api, method="POST", data=payload, **request_kwargs)

    @overload
    @staticmethod
    def login_qrcode_token(
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def login_qrcode_token(
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def login_qrcode_token(
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取登录二维码，扫码可用
        GET https://qrcodeapi.115.com/api/1.0/web/1.0/token/
        """
        api = "https://qrcodeapi.115.com/api/1.0/web/1.0/token/"
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            return httpx_request(url=api, async_=async_, **request_kwargs)
        else:
            return request(url=api, **request_kwargs)

    @overload
    @staticmethod
    def login_qrcode(
        uid: str,
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    @staticmethod
    def login_qrcode(
        uid: str,
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    @staticmethod
    def login_qrcode(
        uid: str,
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """下载登录二维码图片
        GET https://qrcodeapi.115.com/api/1.0/web/1.0/qrcode
        :params uid: 二维码的 uid
        :return: 图片的二进制数据（PNG 图片）
        """
        api = "https://qrcodeapi.115.com/api/1.0/web/1.0/qrcode"
        request_kwargs["params"] = {"uid": uid}
        request_kwargs["parse"] = False
        if request is None:
            return httpx_request(url=api, async_=async_, **request_kwargs)
        else:
            return request(url=api, **request_kwargs)

    def logout(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ):
        """退出当前设备的登录状态
        """
        ssoent = self.login_ssoent
        if not ssoent:
            if async_:
                async def none():
                    pass
                return none()
            else:
                return
        return self.logout_by_ssoent(ssoent, async_=async_, **request_kwargs)

    @overload
    def logout_by_app(
        self, 
        /, 
        app: None | str = None, 
        *, 
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> None:
        ...
    @overload
    def logout_by_app(
        self, 
        /, 
        app: None | str = None, 
        *, 
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, None]:
        ...
    def logout_by_app(
        self, 
        /, 
        app: None | str = None, 
        *, 
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> None | Coroutine[Any, Any, None]:
        """退出登录状态（可以把某个客户端下线，所有已登录设备可从 `login_devices` 获取）
        GET https://passportapi.115.com/app/1.0/{app}/1.0/logout/logout

        :param app: 退出登录的 app

        设备列表如下：

        | No.    | ssoent  | app        | description            |
        |-------:|:--------|:-----------|:-----------------------|
        |     01 | A1      | web        | 网页版                 |
        |     02 | A2      | ?          | 未知: android          |
        |     03 | A3      | ?          | 未知: iphone           |
        |     04 | A4      | ?          | 未知: ipad             |
        |     05 | B1      | ?          | 未知: android          |
        |     06 | D1      | ios        | 115生活(iOS端)         |
        |     07 | D2      | ?          | 未知: ios              |
        |     08 | D3      | 115ios     | 115(iOS端)             |
        |     09 | F1      | android    | 115生活(Android端)     |
        |     10 | F2      | ?          | 未知: android          |
        |     11 | F3      | 115android | 115(Android端)         |
        |     12 | H1      | ipad       | 未知: ipad             |
        |     13 | H2      | ?          | 未知: ipad             |
        |     14 | H3      | 115ipad    | 115(iPad端)            |
        |     15 | I1      | tv         | 115网盘(Android电视端) |
        |     16 | M1      | qandriod   | 115管理(Android端)     |
        |     17 | N1      | qios       | 115管理(iOS端)         |
        |     18 | O1      | ?          | 未知: ipad             |
        |     19 | P1      | windows    | 115生活(Windows端)     |
        |     20 | P2      | mac        | 115生活(macOS端)       |
        |     21 | P3      | linux      | 115生活(Linux端)       |
        |     22 | R1      | wechatmini | 115生活(微信小程序)    |
        |     23 | R2      | alipaymini | 115生活(支付宝小程序)  |
        |     24 | S1      | harmony    | 115(Harmony端)         |
        """
        if app is None:
            app = self.login_app()
        if app == "desktop":
            app = "web"
        api = f"https://passportapi.115.com/app/1.0/{app}/1.0/logout/logout"
        request_kwargs["headers"] = {**(request_kwargs.get("headers") or {}), "Cookie": self.cookies}
        request_kwargs.setdefault("parse", lambda _: None)
        if request is None:
            return httpx_request(url=api, async_=async_, **request_kwargs)
        else:
            return request(url=api, **request_kwargs)

    @overload
    def logout_by_ssoent(
        self, 
        payload: None | str | dict = None, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def logout_by_ssoent(
        self, 
        payload: None | str | dict = None, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def logout_by_ssoent(
        self, 
        payload: None | str | dict = None, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """退出登录状态（可以把某个客户端下线，所有已登录设备可从 `login_devices` 获取）
        GET https://passportapi.115.com/app/1.0/web/1.0/logout/mange
        payload:
            ssoent: str

        设备列表如下：

        | No.    | ssoent  | app        | description            |
        |-------:|:--------|:-----------|:-----------------------|
        |     01 | A1      | web        | 网页版                 |
        |     02 | A2      | ?          | 未知: android          |
        |     03 | A3      | ?          | 未知: iphone           |
        |     04 | A4      | ?          | 未知: ipad             |
        |     05 | B1      | ?          | 未知: android          |
        |     06 | D1      | ios        | 115生活(iOS端)         |
        |     07 | D2      | ?          | 未知: ios              |
        |     08 | D3      | 115ios     | 115(iOS端)             |
        |     09 | F1      | android    | 115生活(Android端)     |
        |     10 | F2      | ?          | 未知: android          |
        |     11 | F3      | 115android | 115(Android端)         |
        |     12 | H1      | ipad       | 未知: ipad             |
        |     13 | H2      | ?          | 未知: ipad             |
        |     14 | H3      | 115ipad    | 115(iPad端)            |
        |     15 | I1      | tv         | 115网盘(Android电视端) |
        |     16 | M1      | qandriod   | 115管理(Android端)     |
        |     17 | N1      | qios       | 115管理(iOS端)         |
        |     18 | O1      | ?          | 未知: ipad             |
        |     19 | P1      | windows    | 115生活(Windows端)     |
        |     20 | P2      | mac        | 115生活(macOS端)       |
        |     21 | P3      | linux      | 115生活(Linux端)       |
        |     22 | R1      | wechatmini | 115生活(微信小程序)    |
        |     23 | R2      | alipaymini | 115生活(支付宝小程序)  |
        |     24 | S1      | harmony    | 115(Harmony端)         |
        """
        api = "https://passportapi.115.com/app/1.0/web/1.0/logout/mange"
        if payload is None:
            payload = {"ssoent": self.login_ssoent or ""}
        elif isinstance(payload, str):
            payload = {"ssoent": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    ########## Account API ##########

    @overload
    def user_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取此用户信息
        GET https://my.115.com/?ct=ajax&ac=nav
        """
        api = "https://my.115.com/?ct=ajax&ac=nav"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def user_info2(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_info2(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_info2(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取此用户信息（更全）
        GET https://my.115.com/?ct=ajax&ac=get_user_aq
        """
        api = "https://my.115.com/?ct=ajax&ac=get_user_aq"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def user_setting(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_setting(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_setting(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取此账户的网页版设置（提示：较为复杂，自己抓包研究）
        GET https://115.com/?ac=setting&even=saveedit&is_wl_tpl=1
        """
        api = "https://115.com/?ac=setting&even=saveedit&is_wl_tpl=1"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def user_setting_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_setting_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_setting_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """修改此账户的网页版设置（提示：较为复杂，自己抓包研究）
        POST https://115.com/?ac=setting&even=saveedit&is_wl_tpl=1
        """
        api = "https://115.com/?ac=setting&even=saveedit&is_wl_tpl=1"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def user_setting2(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_setting2(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_setting2(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取此账户的 app 版设置（提示：较为复杂，自己抓包研究）
        GET https://webapi.115.com/user/setting
        """
        api = "https://webapi.115.com/user/setting"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def user_setting2_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_setting2_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_setting2_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取（并可修改）此账户的网页版设置（提示：较为复杂，自己抓包研究）
        POST https://webapi.115.com/user/setting
        """
        api = "https://webapi.115.com/user/setting"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def user_setting3(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_setting3(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_setting3(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取此账户的 app 版设置（提示：较为复杂，自己抓包研究）
        GET https://proapi.115.com/android/1.0/user/setting
        """
        api = "https://proapi.115.com/android/1.0/user/setting"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def user_setting3_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_setting3_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_setting3_post(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取（并可修改）此账户的网页版设置（提示：较为复杂，自己抓包研究）
        POST https://proapi.115.com/android/1.0/user/setting
        """
        api = "https://proapi.115.com/android/1.0/user/setting"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def user_points_sign(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_points_sign(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_points_sign(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取签到信息
        GET https://proapi.115.com/android/2.0/user/points_sign
        """
        api = "https://proapi.115.com/android/2.0/user/points_sign"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def user_points_sign_post(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_points_sign_post(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_points_sign_post(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """每日签到（注意：不要用 web，即浏览器，的 cookies，会失败）
        POST https://proapi.115.com/android/2.0/user/points_sign
        """
        api = "https://proapi.115.com/android/2.0/user/points_sign"
        t = int(time())
        request_kwargs["data"] = {
            "token": sha1(b"%d-Points_Sign@#115-%d" % (self.user_id, t)).hexdigest(), 
            "token_time": t, 
        }
        return self.request(url=api, method="POST", async_=async_, **request_kwargs)

    @overload
    def user_fingerprint(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def user_fingerprint(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def user_fingerprint(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取截图时嵌入的水印
        GET https://webapi.115.com/user/fingerprint
        """
        api = "https://webapi.115.com/user/fingerprint"
        return self.request(url=api, async_=async_, **request_kwargs)

    ########## App API ##########

    @overload
    @staticmethod
    def app_version_list(
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs
    ) -> dict:
        ...
    @overload
    @staticmethod
    def app_version_list(
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def app_version_list(
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取当前各平台最新版 115 app 下载链接
        GET https://appversion.115.com/1/web/1.0/api/chrome
        """
        api = "https://appversion.115.com/1/web/1.0/api/chrome"
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            return httpx_request(url=api, async_=async_, **request_kwargs)
        else:
            return request(url=api, **request_kwargs)

    ########## File System API ##########

    @overload
    def fs_storage_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_storage_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_storage_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取使用空间的统计数据（最简略，如需更详细，请用 `fs.fs_space_info()`）
        GET https://115.com/index.php?ct=ajax&ac=get_storage_info
        """
        api = "https://115.com/index.php?ct=ajax&ac=get_storage_info"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def fs_space_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_space_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_space_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取使用空间的统计数据（较为简略，如需更详细，请用 `P115Client.fs_index_info()`）
        GET https://proapi.115.com/android/1.0/user/space_info
        """
        api = "https://proapi.115.com/android/1.0/user/space_info"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def fs_space_summury(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_space_summury(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_space_summury(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取数据报告（分组聚合）
        POST https://webapi.115.com/user/space_summury
        """
        api = "https://webapi.115.com/user/space_summury"
        return self.request(url=api, method="POST", async_=async_, **request_kwargs)

    @overload
    def fs_space_report(
        self, 
        payload: str | dict, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_space_report(
        self, 
        payload: str | dict, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_space_report(
        self, 
        payload: str | dict, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取数据报告
        GET https://webapi.115.com/user/report
        payload:
            - month: str # 年月，格式为 YYYYMM
        """
        api = "https://webapi.115.com/user/report"
        if isinstance(payload, str):
            payload = {"month": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_copy(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        pid: int = 0, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_copy(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        pid: int = 0, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_copy(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        pid: int = 0, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """复制文件或文件夹
        POST https://webapi.115.com/files/copy
        payload:
            - fid[0]: int | str
            - fid[1]: int | str
            - ...
            - pid: int | str = 0
        """
        api = "https://webapi.115.com/files/copy"
        if isinstance(payload, (int, str)):
            payload = {"fid[0]": payload}
        elif isinstance(payload, dict):
            payload = dict(payload)
        else:
            payload = {f"fid[{i}]": fid for i, fid in enumerate(payload)}
            if not payload:
                return {"state": False, "message": "no op"}
        payload.setdefault("pid", pid)
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_delete(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_delete(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_delete(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除文件或文件夹
        POST https://webapi.115.com/rb/delete
        payload:
            - fid[0]: int | str
            - fid[1]: int | str
            - ...
        """
        api = "https://webapi.115.com/rb/delete"
        if isinstance(payload, (int, str)):
            payload = {"fid[0]": payload}
        elif not isinstance(payload, dict):
            payload = {f"fid[{i}]": fid for i, fid in enumerate(payload)}
        if not payload:
            return {"state": False, "message": "no op"}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_move(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        pid: int = 0, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_move(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        pid: int = 0, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_move(
        self, 
        payload: int | str | dict | Iterable[int | str], 
        /, 
        pid: int = 0, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """移动文件或文件夹
        POST https://webapi.115.com/files/move
        payload:
            - pid: int | str
            - fid[0]: int | str
            - fid[1]: int | str
            - ...
            - move_proid: str = <default> # 任务 id
        """
        api = "https://webapi.115.com/files/move"
        if isinstance(payload, (int, str)):
            payload = {"fid[0]": payload}
        elif isinstance(payload, dict):
            payload = dict(payload)
        else:
            payload = {f"fid[{i}]": fid for i, fid in enumerate(payload)}
            if not payload:
                return {"state": False, "message": "no op"}
        payload.setdefault("pid", pid)
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_rename(
        self, 
        payload: tuple[int | str, str] | dict | Iterable[tuple[int | str, str]], 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_rename(
        self, 
        payload: tuple[int | str, str] | dict | Iterable[tuple[int | str, str]], 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_rename(
        self, 
        payload: tuple[int | str, str] | dict | Iterable[tuple[int | str, str]], 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """重命名文件或文件夹
        POST https://webapi.115.com/files/batch_rename
        payload:
            - files_new_name[{file_id}]: str # 值为新的文件名（basename）
        """
        api = "https://webapi.115.com/files/batch_rename"
        if isinstance(payload, tuple) and len(payload) == 2 and isinstance(payload[0], (int, str)):
            payload = {f"files_new_name[{payload[0]}]": payload[1]}
        elif not isinstance(payload, dict):
            payload = {f"files_new_name[{fid}]": name for fid, name in payload}
        if not payload:
            return {"state": False, "message": "no op"}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_file(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_file(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_file(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件或文件夹的简略信息
        GET https://webapi.115.com/files/file
        payload:
            - file_id: int | str # 文件或目录的 id，如果有多个则用逗号 "," 隔开
        """
        api = "https://webapi.115.com/files/file"
        if isinstance(payload, (int, str)):
            payload = {"file_id": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件夹的中的文件列表和基本信息（指定 1) cid=0 且 star=1, 2) suffix, 3) type 中任一，则默认 cur=0，可遍历搜索所在目录树）
        GET https://webapi.115.com/files
        payload:
            - cid: int | str = 0 # 文件夹 id
            - limit: int = 32    # 一页大小，意思就是 page_size
            - offset: int = 0    # 索引偏移，索引从 0 开始计算

            - aid: int | str = 1 # area_id，不知道的话，设置为 1
            - asc: 0 | 1 = <default> # 是否升序排列
            - code: int | str = <default>
            - count_folders: 0 | 1 = 1 # 统计文件数和文件夹数
            - cur: 0 | 1 = <default> # 是否只搜索当前目录
            - custom_order: 0 | 1 = <default> # 启用自定义排序，如果指定了 "asc", "fc_mix", "o" 其一，则此参数要设置为 1 （我实现了自动设置）
            - date: str = <default> # 筛选日期
            - fc_mix: 0 | 1 = <default> # 是否目录和文件混合，如果为 0 则目录在前
            - fields: str = <default>
            - format: str = "json"
            - hide_data: str = <default>
            - is_q: 0 | 1 = <default>
            - is_share: 0 | 1 = <default>
            - min_size: int = 0 # 最小的文件大小
            - max_size: int = 0 # 最大的文件大小
            - natsort: 0 | 1 = <default>
            - o: str = <default>
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
            - r_all: 0 | 1 = <default>
            - record_open_time: 0 | 1 = 1 # 是否要记录文件夹的打开时间
            - scid: int | str = <default>
            - show_dir: 0 | 1 = 1
            - snap: 0 | 1 = <default>
            - source: str = <default>
            - sys_dir: int | str = <default>
            - star: 0 | 1 = <default> # 是否星标文件
            - stdir: 0 | 1 = <default>
            - suffix: str = <default> # 后缀名
            - type: int = <default>
                # 文件类型：
                # - 全部: 0
                # - 文档: 1
                # - 图片: 2
                # - 音频: 3
                # - 视频: 4
                # - 压缩包: 5
                # - 应用: 6
                # - 书籍: 7
                # - 仅文件: 99
        """
        api = "https://webapi.115.com/files"
        if isinstance(payload, int):
            payload = {
                "aid": 1, "count_folders": 1, "limit": 32, "offset": 0, 
                "record_open_time": 1, "show_dir": 1, "cid": payload, 
            }
        else:
            payload = {
                "aid": 1, "count_folders": 1, "limit": 32, "offset": 0, 
                "record_open_time": 1, "show_dir": 1, "cid": 0, **payload, 
            }
        if payload.keys() & frozenset(("asc", "fc_mix", "o")):
            payload["custom_order"] = 1
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files2(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files2(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files2(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件夹的中的文件列表和基本信息
        GET https://proapi.115.com/android/2.0/ufile/files
        payload:
            - cid: int | str = 0 # 文件夹 id
            - limit: int = 32    # 一页大小，意思就是 page_size
            - offset: int = 0    # 索引偏移，索引从 0 开始计算

            - aid: int | str = 1 # area_id，不知道的话，设置为 1
            - asc: 0 | 1 = <default> # 是否升序排列
            - code: int | str = <default>
            - count_folders: 0 | 1 = 1 # 统计文件数和文件夹数
            - cur: 0 | 1 = <default> # 是否只搜索当前目录
            - custom_order: 0 | 1 = <default> # 启用自定义排序，如果指定了 "asc", "fc_mix", "o" 其一，则此参数要设置为 1 （我实现了自动设置）
            - date: str = <default> # 筛选日期
            - fc_mix: 0 | 1 = <default> # 是否目录和文件混合，如果为 0 则目录在前
            - fields: str = <default>
            - format: str = "json"
            - hide_data: str = <default>
            - is_q: 0 | 1 = <default>
            - is_share: 0 | 1 = <default>
            - min_size: int = 0 # 最小的文件大小
            - max_size: int = 0 # 最大的文件大小
            - natsort: 0 | 1 = <default>
            - o: str = <default>
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
            - r_all: 0 | 1 = <default>
            - record_open_time: 0 | 1 = 1 # 是否要记录文件夹的打开时间
            - scid: int | str = <default>
            - show_dir: 0 | 1 = 1
            - snap: 0 | 1 = <default>
            - source: str = <default>
            - sys_dir: int | str = <default>
            - star: 0 | 1 = <default> # 是否星标文件
            - stdir: 0 | 1 = <default>
            - suffix: str = <default> # 后缀名
            - type: int = <default>
                # 文件类型：
                # - 全部: 0
                # - 文档: 1
                # - 图片: 2
                # - 音频: 3
                # - 视频: 4
                # - 压缩包: 5
                # - 应用: 6
                # - 书籍: 7
                # - 仅文件: 99
        """
        api = "https://proapi.115.com/android/2.0/ufile/files"
        if isinstance(payload, int):
            payload = {
                "aid": 1, "count_folders": 1, "limit": 32, "offset": 0, 
                "record_open_time": 1, "show_dir": 1, "cid": payload, 
            }
        else:
            payload = {
                "aid": 1, "count_folders": 1, "limit": 32, "offset": 0, 
                "record_open_time": 1, "show_dir": 1, "cid": 0, **payload, 
            }
        if payload.keys() & frozenset(("asc", "fc_mix", "o")):
            payload["custom_order"] = 1
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files3(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files3(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files3(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件夹的中的文件列表和基本信息
        GET https://aps.115.com/natsort/files.php
        payload:
            - cid: int | str = 0 # 文件夹 id
            - limit: int = 32    # 一页大小，意思就是 page_size
            - offset: int = 0    # 索引偏移，索引从 0 开始计算

            - aid: int | str = 1 # area_id，不知道的话，设置为 1
            - asc: 0 | 1 = <default> # 是否升序排列
            - code: int | str = <default>
            - count_folders: 0 | 1 = 1 # 统计文件数和文件夹数
            - cur: 0 | 1 = <default> # 是否只搜索当前目录
            - custom_order: 0 | 1 = <default> # 启用自定义排序，如果指定了 "asc", "fc_mix", "o" 其一，则此参数要设置为 1 （我实现了自动设置）
            - date: str = <default> # 筛选日期
            - fc_mix: 0 | 1 = <default> # 是否目录和文件混合，如果为 0 则目录在前
            - fields: str = <default>
            - format: str = "json"
            - hide_data: str = <default>
            - is_q: 0 | 1 = <default>
            - is_share: 0 | 1 = <default>
            - min_size: int = 0 # 最小的文件大小
            - max_size: int = 0 # 最大的文件大小
            - natsort: 0 | 1 = <default>
            - o: str = <default>
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
            - r_all: 0 | 1 = <default>
            - record_open_time: 0 | 1 = 1 # 是否要记录文件夹的打开时间
            - scid: int | str = <default>
            - show_dir: 0 | 1 = 1
            - snap: 0 | 1 = <default>
            - source: str = <default>
            - sys_dir: int | str = <default>
            - star: 0 | 1 = <default> # 是否星标文件
            - stdir: 0 | 1 = <default>
            - suffix: str = <default> # 后缀名
            - type: int = <default>
                # 文件类型：
                # - 全部: 0
                # - 文档: 1
                # - 图片: 2
                # - 音频: 3
                # - 视频: 4
                # - 压缩包: 5
                # - 应用: 6
                # - 书籍: 7
                # - 仅文件: 99
        """
        api = "https://aps.115.com/natsort/files.php"
        if isinstance(payload, int):
            payload = {
                "aid": 1, "count_folders": 1, "limit": 32, "offset": 0, 
                "record_open_time": 1, "show_dir": 1, "cid": payload, 
            }
        else:
            payload = {
                "aid": 1, "count_folders": 1, "limit": 32, "offset": 0, 
                "record_open_time": 1, "show_dir": 1, "cid": 0, **payload, 
            }
        if payload.keys() & frozenset(("asc", "fc_mix", "o")):
            payload["custom_order"] = 1
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_getid(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_getid(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_getid(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """由路径获取对应的 id（但只能获取目录，不能获取文件）
        GET https://webapi.115.com/files/getid
        payload:
            - path: str
        """
        api = "https://webapi.115.com/files/getid"
        if isinstance(payload, str):
            payload = {"path": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_image(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_image(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_image(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取图片的各种链接
        GET https://webapi.115.com/files/image
        payload:
            - pickcode: str
        """
        api = "https://webapi.115.com/files/image"
        if isinstance(payload, str):
            payload = {"pickcode": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_imglist(
        self, 
        payload: int | str | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_imglist(
        self, 
        payload: int | str | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_imglist(
        self, 
        payload: int | str | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件夹的中的图片列表和基本信息
        GET https://proapi.115.com/android/files/imglist
        payload:
            - cid: int | str = 0 # 文件夹 id
            - limit: int = 32    # 一页大小，建议控制在 <= 9000，不然会报错
            - offset: int = 0    # 索引偏移，索引从 0 开始计算

            - aid: int | str = 1 # area_id，不知道的话，设置为 1
            - asc: 0 | 1 = <default> # 是否升序排列
            - cur: 0 | 1 = <default> # 只罗列当前文件夹
            - o: str = <default>
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
        """
        api = "https://proapi.115.com/android/files/imglist"
        if isinstance(payload, (int, str)):
            payload = {"limit": 32, "offset": 0, "aid": 1, "cid": payload}
        else:
            payload = {"limit": 32, "offset": 0, "aid": 1, "cid": 0, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_imagedata(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_imagedata(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_imagedata(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取图片的分辨率等信息
        POST https://imgjump.115.com/getimgdata_url
        payload:
            - imgurl: str # 图片的访问链接，以 "http://thumb.115.com" 开头
        """
        api = "https://imgjump.115.com/getimgdata_url"
        if isinstance(payload, str):
            payload = {"imgurl": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_shasearch(
        self, 
        payload: str | dict, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_shasearch(
        self, 
        payload: str | dict, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_shasearch(
        self, 
        payload: str | dict, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """通过 sha1 搜索文件
        GET https://webapi.115.com/files/shasearch
        payload:
            - sha1: str
        """
        api = "https://webapi.115.com/files/shasearch"
        if isinstance(payload, str):
            payload = {"sha1": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_video(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_video(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_video(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取视频信息
        GET https://webapi.115.com/files/video
        GET https://v.anxia.com/webapi/files/video

        :param payload: 请求参数，包含以下参数，只传字符串视为 pickcode
            - pickcode: str
            - share_id: int | str = <default>
            - local: 0 | 1 = <default>
        :param use_anxia_api: 是否使用 https://v.anxia.com 的接口
            - 如果为 False（默认），使用 "https://webapi.115.com/files/video"
            - 如果为 True，使用 "https://v.anxia.com/webapi/files/video"
                - 使用这个接口前，请先请求一次 f"https://v.anxia.com/?pickcode={pickcode}&share_id=0"，否则可能报错 403
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口返回值
        """
        if use_anxia_api:
            api = "https://v.anxia.com/webapi/files/video"
        else:
            api = "https://webapi.115.com/files/video"
        if isinstance(payload, str):
            payload = {"pickcode": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_video_subtitle(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_video_subtitle(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_video_subtitle(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取视频字幕
        GET https://webapi.115.com/movies/subtitle
        GET https://v.anxia.com/webapi/movies/subtitle

        :param payload: 请求参数，包含以下参数，只传字符串视为 pickcode
            - pickcode: str
        :param use_anxia_api: 是否使用 https://v.anxia.com 的接口
            - 如果为 False（默认），使用 "https://webapi.115.com/movies/subtitle"
            - 如果为 True，使用 "https://v.anxia.com/webapi/movies/subtitle"
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口返回值
        """
        if use_anxia_api:
            api = "https://v.anxia.com/webapi/movies/subtitle"
        else:
            api = "https://webapi.115.com/movies/subtitle"
        if isinstance(payload, str):
            payload = {"pickcode": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_video_m3u8(
        self, 
        /, 
        pickcode: str, 
        definition: int = 0, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    def fs_files_video_m3u8(
        self, 
        /, 
        pickcode: str, 
        definition: int = 0, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    def fs_files_video_m3u8(
        self, 
        /, 
        pickcode: str, 
        definition: int = 0, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """获取视频的 m3u8 文件列表，此接口必须使用 web 的 cookies

        :param pickcode: 视频文件的 pickcode
        :params definition: 画质，默认列出所有画质。但可进行筛选，常用的为：
            - 0: 各种分辨率（默认）
            - 3: HD (约为720p)
            - 4: UD (约为1080p)
        :param use_anxia_api: 是否使用 https://v.anxia.com 的接口
            - 如果为 False（默认），使用 f"http://115.com/api/video/m3u8/{pickcode}.m3u8?definition={definition}"
                - 使用这个接口得到的 m3u8 文件，其中包含几个不同分辨率的视频的 m3u8 文件链接（此时下载不需要 Cookies）
            - 如果为 True，使用 f"https://v.anxia.com/site/api/video/m3u8/{pickcode}.m3u8?definition={definition}"
                - 使用这个接口得到的 m3u8 文件，其中包含几个不同分辨率的视频的 m3u8 文件链接（此时下载不需要 Cookies）
                - 使用这个接口前，请先请求一次 f"https://v.anxia.com/?pickcode={pickcode}&share_id=0"，否则可能报错 403
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口返回值

        # 其它替代接口：
        # 1. 需要破解里面一个 rsa 请求参数的生成方法，此接口不限设备（不强制为 web 的 cookies）
        GET http://videoplay.115.com/m3u8
        params = {filesha1: str, time: int, userid: int, rsa: str = "<md5_sign>"}
        # 2. 需要破解 data 参数具体如何生成
        POST https://proapi.115.com/android/2.0/video/play
        data = {data: str = "<{b64encode(rsa_encrypt(data))>"}
        """
        if use_anxia_api:
            api = f"https://v.anxia.com/site/api/video/m3u8/{pickcode}.m3u8?definition={definition}"
        else:
            api = f"http://115.com/api/video/m3u8/{pickcode}.m3u8?definition={definition}"
        request_kwargs.setdefault("parse", False)
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def fs_files_history(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_history(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_history(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件的观看历史，主要用于视频
        GET https://webapi.115.com/files/history
        GET https://v.anxia.com/webapi/files/history

        :param payload: 请求参数，包含以下参数，只传字符串视为 pickcode
            - pick_code: str
            - fetch: str = "one"
            - category: int = <default>
            - share_id: int | str = <default>
        :param use_anxia_api: 是否使用 https://v.anxia.com 的接口
            - 如果为 False（默认），使用 "https://webapi.115.com/files/history"
            - 如果为 True，使用 "https://v.anxia.com/webapi/files/history"
                - 使用这个接口前，请先请求一次 f"https://v.anxia.com/?pickcode={pickcode}&share_id=0"，否则可能报错 403
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口返回值
        """
        if use_anxia_api:
            api = "https://v.anxia.com/webapi/files/history"
        else:
            api = "https://webapi.115.com/files/history"
        if isinstance(payload, str):
            payload = {"fetch": "one", "pick_code": payload}
        else:
            payload = {"fetch": "one", **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_history_post(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_history_post(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_history_post(
        self, 
        payload: str | dict, 
        /, 
        use_anxia_api: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """更新文件的观看历史，主要用于视频
        POST https://webapi.115.com/files/history
        POST https://v.anxia.com/webapi/files/history

        :param payload: 请求参数，包含以下参数，只传字符串视为 pickcode
            - pick_code: str
            - op: str = "update"
            - category: int = <default>
            - definition: int = <default>
            - share_id: int | str = <default>
            - time: int = <default>
            - ...（其它未找全的参数）
        :param use_anxia_api: 是否使用 https://v.anxia.com 的接口
            - 如果为 False（默认），使用 "https://webapi.115.com/files/history"
            - 如果为 True，使用 "https://v.anxia.com/webapi/files/history"
                - 使用这个接口前，请先请求一次 f"https://v.anxia.com/?pickcode={pickcode}&share_id=0"，否则可能报错 403
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数

        :return: 接口返回值
        """
        if use_anxia_api:
            api = "https://v.anxia.com/webapi/files/history"
        else:
            api = "https://webapi.115.com/files/history"
        if isinstance(payload, str):
            payload = {"op": "update", "pick_code": payload}
        else:
            payload = {"op": "update", **payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_history(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_history(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_history(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取历史记录
        GET https://proapi.115.com/android/history
        payload:
            - pick_code: str
            - action: str = "get_one"
        """
        api = "https://proapi.115.com/android/history"
        if isinstance(payload, dict):
            payload = {"action": "get_one", **payload}
        else:
            payload = {"action": "get_one", "pick_code": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_history_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_history_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_history_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """历史记录列表
        GET https://webapi.115.com/history/list
        payload:
            - offset: int = 0
            - limit: int = 1150
            - played_end: 0 | 1 = <default>
            - type: int = <default>
                # 类型：
                # - 全部: 0
                # - ？？: 1
                # - ？？: 2
                # - 播放视频: 3
                # - 上传: 4
                # - ？？: 5
                # - ？？: 6
                # - ？？: 7
                # - ？？: 8
        """
        api = "https://webapi.115.com/history/list"
        if isinstance(payload, int):
            payload = {"limit": 1150, "offset": payload}
        else:
            payload = {"limit": 1150, "offset": 0, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_history_receive_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_history_receive_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_history_receive_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """接收列表
        GET https://webapi.115.com/history/receive_list
        payload:
            - offset: int = 0
            - limit: int = 1150
        """
        api = "https://webapi.115.com/history/receive_list"
        if isinstance(payload, int):
            payload = {"limit": 1150, "offset": payload}
        else:
            payload = {"limit": 1150, "offset": 0, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_history_move_target_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_history_move_target_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_history_move_target_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """移动列表
        GET https://webapi.115.com/history/move_target_list
        payload:
            - offset: int = 0
            - limit: int = 1150
        """
        api = "https://webapi.115.com/history/move_target_list"
        if isinstance(payload, int):
            payload = {"limit": 1150, "offset": payload}
        else:
            payload = {"limit": 1150, "offset": 0, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_order(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_order(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_order(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件夹的中的文件列表和基本信息
        POST https://webapi.115.com/files/order
        payload:
            - user_order: str
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
            - file_id: int | str = 0 # 目录 id
            - user_asc: 0 | 1 = <default> # 是否升序排列
            - fc_mix: 0 | 1 = <default>   # 是否目录和文件混合，如果为 0 则目录在前
        """
        api = "https://webapi.115.com/files/order"
        if isinstance(payload, str):
            payload = {"file_id": 0, "user_order": payload}
        else:
            payload = {"file_id": 0, **payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_type(
        self, 
        payload: Literal[1,2,3,4,5,6,7] | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_type(
        self, 
        payload: Literal[1,2,3,4,5,6,7] | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_type(
        self, 
        payload: Literal[1,2,3,4,5,6,7] | dict = 1, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件夹中某个文件类型的扩展名的（去重）列表
        GET https://webapi.115.com/files/get_second_type
        payload:
            - cid: int | str = 0 # 文件夹 id
            - type: int = <default>
                # 文件类型：
                # - 文档: 1
                # - 图片: 2
                # - 音频: 3
                # - 视频: 4
                # - 压缩包: 5
                # - 应用: 6
                # - 书籍: 7
            - file_label: int | str = <default> # 标签 id，如果有多个则用逗号 "," 隔开
        """
        api = "https://webapi.115.com/files/get_second_type"
        if isinstance(payload, int):
            payload = {"cid": 0, "type": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_set(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_set(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_set(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """设置文件或文件夹（备注、标签等）
        POST https://webapi.115.com/files/edit
        payload:
            # 如果是单个文件或文件夹，也可以是多个但用逗号 "," 隔开
            - fid: int | str
            # 如果是多个文件或文件夹
            - fid[]: int | str
            - fid[]: int | str
            - ...
            # 其它配置信息
            - file_desc: str = <default> # 可以用 html
            - file_label: int | str = <default> # 标签 id，如果有多个，用逗号 "," 隔开
            - fid_cover: int | str = <default> # 封面图片的文件 id，如果有多个，用逗号 "," 隔开，如果要删除，值设为 0 即可
            - show_play_long: 0 | 1 = <default> # 文件名称显示时长
        """
        api = "https://webapi.115.com/files/edit"
        if (headers := request_kwargs.get("headers")):
            headers = request_kwargs["headers"] = dict(headers)
        else:
            headers = request_kwargs["headers"] = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self.request(
            api, 
            "POST", 
            data=urlencode(payload), 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def fs_files_batch_set(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_batch_set(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_batch_set(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """批量设置文件或文件夹（显示时长等）
        POST https://webapi.115.com/files/batch_edit
        payload:
            - show_play_long[{fid}]: 0 | 1 = 1 # 设置或取消显示时长
        """
        api = "https://webapi.115.com/files/batch_edit"
        if (headers := request_kwargs.get("headers")):
            headers = request_kwargs["headers"] = dict(headers)
        else:
            headers = request_kwargs["headers"] = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self.request(
            api, 
            "POST", 
            data=urlencode(payload), 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def fs_files_folder_playlong(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_folder_playlong(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_folder_playlong(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件夹内文件总的播放时长
        POST https://aps.115.com/getFolderPlaylong
        payload:
            - folder_ids: int | str # 目录 id，如果有多个，用逗号 "," 隔开
        """
        api = "https://aps.115.com/getFolderPlaylong"
        if isinstance(payload, (int, str)):
            payload = {"folder_ids": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_files_hidden(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_files_hidden(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_files_hidden(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """隐藏或者取消隐藏文件或文件夹
        POST https://webapi.115.com/files/hiddenfiles
        payload:
            - fid[0]: int | str
            - fid[1]: int | str
            - ...
            - hidden: 0 | 1 = 1
        """
        api = "https://webapi.115.com/files/hiddenfiles"
        if isinstance(payload, (int, str)):
            payload = {"hidden": 1, "fid[0]": payload}
        elif isinstance(payload, dict):
            payload = {"hidden": 1, **payload}
        else:
            payload = {f"f[{i}]": f for i, f in enumerate(payload)}
            if not payload:
                return {"state": False, "message": "no op"}
            payload["hidden"] = 1
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_hidden_switch(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_hidden_switch(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_hidden_switch(
        self, 
        payload: str | dict = "", 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """切换隐藏模式
        POST https://115.com/?ct=hiddenfiles&ac=switching
        payload:
            safe_pwd: str = "" # 密码，如果需要进入隐藏模式，请传递此参数
            show: 0 | 1 = <default>
            valid_type: int = 1
        """
        api = "https://115.com/?ct=hiddenfiles&ac=switching"
        if isinstance(payload, str):
            if payload:
                payload = {"valid_type": 1, "show": 1, "safe_pwd": payload}
            else:
                payload = {"valid_type": 1, "show": 0}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_get_repeat(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_get_repeat(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_get_repeat(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """查找重复文件（罗列除此以外的 sha1 相同的文件）
        GET https://webapi.115.com/files/get_repeat_sha
        payload:
            file_id: int | str
            offset: int = 0
            limit: int = 1150
            source: str = ""
            format: str = "json"
        """
        api = "https://webapi.115.com/files/get_repeat_sha"
        if isinstance(payload, (int, str)):
            payload = {"offset": 0, "limit": 1150, "format": "json", "file_id": payload}
        else:
            payload = {"offset": 0, "limit": 1150, "format": "json", **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_index_info(
        self, 
        payload: Literal[0, 1] | dict = 0, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_index_info(
        self, 
        payload: Literal[0, 1] | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_index_info(
        self, 
        payload: Literal[0, 1] | dict = 0, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取当前已用空间、可用空间、登录设备等信息
        GET https://webapi.115.com/files/index_info
        payload:
            count_space_nums: 0 | 1 = 0 # 如果为 0，包含各种类型文件的数量统计；如果为 1，包含登录设备列表
        """
        api = "https://webapi.115.com/files/index_info"
        if not isinstance(payload, dict):
            payload = {"count_space_nums": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_info(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_info(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_info(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件或文件夹的基本信息
        GET https://webapi.115.com/files/get_info
        payload:
            - file_id: int | str
        """
        api = "https://webapi.115.com/files/get_info"
        if isinstance(payload, (int, str)):
            payload = {"file_id": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_mkdir(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_mkdir(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_mkdir(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """新建文件夹
        POST https://webapi.115.com/files/add
        payload:
            - cname: str
            - pid: int | str = 0
        """
        api = "https://webapi.115.com/files/add"
        if isinstance(payload, str):
            payload = {"pid": 0, "cname": payload}
        else:
            payload = {"pid": 0, **payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_search(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_search(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_search(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """搜索文件或文件夹（提示：好像最多只能罗列前 10,000 条数据，也就是 limit + offset <= 10_000）
        GET https://webapi.115.com/files/search
        payload:
            - aid: int | str = 1 # area_id，不知道的话，设置为 1
            - asc: 0 | 1 = <default> # 是否升序排列
            - cid: int | str = 0 # 文件夹 id
            - count_folders: 0 | 1 = <default>
            - date: str = <default> # 筛选日期
            - fc_mix: 0 | 1 = <default> # 是否目录和文件混合，如果为 0 则目录在前
            - file_label: int | str = <default> # 标签 id
            - format: str = "json" # 输出格式（不用管）
            - limit: int = 32 # 一页大小，意思就是 page_size
            - o: str = <default>
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
            - offset: int = 0  # 索引偏移，索引从 0 开始计算
            - pick_code: str = <default>
            - search_value: str = <default>
            - show_dir: 0 | 1 = 1
            - source: str = <default>
            - star: 0 | 1 = <default>
            - suffix: str = <default>
            - type: int = <default>
                # 文件类型：
                # - 全部: 0
                # - 文档: 1
                # - 图片: 2
                # - 音频: 3
                # - 视频: 4
                # - 压缩包: 5
                # - 应用: 6
                # - 书籍: 7
        """
        api = "https://webapi.115.com/files/search"
        if isinstance(payload, str):
            payload = {
                "aid": 1, "cid": 0, "format": "json", "limit": 32, "offset": 0, 
                "show_dir": 1, "search_value": payload, 
            }
        else:
            payload = {
                "aid": 1, "cid": 0, "format": "json", "limit": 32, "offset": 0, 
                "show_dir": 1, **payload, 
            }
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_export_dir(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_export_dir(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_export_dir(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """导出目录树
        POST https://webapi.115.com/files/export_dir
        payload:
            file_ids: int | str   # 有多个时，用逗号 "," 隔开
            target: str = "U_1_0" # 导出目录树到这个目录
            layer_limit: int = <default> # 层级深度，自然数
        """
        api = "https://webapi.115.com/files/export_dir"
        if isinstance(payload, (int, str)):
            payload = {"file_ids": payload, "target": "U_1_0"}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_export_dir_status(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_export_dir_status(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_export_dir_status(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取导出目录树的完成情况
        GET https://webapi.115.com/files/export_dir
        payload:
            export_id: int | str
        """
        api = "https://webapi.115.com/files/export_dir"
        if isinstance(payload, (int, str)):
            payload = {"export_id": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    # TODO 支持异步
    @overload
    def fs_export_dir_future(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> ExportDirStatus:
        ...
    @overload
    def fs_export_dir_future(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, ExportDirStatus]:
        ...
    def fs_export_dir_future(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> ExportDirStatus | Coroutine[Any, Any, ExportDirStatus]:
        """执行导出目录树，新开启一个线程，用于检查完成状态
        payload:
            file_ids: int | str   # 有多个时，用逗号 "," 隔开
            target: str = "U_1_0" # 导出目录树到这个目录
            layer_limit: int = <default> # 层级深度，自然数
        """
        if async_:
            raise NotImplementedError("asynchronous mode not implemented")
        resp = check_response(self.fs_export_dir(payload, **request_kwargs))
        return ExportDirStatus(self, resp["data"]["export_id"])

    @overload
    def fs_category_get(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_category_get(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_category_get(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件或文件夹的统计信息（提示：但得不到根目录的统计信息，所以 cid 为 0 时无意义）
        GET https://webapi.115.com/category/get
        payload:
            cid: int | str
            aid: int | str = 1
        """
        api = "https://webapi.115.com/category/get"
        if isinstance(payload, (int, str)):
            payload = {"cid": payload}
        else:
            payload = {"cid": 0, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    fs_statistic = fs_category_get

    @overload
    def fs_category_shortcut(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_category_shortcut(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_category_shortcut(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """快捷入口列表（罗列所有的快捷入口）
        GET https://webapi.115.com/category/shortcut
        payload:
            - offset: int = 0
            - limit: int = 1150
        """
        if isinstance(payload, int):
            payload = {"limit": 1150, "offset": payload}
        else:
            payload = {"limit": 1150, "offset": 0, **payload}
        api = "https://webapi.115.com/category/shortcut"
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_category_shortcut_set(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_category_shortcut_set(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_category_shortcut_set(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """把一个目录设置或取消为快捷入口（快捷入口需要是目录）
        POST https://webapi.115.com/category/shortcut
        payload:
            file_id: int | str # 有多个时，用逗号 "," 隔开
            op: "add" | "delete" | "top" = "add"
                # 操作代码
                # - add: 添加
                # - delete: 删除
                # - top: 置顶
        """
        api = "https://webapi.115.com/category/shortcut"
        if isinstance(payload, (int, str)):
            payload = {"file_id": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_cover_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        fid_cover: int | str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_cover_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        fid_cover: int | str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_cover_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        fid_cover: int | str = 0,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """设置目录的封面，此接口是对 `fs_files_edit` 的封装
        
        :param fids: 单个或多个文件或文件夹 id
        :param file_label: 图片的 id，如果为 0 则是删除封面
        """
        if isinstance(fids, (int, str)):
            payload = [("fid", fids)]
        else:
            payload = [("fid[]", fid) for fid in fids]
            if not payload:
                return {"state": False, "message": "no op"}
        payload.append(("fid_cover", fid_cover))
        return self.fs_files_set(payload, async_=async_, **request_kwargs)

    @overload
    def fs_desc(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_desc(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_desc(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件或文件夹的备注
        GET https://webapi.115.com/files/desc
        payload:
            - file_id: int | str
            - format: str = "json"
            - compat: 0 | 1 = 1
            - new_html: 0 | 1 = <default>
        """
        api = "https://webapi.115.com/files/desc"
        if isinstance(payload, (int, str)):
            payload = {"format": "json", "compat": 1, "file_id": payload}
        else:
            payload = {"format": "json", "compat": 1, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def fs_desc_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        file_desc: str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_desc_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        file_desc: str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_desc_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        file_desc: str = "",
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """为文件或文件夹设置备注，最多允许 65535 个字节 (64 KB 以内)，此接口是对 `fs_files_edit` 的封装

        :param fids: 单个或多个文件或文件夹 id
        :param file_desc: 备注信息，可以用 html
        """
        if isinstance(fids, (int, str)):
            payload = [("fid", fids)]
        else:
            payload = [("fid[]", fid) for fid in fids]
            if not payload:
                return {"state": False, "message": "no op"}
        payload.append(("file_desc", file_desc))
        return self.fs_files_set(payload, async_=async_, **request_kwargs)

    @overload
    def fs_label_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        file_label: int | str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_label_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        file_label: int | str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_label_set(
        self, 
        fids: int | str | Iterable[int | str], 
        /, 
        file_label: int | str = "",
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """为文件或文件夹设置标签，此接口是对 `fs_files_edit` 的封装

        :param fids: 单个或多个文件或文件夹 id
        :param file_label: 标签 id，如果有多个，用逗号 "," 隔开
        """
        if isinstance(fids, (int, str)):
            payload = [("fid", fids)]
        else:
            payload = [("fid[]", fid) for fid in fids]
            if not payload:
                return {"state": False, "message": "no op"}
        payload.append(("file_label", file_label))
        return self.fs_files_set(payload, async_=async_, **request_kwargs)

    @overload
    def fs_label_batch(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_label_batch(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_label_batch(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """批量设置标签
        POST https://webapi.115.com/files/batch_label
        payload:
            - action: "add" | "remove" | "reset" | "replace"
                # 操作名
                # - 添加: "add"
                # - 移除: "remove"
                # - 重设: "reset"
                # - 替换: "replace"
            - file_ids: int | str # 文件或文件夹 id，如果有多个，用逗号 "," 隔开
            - file_label: int | str = <default> # 标签 id，如果有多个，用逗号 "," 隔开
            - file_label[{file_label}]: int | str = <default> # action 为 replace 时使用此参数，file_label[{原标签id}]: {目标标签id}，例如 file_label[123]: 456，就是把 id 是 123 的标签替换为 id 是 456 的标签
        """
        api = "https://webapi.115.com/files/batch_label"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_score_set(
        self, 
        file_id: int | str, 
        /, 
        score: int,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_score_set(
        self, 
        file_id: int | str, 
        /, 
        score: int,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_score_set(
        self, 
        file_id: int | str, 
        /, 
        score: int = 0,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """给文件或文件夹评分
        POST https://webapi.115.com/files/score
        payload:
            - file_id: int | str # 文件或文件夹 id，如果有多个，用逗号 "," 隔开
            - score: int = 0     # 0 为删除评分
        """
        api = "https://webapi.115.com/files/score"
        payload = {"file_id": file_id, "score": score}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def fs_star_set(
        self, 
        file_id: int | str, 
        /, 
        star: bool = True, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def fs_star_set(
        self, 
        file_id: int | str, 
        /, 
        star: bool = True, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def fs_star_set(
        self, 
        file_id: int | str, 
        /, 
        star: bool = True, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """为文件或文件夹设置或取消星标
        POST https://webapi.115.com/files/star
        payload:
            - file_id: int | str # 文件或文件夹 id，如果有多个，用逗号 "," 隔开
            - star: 0 | 1 = 1
        """
        api = "https://webapi.115.com/files/star"
        payload = {"file_id": file_id, "star": int(star)}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def photo_albumlist(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def photo_albumlist(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def photo_albumlist(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """相册列表
        GET https://webapi.115.com/photo/albumlist
        payload:
            - offset: int = 0
            - limit: int = 1150
            - album_type: int = 1
        """
        api = "https://webapi.115.com/photo/albumlist"
        if isinstance(payload, int):
            payload = {"album_type": 1, "limit": 1150, "offset": payload}
        else:
            payload = {"album_type": 1, "limit": 1150, "offset": 0, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def label_add(
        self, 
        /, 
        *lables: str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def label_add(
        self, 
        /, 
        *lables: str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def label_add(
        self, 
        /, 
        *lables: str,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """添加标签（可以接受多个）
        POST https://webapi.115.com/label/add_multi

        可传入多个 label 描述，每个 label 的格式都是 "{label_name}" 或 "{label_name}\x07{color}"，例如 "tag\x07#FF0000"
        """
        api = "https://webapi.115.com/label/add_multi"
        payload = [("name[]", label) for label in lables if label]
        if not payload:
            return {"state": False, "message": "no op"}
        if (headers := request_kwargs.get("headers")):
            headers = request_kwargs["headers"] = dict(headers)
        else:
            headers = request_kwargs["headers"] = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self.request(
            api, 
            "POST", 
            data=urlencode(payload), 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def label_del(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def label_del(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def label_del(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除标签
        POST https://webapi.115.com/label/delete
        payload:
            - id: int | str # 标签 id，如果有多个，用逗号 "," 隔开
        """
        api = "https://webapi.115.com/label/delete"
        if isinstance(payload, (int, str)):
            payload = {"id": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def label_edit(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def label_edit(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def label_edit(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """编辑标签
        POST https://webapi.115.com/label/edit
        payload:
            - id: int | str # 标签 id
            - name: str = <default>  # 标签名
            - color: str = <default> # 标签颜色，支持 css 颜色语法
            - sort: int = <default>  # 序号
        """
        api = "https://webapi.115.com/label/edit"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def label_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def label_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def label_list(
        self, 
        payload: dict = {}, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """罗列标签列表（如果要获取做了标签的文件列表，用 `fs_search` 接口）
        GET https://webapi.115.com/label/list
        payload:
            - offset: int = 0 # 索引偏移，从 0 开始
            - limit: int = 11500 # 一页大小
            - keyword: str = <default> # 搜索关键词
            - sort: "name" | "update_time" | "create_time" = <default>
                # 排序字段:
                # - 名称: "name"
                # - 创建时间: "create_time"
                # - 更新时间: "update_time"
            - order: "asc" | "desc" = <default> # 排序顺序："asc"(升序), "desc"(降序)
        """
        api = "https://webapi.115.com/label/list"
        payload = {"offset": 0, "limit": 11500, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def life_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def life_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def life_list(
        self, 
        payload: dict = {}, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """罗列登录和增删改操作记录（最新几条）
        GET https://life.115.com/api/1.0/web/1.0/life/life_list
        payload:
            - start: int = 0
            - limit: int = 1000
            - show_type: int = 0
                # 筛选类型，有多个则用逗号 ',' 隔开:
                # 0: 所有
                # 1: 增、删、改、移动、上传、接收、设置标签等文件系统操作
                # 2: 浏览文件
                # 3: <UNKNOWN>
                # 4: account_security
            - type: int = <default>
            - tab_type: int = <default>
            - file_behavior_type: int | str = <default>
            - mode: str = <default>
            - check_num: int = <default>
            - total_count: int = <default>
            - start_time: int = <default>
            - end_time: int = <default> # 默认为次日零点前一秒
            - show_note_cal: 0 | 1 = <default>
            - isShow: 0 | 1 = <default>
            - isPullData: 'true' | 'false' = <default>
            - last_data: str = <default> # JSON object, e.g. {"last_time":1700000000,"last_count":1,"total_count":200}
        """
        api = "https://life.115.com/api/1.0/web/1.0/life/life_list"
        now = datetime.now()
        datetime.combine(now.date(), now.time().max)
        payload = {
            "start": 0, 
            "limit": 1000, 
            "show_type": 0, 
            "end_time": int(datetime.combine(now.date(), now.time().max).timestamp()), 
            **payload, 
        }
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def behavior_detail(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def behavior_detail(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def behavior_detail(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取 life_list 操作记录明细
        GET https://proapi.115.com/android/1.0/behavior/detail
        payload:
            - type: str
                # 操作类型
                # - "browser_image":     浏览图片
                # - "browser_video":     浏览视频
                # - "browser_document":  浏览文件
                # - "new_folder":        新增文件夹
                # - "copy_folder":       复制文件夹
                # - "folder_rename":     文件夹改名
                # - "folder_label":      文件夹设置标签
                # - "star_file":         设置星标
                # - "move_file":         移动文件或文件夹
                # - "delete_file":       删除文件或文件夹
                # - "upload_file":       上传文件
                # - "upload_image_file": 上传图片
                # - "receive_files":     接收文件
                # - "rename_file":       文件改名（未实现）
                # - "copy_file":         复制文件（未实现）
            - limit: int = 32
            - offset: int = 0
            - date: str = <default> # 默认为今天，格式为 yyyy-mm-dd
        """
        api = "https://proapi.115.com/android/1.0/behavior/detail"
        if isinstance(payload, str):
            payload = {"limit": 32, "offset": 0, "date": str(date.today()), "type": payload}
        else:
            payload = {"limit": 32, "offset": 0, "date": str(date.today()), **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def life_calendar_getoption(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def life_calendar_getoption(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def life_calendar_getoption(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取 115 生活的开关设置
        GET https://life.115.com/api/1.0/web/1.0/calendar/getoption
        """
        api = "https://life.115.com/api/1.0/web/1.0/calendar/getoption"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def life_calendar_setoption(
        self, 
        payload: Literal[0, 1] | dict = 1, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def life_calendar_setoption(
        self, 
        payload: Literal[0, 1] | dict = 1, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def life_calendar_setoption(
        self, 
        payload: Literal[0, 1] | dict = 1, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """设置 115 生活的开关选项
        POST https://life.115.com/api/1.0/web/1.0/calendar/setoption
        payload:
            - locus: 0 | 1 = 1     # 开启或关闭最近记录
            - open_life: 0 | 1 = 1 # 显示或关闭
            - birthday: 0 | 1 = <default>
            - holiday: 0 | 1 = <default>
            - lunar: 0 | 1 = <default>
            - view: 0 | 1 = <default>
            - diary: 0 | 1 = <default>
            - del_notice_item: 0 | 1 = <default>
            - first_week: 0 | 1 = <default>
        """
        if isinstance(payload, dict):
            payload = {"locus": 1, "open_life": 1, **payload}
        else:
            payload = {"locus": 1, "open_life": payload}
        api = "https://life.115.com/api/1.0/web/1.0/calendar/setoption"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    ########## Share API ##########

    @overload
    def share_send(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_send(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_send(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """创建（自己的）分享
        POST https://webapi.115.com/share/send
        payload:
            - file_ids: int | str # 文件列表，有多个用逗号 "," 隔开
            - is_asc: 0 | 1 = 1 # 是否升序排列
            - order: str = "file_name"
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
            - ignore_warn: 0 | 1 = 1 # 忽略信息提示，传 1 就行了
            - user_id: int | str = <default>
        """
        api = "https://webapi.115.com/share/send"
        if isinstance(payload, (int, str)):
            payload = {"ignore_warn": 1, "is_asc": 1, "order": "file_name", "file_ids": payload}
        else:
            payload = {"ignore_warn": 1, "is_asc": 1, "order": "file_name", **payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def share_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取（自己的）分享信息
        GET https://webapi.115.com/share/shareinfo
        payload:
            - share_code: str
        """
        api = "https://webapi.115.com/share/shareinfo"
        if isinstance(payload, str):
            payload = {"share_code": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def share_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_list(
        self, 
        payload: dict = {}, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """罗列（自己的）分享信息列表
        GET https://webapi.115.com/share/slist
        payload:
            - limit: int = 32
            - offset: int = 0
            - user_id: int | str = <default>
        """
        api = "https://webapi.115.com/share/slist"
        payload = {"offset": 0, "limit": 32, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def share_update(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_update(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_update(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """变更（自己的）分享的配置（例如改访问密码，取消分享）
        POST https://webapi.115.com/share/updateshare
        payload:
            - share_code: str
            - receive_code: str = <default>         # 访问密码（口令）
            - share_duration: int = <default>       # 分享天数: 1(1天), 7(7天), -1(长期)
            - is_custom_code: 0 | 1 = <default>     # 用户自定义口令（不用管）
            - auto_fill_recvcode: 0 | 1 = <default> # 分享链接自动填充口令（不用管）
            - share_channel: int = <default>        # 分享渠道代码（不用管）
            - action: str = <default>               # 操作: 取消分享 "cancel"
        """
        api = "https://webapi.115.com/share/updateshare"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    @staticmethod
    def share_snap(
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def share_snap(
        payload: dict, 
        /, 
        async_: Literal[True], 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def share_snap(
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        request: None | Callable = None, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取分享链接的某个文件夹中的文件和子文件夹的列表（包含详细信息）
        GET https://webapi.115.com/share/snap
        payload:
            - share_code: str
            - receive_code: str
            - cid: int | str = 0
            - limit: int = 32
            - offset: int = 0
            - asc: 0 | 1 = <default> # 是否升序排列
            - o: str = <default>
                # 用某字段排序：
                # - 文件名："file_name"
                # - 文件大小："file_size"
                # - 文件种类："file_type"
                # - 修改时间："user_utime"
                # - 创建时间："user_ptime"
                # - 上一次打开时间："user_otime"
        """
        api = "https://webapi.115.com/share/snap"
        payload = {"cid": 0, "limit": 32, "offset": 0, **payload}
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            return httpx_request(url=api, params=payload, async_=async_, **request_kwargs)
        else:
            return request(url=api, params=payload, **request_kwargs)

    @overload
    def share_downlist(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_downlist(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_downlist(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取分享链接的某个文件夹中可下载的文件的列表（只含文件，不含文件夹，任意深度，简略信息）
        GET https://proapi.115.com/app/share/downlist
        payload:
            - share_code: str
            - receive_code: str
            - cid: int | str = 0
        """
        api = "https://proapi.115.com/app/share/downlist"
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def share_receive(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_receive(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_receive(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """接收分享链接的某些文件或文件夹
        POST https://webapi.115.com/share/receive
        payload:
            - share_code: str
            - receive_code: str
            - file_id: int | str             # 有多个时，用逗号 "," 分隔
            - cid: int | str = <default>     # 这是你网盘的文件夹 cid
            - user_id: int | str = <default>
        """
        api = "https://webapi.115.com/share/receive"
        payload = {"cid": 0, **payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def share_download_url(
        self, 
        payload: dict, 
        /, 
        strict: bool = True, 
        use_web_api: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> P115Url:
        ...
    @overload
    def share_download_url(
        self, 
        payload: dict, 
        /, 
        strict: bool = True, 
        use_web_api: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, P115Url]:
        ...
    def share_download_url(
        self, 
        payload: dict, 
        /, 
        strict: bool = True, 
        use_web_api: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> P115Url | Coroutine[Any, Any, P115Url]:
        """获取分享链接中某个文件的下载链接，此接口是对 `share_download_url_app` 的封装
        POST https://proapi.115.com/app/share/downurl
        payload:
            - file_id: int | str
            - receive_code: str
            - share_code: str
            - user_id: int | str = <default>
        """
        if use_web_api:
            resp = self.share_download_url_web(payload, async_=async_, **request_kwargs)
        else:
            resp = self.share_download_url_app(payload, async_=async_, **request_kwargs)
        def get_url(resp: dict) -> P115Url:
            info = check_response(resp)["data"]
            file_id = payload["file_id"]
            if not info:
                raise FileNotFoundError(
                    errno.ENOENT, 
                    f"no such id: {file_id!r}, with response {resp}", 
                )
            url = info["url"]
            if strict and not url:
                raise IsADirectoryError(
                    errno.EISDIR, 
                    f"{file_id} is a directory, with response {resp}", 
                )
            return P115Url(
                url["url"] if url else "", 
                id=int(info["fid"]), 
                file_name=info["fn"], 
                file_size=int(info["fs"]), 
                is_directory=not url, 
            )
        if async_:
            async def async_request() -> P115Url:
                return get_url(await cast(Coroutine[Any, Any, dict], resp)) 
            return async_request()
        else:
            return get_url(cast(dict, resp))

    @overload
    def share_download_url_app(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_download_url_app(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_download_url_app(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取分享链接中某个文件的下载链接
        POST https://proapi.115.com/app/share/downurl
        payload:
            - file_id: int | str
            - receive_code: str
            - share_code: str
            - user_id: int | str = <default>
        """
        api = "https://proapi.115.com/app/share/downurl"
        def parse(resp, content: bytes) -> dict:
            resp = loads(content)
            if resp["state"]:
                resp["data"] = loads(rsa_decode(resp["data"]))
            return resp
        request_kwargs["parse"] = parse
        request_kwargs["data"] = {"data": rsa_encode(dumps(payload)).decode()}
        return self.request(url=api, method="POST", async_=async_, **request_kwargs)

    @overload
    def share_download_url_web(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def share_download_url_web(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def share_download_url_web(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取分享链接中某个文件的下载链接（网页版接口，不推荐使用）
        GET https://webapi.115.com/share/downurl
        payload:
            - file_id: int | str
            - receive_code: str
            - share_code: str
            - user_id: int | str = <default>
        """
        api = "https://webapi.115.com/share/downurl"
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def usershare_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def usershare_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def usershare_list(
        self, 
        payload: int | dict = 0, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """共享列表
        GET https://webapi.115.com/usershare/list
        payload:
            - offset: int = 0
            - limit: int = 1150
            - all: 0 | 1 = 1
        """
        api = "https://webapi.115.com/usershare/list"
        if isinstance(payload, int):
            payload = {"all": 1, "limit": 1150, "offset": payload}
        else:
            payload = {"all": 1, "limit": 1150, "offset": 0, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    ########## Download API ##########

    @overload
    def download_url(
        self, 
        pickcode: str, 
        /, 
        strict: bool = True, 
        use_web_api: bool = False, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> P115Url:
        ...
    @overload
    def download_url(
        self, 
        pickcode: str, 
        /, 
        strict: bool = True, 
        use_web_api: bool = False, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, P115Url]:
        ...
    def download_url(
        self, 
        pickcode: str, 
        /, 
        strict: bool = True, 
        use_web_api: bool = False, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> P115Url | Coroutine[Any, Any, P115Url]:
        """获取文件的下载链接，此接口是对 `download_url_app` 的封装
        """
        if use_web_api:
            resp = self.download_url_web(
                {"pickcode": pickcode}, 
                async_=async_, 
                **request_kwargs, 
            )
            def get_url(resp: dict) -> P115Url:
                if not resp["state"]:
                    resp["pickcode"] = pickcode
                    if resp["msg_code"] == 70005:
                        raise FileNotFoundError(errno.ENOENT, resp)
                    elif resp["msg_code"] == 70004 and strict:
                        raise IsADirectoryError(errno.EISDIR, resp)
                    else:
                        raise OSError(errno.EIO, resp)
                return P115Url(
                    resp.get("file_url", ""), 
                    id=int(resp["file_id"]), 
                    pickcode=resp["pickcode"], 
                    file_name=resp["file_name"], 
                    file_size=int(resp["file_size"]), 
                    is_directory=not resp["state"], 
                    headers=resp["headers"], 
                )
        else:
            resp = self.download_url_app(
                {"pickcode": pickcode}, 
                async_=async_, 
                **request_kwargs, 
            )
            def get_url(resp: dict) -> P115Url:
                if not resp["state"]:
                    resp["pickcode"] = pickcode
                    if resp["errno"] == 50003:
                        raise FileNotFoundError(errno.ENOENT, resp)
                    raise OSError(errno.EIO, resp)
                for fid, info in resp["data"].items():
                    url = info["url"]
                    if strict and not url:
                        raise IsADirectoryError(
                            errno.EISDIR, 
                            f"{fid} is a directory, with response {resp}", 
                        )
                    return P115Url(
                        url["url"] if url else "", 
                        id=int(fid), 
                        pickcode=info["pick_code"], 
                        file_name=info["file_name"], 
                        file_size=int(info["file_size"]), 
                        is_directory=not url,
                        headers=resp["headers"], 
                    )
                raise FileNotFoundError(
                    errno.ENOENT, 
                    f"no such pickcode: {pickcode!r}, with response {resp}", 
                )
        if async_:
            async def async_request() -> P115Url:
                return get_url(await cast(Coroutine[Any, Any, dict], resp)) 
            return async_request()
        else:
            return get_url(cast(dict, resp))

    @overload
    def download_url_app(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def download_url_app(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def download_url_app(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件的下载链接
        POST https://proapi.115.com/app/chrome/downurl
        payload:
            - pickcode: str
        """
        api = "https://proapi.115.com/app/chrome/downurl"
        if isinstance(payload, str):
            payload = {"pickcode": payload}
        request_headers = request_kwargs.get("headers")
        headers = request_kwargs.get("headers")
        if headers:
            if isinstance(headers, Mapping):
                headers = ItemsView(headers)
            headers = request_kwargs["headers"] = {
                "User-Agent": next((v for k, v in headers if k.lower() == "user-agent" and v), "")}
        else:
            headers = request_kwargs["headers"] = {"User-Agent": ""}
        def parse(resp, content: bytes) -> dict:
            json = loads(content)
            if json["state"]:
                json["data"] = loads(rsa_decode(json["data"]))
            json["headers"] = headers
            return json
        request_kwargs["parse"] = parse
        request_kwargs["data"] = {"data": rsa_encode(dumps(payload)).decode("ascii")}
        return self.request(api, "POST", async_=async_, **request_kwargs)

    @overload
    def download_url_web(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def download_url_web(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def download_url_web(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取文件的下载链接（网页版接口，不推荐使用）
        GET https://webapi.115.com/files/download
        payload:
            - pickcode: str
        """
        api = "https://webapi.115.com/files/download"
        if isinstance(payload, str):
            payload = {"pickcode": payload}
        headers = request_kwargs.get("headers")
        if headers:
            if isinstance(headers, Mapping):
                headers = ItemsView(headers)
            headers = request_kwargs["headers"] = {
                "User-Agent": next((v for k, v in headers if k.lower() == "user-agent" and v), "")}
        else:
            headers = request_kwargs["headers"] = {"User-Agent": ""}
        def parse(resp, content: bytes) -> dict:
            json = loads(content)
            if "Set-Cookie" in resp.headers:
                if isinstance(resp.headers, Mapping):
                    match = CRE_SET_COOKIE.search(resp.headers["Set-Cookie"])
                    if match is not None:
                        headers["Cookie"] = match[0]
                else:
                    for k, v in reversed(resp.headers.items()):
                        if k == "Set-Cookie" and CRE_SET_COOKIE.match(v) is not None:
                            headers["Cookie"] = v
                            break
            json["headers"] = headers
            return json
        request_kwargs["parse"] = parse
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    ########## Upload API ##########

    @staticmethod
    def _oss_upload_sign(
        bucket: str, 
        object: str, 
        token: dict, 
        method: str = "PUT", 
        params: None | str | Mapping | Sequence[tuple[Any, Any]] = "", 
        headers: None | str | dict = "", 
    ) -> dict:
        """帮助函数：计算认证信息，返回带认证信息的请求头
        """
        subresource_key_set = frozenset((
            "response-content-type", "response-content-language",
            "response-cache-control", "logging", "response-content-encoding",
            "acl", "uploadId", "uploads", "partNumber", "group", "link",
            "delete", "website", "location", "objectInfo", "objectMeta",
            "response-expires", "response-content-disposition", "cors", "lifecycle",
            "restore", "qos", "referer", "stat", "bucketInfo", "append", "position", "security-token",
            "live", "comp", "status", "vod", "startTime", "endTime", "x-oss-process",
            "symlink", "callback", "callback-var", "tagging", "encryption", "versions",
            "versioning", "versionId", "policy", "requestPayment", "x-oss-traffic-limit", "qosInfo", "asyncFetch",
            "x-oss-request-payer", "sequential", "inventory", "inventoryId", "continuation-token", "callback",
            "callback-var", "worm", "wormId", "wormExtend", "replication", "replicationLocation",
            "replicationProgress", "transferAcceleration", "cname", "metaQuery",
            "x-oss-ac-source-ip", "x-oss-ac-subnet-mask", "x-oss-ac-vpc-id", "x-oss-ac-forward-allow",
            "resourceGroup", "style", "styleName", "x-oss-async-process", "regionList"
        ))
        date = formatdate(usegmt=True)
        if params is None:
            params = ""
        else:
            if not isinstance(params, str):
                if isinstance(params, dict):
                    if params.keys() - subresource_key_set:
                        params = [(k, params[k]) for k in params.keys() & subresource_key_set]
                elif isinstance(params, Mapping):
                    params = [(k, params[k]) for k in params if k in subresource_key_set]
                else:
                    params = [(k, v) for k, v in params if k in subresource_key_set]
                params = urlencode(params)
            if params:
                params = "?" + params
        if headers is None:
            headers = ""
        elif isinstance(headers, dict):
            it = (
                (k2, v)
                for k, v in headers.items()
                if (k2 := k.lower()).startswith("x-oss-")
            )
            headers = "\n".join("%s:%s" % e for e in sorted(it))
        signature_data = f"""{method.upper()}


{date}
{headers}
/{bucket}/{object}{params}""".encode("utf-8")
        signature = to_base64(hmac_digest(bytes(token["AccessKeySecret"], "utf-8"), signature_data, "sha1"))
        return {
            "date": date, 
            "authorization": "OSS {0}:{1}".format(token["AccessKeyId"], signature), 
        }

    def _oss_upload_request(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        method: str = "PUT", 
        params: None | str | dict | list[tuple] = None, 
        headers: None | dict = None,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ):
        """帮助函数：请求阿里云 OSS （115 目前所使用的阿里云的对象存储）的公用函数
        """
        headers2 = self._oss_upload_sign(
            bucket, 
            object, 
            token, 
            method=method, 
            params=params, 
            headers=headers, 
        )
        if headers:
            headers2.update(headers)
        headers2["Content-Type"] = ""
        return self.request(
            url=url, 
            params=params, 
            headers=headers2, 
            method=method, 
            async_=async_, 
            **request_kwargs, 
        )

    # NOTE: https://github.com/aliyun/aliyun-oss-python-sdk/blob/master/oss2/api.py#L1359-L1595
    @overload
    def _oss_multipart_upload_init(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> str:
        ...
    @overload
    def _oss_multipart_upload_init(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, str]:
        ...
    def _oss_multipart_upload_init(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> str | Coroutine[Any, Any, str]:
        """帮助函数：分片上传的初始化，获取 upload_id
        """
        request_kwargs["parse"] = lambda resp, content, /: getattr(fromstring(content).find("UploadId"), "text")
        request_kwargs["method"] = "POST"
        request_kwargs["params"] = "uploads"
        request_kwargs["headers"] = {"x-oss-security-token": token["SecurityToken"]}
        return self._oss_upload_request(
            bucket, 
            object, 
            url, 
            token, 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def _oss_multipart_upload_part(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer], 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str, 
        part_number: int, 
        partsize: int = 1 << 24, 
        reporthook: None | Callable = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def _oss_multipart_upload_part(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str, 
        part_number: int, 
        partsize: int = 1 << 24, 
        reporthook: None | Callable = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def _oss_multipart_upload_part(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str, 
        part_number: int, 
        partsize: int = 1 << 24, # default to: 16 MB
        reporthook: None | Callable = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """帮助函数：上传一个分片，返回一个字典，包含如下字段：

        .. python:

            {
                "PartNumber": int,    # 分块序号，从 1 开始计数
                "LastModified": str,  # 最近更新时间
                "ETag": str,          # ETag 值，判断资源是否发生变化
                "HashCrc64ecma": int, # 校验码
                "Size": int,          # 分片大小
            }
        """
        def parse(resp, /) -> dict:
            headers = resp.headers
            return {
                "PartNumber": part_number, 
                "LastModified": datetime.strptime(headers["date"], "%a, %d %b %Y %H:%M:%S GMT").strftime("%FT%X.%f")[:-3] + "Z", 
                "ETag": headers["ETag"], 
                "HashCrc64ecma": int(headers["x-oss-hash-crc64ecma"]), 
                "Size": count_in_bytes, 
            }
        request_kwargs["parse"] = parse
        request_kwargs["params"] = {"partNumber": part_number, "uploadId": upload_id}
        request_kwargs["headers"] = {"x-oss-security-token": token["SecurityToken"]}
        if hasattr(file, "getbuffer"):
            try:
                file = getattr(file, "getbuffer")()
            except TypeError:
                pass
        dataiter: Iterator[Buffer] | AsyncIterator[Buffer]
        if isinstance(file, Buffer):
            count_in_bytes = len(file)
            if async_:
                dataiter = bytes_to_chunk_async_iter(file)
            else:
                dataiter = bytes_to_chunk_iter(file)
        elif isinstance(file, SupportsRead):
            count_in_bytes = 0
            def acc(length):
                nonlocal count_in_bytes
                count_in_bytes += length
            if async_:
                dataiter = bio_chunk_async_iter(file, partsize, callback=acc)
            else:
                dataiter = bio_chunk_iter(file, partsize, callback=acc)
        else:
            count_in_bytes = 0
            def acc(chunk):
                nonlocal count_in_bytes
                count_in_bytes += len(chunk)
                if count_in_bytes >= partsize:
                    raise StopIteration
            if async_:
                dataiter = wrap_aiter(file, callnext=acc)
            else:
                dataiter = wrap_iter(cast(Iterable, file), callnext=acc)
        if reporthook is not None:
            if async_:
                reporthook = ensure_async(reporthook)
                async def reporthook_wrap(b):
                    await reporthook(len(b))
                dataiter = wrap_aiter(dataiter, callnext=reporthook_wrap)
            else:
                dataiter = wrap_iter(cast(Iterable, dataiter), callnext=lambda b: reporthook(len(b)))
        request_kwargs["data"] = dataiter
        return self._oss_upload_request(
            bucket, 
            object, 
            url, 
            token, 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def _oss_multipart_upload_complete(
        self, 
        /, 
        bucket: str, 
        object: str, 
        callback: dict, 
        url: str, 
        token: dict, 
        upload_id: str, 
        parts: list[dict],
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def _oss_multipart_upload_complete(
        self, 
        /, 
        bucket: str, 
        object: str, 
        callback: dict, 
        url: str, 
        token: dict, 
        upload_id: str, 
        parts: list[dict],
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def _oss_multipart_upload_complete(
        self, 
        /, 
        bucket: str, 
        object: str, 
        callback: dict, 
        url: str, 
        token: dict, 
        upload_id: str, 
        parts: list[dict],
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """帮助函数：完成分片上传，会执行回调然后 115 上就能看到文件
        """
        request_kwargs["method"] = "POST"
        request_kwargs["params"] = {"uploadId": upload_id}
        request_kwargs["headers"] = {
            "x-oss-security-token": token["SecurityToken"], 
            "x-oss-callback": to_base64(callback["callback"]), 
            "x-oss-callback-var": to_base64(callback["callback_var"]), 
        }
        request_kwargs["data"] = ("<CompleteMultipartUpload>%s</CompleteMultipartUpload>" % "".join(map(
            "<Part><PartNumber>{PartNumber}</PartNumber><ETag>{ETag}</ETag></Part>".format_map, 
            parts, 
        ))).encode("utf-8")
        return self._oss_upload_request(
            bucket, 
            object, 
            url, 
            token, 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def _oss_multipart_upload_cancel(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bool:
        ...
    @overload
    def _oss_multipart_upload_cancel(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bool]:
        ...
    def _oss_multipart_upload_cancel(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bool | Coroutine[Any, Any, bool]:
        """帮助函数：取消分片上传
        """
        request_kwargs["parse"] = lambda resp: 200 <= resp.status_code < 300 or resp.status_code == 404
        request_kwargs["method"] = "DELETE"
        request_kwargs["params"] = {"uploadId": upload_id}
        request_kwargs["headers"] = {"x-oss-security-token": token["SecurityToken"]}
        return self._oss_upload_request(
            bucket, 
            object, 
            url, 
            token, 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def _oss_multipart_upload_part_iter(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer], 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str, 
        part_number_start, 
        partsize: int, 
        reporthook: None | Callable = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> Iterator[dict]:
        ...
    @overload
    def _oss_multipart_upload_part_iter(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str, 
        part_number_start: int, 
        partsize: int, 
        reporthook: None | Callable = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> AsyncIterator[dict]:
        ...
    def _oss_multipart_upload_part_iter(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str, 
        part_number_start: int = 1, 
        partsize: int = 10 * 1 << 20, # default to: 10 MB
        reporthook: None | Callable = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> Iterator[dict] | AsyncIterator[dict]:
        """帮助函数：迭代器，迭代一次上传一个分片
        """
        def gen_step():
            nonlocal file
            if hasattr(file, "getbuffer"):
                try:
                    file = getattr(file, "getbuffer")()
                except TypeError:
                    pass
            if isinstance(file, Buffer):
                file = memoryview(file)
            elif isinstance(file, SupportsRead):
                pass
            elif async_:
                file = bytes_iter_to_async_reader(file)
            else:
                file = bytes_iter_to_reader(cast(Iterable, file))
            for i, part_number in enumerate(count(part_number_start)):
                if isinstance(file, Buffer):
                    chunk = file[i*partsize:(i+1)*partsize]
                elif isinstance(file, SupportsRead):
                    if async_:
                        chunk = bio_chunk_async_iter(file, partsize)
                    else:
                        chunk = bio_chunk_iter(file, partsize)
                part = yield Yield(self._oss_multipart_upload_part(
                    chunk, 
                    bucket, 
                    object, 
                    url, 
                    token, 
                    upload_id, 
                    part_number=part_number, 
                    partsize=partsize, 
                    reporthook=reporthook, 
                    async_=async_, 
                    **request_kwargs, 
                ))
                if part["Size"] < partsize:
                    break
        return run_gen_step_iter(gen_step, async_=async_)

    @overload
    def _oss_multipart_part_iter(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> Iterator[dict]:
        ...
    @overload
    def _oss_multipart_part_iter(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> AsyncIterator[dict]:
        ...
    def _oss_multipart_part_iter(
        self, 
        /, 
        bucket: str, 
        object: str, 
        url: str, 
        token: dict, 
        upload_id: str,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> Iterator[dict] | AsyncIterator[dict]:
        """帮助函数：上传文件到阿里云 OSS，罗列已经上传的分块
        """
        def gen_step():
            to_num = lambda s: int(s) if isinstance(s, str) and s.isnumeric() else s
            request_kwargs["method"] = "GET"
            request_kwargs["headers"] = {"x-oss-security-token": token["SecurityToken"]}
            request_kwargs["params"] = params = {"uploadId": upload_id}
            request_kwargs["parse"] = lambda resp, content, /: fromstring(content)
            while True:
                etree = yield self._oss_upload_request(
                    bucket, 
                    object, 
                    url, 
                    token, 
                    async_=async_, 
                    **request_kwargs, 
                )
                for el in etree.iterfind("Part"):
                    yield Yield({sel.tag: to_num(sel.text) for sel in el}, identity=True)
                if etree.find("IsTruncated").text == "false":
                    break
                params["part-number-marker"] = etree.find("NextPartNumberMarker").text
        return run_gen_step_iter(gen_step, async_=async_)

    @overload
    def _oss_upload(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer], 
        bucket: str, 
        object: str, 
        callback: dict, 
        token: None | dict = None, 
        filesize: int = -1, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any]] = None, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def _oss_upload(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        bucket: str, 
        object: str, 
        callback: dict, 
        token: None | dict, 
        filesize: int, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]], 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def _oss_upload(
        self, 
        /, 
        file: Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer], 
        bucket: str, 
        object: str, 
        callback: dict, 
        token: None | dict = None, 
        filesize: int = -1, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]] = None, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """帮助函数：上传文件到阿里云 OSS，一次上传全部（即不进行分片）
        """
        url = self.upload_endpoint_url(bucket, object)
        if hasattr(file, "getbuffer"):
            try:
                file = getattr(file, "getbuffer")()
            except TypeError:
                pass
        dataiter: Iterable[Buffer] | AsyncIterable[Buffer]
        if isinstance(file, Buffer):
            if async_:
                dataiter = bytes_to_chunk_async_iter(file)
            else:
                dataiter = bytes_to_chunk_iter(file)
        elif isinstance(file, SupportsRead):
            if not async_ and iscoroutinefunction(file.read):
                raise TypeError(f"{file!r} with async read in non-async mode")
            if async_:
                dataiter = bio_chunk_async_iter(file)
            else:
                dataiter = bio_chunk_iter(file)
        else:
            if not async_ and isinstance(file, AsyncIterable):
                raise TypeError(f"async iterable {file!r} in non-async mode")
            if async_:
                dataiter = ensure_aiter(file)
            else:
                dataiter = cast(Iterable, file)
        if callable(make_reporthook):
            if async_:
                dataiter = progress_bytes_async_iter(
                    cast(AsyncIterable[Buffer], dataiter), 
                    make_reporthook, 
                    None if filesize < 0 else filesize, 
                )
            else:
                dataiter = progress_bytes_iter(
                    cast(Iterable[Buffer], dataiter), 
                    make_reporthook, 
                    None if filesize < 0 else filesize, 
                )
        request_kwargs["data"] = dataiter
        if async_:
            async def async_request():
                nonlocal async_, token
                async_ = cast(Literal[True], async_)
                if not token:
                    token = await self.upload_token(async_=async_)
                request_kwargs["headers"] = {
                    "x-oss-security-token": token["SecurityToken"], 
                    "x-oss-callback": to_base64(callback["callback"]), 
                    "x-oss-callback-var": to_base64(callback["callback_var"]), 
                }
                return await self._oss_upload_request(
                    bucket, 
                    object, 
                    url, 
                    token, 
                    async_=async_, 
                    **request_kwargs, 
                )
            return async_request()
        else:
            if not token:
                token = self.upload_token(async_=async_)
            request_kwargs["headers"] = {
                "x-oss-security-token": token["SecurityToken"], 
                "x-oss-callback": to_base64(callback["callback"]), 
                "x-oss-callback-var": to_base64(callback["callback_var"]), 
            }
            return self._oss_upload_request(
                bucket, 
                object, 
                url, 
                token, 
                async_=async_, 
                **request_kwargs, 
            )

    # TODO: 返回一个task，初始化成功后，生成 {"bucket": bucket, "object": object, "upload_id": upload_id, "callback": callback, "partsize": partsize, "filesize": filesize}
    @overload
    def _oss_multipart_upload(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] ), 
        bucket: str, 
        object: str, 
        callback: dict, 
        token: None | dict = None, 
        upload_id: None | str = None, 
        partsize: int = 10 * 1 << 20, 
        parts: None | list[dict] = None, 
        filesize: int = -1, 
        make_reporthook: None | Callable[[None | int], Any] | Generator[int, Any, Any] = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def _oss_multipart_upload(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        bucket: str, 
        object: str, 
        callback: dict, 
        token: None | dict = None, 
        upload_id: None | str = None, 
        partsize: int = 10 * 1 << 20, 
        parts: None | list[dict] = None, 
        filesize: int = -1, 
        make_reporthook: None | Callable[[None | int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any] = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def _oss_multipart_upload(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        bucket: str, 
        object: str, 
        callback: dict, 
        token: None | dict = None, 
        upload_id: None | str = None, 
        partsize: int = 10 * 1 << 20, # default to: 10 MB
        parts: None | list[dict] = None, 
        filesize: int = -1, 
        make_reporthook: None | Callable[[None | int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any] = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        def gen_step():
            nonlocal file, make_reporthook, parts, token, upload_id
            if not token:
                token = cast(dict, (yield self.upload_token(async_=async_)))
            url = self.upload_endpoint_url(bucket, object)
            skipsize = 0
            if parts is None:
                parts = []
                if upload_id:
                    if async_:
                        async def request():
                            async for part in self._oss_multipart_part_iter(
                                bucket, 
                                object, 
                                url, 
                                token, 
                                cast(str, upload_id), 
                                async_=True, 
                                **request_kwargs, 
                            ):
                                if part["Size"] != partsize:
                                    break
                                parts.append(part)
                        yield request
                    else:
                        for part in self._oss_multipart_part_iter(
                            bucket, 
                            object, 
                            url, 
                            token, 
                            upload_id, 
                            **request_kwargs, 
                        ):
                            if part["Size"] != partsize:
                                break
                            parts.append(part)
                    skipsize = sum(part["Size"] for part in parts)
                else:
                    upload_id = yield self._oss_multipart_upload_init(
                        bucket, object, url, token, async_=async_, **request_kwargs)
            reporthook: None | Callable = None
            close_reporthook: None | Callable = None
            if callable(make_reporthook):
                make_reporthook = make_reporthook(None if filesize < 0 else filesize)
                if isinstance(make_reporthook, Generator):
                    make_reporthook.send(None)
                    close_reporthook = make_reporthook.close
                elif isinstance(make_reporthook, AsyncGenerator):
                    yield partial(make_reporthook.asend, None)
                    close_reporthook = make_reporthook.aclose
            if isinstance(make_reporthook, Generator):
                reporthook = make_reporthook.send
            elif isinstance(make_reporthook, AsyncGenerator):
                reporthook = make_reporthook.asend
            elif callable(make_reporthook):
                reporthook = make_reporthook
            kwargs = dict(
                bucket=bucket, 
                object=object, 
                callback=callback, 
                token=token, 
                upload_id=upload_id, 
                partsize=partsize, 
                parts=parts, 
                filesize=filesize, 
                make_reporthook=lambda _: reporthook, 
                async_=async_, 
                **request_kwargs, 
            )
            try:
                if hasattr(file, "getbuffer"):
                    try:
                        file = getattr(file, "getbuffer")()
                    except TypeError:
                        pass
                if isinstance(file, Buffer):
                    file = memoryview(file)[skipsize:]
                    if skipsize and reporthook is not None:
                        yield partial(reporthook, skipsize)
                elif isinstance(file, SupportsRead):
                    if not async_ and iscoroutinefunction(file.read):
                        raise TypeError(f"{file!r} with async read in non-async mode")
                elif isinstance(file, (str, PathLike)):
                    filepath = fsdecode(file)
                    if async_:
                        try:
                            from aiofile import async_open
                        except ImportError:
                            file = yield to_thread(open, filepath, "rb")
                            yield to_thread(file.seek, skipsize)
                            if skipsize and reporthook is not None:
                                yield partial(reporthook, skipsize)
                        else:
                            async def request():
                                async with async_open(filepath, "rb") as file:
                                    file.seek(skipsize)
                                    if skipsize and reporthook is not None:
                                        await ensure_async(reporthook)(skipsize)
                                    return await self._oss_multipart_upload(file, **kwargs)
                            return (yield request)
                    else:
                        file = open(filepath, "rb")
                        file.seek(skipsize)
                        if skipsize and reporthook is not None:
                            yield partial(reporthook, skipsize)
                elif isinstance(file, (URL, SupportsGeturl)):
                    if isinstance(file, URL):
                        url = str(file)
                    else:
                        url = file.geturl()
                    headers = {"Accept-Encoding": "identity"}
                    if skipsize:
                        headers["Range"] = "bytes=%d-" % skipsize
                    if async_:
                        try:
                            from aiohttp import request as async_request
                        except ImportError:
                            async def request():
                                async with AsyncClient() as client:
                                    async with client.stream("GET", url, headers=headers) as resp:
                                        file = resp.aiter_bytes(65536)
                                        if skipsize and reporthook is not None:
                                            if is_range_request(resp):
                                                await ensure_async(reporthook)(skipsize)
                                            else:
                                                file = await bytes_async_iter_skip(file, skipsize, callback=reporthook)
                                        return await self._oss_multipart_upload(file, **kwargs)
                        else:
                            async def request():
                                async with async_request("GET", url, headers=headers) as resp:
                                    file = resp.content
                                    if skipsize and reporthook is not None:
                                        if is_range_request(resp):
                                            await ensure_async(reporthook)(skipsize)
                                        else:
                                            async for _ in bio_skip_async_iter(file, skipsize, callback=reporthook):
                                                pass
                                    return await self._oss_multipart_upload(file, **kwargs)
                        return (yield request)
                    else:
                        from urllib.request import urlopen, Request

                        with urlopen(Request(url, headers=headers)) as resp:
                            file = resp
                            if skipsize and reporthook is not None:
                                if is_range_request(resp):
                                    yield partial(reporthook, skipsize)
                                else:
                                    for _ in bio_skip_iter(file, skipsize, callback=reporthook):
                                        pass
                            return self._oss_multipart_upload(file, **kwargs)
                elif async_:
                    if skipsize:
                        file = yield bytes_async_iter_skip(file, skipsize, callback=reporthook)
                    else:
                        file = ensure_aiter(file)
                elif isinstance(file, AsyncIterable):
                    raise TypeError(f"async iterable {file!r} in non-async mode")
                elif skipsize:
                    file = bytes_iter_skip(file, skipsize, callback=reporthook)
                try:
                    kwargs = dict(
                        bucket=bucket, object=object, url=url, 
                        token=token, upload_id=upload_id, **request_kwargs, 
                    )
                    if async_:
                        async def request():
                            async for part in self._oss_multipart_upload_part_iter(
                                file, 
                                part_number_start=len(parts)+1, 
                                partsize=partsize, 
                                reporthook=reporthook, 
                                async_=True, 
                                **kwargs, 
                            ):
                                parts.append(part)
                        yield request
                    else:
                        for part in self._oss_multipart_upload_part_iter(
                            file, 
                            part_number_start=len(parts)+1, 
                            partsize=partsize, 
                            reporthook=reporthook, 
                            **kwargs, 
                        ):
                            parts.append(part)
                    return (yield self._oss_multipart_upload_complete(
                        callback=callback, 
                        parts=parts, 
                        async_=async_, # type: ignore
                        **kwargs, 
                    ))
                except BaseException as e:
                    raise MultipartUploadAbort({
                        "bucket": bucket, "object": object, "upload_id": upload_id, 
                        "callback": callback, "partsize": partsize, "filesize": filesize, 
                    }) from e
            finally:
                if close_reporthook is not None:
                    yield close_reporthook
        return run_gen_step(gen_step, async_=async_)

    @cached_property
    def user_id(self, /) -> int:
        cookie_uid = self.__dict__["cookies"].get("UID")
        if cookie_uid:
            return int(cookie_uid.split("_")[0])
        else:
            return 0

    @cached_property
    def user_key(self, /) -> str:
        return self.upload_key()["data"]["userkey"]

    @cached_property
    def upload_url(self, /) -> AttrDict:
        """获取用于上传的一些 http 接口，此接口具有一定幂等性，请求一次，然后把响应记下来即可
        GET https://uplb.115.com/3.0/getuploadinfo.php
        response:
            - endpoint: 此接口用于上传文件到阿里云 OSS 
            - gettokenurl: 上传前需要用此接口获取 token
        """
        api = "https://uplb.115.com/3.0/getuploadinfo.php"
        return AttrDict(self.request(url=api))

    def upload_endpoint_url(
        self, 
        /, 
        bucket: str, 
        object: str, 
    ) -> str:
        endpoint = self.upload_url["endpoint"]
        urlp = urlsplit(endpoint)
        return f"{urlp.scheme}://{bucket}.{urlp.netloc}/{object}"

    @overload
    def upload_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取和上传有关的各种服务信息
        GET https://proapi.115.com/app/uploadinfo
        """
        api = "https://proapi.115.com/app/uploadinfo"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    @staticmethod
    def upload_token(
        request: None | Callable = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    @staticmethod
    def upload_token(
        request: None | Callable = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    @staticmethod
    def upload_token(
        request: None | Callable = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取阿里云 OSS 的 token，用于上传
        GET https://uplb.115.com/3.0/gettoken.php
        """
        api = "https://uplb.115.com/3.0/gettoken.php"
        request_kwargs.setdefault("parse", parse_json)
        if request is None:
            return httpx_request(url=api, async_=async_, **request_kwargs)
        else:
            return request(url=api, **request_kwargs)

    @overload
    def upload_file_sample_init(
        self, 
        /, 
        filename: str, 
        pid: int = 0, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_file_sample_init(
        self, 
        /, 
        filename: str, 
        pid: int = 0, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_file_sample_init(
        self, 
        /, 
        filename: str, 
        pid: int = 0, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """网页端的上传接口的初始化，注意：不支持秒传
        POST https://uplb.115.com/3.0/sampleinitupload.php
        """
        api = "https://uplb.115.com/3.0/sampleinitupload.php"
        payload = {"filename": filename, "target": f"U_1_{pid}"}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def upload_file_sample(
        self, 
        /, 
        file: ( Buffer | SupportsRead[Buffer] | str | PathLike | 
                URL | SupportsGeturl | Iterable[Buffer] ), 
        filename: None | str = None, 
        filesize: int = -1, 
        pid: int = 0, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]] = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_file_sample(
        self, 
        /, 
        file: ( Buffer | SupportsRead[Buffer] | str | PathLike | 
                URL | SupportsGeturl | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        filename: None | str = None, 
        filesize: int = -1, 
        pid: int = 0, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]] = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_file_sample(
        self, 
        /, 
        file: ( Buffer | SupportsRead[Buffer] | str | PathLike | 
                URL | SupportsGeturl | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        filename: None | str = None, 
        filesize: int = -1, 
        pid: int = 0, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]] = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """网页端的上传接口，注意：不支持秒传，但也不需要文件大小和 sha1
        """
        def gen_step():
            nonlocal file, filename, filesize
            if hasattr(file, "getbuffer"):
                try:
                    file = getattr(file, "getbuffer")()
                except TypeError:
                    pass
            if isinstance(file, Buffer):
                if filesize < 0:
                    filesize = len(file)
            elif isinstance(file, SupportsRead):
                if not async_ and iscoroutinefunction(file.read):
                    raise TypeError(f"{file!r} with async read in non-async mode")
                if filesize < 0:
                    try:
                        filesize = fstat(getattr(file, "fileno")()).st_size
                    except Exception:
                        pass
                if not filename:
                    try:
                        filename = ospath.basename(fsdecode(getattr(file, "name")))
                    except Exception:
                        pass
            elif isinstance(file, (str, PathLike)):
                path = fsdecode(file)
                if not filename:
                    filename = ospath.basename(path)
                if async_:
                    try:
                        from aiofile import async_open
                    except ImportError:
                        file = yield partial(to_thread, open, path, "rb")
                    else:
                        async def request():
                            nonlocal filesize
                            async with async_open(path) as file:
                                if filesize < 0:
                                    filesize = fstat(file.file.fileno()).st_size
                                return self.upload_file_sample(
                                    file, 
                                    filename, 
                                    filesize, 
                                    pid=pid, 
                                    make_reporthook=make_reporthook, 
                                    async_=True, 
                                    **request_kwargs, 
                                )
                        return (yield request)
                else:
                    file = open(path, "rb")
                if filesize < 0:
                    filesize = fstat(file.fileno()).st_size
            elif isinstance(file, (URL, SupportsGeturl)):
                if isinstance(file, URL):
                    url = str(file)
                else:
                    url = file.geturl()
                if async_:
                    try:
                        from aiohttp import request as async_request
                    except ImportError:
                        async def request():
                            nonlocal file, filesize, filename
                            async with AsyncClient() as client:
                                async with client.stream("GET", url) as resp:
                                    if not filename:
                                        filename = get_filename(resp)
                                    size = filesize if filesize >= 0 else get_content_length(resp)
                                    if size is None or is_chunked(resp):
                                        file = await resp.aread()
                                        filesize = len(file)
                                    else:
                                        file = resp.aiter_bytes()
                                    return self.upload_file_sample(
                                        file, 
                                        filename, 
                                        filesize, 
                                        pid=pid, 
                                        make_reporthook=make_reporthook, 
                                        async_=True, 
                                        **request_kwargs, 
                                    )
                    else:
                        async def request():
                            nonlocal file, filesize, filename
                            async with async_request("GET", url) as resp:
                                if not filename:
                                    filename = get_filename(resp)
                                size = filesize if filesize >= 0 else get_content_length(resp)
                                if size is None or is_chunked(resp):
                                    file = await resp.read()
                                    filesize = len(file)
                                else:
                                    file = resp.content
                                return self.upload_file_sample(
                                    file, 
                                    filename, 
                                    filesize, 
                                    pid=pid, 
                                    make_reporthook=make_reporthook, 
                                    async_=True, 
                                    **request_kwargs, 
                                )
                    return (yield request)
                else:
                    from urllib.request import urlopen

                    with urlopen(url) as resp:
                        if not filename:
                            filename = get_filename(resp)
                        size = filesize if filesize >= 0 else get_content_length(resp)
                        if size is None or is_chunked(resp):
                            file = resp.read()
                            filesize = len(file)
                        else:
                            file = resp
                        return self.upload_file_sample(
                            file, 
                            filename, 
                            filesize, 
                            pid=pid, 
                            make_reporthook=make_reporthook, 
                            **request_kwargs, 
                        )
            elif async_:
                file = ensure_aiter(file)
            elif isinstance(file, AsyncIterable):
                raise TypeError(f"async iterable {file!r} in non-async mode")

            if callable(make_reporthook):
                if async_:
                    if isinstance(file, Buffer):
                        file = bytes_to_chunk_async_iter(file)
                    elif isinstance(file, SupportsRead):
                        file = bio_chunk_async_iter(file)
                    file = progress_bytes_async_iter(file, make_reporthook, None if filesize < 0 else filesize)
                else:
                    if isinstance(file, Buffer):
                        file = bytes_to_chunk_iter(file)
                    elif isinstance(file, SupportsRead):
                        file = bio_chunk_iter(file)
                    file = progress_bytes_iter(file, make_reporthook, None if filesize < 0 else filesize)

            if not filename:
                filename = str(uuid4())
            resp = yield partial(
                self.upload_file_sample_init, 
                filename, 
                pid=pid, 
                async_=async_, 
                **request_kwargs, 
            )
            api = resp["host"]
            data = {
                "name": filename, 
                "key": resp["object"], 
                "policy": resp["policy"], 
                "OSSAccessKeyId": resp["accessid"], 
                "success_action_status": "200", 
                "callback": resp["callback"], 
                "signature": resp["signature"], 
            }

            if async_:
                headers, request_kwargs["data"] = encode_multipart_data_async(data, {"file": file})
            else:
                headers, request_kwargs["data"] = encode_multipart_data(data, {"file": file})
            request_kwargs["headers"] = {**request_kwargs.get("headers", {}), **headers}
            return (yield partial(
                self.request, 
                url=api, 
                method="POST", 
                async_=async_, 
                **request_kwargs, 
            ))
        return run_gen_step(gen_step, async_=async_)

    @overload
    def upload_key(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_key(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_key(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取 user_key
        GET https://proapi.115.com/android/2.0/user/upload_key
        """
        api = "https://proapi.115.com/android/2.0/user/upload_key"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def upload_init(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_init(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_init(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """秒传接口，参数的构造较为复杂，所以请不要直接使用
        POST https://uplb.115.com/4.0/initupload.php
        """
        api = "https://uplb.115.com/4.0/initupload.php"
        return self.request(url=api, method="POST", async_=async_, **request_kwargs)

    @overload
    def _upload_file_init(
        self, 
        /, 
        filename: str, 
        filesize: int, 
        filesha1: str, 
        target: str, 
        sign_key: str, 
        sign_val: str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def _upload_file_init(
        self, 
        /, 
        filename: str, 
        filesize: int, 
        filesha1: str, 
        target: str, 
        sign_key: str, 
        sign_val: str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def _upload_file_init(
        self, 
        /, 
        filename: str, 
        filesize: int, 
        filesha1: str, 
        target: str = "U_1_0", 
        sign_key: str = "", 
        sign_val: str = "",
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """秒传接口，此接口是对 `upload_init` 的封装
        """
        def gen_sig() -> str:
            sig_sha1 = sha1()
            sig_sha1.update(bytes(userkey, "ascii"))
            sig_sha1.update(b2a_hex(sha1(bytes(f"{userid}{filesha1}{target}0", "ascii")).digest()))
            sig_sha1.update(b"000000")
            return sig_sha1.hexdigest().upper()
        def gen_token() -> str:
            token_md5 = md5(MD5_SALT)
            token_md5.update(bytes(f"{filesha1}{filesize}{sign_key}{sign_val}{userid}{t}", "ascii"))
            token_md5.update(b2a_hex(md5(bytes(userid, "ascii")).digest()))
            token_md5.update(bytes(APP_VERSION, "ascii"))
            return token_md5.hexdigest()
        userid = str(self.user_id)
        userkey = self.user_key
        t = int(time())
        sig = gen_sig()
        token = gen_token()
        encoded_token = ecdh_encode_token(t).decode("ascii")
        data = {
            "appid": 0, 
            "appversion": APP_VERSION, 
            #"behavior_type": 0, 
            "userid": userid, 
            "filename": filename, 
            "filesize": filesize, 
            "fileid": filesha1, 
            "target": target, 
            "sig": sig, 
            "t": t, 
            "token": token, 
        }
        if sign_key and sign_val:
            data["sign_key"] = sign_key
            data["sign_val"] = sign_val
        if (headers := request_kwargs.get("headers")):
            request_kwargs["headers"] = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
        else:
            request_kwargs["headers"] = {"Content-Type": "application/x-www-form-urlencoded"}
        request_kwargs["parse"] = lambda resp, content: loads(ecdh_aes_decode(content, decompress=True))
        request_kwargs["params"] = {"k_ec": encoded_token}
        request_kwargs["data"] = ecdh_aes_encode(urlencode(sorted(data.items())).encode("latin-1"))
        def gen_step():
            resp = yield partial(self.upload_init, async_=async_, **request_kwargs)
            if resp["status"] == 2 and resp["statuscode"] == 0:
                # NOTE: 再次调用一下上传接口，确保能在 life_list 接口中看到更新，目前猜测推送 upload_file 的事件信息，需要用 websocket，待破解
                request_kwargs["parse"] = lambda resp, content, /: None
                if async_:
                    create_task(to_thread(self.upload_init, **request_kwargs))
                else:
                    start_new_thread(partial(self.upload_init, **request_kwargs), ())
            return resp
        return run_gen_step(gen_step, async_=async_)

    @overload
    def upload_file_init(
        self, 
        /, 
        filename: str, 
        filesize: int, 
        filesha1: str, 
        read_range_bytes_or_hash: None | Callable[[str], str | Buffer] = None, 
        pid: int = 0, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_file_init(
        self, 
        /, 
        filename: str, 
        filesize: int, 
        filesha1: str, 
        read_range_bytes_or_hash: None | Callable[[str], str | Buffer] = None, 
        pid: int = 0, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_file_init(
        self, 
        /, 
        filename: str, 
        filesize: int, 
        filesha1: str, 
        read_range_bytes_or_hash: None | Callable[[str], str | Buffer] = None, 
        pid: int = 0, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """秒传接口，此接口是对 `upload_init` 的封装。
        NOTE: 
            - 文件大小 和 sha1 是必需的，只有 sha1 是没用的。
            - 如果文件大于等于 1 MB (1048576 B)，就需要 2 次检验一个范围哈希，就必须提供 `read_range_bytes_or_hash`
        """
        if filesize >= 1 << 20 and read_range_bytes_or_hash is None:
            raise ValueError("filesize >= 1 MB, thus need pass the `read_range_bytes_or_hash` argument")
        filesha1 = filesha1.upper()
        target = f"U_1_{pid}"
        def gen_step():
            resp = yield partial(
                self._upload_file_init, 
                filename, 
                filesize, 
                filesha1, 
                target, 
                async_=async_, 
                **request_kwargs, 
            )
            # NOTE: 当文件大于等于 1 MB (1048576 B)，需要 2 次检验 1 个范围哈希，它会给出此文件的 1 个范围区间
            #       ，你读取对应的数据计算 sha1 后上传，以供 2 次检验
            if resp["status"] == 7 and resp["statuscode"] == 701:
                if read_range_bytes_or_hash is None:
                    raise ValueError("filesize >= 1 MB, thus need pass the `read_range_bytes_or_hash` argument")
                sign_key = resp["sign_key"]
                sign_check = resp["sign_check"]
                data: str | Buffer
                if async_:
                    data = yield partial(
                        ensure_async(read_range_bytes_or_hash), 
                        sign_check, 
                    )
                else:
                    data = read_range_bytes_or_hash(sign_check)
                if isinstance(data, str):
                    sign_val = data.upper()
                else:
                    sign_val = sha1(data).hexdigest().upper()
                resp = yield partial(
                    self._upload_file_init, 
                    filename, 
                    filesize, 
                    filesha1, 
                    target, 
                    sign_key=sign_key, 
                    sign_val=sign_val, 
                    async_=async_, 
                    **request_kwargs, 
                )
            resp["state"] = True
            resp["data"] = {
                "file_name": filename, 
                "file_size": filesize, 
                "sha1": filesha1, 
                "cid": pid, 
                "pickcode": resp["pickcode"], 
            }
            return resp
        return run_gen_step(gen_step, async_=async_)

    # TODO: 支持进度条和随时暂停，基于迭代器，使用一个 flag，每次迭代检查一下
    # TODO: 返回 task，支持 pause（暂停此任务，连接不释放）、stop（停止此任务，连接释放）、cancel（取消此任务）、resume（恢复），此时需要增加参数 wait
    # TODO: class P115MultipartUploadTask:
    #           @classmethod
    #           def from_cache(cls, /, bucket, object, upload_id, callback, file): ...
    @overload
    def upload_file(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] ), 
        filename: None | str = None, 
        pid: int = 0, 
        filesize: int = -1, 
        filesha1: None | str = None, 
        partsize: int = 0, 
        upload_directly: None | bool = False, 
        multipart_resume_data: None | MultipartResumeData = None, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]] = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def upload_file(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        filename: None | str = None, 
        pid: int = 0, 
        filesize: int = -1, 
        filesha1: None | str = None, 
        partsize: int = 0, 
        upload_directly: None | bool = False, 
        multipart_resume_data: None | MultipartResumeData = None, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]] = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def upload_file(
        self, 
        /, 
        file: ( str | PathLike | URL | SupportsGeturl | 
                Buffer | SupportsRead[Buffer] | Iterable[Buffer] | AsyncIterable[Buffer] ), 
        filename: None | str = None, 
        pid: int = 0, 
        filesize: int = -1, 
        filesha1: None | str = None, 
        partsize: int = 0, 
        upload_directly: None | bool = False, 
        multipart_resume_data: None | MultipartResumeData = None, 
        make_reporthook: None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any] | AsyncGenerator[int, Any]] = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """文件上传接口，这是高层封装，推荐使用
        """
        if multipart_resume_data is not None:
            return self._oss_multipart_upload(
                file, 
                bucket=multipart_resume_data["bucket"], 
                object=multipart_resume_data["object"], 
                upload_id=multipart_resume_data["upload_id"], 
                callback=multipart_resume_data["callback"], 
                partsize=multipart_resume_data["partsize"], 
                filesize=multipart_resume_data.get("filesize", -1), 
                make_reporthook=make_reporthook, 
                async_=async_, 
                **request_kwargs, 
            )
        if upload_directly:
            return self.upload_file_sample(
                file, 
                filename, 
                filesize=filesize, 
                pid=pid, 
                make_reporthook=make_reporthook, 
                async_=async_, 
                **request_kwargs, 
            )
        if hasattr(file, "getbuffer"):
            try:
                file = getattr(file, "getbuffer")()
            except TypeError:
                pass
        if async_:
            async def async_request():
                nonlocal file, filename, filesize, filesha1

                async def do_upload(file):
                    resp = await self.upload_file_init(
                        cast(str, filename), 
                        filesize, 
                        cast(str, filesha1), 
                        read_range_bytes_or_hash, 
                        pid=pid, 
                        async_=True, 
                        **request_kwargs, 
                    )
                    status = resp["status"]
                    statuscode = resp.get("statuscode", 0)
                    if status == 2 and statuscode == 0:
                        return resp
                    elif status == 1 and statuscode == 0:
                        bucket, object, callback = resp["bucket"], resp["object"], resp["callback"]
                    else:
                        raise OSError(errno.EINVAL, resp)

                    if upload_directly is None:
                        return await self.upload_file_sample(
                            file, 
                            filename, 
                            pid=pid, 
                            filesize=filesize, 
                            make_reporthook=make_reporthook, 
                            async_=True, 
                            **request_kwargs, 
                        )
                    elif partsize <= 0:
                        return await self._oss_upload(
                            file, 
                            bucket, 
                            object, 
                            callback, 
                            filesize=filesize, 
                            make_reporthook=make_reporthook, 
                            async_=True, 
                            **request_kwargs, 
                        )
                    else:
                        return await self._oss_multipart_upload(
                            file, 
                            bucket, 
                            object, 
                            callback, 
                            partsize=partsize, 
                            filesize=filesize, 
                            make_reporthook=make_reporthook, 
                            async_=True, 
                            **request_kwargs, 
                        )

                read_range_bytes_or_hash = None
                if isinstance(file, Buffer):
                    if filesize < 0:
                        filesize = len(file)
                    if not filesha1:
                        filesha1 = sha1(file).hexdigest()
                    if filesize >= 1 << 20:
                        mmv = memoryview(file)
                        def read_range_bytes_or_hash(sign_check: str):
                            start, end = map(int, sign_check.split("-"))
                            return mmv[start : end + 1]
                elif isinstance(file, (str, PathLike)):
                    @asynccontextmanager
                    async def ctx_async_read(path, /, start=0):
                        try:
                            from aiofile import async_open
                        except ImportError:
                            with open(path, "rb") as file:
                                if start:
                                    file.seek(start)
                                yield file, as_thread(file.read)
                        else:
                            async with async_open(path, "rb") as file:
                                if start:
                                    await getattr(file, "seek")(start)
                                yield file, file.read
                    path = fsdecode(file)
                    if not filename:
                        filename = ospath.basename(path)
                    if filesize < 0:
                        filesize = stat(path).st_size
                    if filesize < 1 << 20:
                        async with ctx_async_read(path) as (_, read):
                            file = cast(bytes, await read())
                        if not filesha1:
                            filesha1 = sha1(file).hexdigest()
                    else:
                        if not filesha1:
                            async with ctx_async_read(path) as (file, _):
                                _, hashobj = await file_digest_async(file, "sha1")
                            filesha1 = hashobj.hexdigest()
                        async def read_range_bytes_or_hash(sign_check):
                            start, end = map(int, sign_check.split("-"))
                            async with ctx_async_read(path, start) as (_, read):
                                return await read(end - start + 1)
                        async with ctx_async_read(path) as (file, _):
                            return await do_upload(file)
                elif isinstance(file, SupportsRead):
                    try:
                        file_seek = ensure_async(getattr(file, "seek"))
                        curpos = await file_seek(0, 1)
                        seekable = True
                    except Exception:
                        curpos = 0
                        seekable = False
                    file_read = ensure_async(file.read)
                    if not filename:
                        try:
                            filename = ospath.basename(fsdecode(getattr(file, "name")))
                        except Exception:
                            filename = str(uuid4())
                    if filesize < 0:
                        try:
                            fileno = getattr(file, "fileno")()
                            filesize = fstat(fileno).st_size - curpos
                        except Exception:
                            try:
                                filesize = len(file) - curpos # type: ignore
                            except TypeError:
                                if seekable:
                                    try:
                                        filesize = (await file_seek(0, 2)) - curpos
                                    finally:
                                        await file_seek(curpos)
                                else:
                                    filesize = 0
                    if 0 < filesize <= 1 << 20:
                        file = await file_read()
                        if not filesha1:
                            filesha1 = sha1(file).hexdigest()
                    else:
                        if not filesha1:
                            if not seekable:
                                return await self.upload_file_sample(
                                    file, 
                                    filename, 
                                    pid=pid, 
                                    filesize=filesize, 
                                    make_reporthook=make_reporthook, 
                                    async_=True, 
                                    **request_kwargs, 
                                )
                            try:
                                _, hashobj = await file_digest_async(file, "sha1")
                                filesha1 = hashobj.hexdigest()
                            finally:
                                await file_seek(curpos)
                        async def read_range_bytes_or_hash(sign_check):
                            if not seekable:
                                raise TypeError(f"not a seekable reader: {file!r}")
                            start, end = map(int, sign_check.split("-"))
                            try:
                                await file_seek(start)
                                return await file_read(end - start + 1)
                            finally:
                                await file_seek(curpos)
                elif isinstance(file, (URL, SupportsGeturl)):
                    @asynccontextmanager
                    async def ctx_async_read(url, /, start=0):
                        if is_ranged and start:
                            headers = {"Range": "bytes=%s-" % start}
                        else:
                            headers = {}
                        try:
                            from aiohttp import request
                        except ImportError:
                            with (await to_thread(urlopen, url, headers=headers)) as resp:
                                if not headers:
                                    await async_through(bio_skip_async_iter(resp, start))
                                yield resp, as_thread(resp.read)
                        else:
                            async with request("GET", url, headers=headers) as resp:
                                if not headers:
                                    await async_through(bio_skip_async_iter(resp.content, start))
                                yield resp, resp.read
                    async def read_range_bytes_or_hash(sign_check):
                        start, end = map(int, sign_check.split("-"))
                        async with ctx_async_read(url, start) as (_, read):
                            return await read(end - start + 1)
                    if isinstance(file, URL):
                        url = str(file)
                    else:
                        url = file.geturl()
                    async with ctx_async_read(url) as (resp, read):
                        is_ranged = is_range_request(resp)
                        if not filename:
                            filename = get_filename(resp) or str(uuid4())
                        if filesize < 0:
                            filesize = get_total_length(resp) or 0
                        if filesize < 1 << 20:
                            file = cast(bytes, await read())
                            if not filesha1:
                                filesha1 = sha1(file).hexdigest()
                        else:
                            if not filesha1 or not is_ranged:
                                return await self.upload_file_sample(
                                    resp, 
                                    filename, 
                                    pid=pid, 
                                    filesize=filesize, 
                                    make_reporthook=make_reporthook, 
                                    async_=True, 
                                    **request_kwargs
                                )
                            return await do_upload(resp)
                elif filesha1:
                    if filesize < 0 or filesize >= 1 << 20:
                        filesize = 0
                else:
                    return await self.upload_file_sample(
                        file, 
                        filename, 
                        pid=pid, 
                        filesize=filesize, 
                        make_reporthook=make_reporthook, 
                        async_=True, 
                        **request_kwargs, 
                    )
                if not filename:
                    filename = str(uuid4())
                return await do_upload(file)
            return async_request()
        else:
            make_reporthook = cast(None | Callable[[None | int], Callable[[int], Any] | Generator[int, Any, Any]], make_reporthook)

            def do_upload(file):
                resp = self.upload_file_init(
                    cast(str, filename), 
                    filesize, 
                    cast(str, filesha1), 
                    read_range_bytes_or_hash, 
                    pid=pid, 
                    async_=False, 
                    **request_kwargs, 
                )
                status = resp["status"]
                statuscode = resp.get("statuscode", 0)
                if status == 2 and statuscode == 0:
                    return resp
                elif status == 1 and statuscode == 0:
                    bucket, object, callback = resp["bucket"], resp["object"], resp["callback"]
                else:
                    raise OSError(errno.EINVAL, resp)

                if upload_directly is None:
                    return self.upload_file_sample(
                        file, 
                        filename, 
                        pid=pid, 
                        filesize=filesize, 
                        make_reporthook=make_reporthook, 
                        async_=False, 
                        **request_kwargs, 
                    )
                elif partsize <= 0:
                    return self._oss_upload(
                        file, 
                        bucket, 
                        object, 
                        callback, 
                        filesize=filesize, 
                        make_reporthook=make_reporthook, 
                        async_=False, 
                        **request_kwargs, 
                    )
                else:
                    return self._oss_multipart_upload(
                        file, 
                        bucket, 
                        object, 
                        callback, 
                        partsize=partsize, 
                        filesize=filesize, 
                        make_reporthook=make_reporthook, 
                        async_=False, 
                        **request_kwargs, 
                    )

            read_range_bytes_or_hash: None | Callable = None
            if isinstance(file, Buffer):
                if filesize < 0:
                    filesize = len(file)
                if not filesha1:
                    filesha1 = sha1(file).hexdigest()
                if filesize >= 1 << 20:
                    mmv = memoryview(file)
                    def read_range_bytes_or_hash(sign_check: str):
                        start, end = map(int, sign_check.split("-"))
                        return mmv[start : end + 1]
            elif isinstance(file, (str, PathLike)):
                path = fsdecode(file)
                if not filename:
                    filename = ospath.basename(path)
                if filesize < 0:
                    filesize = stat(path).st_size
                if filesize < 1 << 20:
                    file = open(path, "rb", buffering=0).read()
                    if not filesha1:
                        filesha1 = sha1(file).hexdigest()
                else:
                    if not filesha1:
                        _, hashobj = file_digest(open(path, "rb"), "sha1")
                        filesha1 = hashobj.hexdigest()
                    def read_range_bytes_or_hash(sign_check: str):
                        start, end = map(int, sign_check.split("-"))
                        with open(path, "rb") as file:
                            file.seek(start)
                            return sha1(file.read(end - start + 1)).hexdigest()
                    file = open(path, "rb")
            elif isinstance(file, SupportsRead):
                file_read: Callable[..., bytes] = getattr(file, "read")
                file_seek = getattr(file, "seek", None)
                if file_seek is not None:
                    try:
                        curpos = file_seek(0, 1)
                        seekable = True
                    except Exception:
                        curpos = 0
                        seekable = False
                if not filename:
                    try:
                        filename = ospath.basename(fsdecode(getattr(file, "name")))
                    except Exception:
                        filename = str(uuid4())
                if filesize < 0:
                    try:
                        fileno = getattr(file, "fileno")()
                        filesize = fstat(fileno).st_size - curpos
                    except Exception:
                        try:
                            filesize = len(file) - curpos # type: ignore
                        except TypeError:
                            if seekable:
                                try:
                                    filesize = file_seek(0, 2) - curpos
                                finally:
                                    file_seek(curpos)
                            else:
                                filesize = 0
                if 0 < filesize < 1 << 20:
                    file = file_read()
                    if not filesha1:
                        filesha1 = sha1(file).hexdigest()
                else:
                    if not filesha1:
                        if not seekable:
                            return self.upload_file_sample(
                                file, 
                                filename, 
                                pid=pid, 
                                filesize=filesize, 
                                make_reporthook=make_reporthook, 
                                async_=False, 
                                **request_kwargs, 
                            )
                        try:
                            _, hashobj = file_digest(file, "sha1")
                            filesha1 = hashobj.hexdigest()
                        finally:
                            file_seek(curpos)
                    def read_range_bytes_or_hash(sign_check: str):
                        if not seekable:
                            raise TypeError(f"not a seekable reader: {file!r}")
                        start, end = map(int, sign_check.split("-"))
                        try:
                            file_seek(start)
                            return sha1(file_read(end - start + 1)).hexdigest()
                        finally:
                            file_seek(curpos)
            elif isinstance(file, (URL, SupportsGeturl)):
                def read_range_bytes_or_hash(sign_check: str):
                    start, end = map(int, sign_check.split("-"))
                    if is_ranged and start:
                        headers = {"Range": "bytes=%s-" % start}
                    else:
                        headers = {}
                    with urlopen(url, headers=headers) as resp:
                        if not headers:
                            through(bio_skip_iter(resp, start))
                        return resp.read(end - start + 1)
                if isinstance(file, URL):
                    url = str(file)
                else:
                    url = file.geturl()
                with urlopen(url) as resp:
                    is_ranged = is_range_request(resp)
                    if not filename:
                        filename = get_filename(resp) or str(uuid4())
                    if filesize < 0:
                        filesize = resp.length or 0
                    if 0 < filesize < 1 << 20:
                        file = resp.read()
                        if not filesha1:
                            filesha1 = sha1(file).hexdigest()
                    else:
                        if not filesha1 or not is_ranged:
                            return self.upload_file_sample(
                                resp, 
                                filename, 
                                pid=pid, 
                                filesize=filesize, 
                                make_reporthook=make_reporthook, 
                                async_=False, 
                                **request_kwargs, 
                            )
                        return do_upload(resp)
            elif filesha1:
                if filesize < 0 or filesize >= 1 << 20:
                    filesize = 0
            else:
                return self.upload_file_sample(
                    file, 
                    filename, 
                    pid=pid, 
                    filesize=filesize, 
                    make_reporthook=make_reporthook, 
                    async_=False, 
                    **request_kwargs, 
                )
            if not filename:
                filename = str(uuid4())
            return do_upload(file)

    ########## Decompress API ##########

    @overload
    def extract_push(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_push(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_push(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """推送一个解压缩任务给服务器，完成后，就可以查看压缩包的文件列表了
        POST https://webapi.115.com/files/push_extract
        payload:
            - pick_code: str
            - secret: str = "" # 解压密码
        """
        api = "https://webapi.115.com/files/push_extract"
        if isinstance(payload, str):
            payload = {"pick_code": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def extract_push_progress(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_push_progress(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_push_progress(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """查询解压缩任务的进度
        GET https://webapi.115.com/files/push_extract
        payload:
            - pick_code: str
        """
        api = "https://webapi.115.com/files/push_extract"
        if isinstance(payload, str):
            payload = {"pick_code": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def extract_info(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_info(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取压缩文件的文件列表，推荐直接用封装函数 `extract_list`
        GET https://webapi.115.com/files/extract_info
        payload:
            - pick_code: str
            - file_name: str = ""
            - next_marker: str = ""
            - page_count: int | str = 999 # NOTE: 介于 1-999
            - paths: str = "文件"
        """
        api = "https://webapi.115.com/files/extract_info"
        if isinstance(payload, str):
            payload = {"paths": "文件", "page_count": 999, "next_marker": "", "file_name": "", "pick_code": payload}
        else:
            payload = {"paths": "文件", "page_count": 999, "next_marker": "", "file_name": "", **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def extract_list(
        self, 
        /, 
        pickcode: str, 
        path: str, 
        next_marker: str, 
        page_count: int, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_list(
        self, 
        /, 
        pickcode: str, 
        path: str, 
        next_marker: str, 
        page_count: int, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_list(
        self, 
        /, 
        pickcode: str, 
        path: str = "", 
        next_marker: str = "", 
        page_count: int = 999, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取压缩文件的文件列表，此方法是对 `extract_info` 的封装，推荐使用
        """
        if not 1 <= page_count <= 999:
            page_count = 999
        payload = {
            "pick_code": pickcode, 
            "file_name": path.strip("/"), 
            "paths": "文件", 
            "next_marker": next_marker, 
            "page_count": page_count, 
        }
        return self.extract_info(payload, async_=async_, **request_kwargs)

    @overload
    def extract_add_file(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_add_file(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_add_file(
        self, 
        payload: list | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """解压缩到某个文件夹，推荐直接用封装函数 `extract_file`
        POST https://webapi.115.com/files/add_extract_file
        payload:
            - pick_code: str
            - extract_file[]: str
            - extract_file[]: str
            - ...
            - to_pid: int | str = 0
            - paths: str = "文件"
        """
        api = "https://webapi.115.com/files/add_extract_file"
        if (headers := request_kwargs.get("headers")):
            headers = request_kwargs["headers"] = dict(headers)
        else:
            headers = request_kwargs["headers"] = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        return self.request(
            api, 
            "POST", 
            data=urlencode(payload), 
            async_=async_, 
            **request_kwargs, 
        )

    @overload
    def extract_progress(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_progress(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_progress(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取 解压缩到文件夹 任务的进度
        GET https://webapi.115.com/files/add_extract_file
        payload:
            - extract_id: str
        """
        api = "https://webapi.115.com/files/add_extract_file"
        if isinstance(payload, (int, str)):
            payload = {"extract_id": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def extract_file(
        self, 
        /, 
        pickcode: str, 
        paths: str | Sequence[str], 
        dirname: str, 
        to_pid: int | str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_file(
        self, 
        /, 
        pickcode: str, 
        paths: str | Sequence[str], 
        dirname: str, 
        to_pid: int | str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_file(
        self, 
        /, 
        pickcode: str, 
        paths: str | Sequence[str] = "", 
        dirname: str = "", 
        to_pid: int | str = 0,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """解压缩到某个文件夹，是对 `extract_add_file` 的封装，推荐使用
        """
        dirname = dirname.strip("/")
        dir2 = f"文件/{dirname}" if dirname else "文件"
        data = [
            ("pick_code", pickcode), 
            ("paths", dir2), 
            ("to_pid", to_pid), 
        ]
        if async_:
            async def async_request():
                nonlocal async_, paths
                async_ = cast(Literal[True], async_)
                if not paths:
                    resp = await self.extract_list(pickcode, dirname, async_=async_, **request_kwargs)
                    if not resp["state"]:
                        return resp
                    paths = [
                        p["file_name"] if p["file_category"] else p["file_name"]+"/" 
                        for p in resp["data"]["list"]
                    ]
                    while (next_marker := resp["data"].get("next_marker")):
                        resp = await self.extract_list(
                            pickcode, dirname, next_marker, async_=async_, **request_kwargs)
                        paths.extend(
                            p["file_name"] if p["file_category"] else p["file_name"]+"/" 
                            for p in resp["data"]["list"]
                        )
                if isinstance(paths, str):
                    data.append(
                        ("extract_dir[]" if paths.endswith("/") else "extract_file[]", paths.strip("/"))
                    )
                else:
                    data.extend(
                        ("extract_dir[]" if path.endswith("/") else "extract_file[]", path.strip("/")) 
                        for path in paths
                    )
                return await self.extract_add_file(data, async_=async_, **request_kwargs)
            return async_request()
        else:
            if not paths:
                resp = self.extract_list(pickcode, dirname, async_=async_, **request_kwargs)
                if not resp["state"]:
                    return resp
                paths = [
                    p["file_name"] if p["file_category"] else p["file_name"]+"/" 
                    for p in resp["data"]["list"]
                ]
                while (next_marker := resp["data"].get("next_marker")):
                    resp = self.extract_list(
                        pickcode, dirname, next_marker, async_=async_, **request_kwargs)
                    paths.extend(
                        p["file_name"] if p["file_category"] else p["file_name"]+"/" 
                        for p in resp["data"]["list"]
                    )
            if isinstance(paths, str):
                data.append(
                    ("extract_dir[]" if paths.endswith("/") else "extract_file[]", paths.strip("/"))
                )
            else:
                data.extend(
                    ("extract_dir[]" if path.endswith("/") else "extract_file[]", path.strip("/")) 
                    for path in paths
                )
            return self.extract_add_file(data, async_=async_, **request_kwargs)

    @overload
    def extract_download_url(
        self, 
        /, 
        pickcode: str, 
        path: str, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> P115Url:
        ...
    @overload
    def extract_download_url(
        self, 
        /, 
        pickcode: str, 
        path: str, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, P115Url]:
        ...
    def extract_download_url(
        self, 
        /, 
        pickcode: str, 
        path: str, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> P115Url | Coroutine[Any, Any, P115Url]:
        """获取压缩包中文件的下载链接
        GET https://webapi.115.com/files/extract_down_file
        payload:
            - pick_code: str
            - full_name: str
        """
        path = path.rstrip("/")
        resp = self.extract_download_url_web(
            {"pick_code": pickcode, "full_name": path.lstrip("/")}, 
            async_=async_, 
            **request_kwargs, 
        )
        def get_url(resp: dict) -> P115Url:
            data = check_response(resp)["data"]
            url = quote(data["url"], safe=":/?&=%#")
            return P115Url(
                url, 
                file_path=path, 
                file_name=posixpath.basename(path), 
                headers=resp["headers"], 
            )
        if async_:
            async def async_request() -> P115Url:
                return get_url(await cast(Coroutine[Any, Any, dict], resp))
            return async_request()
        else:
            return get_url(cast(dict, resp))

    @overload
    def extract_download_url_web(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def extract_download_url_web(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def extract_download_url_web(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取压缩包中文件的下载链接
        GET https://webapi.115.com/files/extract_down_file
        payload:
            - pick_code: str
            - full_name: str
        """
        api = "https://webapi.115.com/files/extract_down_file"
        request_headers = request_kwargs.get("headers")
        headers = request_kwargs.get("headers")
        if headers:
            if isinstance(headers, Mapping):
                headers = ItemsView(headers)
            headers = request_kwargs["headers"] = {
                "User-Agent": next((v for k, v in headers if k.lower() == "user-agent" and v), "")}
        else:
            headers = request_kwargs["headers"] = {"User-Agent": ""}
        def parse(resp, content: bytes):
            json = loads(content)
            if "Set-Cookie" in resp.headers:
                if isinstance(resp.headers, Mapping):
                    match = CRE_SET_COOKIE.search(resp.headers["Set-Cookie"])
                    if match is not None:
                        headers["Cookie"] = match[0]
                else:
                    for k, v in reversed(resp.headers.items()):
                        if k == "Set-Cookie" and CRE_SET_COOKIE.match(v) is not None:
                            headers["Cookie"] = v
                            break
            json["headers"] = headers
            return json
        request_kwargs["parse"] = parse
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    # TODO 支持异步
    @overload
    def extract_push_future(
        self, 
        /, 
        pickcode: str, 
        secret: str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> None | PushExtractProgress:
        ...
    @overload
    def extract_push_future(
        self, 
        /, 
        pickcode: str, 
        secret: str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, None | PushExtractProgress]:
        ...
    def extract_push_future(
        self, 
        /, 
        pickcode: str, 
        secret: str = "",
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> None | PushExtractProgress | Coroutine[Any, Any, None | PushExtractProgress]:
        """执行在线解压，如果早就已经完成，返回 None，否则新开启一个线程，用于检查进度
        """
        if async_:
            raise NotImplementedError("asynchronous mode not implemented")
        resp = check_response(self.extract_push(
            {"pick_code": pickcode, "secret": secret}, 
            **request_kwargs, 
        ))
        if resp["data"]["unzip_status"] == 4:
            return None
        return PushExtractProgress(self, pickcode)

    # TODO 支持异步
    @overload
    def extract_file_future(
        self, 
        /, 
        pickcode: str, 
        paths: str | Sequence[str], 
        dirname: str, 
        to_pid: int | str,
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> ExtractProgress:
        ...
    @overload
    def extract_file_future(
        self, 
        /, 
        pickcode: str, 
        paths: str | Sequence[str], 
        dirname: str, 
        to_pid: int | str,
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, ExtractProgress]:
        ...
    def extract_file_future(
        self, 
        /, 
        pickcode: str, 
        paths: str | Sequence[str] = "", 
        dirname: str = "", 
        to_pid: int | str = 0,
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> ExtractProgress | Coroutine[Any, Any, ExtractProgress]:
        """执行在线解压到目录，新开启一个线程，用于检查进度
        """
        if async_:
            raise NotImplementedError("asynchronous mode not implemented")
        resp = check_response(self.extract_file(
            pickcode, paths, dirname, to_pid, **request_kwargs
        ))
        return ExtractProgress(self, resp["data"]["extract_id"])

    ########## Offline Download API ##########

    @overload
    def offline_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取关于离线的限制的信息
        GET https://115.com/?ct=offline&ac=space
        """
        api = "https://115.com/?ct=offline&ac=space"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def offline_quota_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_quota_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_quota_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取当前离线配额信息（简略）
        GET https://lixian.115.com/lixian/?ct=lixian&ac=get_quota_info
        """
        api = "https://lixian.115.com/lixian/?ct=lixian&ac=get_quota_info"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def offline_quota_package_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_quota_package_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_quota_package_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取当前离线配额信息（详细）
        GET https://lixian.115.com/lixian/?ct=lixian&ac=get_quota_package_info
        """
        api = "https://lixian.115.com/lixian/?ct=lixian&ac=get_quota_package_info"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def offline_download_path(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_download_path(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_download_path(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取当前默认的离线下载到的文件夹信息（可能有多个）
        GET https://webapi.115.com/offine/downpath
        """
        api = "https://webapi.115.com/offine/downpath"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def offline_upload_torrent_path(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_upload_torrent_path(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_upload_torrent_path(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取当前的种子上传到的文件夹，当你添加种子任务后，这个种子会在此文件夹中保存
        GET https://115.com/?ct=lixian&ac=get_id&torrent=1
        """
        api = "https://115.com/?ct=lixian&ac=get_id&torrent=1"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def offline_add_url(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_add_url(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_add_url(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """添加一个离线任务
        POST https://115.com/web/lixian/?ct=lixian&ac=add_task_url
        payload:
            - url: str
            - sign: str = <default>
            - time: int = <default>
            - savepath: str = <default>
            - wp_path_id: int | str = <default>
        """
        api = "https://115.com/web/lixian/?ct=lixian&ac=add_task_url"
        if isinstance(payload, str):
            payload = {"url": payload}
        if "sign" not in payload:
            info = self.offline_info()
            payload["sign"] = info["sign"]
            payload["time"] = info["time"]
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def offline_add_urls(
        self, 
        payload: Iterable[str] | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_add_urls(
        self, 
        payload: Iterable[str] | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_add_urls(
        self, 
        payload: Iterable[str] | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """添加一组离线任务
        POST https://115.com/web/lixian/?ct=lixian&ac=add_task_urls
        payload:
            - url[0]: str
            - url[1]: str
            - ...
            - sign: str = <default>
            - time: int = <default>
            - savepath: str = <default>
            - wp_path_id: int | str = <default>
        """
        api = "https://115.com/web/lixian/?ct=lixian&ac=add_task_urls"
        if not isinstance(payload, dict):
            payload = {f"url[{i}]": url for i, url in enumerate(payload)}
            if not payload:
                raise ValueError("no `url` specified")
        if "sign" not in payload:
            info = self.offline_info()
            payload["sign"] = info["sign"]
            payload["time"] = info["time"]
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def offline_add_torrent(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_add_torrent(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_add_torrent(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """添加一个种子作为离线任务
        POST https://115.com/web/lixian/?ct=lixian&ac=add_task_bt
        payload:
            - info_hash: str
            - wanted: str
            - sign: str = <default>
            - time: int = <default>
            - savepath: str = <default>
            - wp_path_id: int | str = <default>
        """
        api = "https://115.com/web/lixian/?ct=lixian&ac=add_task_bt"
        if "sign" not in payload:
            info = self.offline_info()
            payload["sign"] = info["sign"]
            payload["time"] = info["time"]
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def offline_torrent_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_torrent_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_torrent_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """查看种子的文件列表等信息
        POST https://lixian.115.com/lixian/?ct=lixian&ac=torrent
        payload:
            - sha1: str
        """
        api = "https://lixian.115.com/lixian/?ct=lixian&ac=torrent"
        if isinstance(payload, str):
            payload = {"sha1": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def offline_remove(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_remove(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_remove(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除一组离线任务（无论是否已经完成）
        POST https://lixian.115.com/lixian/?ct=lixian&ac=task_del
        payload:
            - hash[0]: str
            - hash[1]: str
            - ...
            - sign: str = <default>
            - time: int = <default>
            - flag: 0 | 1 = <default> # 是否删除源文件
        """
        api = "https://lixian.115.com/lixian/?ct=lixian&ac=task_del"
        if isinstance(payload, str):
            payload = {"hash[0]": payload}
        if "sign" not in payload:
            info = self.offline_info()
            payload["sign"] = info["sign"]
            payload["time"] = info["time"]
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def offline_list(
        self, 
        payload: int | dict = 1, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_list(
        self, 
        payload: int | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_list(
        self, 
        payload: int | dict = 1, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取当前的离线任务列表
        POST https://lixian.115.com/lixian/?ct=lixian&ac=task_lists
        payload:
            - page: int | str
        """
        api = "https://lixian.115.com/lixian/?ct=lixian&ac=task_lists"
        if isinstance(payload, int):
            payload = {"page": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def offline_clear(
        self, 
        payload: int | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def offline_clear(
        self, 
        payload: int | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def offline_clear(
        self, 
        payload: int | dict = {"flag": 0}, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """清空离线任务列表
        POST https://115.com/web/lixian/?ct=lixian&ac=task_clear
        payload:
            flag: int = 0
                - 0: 已完成
                - 1: 全部
                - 2: 已失败
                - 3: 进行中
                - 4: 已完成+删除源文件
                - 5: 全部+删除源文件
        """
        api = "https://115.com/web/lixian/?ct=lixian&ac=task_clear"
        if isinstance(payload, int):
            flag = payload
            if flag < 0:
                flag = 0
            elif flag > 5:
                flag = 5
            payload = {"flag": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    ########## Recyclebin API ##########

    @overload
    def recyclebin_info(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def recyclebin_info(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def recyclebin_info(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """回收站：文件信息
        POST https://webapi.115.com/rb/rb_info
        payload:
            - rid: int | str
        """
        api = "https://webapi.115.com/rb/rb_info"
        if isinstance(payload, (int, str)):
            payload = {"rid": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def recyclebin_clean(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def recyclebin_clean(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def recyclebin_clean(
        self, 
        payload: int | str | Iterable[int | str] | dict = {}, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """回收站：删除或清空
        POST https://webapi.115.com/rb/clean
        payload:
            - rid[0]: int | str # NOTE: 如果没有 rid，就是清空回收站
            - rid[1]: int | str
            - ...
            - password: int | str = <default>
        """
        api = "https://webapi.115.com/rb/clean"
        if isinstance(payload, (int, str)):
            payload = {"rid[0]": payload}
        elif not isinstance(payload, dict):
            payload = {f"rid[{i}]": rid for i, rid in enumerate(payload)}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def recyclebin_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def recyclebin_list(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def recyclebin_list(
        self, 
        payload: dict = {"limit": 32, "offset": 0}, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """回收站：罗列
        GET https://webapi.115.com/rb
        payload:
            - aid: int | str = 7
            - cid: int | str = 0
            - limit: int = 32
            - offset: int = 0
            - format: str = "json"
            - source: str = <default>
        """ 
        api = "https://webapi.115.com/rb"
        payload = {"aid": 7, "cid": 0, "limit": 32, "offset": 0, "format": "json", **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def recyclebin_revert(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def recyclebin_revert(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def recyclebin_revert(
        self, 
        payload: int | str | Iterable[int | str] | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """回收站：还原
        POST https://webapi.115.com/rb/revert
        payload:
            - rid[0]: int | str
            - rid[1]: int | str
            - ...
        """
        api = "https://webapi.115.com/rb/revert"
        if isinstance(payload, (int, str)):
            payload = {"rid[0]": payload}
        elif not isinstance(payload, dict):
            payload = {f"rid[{i}]": rid for i, rid in enumerate(payload)}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    ########## Captcha System API ##########

    @overload
    def captcha_sign(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def captcha_sign(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def captcha_sign(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取验证码的签名字符串
        GET https://captchaapi.115.com/?ac=code&t=sign
        """
        api = "https://captchaapi.115.com/?ac=code&t=sign"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def captcha_code(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    def captcha_code(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    def captcha_code(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """更新验证码，并获取图片数据（含 4 个汉字）
        GET https://captchaapi.115.com/?ct=index&ac=code
        """
        api = "https://captchaapi.115.com/?ct=index&ac=code"
        request_kwargs["parse"] = False
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def captcha_all(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    def captcha_all(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    def captcha_all(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """返回一张包含 10 个汉字的图片，包含验证码中 4 个汉字（有相应的编号，从 0 到 9，计数按照从左到右，从上到下的顺序）
        GET https://captchaapi.115.com/?ct=index&ac=code&t=all
        """
        api = "https://captchaapi.115.com/?ct=index&ac=code&t=all"
        request_kwargs["parse"] = False
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def captcha_single(
        self, 
        id: int, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    def captcha_single(
        self, 
        id: int, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    def captcha_single(
        self, 
        id: int, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """10 个汉字单独的图片，包含验证码中 4 个汉字，编号从 0 到 9
        GET https://captchaapi.115.com/?ct=index&ac=code&t=single&id={id}
        """
        if not 0 <= id <= 9:
            raise ValueError(f"expected integer between 0 and 9, got {id}")
        api = f"https://captchaapi.115.com/?ct=index&ac=code&t=single&id={id}"
        request_kwargs["parse"] = False
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def captcha_verify(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def captcha_verify(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def captcha_verify(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """提交验证码
        POST https://webapi.115.com/user/captcha
        payload:
            - code: int | str # 从 0 到 9 中选取 4 个数字的一种排列
            - sign: str = <default>
            - ac: str = "security_code" # 默认就行，不要自行决定
            - type: str = "web"         # 默认就行，不要自行决定
            - ctype: str = "web"        # 需要和 type 相同
            - client: str = "web"       # 需要和 type 相同
        """
        if isinstance(payload, (int, str)):
            payload = {"code": payload, "ac": "security_code", "type": "web", "ctype": "web", "client": "web"}
        else:
            payload = {"ac": "security_code", "type": "web", "ctype": "web", "client": "web", **payload}
        if "sign" not in payload:
            payload["sign"] = self.captcha_sign()["sign"]
        api = "https://webapi.115.com/user/captcha"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    ########## Message API ##########

    @overload
    def msg_get_websocket_host(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def msg_get_websocket_host(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def msg_get_websocket_host(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取 websocket 链接
        GET https://msg.115.com/?ct=im&ac=get_websocket_host
        """
        api = "https://msg.115.com/?ct=im&ac=get_websocket_host"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def msg_contacts_notice(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def msg_contacts_notice(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def msg_contacts_notice(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取提示消息
        GET https://msg.115.com/?ct=contacts&ac=notice&client=web
        """
        api = "https://msg.115.com/?ct=contacts&ac=notice&client=web"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def msg_contacts_ls(
        self, 
        payload: dict = {}, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def msg_contacts_ls(
        self, 
        payload: dict = {}, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def msg_contacts_ls(
        self, 
        payload: dict = {}, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取提示消息
        GET https://pmsg.115.com/api/1.0/app/1.0/contact/ls
        payload:
            limit: int = 115
            skip: int = 0
            t: 0 | 1 = 1
        """
        api = "https://pmsg.115.com/api/1.0/app/1.0/contact/ls"
        payload = {"limit": 115, "skip": 0, "t": 1, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    ########## Tools API ##########

    @overload
    def tool_space(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def tool_space(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def tool_space(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """检验空间
        GET https://115.com/?ct=tool&ac=space

        1、校验空间需全局进行扫描，请谨慎操作;
        2、扫描出无父目录的文件将统一放入到"/修复文件"的文件夹中;
        3、"/修复文件"的文件夹若超过存放文件数量限制，将创建多个文件夹存放，避免无法操作。
        4、此接口一天只能使用一次
        """
        api = "https://115.com/?ct=tool&ac=space"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def tool_clear_empty_folder(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def tool_clear_empty_folder(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def tool_clear_empty_folder(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除空文件夹
        GET https://115.com/?ct=tool&ac=clear_empty_folder
        """
        api = "https://115.com/?ct=tool&ac=clear_empty_folder"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def tool_repeat(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def tool_repeat(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def tool_repeat(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """开始一键排重任务
        POST https://aps.115.com/repeat/repeat.php
        payload:
            - folder_id: int | str # 目录 id
        """
        api = "https://aps.115.com/repeat/repeat.php"
        if isinstance(payload, (int, str)):
            payload = {"folder_id": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def tool_repeat_status(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def tool_repeat_status(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def tool_repeat_status(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """查询一键排重任务进度和统计信息（status 为 False 表示进行中，为 True 表示完成）
        GET https://aps.115.com/repeat/repeat_status.php
        """
        api = "https://aps.115.com/repeat/repeat_status.php"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def tool_repeat_list(
        self, 
        payload: dict = {"s": 0, "l": 100}, 
        /, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def tool_repeat_list(
        self, 
        payload: dict = {"s": 0, "l": 100}, 
        /, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def tool_repeat_list(
        self, 
        payload: dict = {"s": 0, "l": 100}, 
        /, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取重复文件列表
        GET https://aps.115.com/repeat/repeat_list.php
        payload:
            - s: int = 0 # offset，从 0 开始
            - l: int = 0 # limit
        """
        api = "https://aps.115.com/repeat/repeat_list.php"
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def tool_repeat_delete(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def tool_repeat_delete(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def tool_repeat_delete(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除重复文件
        POST https://aps.115.com/repeat/repeat_delete.php
        payload:
            # 这 3 个参数用于批量删除
            - filter_field: "parents" | "file_name" | "" | "" = <default>
                # 保留条件
                # - "file_name": 文件名（按长度）
                # - "parents": 所在文件夹路径（按长度）
                # - "user_utime": 操作时间
                # - "user_ptime": 创建时间
            - filter_order: "asc" | "desc" = <default>
                # 排序
                # - "asc": 升序，从小到大，取最小
                # - "desc": 降序，从大到小，取最大
            - batch: 0 | 1 = <default>
            # 这 1 个参数用于手动指定删除对象
            - sha1s[{sha1}]: int | str = <default> # 文件 id，多个用逗号 "," 隔开
        """
        api = "https://aps.115.com/repeat/repeat_delete.php"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def tool_repeat_delete_status(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def tool_repeat_delete_status(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def tool_repeat_delete_status(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除重复文件进度和统计信息（status 为 False 表示进行中，为 True 表示完成）
        GET https://aps.115.com/repeat/delete_status.php
        """
        api = "https://aps.115.com/repeat/delete_status.php"
        return self.request(url=api, async_=async_, **request_kwargs)

    ########## Activities API ##########

    @overload
    def act_xys_get_act_info(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_get_act_info(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_get_act_info(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取许愿树活动的信息
        GET https://act.115.com/api/1.0/web/1.0/act2024xys/get_act_info
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/get_act_info"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def act_xys_home_list(
        self, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_home_list(
        self, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_home_list(
        self, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """首页的许愿树（随机刷新 15 条）
        GET https://act.115.com/api/1.0/web/1.0/act2024xys/home_list
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/home_list"
        return self.request(url=api, async_=async_, **request_kwargs)

    @overload
    def act_xys_my_desire(
        self, 
        payload: int | dict = 0, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_my_desire(
        self, 
        payload: int | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_my_desire(
        self, 
        payload: int | dict = 0, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """我的许愿列表
        GET https://act.115.com/api/1.0/web/1.0/act2024xys/my_desire
        payload:
            - type: 0 | 1 | 2 = 0
                # 类型
                # - 0: 全部
                # - 1: 进行中
                # - 2: 已实现
            - start: int = 0  # 开始索引
            - page: int = 1   # 第几页
            - limit: int = 10 # 每页大小
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/my_desire"
        if isinstance(payload, int):
            payload = {"start": 0, "page": 1, "limit": 10, "type": payload}
        else:
            payload = {"type": 0, "start": 0, "page": 1, "limit": 10, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_my_aid_desire(
        self, 
        payload: int | dict = 0, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_my_aid_desire(
        self, 
        payload: int | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_my_aid_desire(
        self, 
        payload: int | dict = 0, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """我的助愿列表
        GET https://act.115.com/api/1.0/web/1.0/act2024xys/my_aid_desire
        payload:
            - type: 0 | 1 | 2 = 0
                # 类型
                # - 0: 全部
                # - 1: 进行中
                # - 2: 已实现
            - start: int = 0  # 开始索引
            - page: int = 1   # 第几页
            - limit: int = 10 # 每页大小
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/my_aid_desire"
        if isinstance(payload, int):
            payload = {"start": 0, "page": 1, "limit": 10, "type": payload}
        else:
            payload = {"type": 0, "start": 0, "page": 1, "limit": 10, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_wish(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_wish(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_wish(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """创建许愿
        POST https://act.115.com/api/1.0/web/1.0/act2024xys/wish
        payload:
            - content: str # 许愿文本，不少于 5 个字，不超过 500 个字
            - rewardSpace: int = 5 # 奖励容量，单位是 GB
            - images: int | str = <default> # 图片文件在你的网盘的 id，多个用逗号 "," 隔开
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/wish"
        if isinstance(payload, str):
            payload = {"rewardSpace": 5, "content": payload}
        else:
            payload = {"rewardSpace": 5, **payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_wish_del(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_wish_del(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_wish_del(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除许愿
        POST https://act.115.com/api/1.0/web/1.0/act2024xys/del_wish
        payload:
            - ids: str # 许愿的 id，多个用逗号 "," 隔开
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/del_wish"
        if isinstance(payload, str):
            payload = {"ids": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_aid_desire(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_aid_desire(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_aid_desire(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """创建助愿（如果提供 file_ids，则会创建一个分享链接）
        POST https://act.115.com/api/1.0/web/1.0/act2024xys/aid_desire
        payload:
            - id: str # 许愿 id
            - content: str # 助愿文本，不少于 5 个字，不超过 500 个字
            - images: int | str = <default> # 图片文件在你的网盘的 id，多个用逗号 "," 隔开
            - file_ids: int | str = <default> # 文件在你的网盘的 id，多个用逗号 "," 隔开
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/aid_desire"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_aid_desire_del(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_aid_desire_del(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_aid_desire_del(
        self, 
        payload: int | str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """删除助愿
        POST https://act.115.com/api/1.0/web/1.0/act2024xys/del_aid_desire
        payload:
            - ids: int | str # 助愿的 id，多个用逗号 "," 隔开
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/del_aid_desire"
        if isinstance(payload, (int, str)):
            payload = {"ids": payload}
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_get_desire_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_get_desire_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_get_desire_info(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取的许愿信息
        GET https://act.115.com/api/1.0/web/1.0/act2024xys/get_desire_info
        payload:
            - id: str # 许愿的 id
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/get_desire_info"
        if isinstance(payload, str):
            payload = {"id": payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_desire_aid_list(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_desire_aid_list(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_desire_aid_list(
        self, 
        payload: str | dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """获取许愿的助愿列表
        GET https://act.115.com/api/1.0/web/1.0/act2024xys/desire_aid_list
        payload:
            - id: str         # 许愿的 id
            - start: int = 0  # 开始索引
            - page: int = 1   # 第几页
            - limit: int = 10 # 每页大小
            - sort: int | str = <default>
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/desire_aid_list"
        if isinstance(payload, str):
            payload = {"start": 0, "page": 1, "limit": 10, "id": payload}
        else:
            payload = {"start": 0, "page": 1, "limit": 10, **payload}
        return self.request(url=api, params=payload, async_=async_, **request_kwargs)

    @overload
    def act_xys_adopt(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> dict:
        ...
    @overload
    def act_xys_adopt(
        self, 
        payload: dict, 
        /, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, dict]:
        ...
    def act_xys_adopt(
        self, 
        payload: dict, 
        /, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> dict | Coroutine[Any, Any, dict]:
        """采纳助愿
        POST https://act.115.com/api/1.0/web/1.0/act2024xys/adopt
        payload:
            - did: str # 许愿的 id
            - aid: int | str # 助愿的 id
            - to_cid: int = <default> # 助愿中的分享链接转存到你的网盘中目录的 id
        """
        api = "https://act.115.com/api/1.0/web/1.0/act2024xys/adopt"
        return self.request(url=api, method="POST", data=payload, async_=async_, **request_kwargs)

    ########## Other Encapsulations ##########

    # TODO 支持异步
    def open(
        self, 
        /, 
        url: str | Callable[[], str], 
        start: int = 0, 
        seek_threshold: int = 1 << 20, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False, True] = False, 
    ) -> HTTPFileReader:
        """打开下载链接，可以从网盘、网盘上的压缩包内、分享链接中获取：
            - P115Client.download_url
            - P115Client.share_download_url
            - P115Client.extract_download_url
        """
        if async_:
            raise NotImplementedError("asynchronous mode not implemented")
        if headers is None:
            headers = self.headers
        else:
            headers = {**self.headers, **headers}
        return HTTPFileReader(
            url, 
            headers=headers, 
            start=start, 
            seek_threshold=seek_threshold, 
        )

    # TODO: 返回一个 HTTPFileWriter，随时可以写入一些数据，close 代表上传完成，这个对象会持有一些信息
    def open_upload(self): ...

    @overload
    def ed2k(
        self, 
        /, 
        url: str | Callable[[], str], 
        headers: None | Mapping = None, 
        name: str = "", 
        *, 
        async_: Literal[False] = False, 
    ) -> str:
        ...
    @overload
    def ed2k(
        self, 
        /, 
        url: str | Callable[[], str], 
        headers: None | Mapping = None, 
        name: str = "", 
        *, 
        async_: Literal[True], 
    ) -> Coroutine[Any, Any, str]:
        ...
    def ed2k(
        self, 
        /, 
        url: str | Callable[[], str], 
        headers: None | Mapping = None, 
        name: str = "", 
        *, 
        async_: Literal[False, True] = False, 
    ) -> str | Coroutine[Any, Any, str]:
        trantab = dict(zip(b"/|", ("%2F", "%7C")))
        if async_:
            async def request():
                async with self.open(url, headers=headers, async_=True) as file: # type: ignore
                    length, ed2k = await ed2k_hash_async(file)
                return f"ed2k://|file|{(name or file.name).translate(trantab)}|{length}|{ed2k}|/"
            return request()
        else:
            with self.open(url, headers=headers) as file:
                length, ed2k = ed2k_hash(file)
            return f"ed2k://|file|{(name or file.name).translate(trantab)}|{length}|{ed2k}|/"

    @overload
    def hash(
        self, 
        /, 
        url: str | Callable[[], str], 
        digest: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] = "md5", 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False] = False, 
    ) -> tuple[int, HashObj | T]:
        ...
    @overload
    def hash(
        self, 
        /, 
        url: str | Callable[[], str], 
        digest: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] | Callable[[], Callable[[bytes, T], Awaitable[T]]] = "md5", 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[True], 
    ) -> Coroutine[Any, Any, tuple[int, HashObj | T]]:
        ...
    def hash(
        self, 
        /, 
        url: str | Callable[[], str], 
        digest: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] | Callable[[], Callable[[bytes, T], Awaitable[T]]] = "md5", 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False, True] = False, 
    ) -> tuple[int, HashObj | T] | Coroutine[Any, Any, tuple[int, HashObj | T]]:
        digest = convert_digest(digest)
        if async_:
            async def request():
                nonlocal stop
                async with self.open(url, start=start, headers=headers, async_=True) as file: # type: ignore
                    if stop is None:
                        return await file_digest_async(file, digest)
                    else:
                        if stop < 0:
                            stop += file.length
                        return await file_digest_async(file, digest, stop=max(0, stop-start)) # type: ignore
            return request()
        else:
            with self.open(url, start=start, headers=headers) as file:
                if stop is None:
                    return file_digest(file, digest) # type: ignore
                else:
                    if stop < 0:
                        stop = stop + file.length
                    return file_digest(file, digest, stop=max(0, stop-start)) # type: ignore

    @overload
    def hashes(
        self, 
        /, 
        url: str | Callable[[], str], 
        digest: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] = "md5", 
        *digests: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]], 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        async_: Literal[False] = False, 
    ) -> tuple[int, list[HashObj | T]]:
        ...
    @overload
    def hashes(
        self, 
        /, 
        url: str | Callable[[], str], 
        digest: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] | Callable[[], Callable[[bytes, T], Awaitable[T]]] = "md5", 
        *digests: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] | Callable[[], Callable[[bytes, T], Awaitable[T]]], 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        async_: Literal[True], 
    ) -> Coroutine[Any, Any, tuple[int, list[HashObj | T]]]:
        ...
    def hashes(
        self, 
        /, 
        url: str | Callable[[], str], 
        digest: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] | Callable[[], Callable[[bytes, T], Awaitable[T]]] = "md5", 
        *digests: str | HashObj | Callable[[], HashObj] | Callable[[], Callable[[bytes, T], T]] | Callable[[], Callable[[bytes, T], Awaitable[T]]], 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        async_: Literal[False, True] = False, 
    ) -> tuple[int, list[HashObj | T]] | Coroutine[Any, Any, tuple[int, list[HashObj | T]]]:
        digests = (convert_digest(digest), *map(convert_digest, digests))
        if async_:
            async def request():
                nonlocal stop
                async with self.open(url, start=start, headers=headers, async_=True) as file: # type: ignore
                    if stop is None:
                        return await file_mdigest_async(file, *digests)
                    else:
                        if stop < 0:
                            stop += file.length
                        return await file_mdigest_async(file *digests, stop=max(0, stop-start)) # type: ignore
            return request()
        else:
            with self.open(url, start=start, headers=headers) as file:
                if stop is None:
                    return file_mdigest(file, *digests) # type: ignore
                else:
                    if stop < 0:
                        stop = stop + file.length
                    return file_mdigest(file, *digests, stop=max(0, stop-start)) # type: ignore

    @overload
    def read_bytes(
        self, 
        /, 
        url: str, 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    def read_bytes(
        self, 
        /, 
        url: str, 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    def read_bytes(
        self, 
        /, 
        url: str, 
        start: int = 0, 
        stop: None | int = None, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """读取文件一定索引范围的数据
        :param url: 115 文件的下载链接（可以从网盘、网盘上的压缩包内、分享链接中获取）
        :param start: 开始索引，可以为负数（从文件尾部开始）
        :param stop: 结束索引（不含），可以为负数（从文件尾部开始）
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数
        """
        def gen_step():
            def get_bytes_range(start, stop):
                if start < 0 or (stop and stop < 0):
                    length: int = yield self.read_bytes_range(
                        url, 
                        bytes_range="-1", 
                        headers=headers, 
                        async_=async_, 
                        **{**request_kwargs, "parse": lambda resp: get_total_length(resp)}, 
                    )
                    if start < 0:
                        start += length
                    if start < 0:
                        start = 0
                    if stop is None:
                        return f"{start}-"
                    elif stop < 0:
                        stop += length
                if start >= stop:
                    return None
                return f"{start}-{stop-1}"
            bytes_range = yield from get_bytes_range(start, stop)
            if not bytes_range:
                return b""
            return (yield partial(
                self.read_bytes_range, 
                url, 
                bytes_range=bytes_range, 
                headers=headers, 
                async_=async_, 
                **request_kwargs, 
            ))
        return run_gen_step(gen_step, async_=async_)

    @overload
    def read_bytes_range(
        self, 
        /, 
        url: str, 
        bytes_range: str = "0-", 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    def read_bytes_range(
        self, 
        /, 
        url: str, 
        bytes_range: str = "0-", 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    def read_bytes_range(
        self, 
        /, 
        url: str, 
        bytes_range: str = "0-", 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """读取文件一定索引范围的数据
        :param url: 115 文件的下载链接（可以从网盘、网盘上的压缩包内、分享链接中获取）
        :param bytes_range: 索引范围，语法符合 [HTTP Range Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)
        :param headers: 请求头
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数
        """
        if headers:
            headers = {**headers, "Accept-Encoding": "identity", "Range": f"bytes={bytes_range}"}
        else:
            headers = {"Accept-Encoding": "identity", "Range": f"bytes={bytes_range}"}
        request_kwargs["headers"] = headers
        request_kwargs.setdefault("method", "GET")
        request_kwargs.setdefault("parse", False)
        return self.request(url, async_=async_, **request_kwargs)

    @overload
    def read_block(
        self, 
        /, 
        url: str, 
        size: int = 0, 
        offset: int = 0, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False] = False, 
        **request_kwargs, 
    ) -> bytes:
        ...
    @overload
    def read_block(
        self, 
        /, 
        url: str, 
        size: int = 0, 
        offset: int = 0, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[True], 
        **request_kwargs, 
    ) -> Coroutine[Any, Any, bytes]:
        ...
    def read_block(
        self, 
        /, 
        url: str, 
        size: int = 0, 
        offset: int = 0, 
        headers: None | Mapping = None, 
        *, 
        async_: Literal[False, True] = False, 
        **request_kwargs, 
    ) -> bytes | Coroutine[Any, Any, bytes]:
        """读取文件一定索引范围的数据
        :param url: 115 文件的下载链接（可以从网盘、网盘上的压缩包内、分享链接中获取）
        :param size: 下载字节数（最多下载这么多字节，如果遇到 EOF，就可能较小）
        :param offset: 偏移索引，从 0 开始，可以为负数（从文件尾部开始）
        :param async_: 是否异步
        :param request_kwargs: 其它请求参数
        """
        def gen_step():
            if size <= 0:
                return b""
            return (yield self.read_bytes(
                url, 
                start=offset, 
                stop=offset+size, 
                headers=headers, 
                async_=async_, 
                **request_kwargs, 
            ))
        return run_gen_step(gen_step, async_=async_)

    @cached_property
    def fs(self, /) -> P115FileSystem:
        """你的网盘的文件列表的封装对象
        """
        return P115FileSystem(self)

    def get_fs(
        self, 
        /, 
        password: str = "", 
        cache_id_to_readdir: bool | int = False, 
        cache_path_to_id: bool | int = False, 
        refresh: bool = True, 
        request: None | Callable = None, 
        async_request: None | Callable = None, 
    ) -> P115FileSystem:
        """新建你的网盘的文件列表的封装对象
        """
        return P115FileSystem(
            self, 
            password=password, 
            cache_id_to_readdir=cache_id_to_readdir, 
            cache_path_to_id=cache_path_to_id, 
            refresh=refresh, 
            request=request, 
            async_request=async_request, 
        )

    def get_share_fs(self, share_link: str, /, *args, **kwargs) -> P115ShareFileSystem:
        """新建一个分享链接的文件列表的封装对象
        """
        return P115ShareFileSystem(self, share_link, *args, **kwargs)

    def get_zip_fs(self, id_or_pickcode: int | str, /, *args, **kwargs) -> P115ZipFileSystem:
        """新建压缩文件（支持 zip、rar、7z）的文件列表的封装对象（这个压缩文件在你的网盘中，且已经被云解压）

        https://vip.115.com/?ct=info&ac=information
        云解压预览规则：
        1. 支持rar、zip、7z类型的压缩包云解压，其他类型的压缩包暂不支持；
        2. 支持云解压20GB以下的压缩包；
        3. 暂不支持分卷压缩包类型进行云解压，如rar.part等；
        4. 暂不支持有密码的压缩包进行在线预览。
        """
        return P115ZipFileSystem(self, id_or_pickcode, *args, **kwargs)

    @cached_property
    def label(self, /) -> P115LabelList:
        """你的标签列表的封装对象（标签是给文件或文件夹做标记的）
        """
        return P115LabelList(self)

    @cached_property
    def offline(self, /) -> P115Offline:
        """你的离线任务列表的封装对象
        """
        return P115Offline(self)

    def get_offline(self, /, *args, **kwargs) -> P115Offline:
        """新建你的离线任务列表的封装对象
        """
        return P115Offline(self, *args, **kwargs)

    @cached_property
    def recyclebin(self, /) -> P115Recyclebin:
        """你的回收站的封装对象
        """
        return P115Recyclebin(self)

    def get_recyclebin(self, /, *args, **kwargs) -> P115Recyclebin:
        """新建你的回收站的封装对象
        """
        return P115Recyclebin(self, *args, **kwargs)

    @cached_property
    def sharing(self, /) -> P115Sharing:
        """你的分享列表的封装对象
        """
        return P115Sharing(self)

    def get_sharing(self, /, *args, **kwargs) -> P115Sharing:
        """新建你的分享列表的封装对象
        """
        return P115Sharing(self, *args, **kwargs)


# TODO: 这些类再提供一个 Async 版本
class ExportDirStatus(Future):
    _condition: Condition
    _state: str

    def __init__(self, /, client: P115Client, export_id: int | str):
        super().__init__()
        self.status = 0
        self.set_running_or_notify_cancel()
        self._run_check(client, export_id)

    def __bool__(self, /) -> bool:
        return self.status == 1

    def __del__(self, /):
        self.stop()

    def stop(self, /):
        with self._condition:
            if self._state in ["RUNNING", "PENDING"]:
                self._state = "CANCELLED"
                self.set_exception(OSError(errno.ECANCELED, "canceled"))

    def _run_check(self, client, export_id: int | str, /):
        get_status = client.fs_export_dir_status
        payload = {"export_id": export_id}
        def update_progress():
            while self.running():
                try:
                    resp = get_status(payload)
                except:
                    continue
                try:
                    data = check_response(resp)["data"]
                    if data:
                        self.status = 1
                        self.set_result(data)
                        return
                except BaseException as e:
                    self.set_exception(e)
                    return
                sleep(1)
        Thread(target=update_progress).start()


class PushExtractProgress(Future):
    _condition: Condition
    _state: str

    def __init__(self, /, client: P115Client, pickcode: str):
        super().__init__()
        self.progress = 0
        self.set_running_or_notify_cancel()
        self._run_check(client, pickcode)

    def __del__(self, /):
        self.stop()

    def __bool__(self, /) -> bool:
        return self.progress == 100

    def stop(self, /):
        with self._condition:
            if self._state in ["RUNNING", "PENDING"]:
                self._state = "CANCELLED"
                self.set_exception(OSError(errno.ECANCELED, "canceled"))

    def _run_check(self, client, pickcode: str, /):
        check = client.extract_push_progress
        payload = {"pick_code": pickcode}
        def update_progress():
            while self.running():
                try:
                    resp = check(payload)
                except:
                    continue
                try:
                    data = check_response(resp)["data"]
                    extract_status = data["extract_status"]
                    progress = extract_status["progress"]
                    if progress == 100:
                        self.set_result(data)
                        return
                    match extract_status["unzip_status"]:
                        case 1 | 2 | 4:
                            self.progress = progress
                        case 0:
                            raise OSError(errno.EIO, f"bad file format: {data!r}")
                        case 6:
                            raise OSError(errno.EINVAL, f"wrong password/secret: {data!r}")
                        case _:
                            raise OSError(errno.EIO, f"undefined error: {data!r}")
                except BaseException as e:
                    self.set_exception(e)
                    return
                sleep(1)
        Thread(target=update_progress).start()


class ExtractProgress(Future):
    _condition: Condition
    _state: str

    def __init__(self, /, client: P115Client, extract_id: int | str):
        super().__init__()
        self.progress = 0
        self.set_running_or_notify_cancel()
        self._run_check(client, extract_id)

    def __del__(self, /):
        self.stop()

    def __bool__(self, /) -> bool:
        return self.progress == 100

    def stop(self, /):
        with self._condition:
            if self._state in ["RUNNING", "PENDING"]:
                self._state = "CANCELLED"
                self.set_exception(OSError(errno.ECANCELED, "canceled"))

    def _run_check(self, client, extract_id: int | str, /):
        check = client.extract_progress
        payload = {"extract_id": extract_id}
        def update_progress():
            while self.running():
                try:
                    resp = check(payload)
                except:
                    continue
                try:
                    data = check_response(resp)["data"]
                    if not data:
                        raise OSError(errno.EINVAL, f"no such extract_id: {extract_id}")
                    progress = data["percent"]
                    self.progress = progress
                    if progress == 100:
                        self.set_result(data)
                        return
                except BaseException as e:
                    self.set_exception(e)
                    return
                sleep(1)
        Thread(target=update_progress).start()


for name, method in P115Client.__dict__.items():
    if not (callable(method) and method.__doc__):
        continue
    match = CRE_CLIENT_API_search(method.__doc__)
    if match is not None:
        CLIENT_API_MAP[match[1]] = "P115Client." + name


from .fs import P115FileSystem
from .fs_share import P115ShareFileSystem
from .fs_zip import P115ZipFileSystem
from .labellist import P115LabelList
from .offline import P115Offline
from .recyclebin import P115Recyclebin
from .sharing import P115Sharing

# TODO: login_with_qrcode 可以调用另一个 qrcode_login 函数
# TODO: qrcode_login 的返回值，是一个 Future 对象，包含登录必要凭证、二维码链接、登录状态、返回值或报错信息等数据，并且可以被等待完成，也可以把二维码输出到命令行、浏览器、图片查看器等
# TODO: 参考 sqlite 的 Error 体系，构建一个 exception.py 模块
# TODO: 尽量减少各种所谓包装和v2的接口，都合并到一个中
