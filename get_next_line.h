/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:32 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 19:35:00 by omadali          ###   ########.fr       */
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
	size_t			size;
	size_t			offset;
	struct s_chunk	*next;
}	t_chunk;

int		is_byte_eq(char a, char b);
int		check_nl_in_chain(t_chunk *head);
size_t	measure_line_bytes(t_chunk *head);
void	append_stream_chunk(t_chunk **head, char *buf, size_t sz);
void	clear_stream(t_chunk **head);
char	*get_next_line(int fd);

#endif
