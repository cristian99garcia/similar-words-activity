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

from consts import WordType, DRAG_TARGETS, DRAG_ACTION

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GObject


class SectionItem(Gtk.HBox):

    __gsignals__ = {
        "remove-me": (GObject.SIGNAL_RUN_FIRST, None, []),
    }

    def __init__(self, word):
        Gtk.HBox.__init__(self)

        self.set_size_request(1, 20)
        self.set_border_width(2)

        if hasattr(self, "set_margin_start"):
            self.set_margin_start(20)
            self.set_margin_end(20)

        else:
            self.set_margin_left(20)
            self.set_margin_right(20)

        #self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.7,.7,.7,1))

        self.word = word

        self.label = Gtk.Label.new(word)
        self.label.modify_font(Pango.FontDescription("15"))
        self.pack_start(self.label, False, False, 0)

        self.button = Gtk.Button.new_from_icon_name("window-close", Gtk.IconSize.BUTTON)
        self.button.connect("clicked", self._clicked)
        self.pack_end(self.button, False, False, 0)

    def _clicked(self, button):
        self.emit("remove-me")


class Section(Gtk.VBox):

    __gsignals__ = {
        "restore-button": (GObject.SIGNAL_RUN_FIRST, None, [str]),
    }

    def __init__(self, type):
        Gtk.VBox.__init__(self)

        self.type = type

        self.label = Gtk.Label()
        self.label.modify_font(Pango.FontDescription("15"))
        self.label.props.xalign = 0
        self.pack_start(self.label, False, False, 10)

        scroll = Gtk.ScrolledWindow()
        self.pack_start(scroll, True, True, 0)

        self.vbox = Gtk.VBox()
        self.vbox.set_border_width(10)
        self.vbox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.5,.5,.5,1))
        self.vbox.drag_dest_set(Gtk.DestDefaults.ALL, DRAG_TARGETS, DRAG_ACTION)
        self.vbox.connect("drag-data-received", self.on_drag_data_received)
        scroll.add(self.vbox)

        if self.type == WordType.SYNONYM:
            self.label.set_text("Synonyms:")

        elif self.type == WordType.ANTONYM:
            self.label.set_text("Antonyms:")

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        item = SectionItem(data.get_text())
        item.connect("remove-me", self._remove_item)
        self.vbox.pack_start(item, False, False, 1)

        self.show_all()

    def _remove_item(self, item):
        self.emit("restore-button", item.word)
        self.vbox.remove(item)
        del item


class SynonymSection(Section):

    def __init__(self):
        Section.__init__(self, WordType.SYNONYM)


class AntonymSection(Section):

    def __init__(self):
        Section.__init__(self, WordType.ANTONYM)
