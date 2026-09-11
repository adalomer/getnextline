/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:36 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 19:35:00 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static void	read_until_nl(int fd, t_chunk **head)
{
	char	*buf;
	ssize_t	read_bytes;

	while (!check_nl_in_chain(*head))
	{
		buf = malloc(BUFFER_SIZE + 1);
		if (!buf)
			return ;
		read_bytes = read(fd, buf, BUFFER_SIZE);
		if (read_bytes <= 0)
		{
			free(buf);
			if (read_bytes < 0)
				clear_stream(head);
			return ;
		}
		buf[read_bytes] = '\0';
		append_stream_chunk(head, buf, (size_t)read_bytes);
	}
}

static void	pop_fully_read(t_chunk **head)
{
	t_chunk	*tmp;

	while (*head && (*head)->offset >= (*head)->size)
	{
		tmp = (*head)->next;
		free((*head)->raw);
		free(*head);
		*head = tmp;
	}
}

static char	*build_line_from_stream(t_chunk **head)
{
	char	*line;
	size_t	total_len;
	size_t	idx;

	pop_fully_read(head);
	if (!*head)
		return (NULL);
	total_len = measure_line_bytes(*head);
	line = malloc(total_len + 1);
	if (!line)
		return (NULL);
	idx = 0;
	while (*head && idx < total_len)
	{
		line[idx++] = (*head)->raw[(*head)->offset++];
		if (is_byte_eq(line[idx - 1], '\n'))
			break ;
		pop_fully_read(head);
	}
	line[idx] = '\0';
	pop_fully_read(head);
	return (line);
}

char	*get_next_line(int fd)
{
	static t_chunk	*head;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	read_until_nl(fd, &head);
	return (build_line_from_stream(&head));
}
