#include <stdio.h>

int main() {
    char buffer[256];
    printf("Buffer at %p\n", buffer);
    fgets(buffer, sizeof(buffer), stdin);  // Safe alternative to gets
    return 0;
}
