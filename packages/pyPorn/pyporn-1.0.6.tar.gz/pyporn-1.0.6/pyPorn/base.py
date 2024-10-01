# MIT License

# Copyright (c) 2024 AyiinXd

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import aiohttp
import hmac
import hashlib
import os
from typing import Optional, Union

from .exception import ResponseError
from .types import Response
from .version import __version__


class Base:
    version = __version__
    apiToken: str
    baseUrl: str = "https://server.downloader.blue/api"
    def __init__(self, apiToken: str, secret: str, path: Union[str, None] = None):
        self.apiToken = apiToken
        self.secret = secret
        self.path = path if path else "downloads"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.apiToken}"
        }

    async def post(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        signature = await self.createSignature(
            path=url.split("?")[0] if "?" in url else url,
            method="POST"
        )
        self.headers['Xd-Porn-Signature'] = signature
        async with aiohttp.ClientSession(headers=self.headers) as session:
            res = await session.post(
                url=f"{self.baseUrl}{url}",
                json=data,
                headers=headers
            )
            json = await res.json()
            response: Response = Response(**json)
            if response.success:
                return response
            else:
                raise ResponseError(response.message)

    async def get(
        self,
        url: str,
        data: Optional[dict] = None,
        headers: Optional[dict] = None
    ):
        signature = await self.createSignature(
            path=url.split("?")[0] if "?" in url else url,
            method="GET"
        )
        self.headers['Xd-Porn-Signature'] = signature
        async with aiohttp.ClientSession(headers=self.headers) as session:
            req = await session.get(url=f"{self.baseUrl}{url}", json=data, headers=headers)
            json = await req.json()
            response: Response = Response(**json)
            if response.success:
                return response
            else:
                raise ResponseError(response.message)

    def validatePath(self, autoClean: bool = False):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        if autoClean:
            for file in os.listdir(self.path):
                try:
                    os.remove(os.path.join(self.path, file))
                except FileNotFoundError:
                    pass

    async def createSignature(
        self,
        path: str,
        method: str,
    ):
        signature = hmac.new(
            bytes(self.secret,'latin-1'),
            bytes(path+method,'latin-1'),
            hashlib.sha256
        ).hexdigest()
        return signature
