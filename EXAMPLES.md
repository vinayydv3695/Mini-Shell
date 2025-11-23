# Example Commands for Mini Shell

# After starting the shell with: python3 mini_shell.py
# Try these commands:

# 1. Basic Navigation
pwd
ls
cd /tmp
pwd
cd ~
pwd

# 2. Using Aliases (pre-configured)
ll          # same as: ls -la
..          # same as: cd ..
home        # same as: cd ~
h           # same as: history

# 3. Creating Custom Aliases
alias gs='git status'
alias mydir='cd ~/Documents'
alias py='python3'

# 4. Show all aliases
alias

# 5. Test echo
echo Hello from Mini Shell!
echo Today is: $(date)

# 6. View history
history

# 7. Clear screen
clear

# 8. Get help
help

# 9. Run external commands
python3 --version
git --version
whoami
date

# 10. Remove an alias
unalias gs

# 11. Reverse Search Demo
# Press Ctrl+R and start typing part of a previous command
# Example: Type "echo" to find echo commands

# 12. Exit the shell
exit
