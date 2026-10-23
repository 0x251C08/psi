# mypy: disable-error-code="arg-type,override"
"""TUI for interactive project initialization."""

from pathlib import Path
from typing import ClassVar

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    OptionList,
    Static,
)

from psi.commands.init import LANGUAGE_TEMPLATES, init_project


class InitTUI(App):
    """Interactive TUI for project initialization."""

    CSS = """
    Screen {
        layout: vertical;
    }
    #main {
        padding: 1 2;
    }
    #language-list {
        width: 40;
        height: 100%;
        border: solid $primary;
    }
    #framework-list {
        width: 50;
        height: 100%;
        border: solid $primary;
    }
    #details {
        width: 1fr;
        height: 100%;
        border: solid $primary;
        padding: 1;
    }
    .selected {
        background: $primary;
        color: $text;
    }
    #buttons {
        height: auto;
        margin-top: 1;
    }
    Button {
        margin-right: 1;
    }
    """

    BINDINGS: ClassVar[list[tuple[str, str, str]]] = [  # type: ignore[assignment]
        ("q", "quit", "Quit"),
        ("enter", "select", "Select"),
        ("left,right", "switch_panel", "Switch Panel"),
    ]

    def __init__(
        self,
        target_path: Path,
        name: str | None = None,
        force: bool = False,
    ):
        super().__init__()
        self.target_path = target_path
        self.project_name = name or target_path.name
        self.force = force
        self.selected_language: str | None = None
        self.selected_framework: str | None = None
        self.selected_css: str | None = None
        self.focused_panel = "language"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main"):
            with Horizontal():
                # Language selection
                with Vertical():
                    yield Label("Select Language", classes="panel-title")
                    yield OptionList(
                        *[ListItem(Label(f"{lang} - {info['description']}"), id=lang)
                          for lang, info in LANGUAGE_TEMPLATES.items()],
                        id="language-list",
                    )  # type: ignore[arg-type, override]

                # Framework selection
                with Vertical():
                    yield Label("Select Framework", classes="panel-title")
                    yield OptionList(id="framework-list")

                # Details panel
                with Vertical(id="details"):
                    yield Label("Project Details", classes="panel-title")
                    yield Static(id="details-content")

            with Horizontal(id="buttons"):
                yield Input(
                    placeholder=f"Project name (default: {self.project_name})",
                    value=self.project_name,
                    id="project-name-input",
                )
                yield Button("Create Project", id="create-btn", variant="primary")
                yield Button("Cancel", id="cancel-btn", variant="error")

        yield Footer()

    def on_mount(self) -> None:
        """Focus language list on mount."""
        self.query_one("#language-list", OptionList).focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection."""
        if event.option_list.id == "language-list":
            self.selected_language = event.option_list.get_option_at_index(event.option_index).id
            self._update_frameworks()
        elif event.option_list.id == "framework-list":
            self.selected_framework = event.option_list.get_option_at_index(event.option_index).id
            self._update_details()

    def _update_frameworks(self) -> None:
        """Update framework list based on selected language."""
        framework_list = self.query_one("#framework-list", OptionList)
        framework_list.clear_options()

        if not self.selected_language:
            return

        lang_info = LANGUAGE_TEMPLATES[self.selected_language]
        if "frameworks" in lang_info:
            for fw, desc in lang_info["frameworks"].items():
                framework_list.add_option(f"{fw} - {desc}", id=fw)  # type: ignore[call-arg]
            framework_list.index = 0  # type: ignore[attr-defined]
            self.selected_framework = next(iter(lang_info["frameworks"].keys()))
        else:
            self.selected_framework = "default"

        self._update_details()

    def _update_details(self) -> None:
        """Update details panel."""
        details = self.query_one("#details-content", Static)

        if not self.selected_language:
            details.update("Select a language to begin.")
            return

        lang_info = LANGUAGE_TEMPLATES[self.selected_language]

        content = f"[bold]Language:[/bold] {self.selected_language}\n"
        content += f"[bold]Description:[/bold] {lang_info['description']}\n\n"

        if self.selected_framework:
            if "frameworks" in lang_info and self.selected_framework in lang_info["frameworks"]:
                content += f"[bold]Framework:[/bold] {self.selected_framework}\n"
                desc = lang_info['frameworks'][self.selected_framework]
                content += f"[bold]Description:[/bold] {desc}\n\n"

            # Check for CSS options (webdev)
            if self.selected_language == "webdev" and "css_options" in lang_info:
                css_frameworks = ["vanilla", "typescript", "react", "vue", "svelte", "solid"]
                if self.selected_framework in css_frameworks:
                    content += "[bold]CSS Framework:[/bold] (will prompt on create)\n\n"

        content += f"[bold]Target:[/bold] {self.target_path / self.project_name}\n"

        details.update(content)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "create-btn":
            self._create_project()
        elif event.button.id == "cancel-btn":
            self.exit()

    def _create_project(self) -> None:
        """Create the project."""
        name_input = self.query_one("#project-name-input", Input)
        project_name = name_input.value or self.project_name

        # For webdev with certain frameworks, ask about CSS
        css_frameworks = ["vanilla", "typescript", "react", "vue", "svelte", "solid"]
        if self.selected_language == "webdev" and self.selected_framework in css_frameworks:
            self._prompt_css(project_name)
        else:
            self._do_create(project_name)

    def _prompt_css(self, project_name: str) -> None:
        """Prompt for CSS framework."""
        # Simple approach: just use vanilla CSS for now
        # In a full implementation, you'd show a modal
        default_css = "vanilla"
        framework = f"{self.selected_framework}-{default_css}"
        self._do_create(project_name, framework)

    def _do_create(self, project_name: str, framework: str | None = None) -> None:
        """Execute project creation."""
        if not self.selected_language:
            self.notify("Error: No language selected", severity="error")
            return
        try:
            init_project(
                self.selected_language,
                self.target_path,
                project_name,
                self.force,
            )
            self.exit(f"Project created at {self.target_path / project_name}")
        except Exception as e:
            self.notify(f"Error: {e}", severity="error")

    def action_switch_panel(self) -> None:
        """Switch focus between panels."""
        if self.focused_panel == "language":
            self.query_one("#framework-list", OptionList).focus()
            self.focused_panel = "framework"
        else:
            self.query_one("#language-list", OptionList).focus()
            self.focused_panel = "language"

    def action_quit(self) -> None:
        """Quit the app."""
        self.exit()
        # type: ignore[override]


def run_init_tui(target_path: Path, name: str | None = None, force: bool = False) -> None:
    """Run the init TUI."""
    app = InitTUI(target_path, name, force)
    app.run()
