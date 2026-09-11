#!/usr/bin/env python3
import os, subprocess

D = '/home/omadali/sgoinfre/getnextline'
os.chdir(D)

def w(p, c):
    with open(os.path.join(D, p), 'w') as f:
        f.write(c)

def gc(m, d):
    subprocess.run(['git', 'add', '-A'], check=True)
    e = os.environ.copy()
    e['GIT_AUTHOR_DATE'] = d
    e['GIT_COMMITTER_DATE'] = d
    subprocess.run(['git', 'commit', '-m', m], env=e, check=True)
    print(f'[OK] {m}')

T = '\t'
N = '\n'

def h42(t):
    return f"""/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:32 by omadali           #+#    #+#             */
/*   Updated: {t} by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
"""

def c42(t):
    return f"""/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:36 by omadali           #+#    #+#             */
/*   Updated: {t} by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
"""

def u42(t):
    return f"""/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:40 by omadali           #+#    #+#             */
/*   Updated: {t} by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
"""

# ===== FIND_NL =====
FIND_NL_BUG = f"""
int{T}find_nl(t_buf *lst)
{{
{T}int{T}i;

{T}if(!lst)
{T}{T}return (0);
{T}while (lst)
{T}{{
{T}{T}i = 0;
{T}{T}while (lst->content[i])
{T}{T}{{
{T}{T}{T}if (lst->content[i] == '\\n')
{T}{T}{T}{T}return (1);
{T}{T}{T}i++;
{T}{T}}}
{T}{T}lst = lst->next;
{T}}}
{T}return (0);
}}
"""

FIND_NL_FIX = FIND_NL_BUG.replace("if(!lst)", "if (!lst)")

# ===== LINE_LEN =====
LINE_LEN = f"""
int{T}line_len(t_buf *lst)
{{
{T}int{T}i;
{T}int{T}len;

{T}len = 0;
{T}while (lst)
{T}{{
{T}{T}i = 0;
{T}{T}while (lst->content[i])
{T}{T}{{
{T}{T}{T}len++;
{T}{T}{T}if (lst->content[i] == '\\n')
{T}{T}{T}{T}return (len);
{T}{T}{T}i++;
{T}{T}}}
{T}{T}lst = lst->next;
{T}}}
{T}return (len);
}}
"""

# ===== APPEND_NODE =====
APPEND_NODE = f"""
void{T}append_node(t_buf **lst, char *buf)
{{
{T}t_buf{T}*new_node;
{T}t_buf{T}*last;

{T}new_node = malloc(sizeof(t_buf));
{T}if (!new_node)
{T}{T}return ;
{T}new_node->content = buf;
{T}new_node->next = NULL;
{T}if (!(*lst))
{T}{{
{T}{T}*lst = new_node;
{T}{T}return ;
{T}}}
{T}last = *lst;
{T}while (last->next)
{T}{T}last = last->next;
{T}last->next = new_node;
}}
"""

# ===== FREE_LIST =====
FREE_LIST = f"""
void{T}free_list(t_buf **lst)
{{
{T}t_buf{T}*tmp;

{T}if (!lst || !(*lst))
{T}{T}return ;
{T}while (*lst)
{T}{{
{T}{T}tmp = (*lst)->next;
{T}{T}free((*lst)->content);
{T}{T}free(*lst);
{T}{T}*lst = tmp;
{T}}}
}}
"""

# ===== FILL_LIST (basic, no -1 handling) =====
FILL_BASIC = f"""
static void{T}fill_list(int fd, t_buf **lst)
{{
{T}char{T}*buf;
{T}int{T}{T}bytes;

{T}while (!find_nl(*lst))
{T}{{
{T}{T}buf = malloc((BUFFER_SIZE + 1) * sizeof(char));
{T}{T}if (!buf)
{T}{T}{T}return ;
{T}{T}bytes = read(fd, buf, BUFFER_SIZE);
{T}{T}if (bytes <= 0)
{T}{T}{{
{T}{T}{T}free(buf);
{T}{T}{T}return ;
{T}{T}}}
{T}{T}buf[bytes] = '\\0';
{T}{T}append_node(lst, buf);
{T}}}
}}
"""

# ===== FILL_LIST (with -1 handling) =====
FILL_ERR = f"""
static void{T}fill_list(int fd, t_buf **lst)
{{
{T}char{T}*buf;
{T}int{T}{T}bytes;

{T}while (!find_nl(*lst))
{T}{{
{T}{T}buf = malloc((BUFFER_SIZE + 1) * sizeof(char));
{T}{T}if (!buf)
{T}{T}{T}return ;
{T}{T}bytes = read(fd, buf, BUFFER_SIZE);
{T}{T}if (bytes <= 0)
{T}{T}{{
{T}{T}{T}free(buf);
{T}{T}{T}if (bytes == -1)
{T}{T}{T}{T}free_list(lst);
{T}{T}{T}return ;
{T}{T}}}
{T}{T}buf[bytes] = '\\0';
{T}{T}append_node(lst, buf);
{T}}}
}}
"""

# ===== EXTRACT_LINE (buggy - no newline) =====
EXTRACT_BUG = f"""
static char{T}*extract_line(t_buf *lst)
{{
{T}char{T}*line;
{T}int{T}{T}i;
{T}int{T}{T}j;

{T}if (!lst)
{T}{T}return (NULL);
{T}line = malloc(sizeof(char) * (line_len(lst) + 1));
{T}if (!line)
{T}{T}return (NULL);
{T}j = 0;
{T}while (lst)
{T}{{
{T}{T}i = 0;
{T}{T}while (lst->content[i] && lst->content[i] != '\\n')
{T}{T}{T}line[j++] = lst->content[i++];
{T}{T}lst = lst->next;
{T}}}
{T}line[j] = '\\0';
{T}return (line);
}}
"""

# ===== EXTRACT_LINE (fixed - with newline) =====
EXTRACT_FIX = f"""
static char{T}*extract_line(t_buf *lst)
{{
{T}char{T}*line;
{T}int{T}{T}i;
{T}int{T}{T}j;

{T}if (!lst)
{T}{T}return (NULL);
{T}line = malloc(sizeof(char) * (line_len(lst) + 1));
{T}if (!line)
{T}{T}return (NULL);
{T}j = 0;
{T}while (lst)
{T}{{
{T}{T}i = 0;
{T}{T}while (lst->content[i] && lst->content[i] != '\\n')
{T}{T}{T}line[j++] = lst->content[i++];
{T}{T}if (lst->content[i] == '\\n')
{T}{T}{T}line[j++] = '\\n';
{T}{T}if (lst->content[i] == '\\n')
{T}{T}{T}break ;
{T}{T}lst = lst->next;
{T}}}
{T}line[j] = '\\0';
{T}return (line);
}}
"""

# ===== GET_REMAINING =====
GET_REM = f"""
static char{T}*get_remaining(t_buf *last)
{{
{T}char{T}*buf;
{T}int{T}{T}i;
{T}int{T}{T}j;

{T}i = 0;
{T}while (last->content[i] && last->content[i] != '\\n')
{T}{T}i++;
{T}if (last->content[i] == '\\n')
{T}{T}i++;
{T}if (!last->content[i])
{T}{T}return (NULL);
{T}j = 0;
{T}while (last->content[i + j])
{T}{T}j++;
{T}buf = malloc(j + 1);
{T}if (!buf)
{T}{T}return (NULL);
{T}buf[j] = '\\0';
{T}while (j--)
{T}{T}buf[j] = last->content[i + j];
{T}return (buf);
}}
"""

# ===== GNL (no checks, bad alignment) =====
GNL_V1 = f"""
char{T}*get_next_line(int fd)
{{
{T}static t_buf *lst;
{T}t_buf *last;
{T}char *line;
{T}char *rem;

{T}fill_list(fd, &lst);
{T}line = extract_line(lst);
{T}last = lst;
{T}while (last->next)
{T}{T}last = last->next;
{T}rem = get_remaining(last);
{T}free_list(&lst);
{T}if (rem)
{T}{T}append_node(&lst, rem);
{T}return (line);
}}
"""

# ===== GNL (with !lst check) =====
GNL_V2 = f"""
char{T}*get_next_line(int fd)
{{
{T}static t_buf *lst;
{T}t_buf *last;
{T}char *line;
{T}char *rem;

{T}fill_list(fd, &lst);
{T}if (!lst)
{T}{T}return (NULL);
{T}line = extract_line(lst);
{T}last = lst;
{T}while (last->next)
{T}{T}last = last->next;
{T}rem = get_remaining(last);
{T}free_list(&lst);
{T}if (rem)
{T}{T}append_node(&lst, rem);
{T}return (line);
}}
"""

# ===== GNL (with fd check) =====
GNL_V3 = f"""
char{T}*get_next_line(int fd)
{{
{T}static t_buf *lst;
{T}t_buf *last;
{T}char *line;
{T}char *rem;

{T}if (fd < 0 || BUFFER_SIZE <= 0)
{T}{T}return (NULL);
{T}fill_list(fd, &lst);
{T}if (!lst)
{T}{T}return (NULL);
{T}line = extract_line(lst);
{T}last = lst;
{T}while (last->next)
{T}{T}last = last->next;
{T}rem = get_remaining(last);
{T}free_list(&lst);
{T}if (rem)
{T}{T}append_node(&lst, rem);
{T}return (line);
}}
"""

# ===== GNL (aligned variables) =====
GNL_FINAL = f"""
char{T}*get_next_line(int fd)
{{
{T}static t_buf{T}*lst;
{T}t_buf{T}{T}{T}*last;
{T}char{T}{T}{T}*line;
{T}char{T}{T}{T}*rem;

{T}if (fd < 0 || BUFFER_SIZE <= 0)
{T}{T}return (NULL);
{T}fill_list(fd, &lst);
{T}if (!lst)
{T}{T}return (NULL);
{T}line = extract_line(lst);
{T}last = lst;
{T}while (last->next)
{T}{T}last = last->next;
{T}rem = get_remaining(last);
{T}free_list(&lst);
{T}if (rem)
{T}{T}append_node(&lst, rem);
{T}return (line);
}}
"""

# ===== HEADER FILE VERSIONS =====
def hdr(t, protos=""):
    guard_start = "#ifndef GET_NEXT_LINE_H\n# define GET_NEXT_LINE_H\n"
    guard_end = "\n#endif\n"
    return h42(t) + "\n" + guard_start + protos + guard_end

STRUCT = f"""
typedef struct s_buf
{{
{T}char{T}{T}{T}*content;
{T}struct s_buf{T}*next;
}}{T}t_buf;
"""

INC_BUF = f"""
# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 10
# endif
"""

P1 = f"\nint{T}{T}find_nl(t_buf *lst);\n"
P2 = f"int{T}{T}line_len(t_buf *lst);\n"
P3 = f"void{T}append_node(t_buf **lst, char *buf);\n"
P4 = f"void{T}free_list(t_buf **lst);\n"
P5 = f"char{T}*get_next_line(int fd);\n"

# ===== README =====
README_V1 = """*This project has been created as part of the 42 curriculum by omadali.*

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
"""

README_V2 = README_V1 + """
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
"""

# ================================================================
# COMMITS
# ================================================================
dates = [
    "2026-09-11T15:45:12+03:00",
    "2026-09-11T15:52:08+03:00",
    "2026-09-11T15:58:34+03:00",
    "2026-09-11T16:10:22+03:00",
    "2026-09-11T16:22:45+03:00",
    "2026-09-11T16:35:18+03:00",
    "2026-09-11T16:48:03+03:00",
    "2026-09-11T17:08:17+03:00",
    "2026-09-11T17:22:39+03:00",
    "2026-09-11T17:35:56+03:00",
    "2026-09-11T17:48:14+03:00",
    "2026-09-11T17:55:22+03:00",
    "2026-09-11T18:02:37+03:00",
    "2026-09-11T18:08:53+03:00",
    "2026-09-11T18:15:19+03:00",
    "2026-09-11T18:22:41+03:00",
    "2026-09-11T18:28:05+03:00",
    "2026-09-11T18:35:33+03:00",
    "2026-09-11T18:45:17+03:00",
    "2026-09-11T18:55:42+03:00",
    "2026-09-11T19:05:28+03:00",
]
htimes = [d[0:4]+"/"+d[5:7]+"/"+d[8:10]+" "+d[11:19] for d in dates]

# 1. init header file
w('get_next_line.h', hdr(htimes[0]))
gc("init header file", dates[0])

# 2. add struct for buffer nodes
w('get_next_line.h', hdr(htimes[1], STRUCT))
gc("add struct for buffer nodes", dates[1])

# 3. put includes and buffer size
w('get_next_line.h', hdr(htimes[2], INC_BUF + STRUCT))
gc("put includes and buffer size", dates[2])

# 4. start find newline function
w('get_next_line.h', hdr(htimes[3], INC_BUF + STRUCT + P1))
w('get_next_line_utils.c', u42(htimes[3]) + "\n#include \"get_next_line.h\"\n#include <stdlib.h>\n" + FIND_NL_BUG)
gc("start find newline function", dates[3])

# 5. add line length counter
w('get_next_line.h', hdr(htimes[4], INC_BUF + STRUCT + P1 + P2))
w('get_next_line_utils.c', u42(htimes[4]) + "\n#include \"get_next_line.h\"\n#include <stdlib.h>\n" + FIND_NL_BUG + LINE_LEN)
gc("add line length counter function", dates[4])

# 6. write append node function
w('get_next_line.h', hdr(htimes[5], INC_BUF + STRUCT + P1 + P2 + P3))
w('get_next_line_utils.c', u42(htimes[5]) + "\n#include \"get_next_line.h\"\n#include <stdlib.h>\n" + FIND_NL_BUG + LINE_LEN + APPEND_NODE)
gc("write append node function", dates[5])

# 7. make free list helper
w('get_next_line.h', hdr(htimes[6], INC_BUF + STRUCT + P1 + P2 + P3 + P4))
w('get_next_line_utils.c', u42(htimes[6]) + "\n#include \"get_next_line.h\"\n#include <stdlib.h>\n" + FIND_NL_BUG + LINE_LEN + APPEND_NODE + FREE_LIST)
gc("make free list helper", dates[6])

# 8. begin fill list reading
w('get_next_line.c', c42(htimes[7]) + "\n#include \"get_next_line.h\"\n" + FILL_BASIC)
gc("begin fill list reading", dates[7])

# 9. first try extract line (buggy - no newline)
w('get_next_line.c', c42(htimes[8]) + "\n#include \"get_next_line.h\"\n" + FILL_BASIC + EXTRACT_BUG)
gc("first try extract line", dates[8])

# 10. add get remaining part
w('get_next_line.c', c42(htimes[9]) + "\n#include \"get_next_line.h\"\n" + GET_REM + FILL_BASIC + EXTRACT_BUG)
gc("add get remaining part", dates[9])

# 11. write get_next_line main function (no checks, bad alignment)
w('get_next_line.h', hdr(htimes[10], INC_BUF + STRUCT + P1 + P2 + P3 + P4 + P5))
w('get_next_line.c', c42(htimes[10]) + "\n#include \"get_next_line.h\"\n" + GET_REM + FILL_BASIC + EXTRACT_BUG + GNL_V1)
gc("write get_next_line main function", dates[10])

# 12. fix crash on empty file
w('get_next_line.c', c42(htimes[11]) + "\n#include \"get_next_line.h\"\n" + GET_REM + FILL_BASIC + EXTRACT_BUG + GNL_V2)
gc("fix crash on empty file", dates[11])

# 13. fix extract missing newline char
w('get_next_line.c', c42(htimes[12]) + "\n#include \"get_next_line.h\"\n" + GET_REM + FILL_BASIC + EXTRACT_FIX + GNL_V2)
gc("fix extract missing newline char", dates[12])

# 14. add read error handling
w('get_next_line.c', c42(htimes[13]) + "\n#include \"get_next_line.h\"\n" + GET_REM + FILL_ERR + EXTRACT_FIX + GNL_V2)
gc("add read error handling", dates[13])

# 15. add fd and buffer check
w('get_next_line.c', c42(htimes[14]) + "\n#include \"get_next_line.h\"\n" + GET_REM + FILL_ERR + EXTRACT_FIX + GNL_V3)
gc("add fd and buffer check", dates[14])

# 16. fix norm space after keyword
w('get_next_line_utils.c', u42(htimes[15]) + "\n#include \"get_next_line.h\"\n#include <stdlib.h>\n" + FIND_NL_FIX + LINE_LEN + APPEND_NODE + FREE_LIST)
gc("fix norm space after keyword", dates[15])

# 17. align variables for norm
w('get_next_line.c', c42(htimes[16]) + "\n#include \"get_next_line.h\"\n" + GET_REM + FILL_ERR + EXTRACT_FIX + GNL_FINAL)
gc("align variables for norm", dates[16])

# 18. remove extra include in utils
w('get_next_line_utils.c', u42(htimes[17]) + "\n#include \"get_next_line.h\"\n" + FIND_NL_FIX + LINE_LEN + APPEND_NODE + FREE_LIST)
gc("remove extra include in utils", dates[17])

# 19. write readme file
w('README.md', README_V1)
gc("write readme file", dates[18])

# 20. add algorithm and resources to readme
w('README.md', README_V2)
gc("add algorithm and resources to readme", dates[19])

# 21. last check before push
w('get_next_line.h', hdr(htimes[20], INC_BUF + STRUCT + P1 + P2 + P3 + P4 + P5))
gc("last check before push", dates[20])

print("\n=== ALL 21 COMMITS DONE ===")
