from files3.f3utils import *
import lz4.frame as lzf
from io import BytesIO
import pickletools
import zipfile
import pickle
import sys
import os
import io

# 目标文件不是F3Inst文件的错误
class NotF3InstError(Exception): ...

# 目标文件丢失源代码文件路径的错误
class LostSourceCodeError(Exception): ...

class _F3Unpickler(pickle._Unpickler):
    @memoize
    def find_class(self, __module_name: str, __global_name: str):
        """
        Find the class by the module name and the global name
        :param __module_name: like __main__
        :param __global_name: like MyClass
        :return:
        """
        # Try to get the target file path
        try:
            if self.rlinkpath:
                tar_file = self.rlinkpath
            elif len(self.metastack) > 1:
                tar_file = self.metastack[1][0]
            else:
                tar_file = self.stack[0]
            tar_file = os.path.abspath(tar_file)
        except:
            raise NotF3InstError(f"Can not get scp. # Meta = {self.metastack}, Stack = {self.stack}")

        # Get the directory of the target file
        tar_dir = os.path.dirname(tar_file)

        # If the module name is '__main__', do the following
        if __module_name == '__main__':
            # Check if the target file exists
            if not os.path.exists(tar_file):
                raise LostSourceCodeError(f"Can not find target source code file (not exist). # target file = {tar_file}")

            # Get the base name of the target file and remove the extension
            tar_name = os.path.basename(tar_file)
            tar_name, _ = os.path.splitext(tar_name)

            # Check if it's an init file
            if tar_name == "__init__":
                tar_name = os.path.basename(tar_dir)
                tar_dir = os.path.dirname(tar_dir)
                if not tar_name:
                    raise ValueError("Source code file:__init__.py file at a disk root.")

            # Set the module name to the base name of the target file
            __module_name = tar_name

        # Add the target directory to the system path
        sys.path.append(tar_dir)

        # Find and return the class
        kclass = super(_F3Unpickler, self).find_class(__module_name, __global_name)

        # Remove the target directory from the system path
        sys.path.pop(-1)

        return kclass

    def load(self, relink_path:str=None):
        self.rlinkpath = relink_path
        scp_obj = super(_F3Unpickler, self).load()  # [scp, obj]

        try:
            scp, obj = scp_obj
        except:
            raise NotF3InstError("Can not parse scp|obj from raw. Please make sure it's created by files3 >= 0.6")

        return obj

def f3dumps(obj, relink_path:str=None):
    """
    save as [scp, obj]
    * mean if any custom class in obj. we can get it's creater code path before find_class.
    * so it help code to find the real class code.

    :param obj:
    :param scp: Source Code Path(Auto Get)
    :return:
    """
    if relink_path is not None:
        scp = relink_path
    else:
        scp = get_top_target_file_path()
    s = pickle.dumps([scp, obj])
    s = pickletools.optimize(s)
    return lzf.compress(s)

def f3loads(s, *, fix_imports=True, encoding="ASCII", errors="strict",
           buffers=None, relink_path=None):
    """

    :param s:
    :param fix_imports:
    :param encoding:
    :param errors:
    :param buffers:
    :param relink_path: relink path
    :return:
    """
    try:
        s = lzf.decompress(s)
    except:
        raise NotF3InstError("Can not decompress bytes data. Please make sure it's created by files3 >= 0.6")
    if isinstance(s, str):
        raise UnicodeError("Can't load pickle from unicode string")
    file = io.BytesIO(s)
    return _F3Unpickler(file, fix_imports=fix_imports, buffers=buffers,
                      encoding=encoding, errors=errors).load(relink_path)

def packtarget(path):
    path = os.path.abspath(path)

    # 创建一个BytesIO对象用于存储zip文件
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_STORED) as zf:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    # 创建文件的完整路径
                    file_path = os.path.join(root, file)
                    # 相对于arcname的路径
                    arcname_file = os.path.relpath(file_path, os.path.join(path, '..'))
                    # 将文件添加到zip文件中
                    zf.write(file_path, arcname=arcname_file)
        else:
            zf.write(path, arcname=arcname)
    # 将buffer的指针移动到开始位置
    buffer.seek(0)
    # 返回zip文件的字节内容
    return buffer.getvalue()


def unpacktarget(zip_bytes, extract_path, overwrite=False):
    """
    解压zip字节流到指定目录

    :param zip_bytes: zip文件的字节流
    :param extract_path: 解压目标目录
    """
    # 确保目标目录存在
    extract_path = os.path.abspath(extract_path)
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    # 使用BytesIO将字节流转换为文件对象
    with BytesIO(zip_bytes) as buffer:
        # with open("Z:/test.zip", "wb") as f:
        #     f.write(buffer.getvalue())

        with zipfile.ZipFile(buffer, 'r') as zf:
            # 解压所有文件和目录到目标路径
            for file in zf.namelist():
                file_path = os.path.join(extract_path, file)
                if os.path.exists(file_path) and not overwrite:
                    raise FileExistsError(f"files.unpack: File already exists: {file_path}\n\nIf you want to overwrite, please set overwrite=True.")
                zf.extract(file, extract_path)


def getpacktarget(zip_bytes) -> zipfile.ZipFile:
    """
    获取zip文件对象

    :param zip_bytes: zip文件的字节流
    :return: zipfile.ZipFile对象
    """
    # 使用BytesIO将字节流转换为文件对象
    buffer = BytesIO(zip_bytes)
    return zipfile.ZipFile(buffer, 'r')


class F3SegmentTail:
    """
    允许向文件尾部添加一段16 + len(TAIL_IDENTITY)字节的数据
    第一个字节: 0:远古版本, z: zip文件, f: f3文件
    """
    TAIL_IDENTITY = b'.\x00F3'
    TAIL_LENGTH = len(TAIL_IDENTITY)
    def __init__(self):
        # assert length < 255, "The length must be less than 255"
        self._bytearray = bytearray(16)

    @property
    def data(self):
        return bytes(self._bytearray)

    @data.setter
    def data(self, value:bytes):
        if not isinstance(value, bytes):
            raise TypeError("Data must be bytes")
        if len(value) > 16:
            raise ValueError(f"Data length must be less than {16}")
        self._bytearray[:len(value)] = value

    def clear(self):
        self._bytearray = bytearray(16)

    def parse(self, fio:io.BufferedIOBase, *, clear=True) -> bool:
        """
        从文件中解析尾部f3segmentTail数据到自身
        成功返回True，否则返回False
        """
        if clear:
            self.clear()
        if isinstance(fio, str):
            fio = open(fio, 'rb')

        _initial = fio.tell()

        # 读取文件末尾TAIL_LENGTH长度的数据
        fio.seek(-self.TAIL_LENGTH, io.SEEK_END)
        tail = fio.read(self.TAIL_LENGTH)
        # 如果读取的数据不是TAIL_IDENTITY，则返回False
        if tail != self.TAIL_IDENTITY:
            fio.seek(_initial)
            return False
        # 读取数据
        fio.seek(-self.TAIL_LENGTH - 16, io.SEEK_END)
        self._bytearray = bytearray(fio.read(16))
        fio.seek(_initial)
        return True

    def write(self, fio:io.BufferedIOBase):
        """
        将自身数据写入文件末尾
        """
        if isinstance(fio, str):
            fio = open(fio, 'ab')
        fio.write(self._bytearray)
        fio.write(self.TAIL_IDENTITY)

    @property
    def zf(self):
        return self._bytearray[0]

    @zf.setter
    def zf(self, value:bool):
        self._bytearray[0] = int(value)



if __name__ == '__main__':
    s = f3dumps(open("f3io.py", "rb").read())

    f3st = F3SegmentTail()
    f3st.data = b'\x01'

    with open("f3io.f3", "wb") as f:
        f.write(s)
        f3st.write(f)

    with open("f3io.f3", "rb") as f:
        if f3st.parse(f):
            print(f3st.data)
            print(f3loads(f.read()))
