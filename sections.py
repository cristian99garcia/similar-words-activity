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

from utils import make_pixbuf
from consts import WordType, DRAG_TARGETS, DRAG_ACTION, CORRECT_COLOR, INCORRECT_COLOR, SECTION_BG_COLOR

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GObject


class SectionItem(Gtk.EventBox):

    __gsignals__ = {
        "change-me": (GObject.SIGNAL_RUN_FIRST, None, []),
        "remove-me": (GObject.SIGNAL_RUN_FIRST, None, []),
    }

    def __init__(self, word):
        Gtk.EventBox.__init__(self)

        self.word = word

        self.set_size_request(1, 20)
        self.set_border_width(2)

        if hasattr(self, "set_margin_start"):
            self.set_margin_start(20)
            self.set_margin_end(20)

        else:
            self.set_margin_left(20)
            self.set_margin_right(20)

        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, DRAG_TARGETS, DRAG_ACTION)
        self.drag_source_set_icon_pixbuf(make_pixbuf(self.word))

        #self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.7,.7,.7,1))

        self.hbox = Gtk.HBox()
        self.add(self.hbox)

        self.label = Gtk.Label.new(word)
        self.label.modify_font(Pango.FontDescription("15"))
        self.hbox.pack_start(self.label, False, False, 0)

        self.button = Gtk.Button.new_from_icon_name("window-close", Gtk.IconSize.BUTTON)
        self.button.connect("clicked", self._clicked)
        self.hbox.pack_end(self.button, False, False, 0)

        self.connect("drag-data-get", self.on_drag_data_get)

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        data.set_text(self.word, -1)
        self.emit("change-me")

    def _clicked(self, button):
        self.emit("remove-me")

    def set_correct(self):
        self.label.override_color(Gtk.StateFlags.INSENSITIVE, CORRECT_COLOR)

    def set_incorrect(self):
        self.label.override_color(Gtk.StateFlags.INSENSITIVE, INCORRECT_COLOR)


class Section(Gtk.VBox):

    __gsignals__ = {
        "restore-button": (GObject.SIGNAL_RUN_FIRST, None, [str]),
    }

    def __init__(self, type):
        Gtk.VBox.__init__(self)

        self.type = type
        self.items = []

        self.label = Gtk.Label()
        self.label.modify_font(Pango.FontDescription("15"))
        self.label.props.xalign = 0
        self.pack_start(self.label, False, False, 10)

        scroll = Gtk.ScrolledWindow()
        self.pack_start(scroll, True, True, 0)

        self.vbox = Gtk.VBox()
        self.vbox.set_border_width(10)
        self.vbox.override_background_color(Gtk.StateType.NORMAL, SECTION_BG_COLOR)
        self.vbox.drag_dest_set(Gtk.DestDefaults.ALL, DRAG_TARGETS, DRAG_ACTION)
        self.vbox.connect("drag-data-received", self.on_drag_data_received)
        scroll.add(self.vbox)

        if self.type == WordType.SYNONYM:
            self.label.set_text("Synonyms:")

        elif self.type == WordType.ANTONYM:
            self.label.set_text("Antonyms:")

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        item = SectionItem(data.get_text())
        item.connect("change-me", self._change_item)
        item.connect("remove-me", self._remove_item)
        self.vbox.pack_start(item, False, False, 1)

        self.items.append(item)

        self.show_all()

    def _change_item(self, item):
        self.vbox.remove(item)
        del item

    def _remove_item(self, item):
        self.emit("restore-button", item.word)
        self.vbox.remove(item)
        del item

    def get_words(self):
        words = [item.word for item in self.items]
        return words

    def set_correct_word(self, word):
        for item in self.items:
            if item.word == word:
                item.set_correct()
                break

    def set_incorrect_word(self, word):
        for item in self.items:
            if item.word == word:
                item.set_incorrect()
                break

    def clear(self):
        while len(self.items) > 0:
            for item in self.items:
                self.vbox.remove(item)
                self.items.remove(item)
                del item


class SynonymSection(Section):

    def __init__(self):
        Section.__init__(self, WordType.SYNONYM)


class AntonymSection(Section):

    def __init__(self):
        Section.__init__(self, WordType.ANTONYM)
