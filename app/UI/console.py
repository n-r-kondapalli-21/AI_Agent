from rich.console import Console

# from app.UI.themes.default import default_theme 
# from app.UI.themes.matrix import matrix_theme
# from app.UI.themes.ocean import ocean_theme
# from app.UI.themes.cyberpunk import cyberpunk_theme
from app.UI.themes.dracula import dracula_theme

console = Console(
    theme = dracula_theme,
    soft_wrap = True,
    highlight = False,
)