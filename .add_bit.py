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

H42 = lambda t: (
    "/* ************************************************************************** */\n"
    "/*                                                                            */\n"
    "/*                                                        :::      ::::::::   */\n"
    "/*   get_next_line.h                                    :+:      :+:    :+:   */\n"
    "/*                                                    +:+ +:+         +:+     */\n"
    "/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */\n"
    "/*                                                +#+#+#+#+#+   +#+           */\n"
    "/*   Created: 2026/09/11 15:34:32 by omadali           #+#    #+#             */\n"
    f"/*   Updated: {t} by omadali          ###   ########.fr       */\n"
    "/*                                                                            */\n"
    "/* ************************************************************************** */\n"
)

U42 = lambda t: (
    "/* ************************************************************************** */\n"
    "/*                                                                            */\n"
    "/*                                                        :::      ::::::::   */\n"
    "/*   get_next_line_utils.c                              :+:      :+:    :+:   */\n"
    "/*                                                    +:+ +:+         +:+     */\n"
    "/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */\n"
    "/*                                                +#+#+#+#+#+   +#+           */\n"
    "/*   Created: 2026/09/11 15:34:40 by omadali           #+#    #+#             */\n"
    f"/*   Updated: {t} by omadali          ###   ########.fr       */\n"
    "/*                                                                            */\n"
    "/* ************************************************************************** */\n"
)

C42 = lambda t: (
    "/* ************************************************************************** */\n"
    "/*                                                                            */\n"
    "/*                                                        :::      ::::::::   */\n"
    "/*   get_next_line.c                                    :+:      :+:    :+:   */\n"
    "/*                                                    +:+ +:+         +:+     */\n"
    "/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */\n"
    "/*                                                +#+#+#+#+#+   +#+           */\n"
    "/*   Created: 2026/09/11 15:34:36 by omadali           #+#    #+#             */\n"
    f"/*   Updated: {t} by omadali          ###   ########.fr       */\n"
    "/*                                                                            */\n"
    "/* ************************************************************************** */\n"
)

# ===== HEADER =====
HEADER_BODY = f"""
# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 10
# endif

typedef struct s_buf
{{
{T}char{T}{T}{T}*content;
{T}struct s_buf{T}*next;
}}{T}t_buf;

int{T}{T}check_byte(char c, char target);
int{T}{T}find_nl(t_buf *lst);
int{T}{T}line_len(t_buf *lst);
void{T}append_node(t_buf **lst, char *buf);
void{T}free_list(t_buf **lst);
char{T}*get_next_line(int fd);
"""

def make_header(t):
    return H42(t) + "\n#ifndef GET_NEXT_LINE_H\n# define GET_NEXT_LINE_H\n" + HEADER_BODY + "\n#endif\n"

# ===== UTILS =====
UTILS_BODY = f"""
#include "get_next_line.h"

int{T}check_byte(char c, char target)
{{
{T}return (!(c ^ target));
}}

int{T}find_nl(t_buf *lst)
{{
{T}int{T}i;

{T}if (!lst)
{T}{T}return (0);
{T}while (lst)
{T}{{
{T}{T}i = 0;
{T}{T}while (lst->content[i])
{T}{T}{{
{T}{T}{T}if (check_byte(lst->content[i], '\\n'))
{T}{T}{T}{T}return (1);
{T}{T}{T}i++;
{T}{T}}}
{T}{T}lst = lst->next;
{T}}}
{T}return (0);
}}

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
{T}{T}{T}if (check_byte(lst->content[i], '\\n'))
{T}{T}{T}{T}return (len);
{T}{T}{T}i++;
{T}{T}}}
{T}{T}lst = lst->next;
{T}}}
{T}return (len);
}}

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

# ===== GNL.C =====
GNL_BODY = f"""
#include "get_next_line.h"

static char{T}*get_remaining(t_buf *last)
{{
{T}char{T}*buf;
{T}int{T}{T}i;
{T}int{T}{T}j;

{T}i = 0;
{T}while (last->content[i] && !check_byte(last->content[i], '\\n'))
{T}{T}i++;
{T}if (check_byte(last->content[i], '\\n'))
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
{T}{T}while (lst->content[i] && !check_byte(lst->content[i], '\\n'))
{T}{T}{T}line[j++] = lst->content[i++];
{T}{T}if (check_byte(lst->content[i], '\\n'))
{T}{T}{T}line[j++] = '\\n';
{T}{T}if (check_byte(lst->content[i], '\\n'))
{T}{T}{T}break ;
{T}{T}lst = lst->next;
{T}}}
{T}line[j] = '\\0';
{T}return (line);
}}

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

# Read current README
with open(os.path.join(D, 'README.md'), 'r') as f:
    readme = f.read()

# Add bit operation explanation to algorithm section
BIT_SECTION = """
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

For example, detecting newline (`\\n` = `0x0A` = `00001010` in binary):
```
'\\n' ^ '\\n' = 00001010 ^ 00001010 = 00000000 -> !(0) = 1 (match!)
'A'  ^ '\\n' = 01000001 ^ 00001010 = 01001011 -> !(nonzero) = 0 (no match)
```

This bit-level approach is used throughout the project for all newline
detection instead of direct character comparison.
"""

readme_new = readme.rstrip() + "\n" + BIT_SECTION

# ===== COMMIT 1: add check_byte function =====
w('get_next_line_utils.c', U42("2026/09/11 19:15:00") + UTILS_BODY)
w('get_next_line.h', make_header("2026/09/11 19:15:00"))
gc("add bitwise byte checker function", "2026-09-11T19:15:00+03:00")

# ===== COMMIT 2: use bit check in gnl.c =====
w('get_next_line.c', C42("2026/09/11 19:28:00") + GNL_BODY)
gc("use bit check in extract and remaining", "2026-09-11T19:28:00+03:00")

# ===== COMMIT 3: update readme =====
w('README.md', readme_new)
gc("add bit operation explanation to readme", "2026-09-11T19:40:00+03:00")

print("\n=== BIT FEATURE COMMITS DONE ===")
