#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

// Define the function pointer type for the function we are loading
typedef void (*foo_t)();

int main() {
    // Open the binary file
    int fd = open("dummy", O_RDONLY);
    if (fd < 0) {
        perror("open");
        return EXIT_FAILURE;
    }

    // Get the size of the file
    off_t size = lseek(fd, 0, SEEK_END);
    lseek(fd, 0, SEEK_SET);

    // Allocate a memory region with mmap
    void *mem = mmap(NULL, size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE, fd, 0);
    if (mem == MAP_FAILED) {
        perror("mmap");
        close(fd);
        return EXIT_FAILURE;
    }

    // Now we need to find the offset for foo()
    size_t foo_offset = 0x1129;  // Make sure this offset is correct for foo()

    // Create a function pointer to the loaded code
    foo_t foo = (foo_t)((char *)mem + foo_offset);

    // Execute the loaded function
    printf("Calling foo()...\n");
    foo(); // Call the function

    // Clean up
    if (munmap(mem, size) == -1) {
        perror("munmap");
    }
    close(fd);
    return EXIT_SUCCESS;
}
