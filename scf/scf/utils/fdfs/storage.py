from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings
from rest_framework.exceptions import APIException


class FDFSStorage(Storage):
    """FDFS自定义文件存储类"""
    def __init__(self, client_conf=None, base_url=None):
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF

        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL

        self.base_url = base_url

    def _save(self, name, content):
        """
        name: 上传文件的名称
        content: 包含上传文件内容的File对象，content.read()获取上传文件内容
        """
        # 将文件上传到FDFS文件系统
        client = Fdfs_client(self.client_conf)
        # 上传
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            raise APIException('上传文件到FDFS失败')
        # 获取文件id
        file_id = res.get('Remote file_id')
        return file_id

    def exists(self, name):
        """
        判断上传文件的名称和文件系统中原有的文件名是否冲突
        name: 上传文件的名称
        """
        return False

    def url(self, name):
        return self.base_url + name

    def delete(self, name):
        """
        name:文件id
        :param name:
        :return:
        """
        client = Fdfs_client(self.client_conf)
        # 删除FDFS中存储的图片
        client.delete_file(name)
