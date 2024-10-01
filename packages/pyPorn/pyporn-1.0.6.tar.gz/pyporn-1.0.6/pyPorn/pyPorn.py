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

from aiohttp import ClientSession
from typing import Union

from .base import Base
from .enums import Provider
from .exception import PyPornError
from .types import User, Response, Video, Videos


class PyPorn(Base):
    """PyPorn Client, the main means for interacting with API AyiinHub.

    Parameters:
        apiToken (``str``):
            API token for Authorization Users, e.g.: "AxD_ABCDEFghIklzyxWvuew".\n
            Get the *API Token* in [PyPornAuth](https://www.downloader.blue).

        secret (``str``):
            Secret for Authorization Users, e.g.: "ABCDEFghIklzyxWvuew".\n
            Get the *Secret* in [PyPornAuth](https://www.downloader.blue).

        path (``str``, *optional*):
            Path For Download Content.
            Defaults to "downloads".

    Example:
        >>> from pyPorn import PyPorn
        >>> 
        >>> pyPorn = PyPorn(
                apiToken="YOUR_API_TOKEN",
                secret="YOUR_SECRET"
            )
    """
    def __init__(
        self,
        apiToken: str,
        secret: str,
        path: Union[str, None] = None
    ):
        super().__init__(
            apiToken=apiToken,
            secret=secret,
            path=path
        )

    async def userInfo(self):
        res = await self.get("/auth")
        if not isinstance(res, Response):
            raise PyPornError("Failed to get User Info")
        return User(**res.result)

    async def downloadContent(self, url: str, fileName: str):
        """Download the content.

        Args:
            url (``str``): Get the url from :obj:`~pyPorn.types.video.Video`
            fileName (``str``): Name of the file

        Example:
            >>> from pyPorn import PyPorn
            >>> from pyPorn.enums import Provider
            >>> from pyPorn.exception import PyPornError
            >>> 
            >>> pyPorn = PyPorn(
                    apiToken="YOUR_API_TOKEN",
                    secret="YOUR_SECRET"
                )
            >>> try:
            >>>     content = pyPorn.getContent(provider=Provider.XNXX, query="korean")
            >>>     path = pyPorn.downloadContent(url=content.assets.video, fileName=content.data.title)
            >>> except PyPornError as e:
            >>>     print(e)
            >>>     return
            >>> else:
            >>>     print(path)

        Raises:
            PyPornError: The response is not a Httpx Response
            PyPornError: Failed to download.

        Returns:
            str: string of the path downloaded file
        """
        async with ClientSession() as session:
            response = await session.get(url=url)
            if response.status == 200:
                with open(f'{self.path}/{fileName}.mp4', 'wb+') as file:
                    async for chunk, _ in response.content.iter_chunks():
                        file.write(chunk)

                return f"{self.path}/{fileName}.mp4"
            else:
                raise PyPornError(f"Failed to download. Status Code: {response.status}")

    async def getContent(self, provider: Provider, id: str) -> "Video":
        """Get the Video by id.

        Parameters:
            provider (:obj:`~pyPorn.enums.Provider`):
                Provider of the WebSite.

        Example:
            >>> from pyPorn import PyPorn
            >>> from pyPorn.enums import Provider
            >>> from pyPorn.exception import PyPornError
            >>> 
            >>> pyPorn = PyPorn(
                    apiToken="YOUR_API_TOKEN",
                    secret="YOUR_SECRET"
                )
            >>> try:
            >>>     content = pyPorn.getContent(provider=Provider.XNXX, query="korean")
            >>> except PyPornError as e:
            >>>     print(e)
            >>>     return
            >>> else:
            >>>     print(content)

        Raises:
            :obj:`~pyPorn.exception.PyPornError`:
                The response is from the API.

        Returns:
            :obj:`~pyPorn.types.video.Video`
        """

        req = await self.post(f'/{provider.value}/detail?id={id}')
        if req.success:
            return Video(**req.result)
        raise PyPornError(req.result)

    async def randomContent(self, provider: Provider) -> "Video":
        """Get the Random Video.

        Parameters:
            provider (:obj:`~pyPorn.enums.Provider`):
                Provider of the WebSite.

        Example:
            >>> from pyPorn import PyPorn
            >>> from pyPorn.enums import Provider
            >>> from pyPorn.exception import PyPornError
            >>> 
            >>> pyPorn = PyPorn(
                    apiToken="YOUR_API_TOKEN",
                    secret="YOUR_SECRET"
                )
            >>> try:
            >>>     content = pyPorn.randomContent(provider=Provider.XNXX)
            >>> except PyPornError as e:
            >>>     print(e)
            >>>     return
            >>> else:
            >>>     print(content)

        Raises:
            :obj:`~pyPorn.exception.PyPornError`:
                The response is from the API.

        Returns:
            :obj:`~pyPorn.types.video.Video`
        """

        req = await self.post(f'/{provider.value}/random')
        if req.success:
            return Video(**req.result)
        raise PyPornError(req.result)

    async def relatedContent(self, provider: Provider, id: str) -> "Videos":
        """Get the Related Videos by id.

        Parameters:
            provider (:obj:`~pyPorn.enums.Provider`):
                Provider of the WebSite.

        Example:
            >>> from pyPorn import PyPorn
            >>> from pyPorn.enums import Provider
            >>> from pyPorn.exception import PyPornError
            >>> 
            >>> pyPorn = PyPorn(
                    apiToken="YOUR_API_TOKEN",
                    secret="YOUR_SECRET"
                )
            >>> try:
            >>>     content = pyPorn.relatedContent(provider=Provider.XNXX, id="video-u10yx0f/chin")
            >>> except PyPornError as e:
            >>>     print(e)
            >>>     return
            >>> else:
            >>>     print(content)

        Raises:
            :obj:`~pyPorn.exception.PyPornError`:
                The response is from the API.

        Returns:
            :obj:`~pyPorn.types.videos.Videos`
        """

        req = await self.post(f'/{provider.value}/related?id={id}')
        if req.success:
            return Videos(videos=req.result["data"])
        raise PyPornError(req.message)

    async def searchContent(self, provider: Provider, query: str, page: int = 0) -> "Videos":
        """Search the Video by query.

        Parameters:
            provider (:obj:`~pyPorn.enums.Provider`):
                Provider of the WebSite.

            query (``str``):
                Query for Search the Video.

            page (``int``, *optional*):
                Page Number for Search the Video in page.

        Example:
            >>> from pyPorn import PyPorn
            >>> from pyPorn.enums import Provider
            >>> from pyPorn.exception import PyPornError
            >>> 
            >>> pyPorn = PyPorn(
                    apiToken="YOUR_API_TOKEN",
                    secret="YOUR_SECRET"
                )
            >>> try:
            >>>     contents = pyPorn.searchContent(provider=Provider.XNXX, query="korean")
            >>> except PyPornError as e:
            >>>     print(e)
            >>>     return
            >>> else:
            >>>     print(contents.videos)
            >>> 
            >>> # or with page
            >>> try:
            >>>     contents = pyPorn.searchContent(provider=Provider.XNXX, query="korean", page=1)
            >>> except PyPornError as e:
            >>>     print(e)
            >>>     return
            >>> else:
            >>>     print(contents.videos)

        Raises:
            :obj:`~pyPorn.exception.PyPornError`:
                The response is from the API.

        Returns:
            :obj:`~pyPorn.types.videos.Videos`
        """

        req = await self.post(f'/{provider.value}/search?key={query}&page={page}')
        if req.success:
            return Videos(videos=req.result["data"])
        raise PyPornError(req.message)
