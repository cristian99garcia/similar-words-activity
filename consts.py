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

SUGAR = None

try:
    import sugar3
    SUGAR = True

except ImportError:
    SUGAR = False


DRAG_TARGETS = [Gtk.TargetEntry.new("TEXT", 0, 0)]
DRAG_ACTION = Gdk.DragAction.MOVE
CORRECT_COLOR = None
INCORRECT_COLOR = None
SECTION_BG_COLOR = None

if not SUGAR:
    CORRECT_COLOR = Gdk.RGBA(0.2, 1, 0.2, 1)
    INCORRECT_COLOR = Gdk.RGBA(1, 0.2, 0.2, 1)
    SECTION_BG_COLOR = Gdk.RGBA(0.5, 0.5, 0.5, 1)

else:
    CORRECT_COLOR = Gdk.RGBA(0, 1, 0, 1)
    INCORRECT_COLOR = Gdk.RGBA(1, 0, 0, 1)
    SECTION_BG_COLOR = Gdk.RGBA(1, 1, 1, 1)


class WordType:  # Best enum ever
    SIMILAR = 1
    DIFFERENT = 2


WORDS_DATA = {
    "Hello": [
        [WordType.SIMILAR, "Greetings"],
        [WordType.DIFFERENT, "Goodbye"],
        [WordType.SIMILAR, "Hi"],
        [WordType.SIMILAR, "Welcome"],
        [WordType.SIMILAR, "Howdy"],
        [WordType.DIFFERENT, "Until next time!"],
        [WordType.SIMILAR, "What's up"],
        [WordType.SIMILAR, "How are you?"],
        [WordType.DIFFERENT, "Bye bye"],
    ],
    "Congratulations": [
        [WordType.DIFFERENT, "You did bad"],
        [WordType.SIMILAR, "Compliments"],
        [WordType.SIMILAR, "Good work"],
        [WordType.SIMILAR, "Cheers"],
        [WordType.DIFFERENT, "Bad luck"],
        [WordType.DIFFERENT, "Terrible job"],
        [WordType.SIMILAR, "Hats off"],
        [WordType.SIMILAR, "Well done"],
        [WordType.DIFFERENT, "Dig"],
        [WordType.DIFFERENT, "Berate"],
    ],
    "Tool": [
        [WordType.SIMILAR, "Utensil"],
        [WordType.DIFFERENT, "Plaything"],
        [WordType.SIMILAR, "Instument"],
        [WordType.SIMILAR, "Device"],
        [WordType.DIFFERENT, "Useless thing"],
    ],
    "Meal": [
        [WordType.SIMILAR, "Lunch"],
        [WordType.DIFFERENT, "Hungry"],
        [WordType.DIFFERENT, "Abstinence"],
        [WordType.SIMILAR, "Dinner"],
        [WordType.SIMILAR, "Snack"],
        [WordType.SIMILAR, "Food"],
        [WordType.DIFFERENT, "Fast"],
        [WordType.SIMILAR, "Aliment"],
    ]
}