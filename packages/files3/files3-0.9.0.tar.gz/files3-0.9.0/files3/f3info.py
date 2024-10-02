import os

PF_DTYPE = ".inst"

__doc__ = """
f3info.py
~~~~~~~~~

This module provides the F3Info class.

Classes
-------
F3Info
    # The info class of files3. used to manage the path and type of the data file.
"""


class F3Info(object):
    def __init__(self, path: str = '/', type: str = PF_DTYPE, sub_type:str = PF_DTYPE):  # TODO: 添加一种sub type
        # 记录工作位置
        self.path = self.NewPath(path)

        # 记录数据文件后缀
        self.type = self.NewType(type.lower())
        self.stype = self.NewType(sub_type.lower())

    @classmethod
    def NewPath(cls, path: str) -> str:
        """
        指定新的数据文件目录
        """
        # 获取绝对路径
        path = os.path.abspath(path)
        # 如果路径不存在，则创建
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @classmethod
    def NewType(cls, type: str) -> str:
        """
        指定新的数据文件后缀
        """
        # 确保类型以'.'开头
        assert type[0] == '.', "'type'[0] must be '.'"
        return type

    @staticmethod
    def SplitPath(fpath) -> (str, str, str):
        """
        分割 完整/相对路径为dir fname ftype
        """
        # 检查路径是否存在，是否为文件
        if not os.path.exists(fpath):
            raise ValueError(f"Target path is not exists: {fpath}")
        if not os.path.isfile(fpath):
            raise ValueError(f"Target path is not a file: {fpath}")

        # 获取绝对路径，目录，文件名和类型
        fpath = os.path.abspath(fpath)
        dir = os.path.dirname(fpath)
        fname_type = os.path.basename(fpath)
        fname, ftype = os.path.splitext(fname_type)
        return dir, fname, ftype

    def __str__(self):
        # 返回类名，路径和类型
        return f"{self.__class__.__name__}<fpath={self.path}, ftype={self.type}>"

    def __call__(self, key: str, skey:str=None) -> str:
        """
        生成key的完整路径
        """
        # 将路径，键和类型连接成完整的路径
        if skey is not None:
            return os.path.join(self.path, key + self.type, skey + self.stype)
        return os.path.join(self.path, key + self.type)
