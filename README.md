# 🐚 Mini Shell

A simple, lightweight command-line interface (CLI) built in Python that provides basic shell functionality with support for aliases and reverse search.

## ✨ Features

- **Basic Shell Commands**: Navigate directories, list files, and execute system commands
- **Alias Support**: Create shortcuts for frequently used commands
- **Command History**: Navigate through previous commands using arrow keys
- **Reverse Search**: Press `Ctrl+R` to search through command history
- **Colored Output**: Directories and executables are color-coded
- **Persistent Configuration**: Aliases and history saved between sessions

---

## 🚀 Installation

**Prerequisites:** Python 3.6 or higher

```bash
# Make executable
chmod +x mini_shell.py

# Run the shell
python3 mini_shell.py
```

---

## 🛠️ Built-in Commands

| Command | Description | Example |
|---------|-------------|---------|
| `cd [dir]` | Change directory | `cd ~/Documents` |
| `pwd` | Print working directory | `pwd` |
| `ls [path]` | List directory contents | `ls /home` |
| `echo [text]` | Print text to screen | `echo Hello` |
| `clear` | Clear terminal screen | `clear` |
| `history` | Show command history | `history` |
| `history -c` | Clear command history | `history -c` |
| `alias [name=value]` | Create/show aliases | `alias ll='ls -la'` |
| `unalias [name]` | Remove an alias | `unalias ll` |
| `help` | Show available commands | `help` |
| `exit` or `quit` | Exit the shell | `exit` |

### Pre-configured Aliases
- `ll` → `ls -la`
- `la` → `ls -a`
- `..` → `cd ..`
- `...` → `cd ../..`
- `home` → `cd ~`
- `h` → `history`

---

## 🔥 Advanced Features

### Reverse Search (Ctrl+R)
1. Press `Ctrl+R`
2. Start typing part of a previous command
3. Press `Ctrl+R` again to cycle through matches
4. Press `Enter` to execute or `Ctrl+C` to cancel

### Command History Navigation
- **Up Arrow** (↑): Previous command
- **Down Arrow** (↓): Next command

### External Commands
Run any system command not built into the shell:
```bash
python3 script.py
git status
cat file.txt
```

---

## 📁 Configuration Files

### `~/.minishell_config.json`
Stores aliases (auto-created on first run):
```json
{
  "aliases": {
    "ll": "ls -la",
    "proj": "cd ~/projects"
  }
}
```

### `~/.minishell_history`
Stores command history (plain text, one command per line)

---

## 🏗️ Architecture

### Class Structure
```
MiniShell
├── __init__()           # Initialize shell
├── setup_readline()     # Configure history/reverse search
├── load/save_config()   # Handle aliases
├── load/save_history()  # Handle command history
├── parse_command()      # Expand aliases
├── execute_builtin()    # Run built-in commands
├── execute_external()   # Run system commands
└── run()                # Main shell loop
```

### Execution Flow
```
User Input → readline → parse_command → execute_command
                                            ↓
                            ┌───────────────┴────────────────┐
                            ↓                                ↓
                     execute_builtin()              execute_external()
```

---

## 🎯 Example Session

```bash
$ python3 mini_shell.py

user@computer:~$ pwd
/home/user

user@computer:~$ cd Documents
user@computer:~/Documents$ ls
file1.txt  file2.txt  project/

user@computer:~/Documents$ alias myproj='cd ~/Documents/project'
Alias created: myproj='cd ~/Documents/project'

user@computer:~/Documents$ myproj
user@computer:~/Documents/project$ ..
user@computer:~/Documents$ exit
Goodbye!
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission denied | `chmod +x mini_shell.py` |
| History not working | `touch ~/.minishell_history` |
| Aliases not saving | Check `~/.minishell_config.json` permissions |
| Colors not showing | Use a modern terminal emulator |

---

## 📝 Key Implementation Details

### Colored Prompt
Uses ANSI escape codes for colored output:
```python
def get_prompt(self):
    # Green username@hostname, Blue directory
    return f"\033[1;32m{user}@{hostname}\033[0m:\033[1;34m{cwd}\033[0m$ "
```

### Alias Expansion
```python
def parse_command(self, command):
    parts = command.strip().split()
    if parts[0] in self.aliases:
        # Replace alias with expanded command
        parts = self.aliases[parts[0]].split() + parts[1:]
    return parts
```

---

This project is open source and available for educational purposes.


