import gc
import random
import asyncio
import json
import rio
import rio.components.class_container
import rio.data_models
import rio.debug
import rio.debug.dev_tools
import rio.debug.dev_tools.dev_tools_connector
import rio.debug.dev_tools.icons_page
import rio.debug.dev_tools.layout_display
import rio.debug.layouter


def filter_function(component: rio.Component) -> bool:
    # Don't care about the connection lost popup
    # if type(component).__name__ == "DefaultConnectionLostComponent":
    #     return False

    # Everything else is fine
    return True


class LoginBox(rio.Component):
    TEXT_STYLE = rio.TextStyle(fill=rio.Color.from_hex("02dac5"), font_size=0.9)

    def build(self) -> rio.Component:
        return rio.Rectangle(
            content=rio.Column(
                rio.TextInput(
                    text="",
                    label="Benutzername",
                    accessibility_label="Benutzername",
                    min_height=0.5,
                ),
                rio.TextInput(
                    text="",
                    label="Passwort",
                    accessibility_label="Passwort",
                    is_secret=True,
                ),
                rio.Column(
                    rio.Row(
                        rio.Button(
                            rio.Text("LOGIN", style=self.TEXT_STYLE),
                            shape="rectangle",
                            style="minor",
                            color="secondary",
                            margin_bottom=0.4,
                        )
                    ),
                    rio.Row(
                        rio.Button(
                            rio.Text("REG", style=self.TEXT_STYLE),
                            shape="rectangle",
                            style="minor",
                            color="secondary",
                        ),
                        rio.Spacer(),
                        rio.Button(
                            rio.Text("LST PWD", style=self.TEXT_STYLE),
                            shape="rectangle",
                            style="minor",
                            color="secondary",
                        ),
                        proportions=(49, 2, 49),
                    ),
                ),
                spacing=0.4,
            ),
            fill=rio.Color.TRANSPARENT,
            align_x=0.5,
            align_y=0.5,
        )


class MyRoot(rio.Component):
    messages: list[str] = [
        "Initial",
    ]
    text_value: str = "<->"
    number_value: float = 0

    is_on: bool = False

    entries: list[int] = list(range(10))

    async def on_randomize(self) -> None:
        random.shuffle(self.entries)
        await self.force_refresh()

    async def _find_dead_components(self) -> None:
        try:
            import objgraph  # type: ignore
        except ImportError:
            print("Please install `objgraph`")
            return
        key = ("Foobar",)
        # Make sure only real problem components exist
        gc.collect()

        # Find all components present in the app
        alive_component_ids: set[int] = set()
        to_do: list[rio.Component] = [self.session._root_component]

        while to_do:
            component = to_do.pop()
            alive_component_ids.add(id(component))
            to_do.extend(component._iter_direct_children_())

        # Find all components which are alive according to Python, but aren't
        # part of the app
        zombie_component_ids: set[int] = (
            set(self.session._weak_components_by_id.keys())
            - alive_component_ids
        )

        # Select one component to debug
        component = None

        for cmp_id, component in self.session._weak_components_by_id.items():
            if cmp_id not in zombie_component_ids:
                continue

            if isinstance(component, rio.debug.dev_tools.icons_page.IconsPage):
                gc.collect()
                objgraph.show_backrefs(
                    [component],
                    filename="/home/jakob/Downloads/sample-graph.png",
                    max_depth=10,
                )

    def build_dialog(self) -> rio.Component:
        return rio.Card(
            rio.Button(
                "Hello, World!",
                on_press=lambda: print("Hello, World!"),
                margin=3,
            ),
            align_x=0.5,
            align_y=0.5,
        )

    async def on_press(self) -> None:
        self.is_on = not self.is_on

    async def on_button_press(self) -> None:
        await self.session.set_clipboard("Hello, World!")

    def build(self) -> rio.Component:
        return rio.Popup(
            anchor=rio.Button(
                "Toggle Popup",
                on_press=self.on_press,
            ),
            content=rio.Text("I'm here!"),
            is_open=self.is_on,
            # is_open=True,
            align_x=0.5,
            align_y=0.5,
            position="top",
        )

        table = rio.Table(
            # pd.DataFrame(
            {
                "a": [1, 2, 3],
                "b": [4, 5, 6],
                "c": [7, 8, 9],
                "d": [10, 11, 12],
            }
            # ),
        )

        table["header", -2:].style(
            font_weight="bold",
        )

        table[:2, 0].style(
            font_weight="bold",
        )

        return table

        return rio.Column(
            # blabla
            *([] if self.content is None else [self.content])
            # blabla
        )

        return rio.Column(
            # blabla
            rio.Switcher(self.content),
            # blabla
        )

        return rio.Button(
            "Open Dialog",
            on_press=self.on_press,
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Row(
            rio.Popup(
                anchor=rio.Button(
                    "Toggle Popup",
                    on_press=lambda: setattr(self, "is_on", not self.is_on),
                ),
                content=rio.Button(
                    "Toggle Popup",
                    on_press=lambda: setattr(self, "is_on", not self.is_on),
                    margin=1,
                ),
                position="left",
                gap=10,
                # alignment=1,
                is_open=self.is_on,
                align_x=0.5,
                align_y=0.5,
            ),
            rio.Tooltip(
                anchor=rio.Text("Hover for Tooltip"),
                tip=rio.Text("This is a tooltip"),
                align_x=0.5,
                align_y=0.5,
            ),
            spacing=3,
        )

        return rio.Column(
            rio.FlowContainer(
                *[
                    rio.Text(
                        f"Entry {ii}",
                        key=f"entry_{ii}",
                        margin=0.5,
                    )
                    for ii in self.entries
                ],
                grow_y=True,
            ),
            rio.Button(
                "Randomize",
                on_press=self.on_randomize,
            ),
        )


ALL_IMAGES = [
    rio.URL(
        "https://fastly.picsum.photos/id/13/2500/1667.jpg?hmac=SoX9UoHhN8HyklRA4A3vcCWJMVtiBXUg0W4ljWTor7s"
    ),
    rio.URL(
        "https://fastly.picsum.photos/id/19/2500/1667.jpg?hmac=7epGozH4QjToGaBf_xb2HbFTXoV5o8n_cYzB7I4lt6g"
    ),
    rio.URL(
        "https://fastly.picsum.photos/id/28/4928/3264.jpg?hmac=GnYF-RnBUg44PFfU5pcw_Qs0ReOyStdnZ8MtQWJqTfA"
    ),
    rio.URL(
        "https://fastly.picsum.photos/id/29/4000/2670.jpg?hmac=rCbRAl24FzrSzwlR5tL-Aqzyu5tX_PA95VJtnUXegGU"
    ),
]


class MyRoot(rio.Component):
    def _on_file(self, file: rio.FileInfo) -> None:
        print(f"Got file {file.name} with size {file.size_in_bytes}")

    def build(self) -> rio.Component:
        return rio.Column(
            rio.TextInput(
                text="Foobar",
            ),
            rio.TextInput(
                text="Foobar",
                style="rounded",
            ),
            rio.TextInput(
                text="Foobar",
                style="pill",
            ),
            rio.Text(
                "Foobar",
                justify="center",
                style=rio.TextStyle(),
            ),
            rio.Text(
                "Foobar",
                justify="center",
                style=rio.TextStyle(
                    underlined=True,
                ),
            ),
            rio.Text(
                "Foobar",
                justify="center",
                style=rio.TextStyle(
                    strikethrough=True,
                ),
            ),
            rio.Text(
                "Foobar",
                justify="center",
                style=rio.TextStyle(
                    underlined=True,
                    strikethrough=True,
                ),
            ),
            spacing=0.5,
            min_width=10,
            align_x=0.5,
            align_y=0.5,
        )

        return rio.ColorPicker(
            color=rio.Color.RED,
        )

        file_types = [
            # "pdf",
            # "doc",
            # "jpeg",
            # "mp3",
            "ogg",
            "mkv",
        ]

        # return rio.Column(
        #     rio.FilePickerArea(
        #         file_types=file_types,
        #         on_file_upload=self._on_file,
        #     ),
        #     rio.FilePickerArea(
        #         file_types=file_types,
        #         on_file_upload=self._on_file,
        #         min_width=80,
        #         min_height=30,
        #     ),
        #     spacing=8,
        #     align_x=0.5,
        #     align_y=0.5,
        # )

        return rio.Button(
            "Open Dialog",
            style="colored-text",
            on_press=lambda: self.session.show_yes_no_dialog(
                "Heyho?",
                owning_component=self,
            ),
            align_x=0.5,
            align_y=0.35,
        )


class ThemeSample(rio.Component):
    theme: rio.Theme

    async def _apply_theme_worker(self) -> None:
        # Wait for a bit to ensure the client has time to update the HTML
        await asyncio.sleep(0.2)

        # Get all variables to apply
        light_or_dark = "light" if self.theme.is_light_theme else "dark"
        theme_vars = self.session._calculate_theme_css_values(self.theme)

        # Apply the theme
        await self.session._evaluate_javascript(
            f"""
let themeVars = {json.dumps(theme_vars)};

let elem = globalThis.componentsById[{self._id}].element;

for (let key in themeVars) {{
    elem.style.setProperty(
        key,
        themeVars[key],
    );
}}

// Set the theme variant
document.documentElement.setAttribute(
    "data-theme",
    {json.dumps(light_or_dark)}
);

            """
        )

    def build(self) -> rio.Component:
        # Apply the theme
        asyncio.create_task(
            self._apply_theme_worker(),
        )

        # Build the content
        content = rio.Row(
            # Main Content
            rio.Column(
                rio.Text(
                    "Lorem Ipsum",
                    style="heading1",
                ),
                rio.Markdown(
                    """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec
ultricies elit. Nullam nec ultricies elit. Nullam nec ultricies elit.
                    """,
                ),
                rio.Image(
                    rio.URL("https://picsum.photos/300/200"),
                    min_width=26,
                    min_height=14,
                    corner_radius=self.theme.corner_radius_medium,
                ),
                rio.Markdown(
                    """
Lorem markdownum auctor fiant aversa, scopulos bos ima ruptosque turbam, fertur
flexile amictu temptaretque *superum temptarunt* volatu ad veros. Fatebor
Aesacos.

```js
rom_root(record);
direct = subdirectory(symbolic_restore_t, url);
```

Coniuge et tamen et omnibus ille concordant mitissima accedere fratrem
auditurum, spes petunt ore insigne mille. Te explorant ardor, dies inde eloquio
rostrum vestemque et frustra purum. Cynthia quoniam dextra aequoris, emissi [in
                    """,
                ),
                grow_x=True,
            ),
            # (Fake) Drawer
            rio.ThemeContextSwitcher(
                content=rio.Rectangle(
                    content=rio.Grid(
                        rio.Text(
                            "Drawer Heading",
                            style="heading2",
                        ),
                        rio.TextInput(
                            text="Foobar",
                            style="rounded",
                        ),
                        [
                            rio.Text("Switch"),
                            rio.Switch(),
                        ],
                        [
                            rio.Button("Major", style="major"),
                            rio.Button("Minor", style="minor"),
                        ],
                        [
                            rio.Button("Colored Text", style="colored-text"),
                            rio.Button("Plain Text", style="plain-text"),
                        ],
                        rio.Spacer(),
                        rio.Separator(),
                        rio.Row(
                            rio.Icon("material/castle"),
                            rio.Text(
                                "Castles are Cool",
                                grow_x=True,
                            ),
                            spacing=0.5,
                        ),
                        row_spacing=1,
                        column_spacing=1,
                        margin=2,
                    ),
                    fill=self.theme.neutral_color,
                    corner_radius=(
                        self.theme.corner_radius_large,
                        0,
                        0,
                        self.theme.corner_radius_large,
                    ),
                    shadow_color=self.theme.shadow_color,
                    shadow_radius=1.3,
                ),
                color="neutral",
            ),
            spacing=1,
        )

        # Wrap up the content
        #
        # A rectangle acts as a fake background
        return rio.Rectangle(
            # A Theme context switcher ensures that the theme variables are
            # locally exposed.
            content=rio.ThemeContextSwitcher(
                content=content,
                color="background",
            ),
            fill=self.theme.background_color,
        )


class ThemeViewer(rio.Component):
    def build(self) -> rio.Component:
        # Decide on the colors to use
        theme_colors: list[rio.Color] = [
            self.session.theme.primary_color,
            rio.Color.RED,
            rio.Color.GREEN,
            rio.Color.YELLOW,
        ]

        # Create the themes
        light_viewers: list[ThemeSample] = []
        dark_viewers: list[ThemeSample] = []

        for col in theme_colors:
            light_theme, dark_theme = rio.Theme.pair_from_colors(
                primary_color=col,
            )

            light_viewers.append(ThemeSample(theme=light_theme))
            dark_viewers.append(ThemeSample(theme=dark_theme))

        # Populate
        return rio.Grid(
            light_viewers,
            dark_viewers,
            row_spacing=0.4,
            column_spacing=0.4,
        )


app = rio.App(
    # Uncomment this line to enable the custom navigation
    build=ThemeViewer,
    theme=rio.Theme.pair_from_colors(),
    default_attachments=[],
)
