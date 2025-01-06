# utils.py
#
# Copyright 2024 Lo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

def get_category_color(card, category: str, activatable: bool = True):
    color: str = ""

    if category == 'diatomic nonmetal' or category == 'polyatomic nonmetal':
        color = "green"

    match category:
        case 'alkali metal':
            color = "red"
        case 'transition metal':
            color = "blue"
        case 'noble gas':
            color = "orange"
        case 'metalloid':
            color = "yellow"
        case 'alkaline earth metal':
            color = "purple"
        case 'lanthanide':
            color = "teal"
        case 'post-transition metal':
            color = "pink"
        case 'actinide':
            color = "slate"

    if not color == "":
        if activatable:
            card.add_css_class("suggested-action")
            card.add_css_class(color)
        else:
            card.add_css_class(f"elements-{color}")

