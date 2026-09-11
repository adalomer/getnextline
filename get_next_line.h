/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:32 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 19:22:00 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 10
# endif

typedef struct s_chunk
{
	char			*raw;
	struct s_chunk	*next;
}	t_chunk;

int		match_byte(char a, char b);
int		has_newline(t_chunk *head);
size_t	calc_line_len(t_chunk *head);
void	push_chunk(t_chunk **head, char *buffer);
void	purge_chunks(t_chunk **head);
char	*get_next_line(int fd);

#endif
