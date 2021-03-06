"""
*
*   copyright: 2012 Leif Theden <leif.theden@gmail.com>
*   license: GPL-3
*
*   This file is part of pyrikura/purikura.
*
*   pyrikura is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   pyrikura is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with pyrikura.  If not, see <http://www.gnu.org/licenses/>.
*
"""

from pyrikura.broker import Broker
from pyrikura.plugin import Plugin
import os, shutil



class FileCopyBroker(Broker):

    def _do_copy(self, path, dest):
        shutil.copyfile(path, dest)
        print "copy", path, dest

    def process(self, msg, sender=None):
        try:
            overwrite = self.overwrite
        except AttributeError:
            overwrite = False

        new_path = os.path.join(self.dest, os.path.basename(msg))

        if not overwrite and os.path.exists(new_path):
            i = 1
            root, ext = os.path.splitext(new_path)
            new_path = "{0}-{1:04d}{2}".format(root, i, ext)
            while os.path.exists(new_path):
                i += 1
                new_path = "{0}-{1:04d}{2}".format(root, i, ext)

        self._do_copy(msg, new_path)
        self.publish([new_path])
        
class FileCopy(Plugin):
    _decendant = FileCopyBroker
