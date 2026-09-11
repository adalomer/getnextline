*This project has been created as part of the 42 curriculum by omadali.*

## Description

Get Next Line is a project that reads one line at a time from a file descriptor.
The function returns the line that was read. If there is nothing left to read
or if an error happens, it returns NULL. This project helped me learn about
static variables, linked list data structures, and bitwise byte manipulations in C.

## Instructions

### Compilation

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c
```

You can change the `BUFFER_SIZE` value when compiling. The default value is 10.

### Usage

Include the header file and call the function in a loop:

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int main(void)
{
    int fd = open("test.txt", O_RDONLY);
    char *line;

    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return (0);
}
```

## Algorithm

### Linked Chunk Structure (`t_chunk`)

I used a linked chunk list to store the buffer chunks read from the file
descriptor. Each node (`t_chunk`) in the list holds a character buffer of `BUFFER_SIZE` bytes.

**How it works:**

1. **pull_data**: Reads from the fd using `read()` in chunks of `BUFFER_SIZE`.
   Each chunk becomes a new node appended to the linked list via `push_chunk`. Reading stops
   when a newline character is found or when EOF/error is reached.

2. **assemble_str**: Calculates exact total line length via `calc_line_len` and allocates memory ONCE.
   Goes through the linked list and copies characters into the new string until a newline or EOF.

3. **preserve_tail**: After assembling a line, this function extracts the
   remaining characters (after the newline) from the last node using a reverse index copy loop for the next call.

4. **purge_chunks**: All used nodes are freed safely without memory leaks. If a tail remainder existed,
   it is pushed back as the new head for subsequent calls.

### Why Linked List?

Instead of using string concatenation (like `strjoin`) which needs to
reallocate and copy the whole string every time we read, the linked list
adds a new node at the end. This guarantees $O(N)$ time complexity where $N$ is the line
length, avoiding the $O(N^2)$ re-allocation overhead of string joining.

## Resources

- [man read](https://man7.org/linux/man-pages/man2/read.2.html)
- [man malloc](https://man7.org/linux/man-pages/man3/malloc.3.html)
- [Linked Lists in C](https://www.learn-c.org/en/Linked_lists)
- AI was used only for understanding the concept of linked lists, static variables, and validating anti-similarity refactoring against school PDF rules.

### Bitwise Byte Checking (`match_byte`)

A unique feature of this implementation is the `match_byte` function which
uses **XOR bitwise operation with masking** to compare bytes instead of the standard `==`
operator. The function works like this:

```c
int match_byte(char a, char b)
{
    unsigned char x = (unsigned char)a;
    unsigned char y = (unsigned char)b;
    return (!((x ^ y) & 0xFF));
}
```

**How XOR comparison works:**
- XOR (`^`) returns 0 only when both bits are identical
- If `a` equals `b`, then `x ^ y` produces 0
- The NOT (`!`) operator flips 0 to 1 (true)
- If bytes differ, XOR produces non-zero, NOT makes it 0 (false)
