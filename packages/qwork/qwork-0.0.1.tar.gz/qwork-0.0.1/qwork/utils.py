import os
from files3 import files
from PyQt5.QtWidgets import QFileDialog


class QSetting:  # Settings
    def __init__(self, setting_path:str="", setting_filename:str="setting", type_suffix:str=".qst"):
        setting_path = os.path.abspath(setting_path)
        if not os.path.isdir(setting_path):
            raise NotADirectoryError(f"QSetting:{setting_path} is not a directory.")
        self._f = files(setting_path, type_suffix)
        self._filename = setting_filename

    @property
    def settings(self) -> dict:
        if not self._f.has(self._filename):
            self._f[self._filename] = {}
            return {}
        return self._f[self._filename]

    def __getitem__(self, stkey:str):
        _st = self.settings
        if stkey in _st:
            return _st[stkey]
        return None

    def __setitem__(self, stkey:str, value):
        _st = self.settings
        _st[stkey] = value
        self._f[self._filename] = _st


    def getOpenFileName(self, title: str = "Open File", dirpath: str = "", filter_string: str = "All Files (*)") -> tuple[str, str]:
        _last_dir:str = self["getOpenFileName"]
        _0, _1 = QFileDialog.getOpenFileName(None, title, dirpath if _last_dir is None else _last_dir, filter_string)
        if _0 and os.path.exists(_0):
            self["getOpenFileName"] = os.path.dirname(_0)
        return _0, _1

    def getSaveFileName(self, title: str = "Save File", dirpath: str = "", filter_string: str = "All Files (*)", *, filename:str=None) -> tuple[str, str]:
        _last_dir:str = self["getSaveFileName"]
        _last_dir = dirpath if _last_dir is None else _last_dir
        if filename and not _last_dir.endswith(filename):
            _last_dir = os.path.join(_last_dir, filename)
        _0, _1 = QFileDialog.getSaveFileName(None, title, _last_dir, filter_string)
        if _0 and os.path.exists(_0):
            self["getSaveFileName"] = os.path.dirname(_0)
        return _0, _1

    def getExistingDirectory(self, title: str = "Open Directory", dirpath: str = "", *, stlast:bool=False) -> str:
        _last_dir:str = self["getExistingDirectory"]
        _0 = QFileDialog.getExistingDirectory(None, title, dirpath if _last_dir is None else _last_dir)
        if _0 and os.path.exists(_0):
            if stlast:
                self["getExistingDirectory"] = os.path.dirname(_0)
            else:
                self["getExistingDirectory"] = _0
        return _0

    def getOpenFileNames(self, title: str = "Open Files", dirpath: str = "", filter_string: str = "All Files (*)") -> tuple[list[str], str]:
        _last_dir:str = self["getOpenFileNames"]
        _0, _1 = QFileDialog.getOpenFileNames(None, title, dirpath if _last_dir is None else _last_dir, filter_string)
        if _0 and os.path.exists(_0[0]):
            self["getOpenFileNames"] = os.path.dirname(_0[0])
        return _0, _1



