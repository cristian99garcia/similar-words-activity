#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk

DRAG_TARGETS = [Gtk.TargetEntry.new("TEXT", 0, 0)]
DRAG_ACTION = Gdk.DragAction.MOVE
CORRECT_COLOR = Gdk.RGBA(0.2, 1, 0.2, 1)
INCORRECT_COLOR = Gdk.RGBA(1, 0.2, 0.2, 1)

class WordType:  # Best enum ever
    SYNONYM = 1
    ANTONYM = 2


WORDS_DATA = {
    "Test": [
        [WordType.SYNONYM, "SHreger"],
        [WordType.SYNONYM, "SQadhrwwdgr"],
        [WordType.ANTONYM, "AYgf"],
        [WordType.SYNONYM, "SHtesdbr"],
        [WordType.ANTONYM, "AHedvvsr"],
        [WordType.ANTONYM, "AGryj"],
        [WordType.SYNONYM, "SRegeewdfaets"],
        [WordType.ANTONYM, "AGwsdvtt"],
        [WordType.SYNONYM, "SUinvfobt"],
        [WordType.ANTONYM, "AMobrenth"],
        [WordType.SYNONYM, "SPolqnirw"],
        [WordType.ANTONYM, "AQonngek"],
    ]
}