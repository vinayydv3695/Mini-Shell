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
            'echo': self.cmd_echo,
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
