*This project has been created as part of the 42 curriculum by omadali.*

## Description

Get Next Line is a project that reads one line at a time from a file descriptor.
The function returns the line that was read. If there is nothing left to read
or if an error happens, it returns NULL. This project helped me learn about
static variables and linked list data structure in C language.

## Instructions

### Compilation

```
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c
```

You can change the BUFFER_SIZE value when compiling. The default value is 10.

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

### Linked List Approach

I used a linked list to store the buffer chunks that are read from the file
descriptor. Each node in the list holds a character buffer of BUFFER_SIZE bytes.

**How it works:**

1. **fill_list**: Reads from the fd using `read()` in chunks of BUFFER_SIZE.
   Each chunk becomes a new node appended to the linked list. Reading stops
   when a newline character is found or when EOF/error is reached.

2. **extract_line**: Goes through the linked list and copies characters into
   a new string until a newline character or end of data. The newline is
   included in the returned string.

3. **get_remaining**: After extracting a line, this function saves the
   remaining characters (after the newline) from the last node for the
   next call to get_next_line.

4. **cleanup**: All used nodes are freed, and a new node with remaining
   content (if any) is created for the next function call.

### Why Linked List?

Instead of using string concatenation (like strjoin) which needs to
reallocate and copy the whole string every time we read, the linked list
just adds a new node at the end. This is better for memory because we
dont need to copy data we already read. When we extract the line we go
through the list one time. This gives O(n) time where n is the line
length, instead of O(n^2) for repeated string joining.

## Resources

- [man read](https://man7.org/linux/man-pages/man2/read.2.html)
- [man malloc](https://man7.org/linux/man-pages/man3/malloc.3.html)
- [Linked Lists in C](https://www.learn-c.org/en/Linked_lists)
- AI was used only for understanding the concept of linked lists
  and static variables, not for writing the actual code

### Bitwise Byte Checking

A unique feature of this implementation is the `check_byte` function which
uses **XOR bitwise operation** to compare bytes instead of the standard `==`
operator. The function works like this:

```c
int check_byte(char c, char target)
{
    return (!(c ^ target));
}
```

**How XOR comparison works:**
- XOR (`^`) returns 0 only when both bits are identical
- If `c` equals `target`, then `c ^ target` produces 0
- The NOT (`!`) operator flips 0 to 1 (true)
- If bytes differ, XOR produces non-zero, NOT makes it 0 (false)

For example, detecting newline (`\n` = `0x0A` = `00001010` in binary):
```
'\n' ^ '\n' = 00001010 ^ 00001010 = 00000000 -> !(0) = 1 (match!)
'A'  ^ '\n' = 01000001 ^ 00001010 = 01001011 -> !(nonzero) = 0 (no match)
```

This bit-level approach is used throughout the project for all newline
detection instead of direct character comparison.
