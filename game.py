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

from words_box import WordsBox

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class Game(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.wbox = WordsBox()
        self.pack_start(self.wbox, True, True, 0)


if __name__ == "__main__":
    win = Gtk.Window()
    win.set_title("Similar and Different words game")
    win.set_icon_from_file("activity/icon.svg")
    win.maximize()

    game = Game()
    win.add(game)
    win.connect("destroy", Gtk.main_quit)

    win.show_all()
    Gtk.main()