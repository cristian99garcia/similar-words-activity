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

from utils import get_words, get_word_type
from consts import WordType
from buttonbox import ButtonBox
from sections import SimilarSection
from sections import DifferentSection

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from gi.repository import Pango
from gi.repository import GObject


class WordsBox(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.set_size_request(1, 200)

        self.label = Gtk.Label.new("The word is...")
        self.label.modify_font(Pango.FontDescription("Bold 32"))
        self.pack_start(self.label, False, False, 10)

        self.time_label = Gtk.Label.new("")
        self.time_label.modify_font(Pango.FontDescription("Bold 18"))
        self.pack_start(self.time_label, False, False, 0)

        self.word = None
        self.words = []
        self.boxes = []
        self.boxes_limit = 10
        self.start_count = 0
        self.time_limit = 30
        self.time_count = 0
        self.in_game = False

        scroll = Gtk.ScrolledWindow()
        scroll.set_size_request(1, 100)
        self.pack_start(scroll, False, False, 10)

        self.boxes_section = Gtk.VBox()
        scroll.add(self.boxes_section)

        hbox = Gtk.HBox()
        hbox.set_border_width(15)
        self.pack_start(hbox, True, True, 0)

        self.similar_section = SimilarSection()
        self.similar_section.connect("restore-button", self._restore_button)
        hbox.pack_start(self.similar_section, True, True, 2)

        self.different_section = DifferentSection()
        self.different_section.connect("restore-button", self._restore_button)
        hbox.pack_start(self.different_section, True, True, 2)

        bbox = Gtk.ButtonBox()
        bbox.set_layout(Gtk.ButtonBoxStyle.CENTER)
        self.pack_start(bbox, False, False, 10)

        self.stop_button = Gtk.Button("I finish!")
        self.stop_button.set_sensitive(False)
        self.stop_button.connect("clicked", self._force_stop)
        bbox.add(self.stop_button)

        self.start()
        self.show_all()

    def _restore_button(self, section, word):
        for box in self.boxes:
            if box.get_has_word(word):
                box.restore_button_from_word(word)
                break

    def start(self):
        self.start_count = 3
        self.time_count = self.time_limit

        GObject.timeout_add(1000, self._start_timeout)

    def _force_stop(self, button):
        self.time_count = 0
        self.in_game = False
        self.game_over()

    def _start_timeout(self):
        if self.start_count == 0:
            self.in_game = True
            self.select_words()
            self.show_buttons()
            self.stop_button.set_sensitive(True)

            GObject.timeout_add(1000, self._time_timeout)

            return False

        elif self.start_count == 3:
            self.in_game = True
            self.time_label.set_text("Ready")

        elif self.start_count == 2:
            self.time_label.set_text("Set")

        elif self.start_count == 1:
            self.time_label.set_text("Go!")

        self.start_count -= 1

        return True

    def _time_timeout(self):
        if not self.in_game:
            return False

        if self.time_count == 0:
            self.game_over()
            return False

        self.time_count -= 1
        self.time_label.set_text("Time left: %d" % self.time_count)

        return True

    def select_words(self):
        self.word, self.words = get_words()
        self.label.set_text(self.word)

    def make_box(self):
        box = ButtonBox()
        self.boxes_section.pack_start(box, False, True, 0)
        self.boxes.append(box)

        self.show_all()

    def show_buttons(self):
        for box in self.boxes:
            self.remove(box)
            del box

        self.make_box()

        for type, word in self.words:
            box = self.boxes[-1]
            if box.get_words_count() == self.boxes_limit:
                self.make_box()
                box = self.boxes[-1]

            box.append_word(type, word)

        self.show_all()

    def game_over(self):
        matched = 0
        self.boxes_section.set_sensitive(False)
        self.similar_section.vbox.set_sensitive(False)
        self.different_section.vbox.set_sensitive(False)
        self.stop_button.set_sensitive(False)

        for word in self.similar_section.get_words():
            if get_word_type(self.words, word) == WordType.SIMILAR:
                self.similar_section.set_correct_word(word)
                matched += 1

            else:
                self.similar_section.set_incorrect_word(word)

        for word in self.different_section.get_words():
            if get_word_type(self.words, word) == WordType.DIFFERENT:
                self.different_section.set_correct_word(word)
                matched += 1

            else:
                self.different_section.set_incorrect_word(word)

        self.label.set_text("You matched %d of %d words" % (matched, len(self.words)))
        self.time_label.set_text("Time ended!")

        GObject.timeout_add(3000, self._restart)

    def _restart(self):
        self.boxes_section.set_sensitive(True)

        while len(self.boxes_section.get_children()) > 0:
            self.boxes_section.remove(self.boxes_section.get_children()[0])

        self.similar_section.vbox.set_sensitive(True)
        self.similar_section.clear()

        self.different_section.vbox.set_sensitive(True)
        self.different_section.clear()

        self.label.set_label("The word is...")
        self.time_label.set_label("Ready")

        self.start()

        return False
