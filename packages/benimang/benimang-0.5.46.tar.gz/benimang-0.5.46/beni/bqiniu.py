from contextlib import asynccontextmanager
from typing import Any, NamedTuple, Tuple, cast

from qiniu import (Auth, BucketManager, build_batch_delete, etag, put_data,
                   put_file)
from qiniu.http import ResponseInfo

from beni import bhttp, bpath, bzip
from beni.bfunc import jsonDumpsMini, runThread, toAny
from beni.btype import XPath


class QiniuItem(NamedTuple):
    key: str
    size: int
    qetag: str
    time: int


_FileListResult = tuple[dict[str, Any], Any, Any]


class QiniuBucket():

    def __init__(self, bucket: str, baseUrl: str, ak: str, sk: str) -> None:
        self.q = Auth(ak, sk)
        self.bucketManager = BucketManager(self.q)
        self.bucket = bucket
        self.baseUrl = baseUrl

    async def uploadBytes(self, key: str, data: bytes):
        token = self.q.upload_token(self.bucket, key)
        _, info = await runThread(
            lambda: cast(Tuple[Any, ResponseInfo], put_data(token, key, data))
        )
        assert info.exception is None
        assert info.status_code == 200
        return self.getPublicFileUrl(key)

    async def uploadStr(self, key: str, data: str):
        await self.uploadBytes(key, data.encode())
        return self.getPublicFileUrl(key)

    async def uploadJson(self, key: str, data: dict[str, Any]):
        await self.uploadStr(key, jsonDumpsMini(data))
        return self.getPublicFileUrl(key)

    async def getPrivateBytes(self, key: str) -> bytes:
        url = self.getPrivateFileUrl(key)
        return await bhttp.getBytes(url)

    async def getPrivateStr(self, key: str) -> str:
        url = self.getPrivateFileUrl(key)
        return await bhttp.getStr(url)

    async def getPrivateJson(self, key: str) -> dict[str, Any]:
        url = self.getPrivateFileUrl(key)
        return await bhttp.getJson(url)

    async def getPublicBytes(self, key: str) -> bytes:
        return await bhttp.getBytes(
            self.getPublicFileUrl(key)
        )

    async def getPublicStr(self, key: str) -> str:
        return await bhttp.getStr(
            self.getPublicFileUrl(key)
        )

    async def getPublicJson(self, key: str) -> dict[str, Any]:
        return await bhttp.getJson(
            self.getPublicFileUrl(key)
        )

    async def uploadFile(self, key: str, localFile: XPath):
        token = self.q.upload_token(self.bucket, key)
        _, info = await runThread(
            lambda: cast(Tuple[Any, ResponseInfo], put_file(token, key, localFile, version='v2'))
        )
        assert info.exception is None
        assert info.status_code == 200
        return self.getPublicFileUrl(key)

    def getPublicFileUrl(self, key: str):
        return f'{self.baseUrl}/{key}'

    def getPrivateFileUrl(self, key: str):
        return self.q.private_download_url(
            self.getPublicFileUrl(key)
        )

    @asynccontextmanager
    async def _downloadPrivateFile(self, key: str):
        url = self.getPrivateFileUrl(key)
        with bpath.useTempFile() as tempFile:
            tempFile = bpath.tempFile()
            await bhttp.download(url, tempFile)
            assert tempFile.exists()
            yield tempFile

    async def downloadPrivateFile(self, key: str, localFile: XPath):
        async with self._downloadPrivateFile(key) as tempFile:
            bpath.move(tempFile, localFile, True)

    async def downloadPrivateFileUnzip(self, key: str, outputDir: XPath):
        async with self._downloadPrivateFile(key) as tempFile:
            with bpath.useTempPath() as tempDir:
                bzip.unzip(tempFile, tempDir)
                for file in bpath.listFile(tempDir, True):
                    toFile = bpath.changeRelative(file, tempDir, outputDir)
                    bpath.move(file, toFile, True)

    async def downloadPrivateFileSevenUnzip(self, key: str, outputDir: XPath):
        async with self._downloadPrivateFile(key) as tempFile:
            with bpath.useTempPath() as tempDir:
                await bzip.sevenUnzip(tempFile, tempDir)
                for file in bpath.listFile(tempDir, True):
                    toFile = bpath.changeRelative(file, tempDir, outputDir)
                    bpath.move(file, toFile, True)

    async def getFileList(self, prefix: str, limit: int = 100) -> tuple[list[QiniuItem], str | None]:
        result, _, _ = await runThread(
            lambda: cast(_FileListResult, self.bucketManager.list(self.bucket, prefix, None, limit))
        )
        assert type(result) is dict
        fileList = [QiniuItem(x['key'], x['fsize'], x['hash'], x['putTime']) for x in result['items']]
        return fileList, cast(str | None, result.get('marker', None))

    async def getFileListByMarker(self, marker: str, limit: int = 100):
        result, _, _ = await runThread(
            lambda: cast(_FileListResult, self.bucketManager.list(self.bucket, None, marker, limit))
        )
        assert type(result) is dict
        fileList = [QiniuItem(x['key'], x['fsize'], x['hash'], x['putTime']) for x in result['items']]
        return fileList, cast(str | None, result.get('marker', None))

    async def deleteFiles(self, *keyList: str):
        result, _ = await runThread(
            lambda: cast(tuple[Any, Any], self.bucketManager.batch(build_batch_delete(self.bucket, keyList)))
        )
        assert result

    async def hashFile(self, file: XPath):
        return await runThread(
            lambda: etag(file)
        )

    async def getFileStatus(self, key: str):
        return await runThread(
            lambda: toAny(self.bucketManager.stat(self.bucket, key))[0]
        )

    async def move(self, oldKey: str, newKey: str):
        result, _ = await runThread(
            lambda: cast(tuple[Any, Any], self.bucketManager.move(self.bucket, oldKey, self.bucket, newKey))
        )
        assert result == {}
        return self.getPublicFileUrl(newKey)

    async def copy(self, oldKey: str, newKey: str):
        result, _ = await runThread(
            lambda: cast(tuple[Any, Any], self.bucketManager.copy(self.bucket, oldKey, self.bucket, newKey))
        )
        assert result == {}
        return self.getPublicFileUrl(newKey)
