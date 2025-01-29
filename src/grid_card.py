# grid_card.py
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

import gi, json
from gi.repository import Gtk


@Gtk.Template(resource_path="/io/github/lo2dev/Nucleus/grid-card.ui")
class NucleusGridCard(Gtk.ToggleButton):
    __gtype_name__ = "NucleusGridCard"

    atomic_number = Gtk.Template.Child()
    symbol = Gtk.Template.Child()
    elem_property = Gtk.Template.Child()


    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.atomic_number.props.label = str(data['number'])
        self.symbol.props.label = data['symbol']

        atomic_mass = f"{data['atomic_mass']:.3f}"
        self.elem_property.props.label = atomic_mass.rstrip('0').rstrip('.')

