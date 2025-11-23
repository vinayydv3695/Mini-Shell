#!/usr/bin/env python3
"""
Mini Shell - A simple command-line interface
Author: Your Name
Date: November 2025
"""

import os
import sys
import subprocess
import json
import readline
import shutil
import fnmatch
import re
import difflib
from pathlib import Path
from datetime import datetime


class MiniShell:
    """A simple command-line shell with basic commands, aliases, and reverse search."""
    
    def __init__(self):
        self.running = True
        self.current_dir = os.getcwd()
        self.aliases = {}
        self.command_history = []
        self.config_file = Path.home() / ".minishell_config.json"
        self.history_file = Path.home() / ".minishell_history"
        
        # Load configuration and history
        self.load_config()
        self.load_history()
        
        # Setup readline for command history and reverse search
        self.setup_readline()
        
    def setup_readline(self):
        """Configure readline for command history and reverse search."""
        # Enable tab completion
        readline.parse_and_bind("tab: complete")
        
        # Load history into readline
        if self.history_file.exists():
            try:
                readline.read_history_file(self.history_file)
            except Exception as e:
                print(f"Warning: Could not load history: {e}")
        
        # Set history length
        readline.set_history_length(1000)
    
    def load_config(self):
        """Load aliases and configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.aliases = config.get('aliases', {})
                    print(f"Loaded {len(self.aliases)} alias(es)")
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
    
    def save_config(self):
        """Save aliases and configuration to file."""
        try:
            config = {'aliases': self.aliases}
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error: Could not save config: {e}")
    
    def load_history(self):
        """Load command history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    self.command_history = [line.strip() for line in f.readlines()]
            except Exception as e:
                print(f"Warning: Could not load history: {e}")
    
    def save_history(self):
        """Save command history to file."""
        try:
            readline.write_history_file(self.history_file)
        except Exception as e:
            print(f"Error: Could not save history: {e}")
    
    def add_to_history(self, command):
        """Add command to history."""
        if command.strip():
            self.command_history.append(command)
            readline.add_history(command)
    
    def get_prompt(self):
        """Generate the shell prompt."""
        user = os.environ.get('USER', 'user')
        hostname = os.uname().nodename
        cwd = os.getcwd()
        
        # Shorten home directory to ~
        home = str(Path.home())
        if cwd.startswith(home):
            cwd = '~' + cwd[len(home):]
        
        return f"\033[1;32m{user}@{hostname}\033[0m:\033[1;34m{cwd}\033[0m$ "
    
    def parse_command(self, command):
        """Parse command and expand aliases."""
        parts = command.strip().split()
        if not parts:
            return []
        
        # Check if first part is an alias
        if parts[0] in self.aliases:
            alias_cmd = self.aliases[parts[0]]
            # Replace alias with its value
            parts = alias_cmd.split() + parts[1:]
        
        return parts
    
    # Built-in Commands
    
    def cmd_cd(self, args):
        """Change directory."""
        if not args:
            # No argument, go to home directory
            target = str(Path.home())
        else:
            target = args[0]
        
        try:
            os.chdir(target)
            self.current_dir = os.getcwd()
        except FileNotFoundError:
            print(f"cd: {target}: No such file or directory")
        except PermissionError:
            print(f"cd: {target}: Permission denied")
        except Exception as e:
            print(f"cd: {e}")
    
    def cmd_pwd(self, args):
        """Print working directory."""
        print(os.getcwd())
    
    def cmd_ls(self, args):
        """List directory contents."""
        try:
            path = args[0] if args else '.'
            items = sorted(os.listdir(path))
            
            # Color coding: directories in blue, executables in green
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    print(f"\033[1;34m{item}/\033[0m", end="  ")
                elif os.access(full_path, os.X_OK):
                    print(f"\033[1;32m{item}*\033[0m", end="  ")
                else:
                    print(item, end="  ")
            print()  # New line
        except FileNotFoundError:
            print(f"ls: cannot access '{path}': No such file or directory")
        except PermissionError:
            print(f"ls: cannot access '{path}': Permission denied")
    
    def cmd_echo(self, args):
        """Print arguments."""
        print(' '.join(args))
    
    def cmd_clear(self, args):
        """Clear the screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    # File operations
    def cmd_cat(self, args):
        """Concatenate and print files to stdout."""
        if not args:
            print("cat: missing file operand")
            return
        for path in args:
            try:
                with open(path, 'r') as f:
                    print(f.read(), end='')
            except FileNotFoundError:
                print(f"cat: {path}: No such file or directory")
            except Exception as e:
                print(f"cat: {e}")

    def cmd_touch(self, args):
        """Create an empty file or update its timestamp."""
        if not args:
            print("touch: missing file operand")
            return
        for path in args:
            try:
                Path(path).parent.mkdir(parents=True, exist_ok=True)
                with open(path, 'a'):
                    os.utime(path, None)
            except Exception as e:
                print(f"touch: {e}")

    def cmd_mkdir(self, args):
        """Create directories."""
        if not args:
            print("mkdir: missing operand")
            return
        for d in args:
            try:
                os.makedirs(d, exist_ok=True)
            except Exception as e:
                print(f"mkdir: cannot create directory '{d}': {e}")

    def cmd_rm(self, args):
        """Remove files or directories. Use -r for recursive removal."""
        if not args:
            print("rm: missing operand")
            return
        recursive = False
        paths = []
        for a in args:
            if a == '-r' or a == '-rf' or a == '-fr':
                recursive = True
            else:
                paths.append(a)
        for p in paths:
            try:
                if os.path.isdir(p) and not os.path.islink(p):
                    if recursive:
                        shutil.rmtree(p)
                    else:
                        print(f"rm: cannot remove '{p}': Is a directory")
                else:
                    os.remove(p)
            except FileNotFoundError:
                print(f"rm: cannot remove '{p}': No such file or directory")
            except Exception as e:
                print(f"rm: {e}")

    def cmd_rmdir(self, args):
        """Remove empty directories."""
        if not args:
            print("rmdir: missing operand")
            return
        for d in args:
            try:
                os.rmdir(d)
            except FileNotFoundError:
                print(f"rmdir: failed to remove '{d}': No such file or directory")
            except OSError as e:
                print(f"rmdir: failed to remove '{d}': {e}")

    def cmd_mv(self, args):
        """Move (rename) files."""
        if len(args) < 2:
            print("mv: missing file operand")
            return
        src = args[:-1]
        dest = args[-1]
        try:
            if len(src) > 1:
                # Move multiple into directory
                os.makedirs(dest, exist_ok=True)
                for s in src:
                    shutil.move(s, dest)
            else:
                shutil.move(src[0], dest)
        except Exception as e:
            print(f"mv: {e}")

    def cmd_cp(self, args):
        """Copy files or directories. Use -r to copy directories."""
        if len(args) < 2:
            print("cp: missing file operand")
            return
        recursive = False
        parts = [a for a in args if a != '-r']
        if '-r' in args:
            recursive = True
        srcs = parts[:-1]
        dest = parts[-1]
        try:
            if len(srcs) > 1:
                os.makedirs(dest, exist_ok=True)
                for s in srcs:
                    if os.path.isdir(s):
                        if recursive:
                            shutil.copytree(s, os.path.join(dest, os.path.basename(s)), dirs_exist_ok=True)
                        else:
                            print(f"cp: -r not specified; omitting directory '{s}'")
                    else:
                        shutil.copy2(s, dest)
            else:
                s = srcs[0]
                if os.path.isdir(s):
                    if recursive:
                        shutil.copytree(s, dest, dirs_exist_ok=True)
                    else:
                        print(f"cp: -r not specified; omitting directory '{s}'")
                else:
                    if os.path.isdir(dest):
                        shutil.copy2(s, dest)
                    else:
                        shutil.copy2(s, dest)
        except Exception as e:
            print(f"cp: {e}")

    # Text processing
    def cmd_head(self, args):
        """Show first lines of a file. Usage: head [-n N] file"""
        n = 10
        files = []
        i = 0
        while i < len(args):
            if args[i] == '-n' and i + 1 < len(args):
                try:
                    n = int(args[i+1])
                    i += 2
                    continue
                except ValueError:
                    pass
            files.append(args[i])
            i += 1
        if not files:
            print("head: missing file operand")
            return
        for f in files:
            try:
                with open(f, 'r') as fh:
                    for l in fh.readlines()[:n]:
                        print(l, end='')
            except Exception as e:
                print(f"head: {e}")

    def cmd_tail(self, args):
        """Show last lines of a file. Usage: tail [-n N] file"""
        n = 10
        files = []
        i = 0
        while i < len(args):
            if args[i] == '-n' and i + 1 < len(args):
                try:
                    n = int(args[i+1])
                    i += 2
                    continue
                except ValueError:
                    pass
            files.append(args[i])
            i += 1
        if not files:
            print("tail: missing file operand")
            return
        for f in files:
            try:
                with open(f, 'r') as fh:
                    lines = fh.readlines()
                    for l in lines[-n:]:
                        print(l, end='')
            except Exception as e:
                print(f"tail: {e}")

    def cmd_grep(self, args):
        """Simple grep implementation: grep PATTERN [file...]"""
        if not args:
            print("grep: missing pattern")
            return
        pattern = args[0]
        files = args[1:] if len(args) > 1 else []
        regex = re.compile(pattern)
        if not files:
            # read stdin
            for line in sys.stdin:
                if regex.search(line):
                    print(line, end='')
            return
        for f in files:
            try:
                with open(f, 'r') as fh:
                    for i, line in enumerate(fh, 1):
                        if regex.search(line):
                            print(f"{f}:{i}:{line.strip()}")
            except Exception as e:
                print(f"grep: {e}")

    def cmd_wc(self, args):
        """Word/line/byte count. Usage: wc [file...]"""
        files = args if args else []
        def counts(text):
            lines = text.count('\n')
            words = len(text.split())
            bytes_ = len(text.encode('utf-8'))
            return lines, words, bytes_
        if not files:
            text = sys.stdin.read()
            l, w, b = counts(text)
            print(f"{l:7d} {w:7d} {b:7d}")
            return
        for f in files:
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
                    text = fh.read()
                    l, w, b = counts(text)
                    print(f"{l:7d} {w:7d} {b:7d} {f}")
            except Exception as e:
                print(f"wc: {e}")

    def cmd_sort(self, args):
        """Sort lines of a file or stdin."""
        files = args if args else []
        lines = []
        if not files:
            lines = sys.stdin.read().splitlines()
        else:
            for f in files:
                try:
                    with open(f, 'r') as fh:
                        lines.extend(fh.read().splitlines())
                except Exception as e:
                    print(f"sort: {e}")
        for l in sorted(lines):
            print(l)

    def cmd_diff(self, args):
        """Show unified diff between two files."""
        if len(args) != 2:
            print("diff: need two file operands")
            return
        a, b = args
        try:
            with open(a, 'r') as fa, open(b, 'r') as fb:
                a_lines = fa.readlines()
                b_lines = fb.readlines()
                for line in difflib.unified_diff(a_lines, b_lines, fromfile=a, tofile=b):
                    print(line, end='')
        except Exception as e:
            print(f"diff: {e}")

    # Search / system utilities
    def cmd_find(self, args):
        """Simple find: find [path] -name pattern"""
        if not args:
            path = '.'
            pattern = '*'
        else:
            path = args[0]
            pattern = '*'
            if '-name' in args:
                try:
                    idx = args.index('-name')
                    pattern = args[idx+1]
                except Exception:
                    pass
        for root,dirs,files in os.walk(path):
            for name in files + dirs:
                if fnmatch.fnmatch(name, pattern):
                    print(os.path.join(root, name))

    def cmd_which(self, args):
        """Locate a command in PATH."""
        if not args:
            print("which: missing operand")
            return
        for cmd in args:
            path = shutil.which(cmd)
            if path:
                print(path)
            else:
                print(f"which: no {cmd} in ({os.environ.get('PATH', '')})")

    def cmd_du(self, args):
        """Disk usage summary for files/directories."""
        paths = args if args else ['.']
        for p in paths:
            total = 0
            if os.path.isfile(p):
                total = os.path.getsize(p)
                print(f"{total}\t{p}")
                continue
            for root, dirs, files in os.walk(p):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(root, f))
                    except Exception:
                        pass
            print(f"{total}\t{p}")

    def cmd_env(self, args):
        """Print environment variables."""
        for k, v in os.environ.items():
            print(f"{k}={v}")

    def cmd_tree(self, args):
        """Simple tree implementation: tree [path]"""
        start = args[0] if args else '.'
        def walk(dirpath, prefix=''):
            try:
                entries = sorted(os.listdir(dirpath))
            except Exception as e:
                print(f"tree: {e}")
                return
            for i, name in enumerate(entries):
                path = os.path.join(dirpath, name)
                connector = '└── ' if i == len(entries)-1 else '├── '
                print(prefix + connector + name)
                if os.path.isdir(path):
                    extension = '    ' if i == len(entries)-1 else '│   '
                    walk(path, prefix + extension)
        print(start)
        walk(start)
    
    def cmd_history(self, args):
        """Show command history."""
        if args and args[0] == '-c':
            # Clear history
            self.command_history = []
            readline.clear_history()
            print("History cleared")
        else:
            # Show history with line numbers
            for i, cmd in enumerate(self.command_history[-50:], 1):
                print(f"{i:4d}  {cmd}")
    
    def cmd_alias(self, args):
        """Create or display aliases."""
        if not args:
            # Display all aliases
            if not self.aliases:
                print("No aliases defined")
            else:
                for name, value in sorted(self.aliases.items()):
                    print(f"alias {name}='{value}'")
        else:
            # Parse alias definition
            if '=' in args[0]:
                # New alias format: alias name=value
                parts = args[0].split('=', 1)
                name = parts[0]
                value = parts[1].strip("'\"")
                self.aliases[name] = value
                self.save_config()
                print(f"Alias created: {name}='{value}'")
            else:
                # Display specific alias
                name = args[0]
                if name in self.aliases:
                    print(f"alias {name}='{self.aliases[name]}'")
                else:
                    print(f"alias: {name}: not found")
    
    def cmd_unalias(self, args):
        """Remove an alias."""
        if not args:
            print("unalias: usage: unalias name")
        else:
            name = args[0]
            if name in self.aliases:
                del self.aliases[name]
                self.save_config()
                print(f"Alias removed: {name}")
            else:
                print(f"unalias: {name}: not found")
    
    def cmd_exit(self, args):
        """Exit the shell."""
        print("Goodbye!")
        self.running = False
    
    def cmd_help(self, args):
        """Display help information."""
        print("\nMini Shell - Available Commands:")
        print("=" * 50)
        print("Built-in Commands:")
        print("  cd [dir]       - Change directory (default: home)")
        print("  pwd            - Print working directory")
        print("  ls [path]      - List directory contents")
        print("  echo [args]    - Print arguments")
        print("  clear          - Clear the screen")
        print("  history        - Show command history")
        print("  history -c     - Clear command history")
        print("  alias          - Show all aliases")
        print("  alias name=cmd - Create an alias")
        print("  unalias name   - Remove an alias")
        print("  help           - Show this help message")
        print("  exit           - Exit the shell")
        print("\nFeatures:")
        print("  • Reverse Search: Press Ctrl+R to search history")
        print("  • Arrow Keys: Navigate through command history")
        print("  • Tab Completion: (limited support)")
        print("  • External Commands: Run any system command")
        print("=" * 50)
    
    def execute_builtin(self, command, args):
        """Execute built-in commands."""
        builtins = {
            'cd': self.cmd_cd,
            'pwd': self.cmd_pwd,
            'ls': self.cmd_ls,
            'tree': self.cmd_tree,
            'cat': self.cmd_cat,
            'touch': self.cmd_touch,
            'mkdir': self.cmd_mkdir,
            'rm': self.cmd_rm,
            'rmdir': self.cmd_rmdir,
            'mv': self.cmd_mv,
            'cp': self.cmd_cp,
            'echo': self.cmd_echo,
            'head': self.cmd_head,
            'tail': self.cmd_tail,
            'grep': self.cmd_grep,
            'wc': self.cmd_wc,
            'sort': self.cmd_sort,
            'diff': self.cmd_diff,
            'find': self.cmd_find,
            'which': self.cmd_which,
            'du': self.cmd_du,
            'env': self.cmd_env,
            'clear': self.cmd_clear,
            'history': self.cmd_history,
            'alias': self.cmd_alias,
            'unalias': self.cmd_unalias,
            'exit': self.cmd_exit,
            'quit': self.cmd_exit,
            'help': self.cmd_help,
        }
        
        if command in builtins:
            builtins[command](args)
            return True
        return False
    
    def execute_external(self, command, args):
        """Execute external system commands."""
        try:
            # Combine command and args
            full_command = [command] + args
            
            # Run the command
            result = subprocess.run(
                full_command,
                capture_output=False,
                text=True
            )
            
            return result.returncode == 0
        except FileNotFoundError:
            print(f"{command}: command not found")
            return False
        except Exception as e:
            print(f"Error executing command: {e}")
            return False
    
    def execute_command(self, command_line):
        """Parse and execute a command."""
        if not command_line.strip():
            return
        
        # Parse command with alias expansion
        parts = self.parse_command(command_line)
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:]
        
        # Try to execute as built-in
        if self.execute_builtin(command, args):
            return
        
        # Try to execute as external command
        self.execute_external(command, args)
    
    def run(self):
        """Main shell loop."""
        print("\n" + "=" * 50)
        print("Welcome to Mini Shell!")
        print("Type 'help' for available commands")
        print("Press Ctrl+R for reverse search")
        print("Press Ctrl+C to cancel, Ctrl+D to exit")
        print("=" * 50 + "\n")
        
        while self.running:
            try:
                # Get input with custom prompt
                command = input(self.get_prompt())
                
                # Add to history
                self.add_to_history(command)
                
                # Execute command
                self.execute_command(command)
                
            except KeyboardInterrupt:
                # Ctrl+C pressed
                print("\n(Use 'exit' or Ctrl+D to quit)")
            except EOFError:
                # Ctrl+D pressed
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        # Save history before exiting
        self.save_history()


def main():
    """Main entry point."""
    shell = MiniShell()
    shell.run()


if __name__ == "__main__":
    main()
