from rich.theme import Theme


dracula_theme = Theme(
    {
        # Structural
        "title":   "bold #bd93f9",   # purple
        "header":  "bold #f8f8f2",   # foreground white

        # Roles
        "agent":   "bold #ff79c6",   # pink
        "user":    "bold #50fa7b",   # green

        "provider": "bold #8be9fd",  # cyan
        "model":    "#f8f8f2",       # plain foreground

        "tool":    "bold #bd93f9",   # purple (distinct from agent pink)

        # Status
        "success": "bold #50fa7b",   # green
        "warning": "bold #f1fa8c",   # yellow
        "error":   "bold #ff5555",   # red

        # Secondary text
        "info":    "#8be9fd",        # cyan, no bold — keeps it calm
        "muted":   "#6272a4",        # comment gray-blue (Dracula's actual muted tone)
    }
)