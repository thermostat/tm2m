
## TMUX 2nd Memory ##

Tools for retaining/remembering valuable command-line history using TMUX.

Installing this tool creates two commands: `tm2m` for adding history
items, and `tm2m_pick` for using a curses-based picker to select the
history item and optionally add it to your tmux buffer.

## TODO ##

1. Add timestamp, and some aggregate "score" to HistoryItems, allowing
for better sorting.
1. Add default tmux window name to adding history.
1. Real support for "named" sessions, not just bash/zsh, etc.
