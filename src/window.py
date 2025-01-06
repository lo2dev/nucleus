# window.py
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
from gi.repository import Adw, Gtk, Gio


from .grid_card import ElementsGridCard
from .element_info import ElementsElementInfo
from .utils import get_category_color


@Gtk.Template(resource_path="/io/github/lo2dev/Elements/window.ui")
class ElementsWindow(Adw.ApplicationWindow):
    __gtype_name__ = "ElementsWindow"

    periodic_table = Gtk.Template.Child()
    split_view = Gtk.Template.Child()
    sidebar_scrolled_window = Gtk.Template.Child()
    close_sidebar_button = Gtk.Template.Child()
    source_button = Gtk.Template.Child()

    last_selected_element: Gtk.ToggleButton = None
    element_source_link: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        data_file = Gio.resources_lookup_data(
            "/io/github/lo2dev/Elements/PeriodicTableJSON.json",
            Gio.ResourceLookupFlags.NONE,
        )

        decoded_text = data_file.unref_to_array().decode("utf-8")
        json_file = json.loads(decoded_text)

        for element in json_file["elements"]:
            card = ElementsGridCard(element)
            get_category_color(card, element['category'])

            card.connect("clicked", self.on_grid_card_clicked, element)

            self.periodic_table.attach(
                card,
                element['xpos'],
                element['ypos'],
                width=1,
                height=1
            )

        #Grid numbers
        for number in range(1, 19):
            self.periodic_table.attach(
                child=Gtk.Label(
                    label=number,
                ),
                column=number,
                row=0,
                width=1,
                height=1
            )

        for number in range(1, 9):
            self.periodic_table.attach(
                child=Gtk.Label(
                    label=number,
                ),
                column=0,
                row=number,
                width=1,
                height=1
            )

        # example_card = ElementsGridCard(
        #     data = {
        #         "number": 1,
        #         "symbol": "H",
        #         "name": "Hydrogen",
        #         "atomic_mass": 1.008
        #     }
        # )

        # legend = ElementsGridCard(
        #     data = {
        #         "number": "Atomic Number",
        #         "symbol": "Symbol",
        #         "name": "Name",
        #         "atomic_mass": "Atomic Mass"
        #     },
        #     legend=True
        # )
        #self.periodic_table.attach(example_card, 7, 2, width=1, height=1)
        #self.periodic_table.attach(legend, 8, 2, width=1, height=1)

        #self.split_view.connect("notify::show-sidebar", self.on_show_sidebar_changed)
        self.source_button.connect(
            "clicked",
            lambda _: Gtk.UriLauncher(uri=self.element_source_link).launch(
                self, None
            ),
        )


    def on_close_sidebar(self, _clicked_button, last_selected_element) -> None:
        last_selected_element.props.active = False
        self.split_view.props.show_sidebar = False


    def on_show_sidebar_changed(self, split_view, is_open):
        if split_view.props.show_sidebar == False:
            self.last_selected_element.props.active = False


    def on_grid_card_clicked(self, button, element_data):
        if self.last_selected_element == None:
            self.last_selected_element = button

        if button != self.last_selected_element:
            self.last_selected_element.props.active = False
            self.last_selected_element = button

            if self.split_view.props.show_sidebar == False:
                self.split_view.props.show_sidebar = True

            self.load_chem_info(element_data)

        elif button == self.last_selected_element:
            if self.split_view.props.show_sidebar == False:
                self.load_chem_info(element_data)
                self.split_view.props.show_sidebar = True
            else:
                self.split_view.props.show_sidebar = False

        self.close_sidebar_button.connect(
            "clicked",
            self.on_close_sidebar,
            self.last_selected_element
        )


    def load_chem_info(self, data) -> None:
        self.element_source_link = data['source']
        info = ElementsElementInfo(data)
        self.sidebar_scrolled_window.props.child = info

