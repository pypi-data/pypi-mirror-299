import os
import re
import shutil
import typing
import zipfile
from files3.f3info import F3Info
from files3.f3bool import *
from files3.f3core import F3Core, packtarget, unpacktarget, getpacktarget
from files3.f3utils import *

function = type(lambda: ...)

class F3Shell(object):
    _F3INSTS = ['_f3info', 'set', 'get', 'has', 'delete', 'retype', 'relink', 'keys', 'values', 'items', 'hash']
    _F3BACKEND = F3Core()

    def __init__(self, path="", type=".inst", sub_type=".inst"):
        self._f3info = F3Info(path, type, sub_type)

    def _shell_magic_filter_(self, item, type=True, listes=[]):
        """
        标准筛选支持:（sysfunc .protected.）
        1.str
        2.... or slice[:](仅限全选)
        3.re.Pattern 对每个key(type == False)或是fname(type == True)
        4.func(name, type)->bool 将返回True的结果对应的item选中
        5.[]  各个条件间相并
        :param item:
        :param type: whether suffix or not. If False, only select self.info.type
        :param listes: 递归用，用户勿传     Recursive use, users do not pass
        :return: [] of '$name + $type'
        """
        _end = self._f3info.type if type else ""
        # 第一轮筛选 -- 简单筛选
        if isinstance(item, slice) or item is ...:
            return self._F3BACKEND.list(self._f3info)
        elif isinstance(item, str):
            return [item + _end]

        _return = []
        # 第二轮筛选 -- advanced筛选
        if not listes:
            listes = os.listdir()
        if isinstance(item, function):
            for fname in listes:
                _key, _type = os.path.splitext(fname)
                if type or self._f3info.type == _type:
                    try:
                        _value = item(_key)
                    except Exception as err:
                        print(f"Bad filter function: {item}. Cause error: {err}\n\nPlease check your function(fname)->bool and it's code.")
                    if bool(_value) == True:
                        _return += [(_key + _end) if not type else fname]

        elif isinstance(item, re.Pattern):
            for fname in listes:
                _key, _type = os.path.splitext(fname)
                if type or self._f3info.type == _type:
                    if item.match(_key if not type else fname):
                        _return += [(_key + _end) if not type else fname]
        elif isinstance(item, list):
            for _item in item:
                _return += self._shell_magic_filter_(_item, type, listes)
        else:
            raise Exception("Unkown item - " + str(item))
        return list(set(_return))

    def __getitem__(self, item):
        if isinstance(item, tuple):
            if len(item) != 2:
                raise ValueError("Tuple must have 2 elements(key:str, skey:str). But got " + str(item))
            return self.get(item[0], item[1])
        _return = []
        for key in self._shell_magic_filter_(item, type=False):
            _return += [self.get(key)]
        return F3False if not _return else (_return[0] if len(_return) == 1 else _return)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            if len(key) != 2:
                raise ValueError("Tuple must have 2 elements(key:str, skey:str). But got " + str(key))
            self.set(key[0], value, key[1])
            return
        for key in self._shell_magic_filter_(key, type=False):
            self.set(key, value)

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        if key not in self._F3INSTS and not (key[:2] != '__' and key[-2:] == '__'):
            self.__setitem__(key, value)
        else:
            super(F3Shell, self).__setattr__(key, value)

    def __delitem__(self, key):
        if isinstance(key, tuple):
            if len(key) != 2:
                raise ValueError("Tuple must have 2 elements(key:str, skey:str). But got " + str(key))
            self.delete(key[0], key[1])
            return
        for key in self._shell_magic_filter_(key, type=False):
            self.delete(key)

    def __delattr__(self, item):
        self.delete(item)

    def __len__(self):
        return len(list(self.keys()))

    def __contains__(self, item):
        _return = True
        for key in self._shell_magic_filter_(item, type=False):
            _return *= self.has(item)
        return bool(_return)

    def __iter__(self):
        return self.keys()

    def keys(self) -> typing.Iterable:
        return F3Shell._F3BACKEND.iter(self._f3info)

    def values(self) -> typing.Iterable:
        for key in self.keys():
            yield self.get(key)

    def items(self) -> typing.Iterable:
        for key in self.keys():
            yield key, self.get(key)

    def has(self, key: str, skey:str=None) -> F3Bool:
        """
        成功返回F3True，如果目标文件不存在，则返回F3False
        Has a pyfile file exists. Returns True successfully, or False if the target file doesnot exists

        :param info:     InfoPackage inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param skey:     sub key, 如果启用了子键，则会将主键目标视作文件夹
        """
        return F3Shell._F3BACKEND.has(self._f3info, key, skey)

    def set(self, key: str, pyobject: object, skey:str=None, *, error=False) -> F3Bool:
        """
        存储python对象到目标文件夹下。成功返回F3True，如果目标文件被锁定或占用，则返回F3False
        Storing Python objects to pyfile under specific path in InfoPackage. Returns True successfully. If the target file is locked or occupied, returns False

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param pyobject: python对象   python object
        :param skey:     sub key, 如果启用了子键，则会将主键目标视作文件夹
        :param error:    bool  whether raise error.
        """
        return F3Shell._F3BACKEND.set(self._f3info, key, pyobject, skey, error=error)

    def get(self, key: str, skey:str=None, *, error=False) -> object:
        """
        成功返回读取到的pyobject，如果目标文件不存在，则返回F3False
        Find data files. The read pyobject is returned successfully. If the target file does not exist, false is returned

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param skey:     sub key, 如果启用了子键，则会将主键目标视作文件夹
        :param error:    bool  whether raise error.
        """
        return F3Shell._F3BACKEND.get(self._f3info, key, skey, error=error)

    def delete(self, key: str, skey:str=None, *, error=False) -> F3Bool:
        """
        成功或目标文件不存在则返回F3True，如果目标文件存在而无法删除，则返回F3False
        Delete pyfile file. Returns True if the target file is successful or does not exist. Returns False if the target file exists and cannot be deleted

        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        :param skey:     sub key, 如果启用了子键，则会将主键目标视作文件夹
        """
        return F3Shell._F3BACKEND.delete(self._f3info, key, skey, error=error)

    def list(self, key:str=None, *, error=False) -> list:
        """
        列举目标文件夹下所有目标类型的文件的key。返回一个列表结果
        List all info of keys (In the target folder The key of a file of type). Returns a list result
        :param info:     F3Info inst
        :param key:      文件名称，类似数据库的主键，不能重复
                         File name. It is similar to the primary key of a database and cannot be duplicated
        """
        return self._F3BACKEND.list(self._f3info, key, error=error)

    def retype(self, new_type: str, *keys) -> list:
        """
        修改工作目录下的现有一些文件的后缀到新的后缀
        Modify the suffix of some existing files in the working directory to a new suffix
        :param new_type:带.      contain dot
        :param keys: 目标的主键，如果不指定，则默认全部文件
        :return:
            failed list: 由于名称重复而未能成功retype的文件名(带原始后缀)      Failed to retype file successfully due to duplicate name(with the original suffix
        """
        faileds = []
        assert '.' == new_type[0], "type must contain '.'"
        # assert self.backend._pflevel >= 1, "For using this function, pyfile_files is needy or more advanced pyfile_files. (Basic_files is not accept.)"
        for fname in os.path.listdir(self._f3info.path):
            _path = os.path.join(self._f3info.path, fname)
            if os.path.isfile(_path):
                _base, _type = os.path.splitext(fname)
                if _type.lower() == self._f3info.type:
                    _newpath = os.path.join(self._f3info.path, _base + new_type)
                    if os.path.exists(_newpath):
                        faileds += [fname]
                    else:
                        # Copy from to new type
                        shutil.copyfile(_path, _newpath)
                        # Check Whether exists or not
                        if not os.path.exists(_newpath):
                            faileds.append(fname)
                        else:
                            os.remove(_path)
        return faileds

    def relink(self, new_scp: str, *keys) -> list:
        """
        修改工作目录下的现有一些文件的源文件路径到新的路径
        :param new_scp: new source code path
        :param keys:
        :return:
        """
        err_list = []
        for k in keys:
            _path = self._f3info(k)
            if not os.path.exists(_path):
                raise ValueError(f"Target path is not exists: {k}")
            try:
                obj = self._F3BACKEND.get(self._f3info, k, _sys_relink=new_scp, error=True)
                self._F3BACKEND.set(self._f3info, k, obj, error=True)
            except Exception as err:
                err_list.append((k, err))
                print(f"Relink {k}{self._f3info.type} failed. Cause error: {err}")
        return err_list


    def hash(self, key:str, skey:str=None, *, error=False) -> int:
        """
        获取目标的文件指纹
        :param key:
        :param skey:
        :param error:
        :return:
        """
        _path = self._f3info(key, skey)
        if not os.path.isfile(_path):
            return hash(self.f3pack(_path, error=error))
        return hash(open(_path, 'rb').read())

    @staticmethod
    def f3dumps(obj: object, *, error=True) -> bytes:
        """
        将python对象转换为f3格式的bytes
        :param obj: python对象
        :return: f3格式的bytes
        """
        try:
            return F3Core.dumps(obj)
        except Exception as err:
            if error: raise err
            return F3False

    @staticmethod
    def f3loads(data: bytes, *, error=True) -> object:
        """
        将f3格式的bytes转换为python对象
        :param data: f3格式的bytes
        :return: python对象
        """
        # check
        if not isinstance(data, bytes):
            if error: raise TypeError("data must be bytes")
            return F3False

        # body
        try:
            return F3Core.loads(data)
        except Exception as err:
            if error: raise err
            return F3False


    @staticmethod
    def f3pack(path: str, *, error=True) -> bytes:
        """
        将目标目录打包为f3格式的bytes
        * 先使用ZIP_STORED压缩，再使用f3格式打包
        :param path: 目标文件或目录的路径
        :return: f3zip格式的bytes
        """
        # check
        if not os.path.exists(path):
            if error: raise ValueError(f"Path is not exists: {path}")
            return F3False

        # body
        path = os.path.abspath(path)
        try:
            s = packtarget(path)
            return F3Core.dumps(s, error=error)
        except Exception as err:
            if error: raise err
            return F3False

    @staticmethod
    def f3unpack(data: bytes, path: str=None, *, error=True, overwrite=False) -> F3Bool|zipfile.ZipFile:
        """
        将f3格式的bytes解包到目标目录
        * 先解包f3格式，再解包ZIP_STORED压缩
        :param data: f3zip格式的bytes
        :param path: 目标目录的路径. 如果为None, 返回值为zipfile.ZipFile实例
        :param overwrite: bool, 是否覆盖已存在的文件(仅在path不为None时有效)
        """
        # check
        if not isinstance(data, bytes):
            if error: raise TypeError("data must be bytes")
            return F3False

        # body
        try:
            s = F3Core.loads(data, error=error)
            if s is not F3False:
                if path is not None:
                    unpacktarget(s, os.path.abspath(path), overwrite=overwrite)
                    return F3True
                else:
                    return getpacktarget(s)
            return F3False
        except Exception as err:
            if error: raise err
            return F3False


if __name__ == '__main__':
    ...
