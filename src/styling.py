"""Terminal styling utilities for better output formatting"""

class Colors:
    # Basic colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

def success(text):
    return f"{Colors.BRIGHT_GREEN}✓{Colors.RESET} {text}"

def error(text):
    return f"{Colors.BRIGHT_RED}✗{Colors.RESET} {text}"

def warning(text):
    return f"{Colors.BRIGHT_YELLOW}⚠{Colors.RESET} {text}"

def info(text):
    return f"{Colors.BRIGHT_BLUE}ℹ{Colors.RESET} {text}"

def step(num, total, text):
    return f"{Colors.BRIGHT_CYAN}[{num}/{total}]{Colors.RESET} {text}"

def bold(text):
    return f"{Colors.BOLD}{text}{Colors.RESET}"

def dim(text):
    return f"{Colors.DIM}{text}{Colors.RESET}"

def header(text):
    line = "═" * len(text)
    return f"\n{Colors.BOLD}{Colors.BRIGHT_CYAN}{line}\n{text}\n{line}{Colors.RESET}\n"

def box(title, content, status="info"):
    color_map = {
        "success": Colors.BRIGHT_GREEN,
        "error": Colors.BRIGHT_RED,
        "warning": Colors.BRIGHT_YELLOW,
        "info": Colors.BRIGHT_BLUE
    }
    color = color_map.get(status, Colors.BRIGHT_BLUE)
    
    lines = content.split('\n')
    max_len = max(len(line) for line in lines + [title])
    width = max_len + 4
    
    output = f"\n{color}┌{'─' * (width - 2)}┐{Colors.RESET}\n"
    output += f"{color}│{Colors.RESET} {Colors.BOLD}{title}{Colors.RESET}{' ' * (width - len(title) - 3)}{color}│{Colors.RESET}\n"
    output += f"{color}├{'─' * (width - 2)}┤{Colors.RESET}\n"
    
    for line in lines:
        output += f"{color}│{Colors.RESET} {line}{' ' * (width - len(line) - 3)}{color}│{Colors.RESET}\n"
    
    output += f"{color}└{'─' * (width - 2)}┘{Colors.RESET}\n"
    return output

def progress_bar(current, total, width=30):
    filled = int(width * current / total)
    bar = '█' * filled + '░' * (width - filled)
    percent = int(100 * current / total)
    return f"{Colors.BRIGHT_CYAN}[{bar}]{Colors.RESET} {percent}%"

def table(headers, rows):
    """Create a formatted table"""
    col_widths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]
    
    def format_row(row, is_header=False):
        formatted = " │ ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))
        if is_header:
            return f"{Colors.BOLD}{formatted}{Colors.RESET}"
        return formatted
    
    separator = "─┼─".join("─" * w for w in col_widths)
    
    output = "\n┌─" + "─┬─".join("─" * w for w in col_widths) + "─┐\n"
    output += "│ " + format_row(headers, True) + " │\n"
    output += "├─" + separator + "─┤\n"
    
    for row in rows:
        output += "│ " + format_row(row) + " │\n"
    
    output += "└─" + "─┴─".join("─" * w for w in col_widths) + "─┘\n"
    return output
