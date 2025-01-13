# element_info.py
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
import re as regex
from gi.repository import Adw, Gtk, Gio
from .utils import get_category_color


@Gtk.Template(resource_path="/io/github/lo2dev/Elements/element-info.ui")
class ElementsElementInfo(Gtk.Box):
    __gtype_name__ = "ElementsElementInfo"

    element_card = Gtk.Template.Child()

    atomic_number = Gtk.Template.Child()
    element_symbol = Gtk.Template.Child()
    element_name = Gtk.Template.Child()
    element_property = Gtk.Template.Child()


    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.atomic_number.props.label = str(data['number'])
        self.element_symbol.props.label = data['symbol']
        self.element_name.props.label = data['name']
        self.element_property.props.label = data['category'].capitalize()
        get_category_color(self.element_card, data['category'], activatable=False)

        properties = {
            'General Properties': [
                'appearance',
                'atomic_mass',
                'summary',
            ],
            '': [
                'group',
                'period',
                'block'
            ],
            'Physical Properties': [
                'phase',
                'density',
                'melt',
                'boil',
                'molar_heat'
            ],
            'Other Properties': [
                'discovered_by',
                'named_by',

            ],
        }

        for category in properties:
            group = Adw.PreferencesGroup(title=category)

            for property in properties[category]:
                row = Adw.ActionRow(
                    title=regex.sub(r"_", " ", property.capitalize()),
                    subtitle=data[property] if data[property] else "-",
                    subtitle_selectable=True,
                    css_classes=['property'],
                )

                if property == 'phase':
                    if data[property] == "Gas":
                        row.add_suffix(Gtk.Image(icon_name="gas-symbolic"))
                    elif data[property] == "Solid":
                        row.add_suffix(Gtk.Image(icon_name="weight-symbolic"))
                    elif data[property] == "Liquid":
                        row.add_suffix(Gtk.Image(icon_name="liquid-symbolic"))
                elif property == 'appearance':
                    row.props.subtitle = row.props.subtitle.title()
                elif property == 'atomic_mass':
                    row.props.subtitle = f"{data[property]} u"

                group.add(row)

            self.append(group)

