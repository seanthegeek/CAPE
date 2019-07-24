# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import os
import struct
HAVE_RE2 = False
try:
    import re2 as re
    HAVE_RE2 = True
except ImportError:
    import re

from lib.cuckoo.common.abstracts import Processing
from lib.cuckoo.common.objects import File, ProcDump
from lib.cuckoo.common.constants import CUCKOO_ROOT

class ProcessMemory(Processing):
    """Analyze process memory dumps."""
    order = 10

    def run(self):
        """Run analysis.
        @return: structured results.
        """
        self.key = "procmemory"
        results = []
        do_strings = self.options.get("strings", False)
        nulltermonly = self.options.get("nullterminated_only", True)
        minchars = self.options.get("minchars", 5)

        if os.path.exists(self.pmemory_path):
            for dmp in os.listdir(self.pmemory_path):
                # if we're re-processing this task, this means if zips are enabled, we won't do any reprocessing on the
                # process dumps (only matters for now for Yara)
                if not dmp.endswith(".dmp"):
                    continue

                dmp_path = os.path.join(self.pmemory_path, dmp)
                if os.path.getsize(dmp_path) == 0:
                    continue

                dmp_file = File(dmp_path)
                process_name = ""
                process_path = ""
                process_id = int(os.path.splitext(os.path.basename(dmp_path))[0])
                if "behavior" in self.results and "processes" in self.results["behavior"]:
                    for process in self.results["behavior"]["processes"]:
                        if process_id == process["process_id"]:
                            process_name = process["process_name"]
                            process_path = process["module_path"]

                procdump = ProcDump(dmp_path, pretty=True)

                proc = dict(
                    file=dmp_path,
                    pid=process_id,
                    name=process_name,
                    path=process_path,
                    yara=dmp_file.get_yara(os.path.join(CUCKOO_ROOT, "data", "yara", "index_memory.yar")),
                    address_space=procdump.pretty_print(),
                )
                endlimit = ""
                if not HAVE_RE2:
                    endlimit = "8192"

                if do_strings:
                    if nulltermonly:
                        apat = "([\x20-\x7e]{" + str(minchars) + "," + endlimit + "})\x00"
                        upat = "((?:[\x20-\x7e][\x00]){" + str(minchars) + "," + endlimit + "})\x00\x00"
                    else:
                        apat = "[\x20-\x7e]{" + str(minchars) + "," + endlimit + "}"
                        upat = "(?:[\x20-\x7e][\x00]){" + str(minchars) + "," + endlimit + "}"

                    matchdict = procdump.search(apat, all=True)
                    strings = matchdict["matches"]
                    matchdict = procdump.search(upat, all=True)
                    ustrings = matchdict["matches"]
                    for ws in ustrings:
                        strings.append(str(ws.decode("utf-16le")))

                    proc["strings_path"] = dmp_path + ".strings"
                    f=open(proc["strings_path"], "w")
                    f.write("\n".join(strings))
                    f.close()

                procdump.close()
                results.append(proc)
        return results
