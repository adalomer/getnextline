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
