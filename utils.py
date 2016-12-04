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
import random
from consts import WORDS_DATA

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import GdkPixbuf


def make_pixbuf(word):
    font_size = 38
    font_family = "Arial"

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 200, 200)
    context = cairo.Context(surface)
    context.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size)

    (x, y, width, height, dx, dy) = context.text_extents(word)
    border = 15
    svg_width = width + border * 2
    svg_height = height + border * 2

    svg = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' +\
          ('<svg width="%d" height="%d">\n' % (svg_width, svg_height)) +\
          ('<rect x="0" y="0" width="%d" height="%d" fill="#FFFFFF"></rect>\n' % (svg_width, svg_height)) +\
          ('<text x="%d" y="%d" fill="balck" font-family="%s" font-size="%s">%s</text>\n' % (svg_width / 2 - width / 2, svg_height / 2 + height / 2, font_family, font_size, word)) +\
          '</svg>'

    loader = GdkPixbuf.PixbufLoader()
    loader.write(svg.encode())
    loader.close()
    pixbuf = loader.get_pixbuf()

    return pixbuf


def get_words():
    word = WORDS_DATA.keys()[random.randint(0, len(WORDS_DATA) - 1)]
    words = WORDS_DATA[word]
    random.shuffle(words)

    return word, words


def get_word_type(words, word):
    for data in words:
        if data[1] == word:
            return data[0]


def make_separator(expand=True):
    separator = Gtk.SeparatorToolItem()
    separator.props.draw = not expand
    separator.set_expand(expand)

    return separator
