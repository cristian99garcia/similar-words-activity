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

import cairo

from consts import WordType, DRAG_TARGETS, DRAG_ACTION

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf


class WordButton(Gtk.Button):

    __gsignals__ = {
        "remove-me": (GObject.SIGNAL_RUN_FIRST, None, []),
    }

    def __init__(self, type, word):
        Gtk.Button.__init__(self)

        self.type = type
        self.word = word

        self.set_label(self.word)
        self.set_border_width(2)

        self.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, DRAG_TARGETS, DRAG_ACTION)
        self.drag_source_set_icon_pixbuf(self.make_pixbuf())

        self.connect("drag-data-get", self.on_drag_data_get)

    def make_pixbuf(self):
        font_size = 38
        font_family = "Arial"

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
        context = cairo.Context(surface)
        context.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(font_size)

        (x, y, width, height, dx, dy) = context.text_extents(self.word)
        border = 15
        svg_width = width + border * 2
        svg_height = height + border * 2

        svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' +\
              ('<svg width="%d" height="%d">\n' % (svg_width, svg_height)) +\
              ('<rect x="0" y="0" width="%d" height="%d" fill="#FFFFFF"></rect>\n' % (svg_width, svg_height)) +\
              ('<text x="%d" y="%d" fill="balck" font-family="%s" font-size="%s">%s</text>\n' % (svg_width / 2 - width / 2, svg_height / 2 + height / 2, font_family, font_size, self.word)) +\
              '</svg>'

        loader = GdkPixbuf.PixbufLoader()
        loader.write(svg.encode())
        loader.close()
        pixbuf = loader.get_pixbuf()

        return pixbuf

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        data.set_text(self.word, -1)
        self.emit("remove-me")


class ButtonBox(Gtk.ButtonBox):

    def __init__(self):
        Gtk.ButtonBox.__init__(self)

        self.set_border_width(2)
        self.set_layout(Gtk.ButtonBoxStyle.CENTER)

        self.words = []

    def get_words_count(self):
        return len(self.words)

    def get_has_word(self, word):
        for type, _word in self.words:
            if word == _word:
                return True

        return False

    def append_word(self, type, word):
        self.words.append([type, word])

        button = WordButton(type, word)
        button.connect("remove-me", self.remove_button)
        self.add(button)
        self.show_all()

    def remove_button(self, button):
        button.hide()

    def restore_button_from_word(self, word):
        for button in self.get_children():
            if button.word == word:
                button.show_all()
                break
