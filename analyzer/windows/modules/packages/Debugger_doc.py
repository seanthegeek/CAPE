# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import shutil

from lib.common.abstracts import Package

class Debugger_doc(Package):
    """CAPE Word Debugger package."""
    
    def __init__(self, options={}, config=None):
        """@param options: options dict."""
        self.config = config
        self.options = options
        self.pids = []
        self.options["dll"] = "Debugger.dll"
        self.options["dll_64"] = "Debugger_x64.dll"

    PATHS = [
        ("ProgramFiles", "Microsoft Office", "WINWORD.EXE"),
        ("ProgramFiles", "Microsoft Office", "Office*", "WINWORD.EXE"),
        ("ProgramFiles", "Microsoft Office*", "root", "Office*", "WINWORD.EXE"),
        ("ProgramFiles", "Microsoft Office", "WORDVIEW.EXE"),
    ]

    def start(self, path):
        word = self.get_path_glob("Microsoft Office Word")
        if "." not in os.path.basename(path):
            new_path = path + ".doc"
            os.rename(path, new_path)
            path = new_path

        return self.execute(word, "\"%s\" /q" % path, path)
