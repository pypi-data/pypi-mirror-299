from typing import Optional
from rich.console import RenderableType
from textual.reactive import reactive
from textual.widget import Widget
from smassh.src import generate_figlet
from smassh.ui.events import SetScreen


class NavItemBase(Widget):
    """
    Base Widget for Header NavItems
    """

    DEFAULT_CSS = """
    NavItemBase {
        content-align: center middle;
        height: auto;
        width: auto;
        padding: 0 1;
    }
    """

    def __init__(self, text: str, screen_name: Optional[str] = None) -> None:
        super().__init__()
        self.text = text
        self.screen_name = screen_name

    def on_click(self) -> None:
        if self.screen_name:
            self.post_message(SetScreen(self.screen_name))

    def render(self) -> RenderableType:
        return self.text


class Banner(NavItemBase):
    """
    Text Widget to render text in a bigger font
    """

    DEFAULT_CSS = """
    Banner {
        height: 100%;
    }
    """

    is_tall = reactive(True, layout=True, always_update=True)

    def watch_is_tall(self, value: bool) -> None:
        self.styles.height = "5" if value else "3"

    def render(self) -> RenderableType:
        return generate_figlet(self.text) if self.is_tall else self.text.upper()


class NavItem(NavItemBase):
    """
    Just a label widget with a callback
    """
