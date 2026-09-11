/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:36 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 19:22:00 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static char	*preserve_tail(t_chunk *last)
{
	char	*rem;
	int		start;
	int		len;

	start = 0;
	while (last->raw[start] && !match_byte(last->raw[start], '\n'))
		start++;
	if (match_byte(last->raw[start], '\n'))
		start++;
	if (!last->raw[start])
		return (NULL);
	len = 0;
	while (last->raw[start + len])
		len++;
	rem = malloc(len + 1);
	if (!rem)
		return (NULL);
	rem[len] = '\0';
	while (len--)
		rem[len] = last->raw[start + len];
	return (rem);
}

static void	pull_data(int fd, t_chunk **head)
{
	char	*buf;
	ssize_t	bytes;

	while (!has_newline(*head))
	{
		buf = malloc(BUFFER_SIZE + 1);
		if (!buf)
			return ;
		bytes = read(fd, buf, BUFFER_SIZE);
		if (bytes <= 0)
		{
			free(buf);
			if (bytes < 0)
				purge_chunks(head);
			return ;
		}
		buf[bytes] = '\0';
		push_chunk(head, buf);
	}
}

static char	*assemble_str(t_chunk *head)
{
	char	*str;
	size_t	total;
	size_t	i;
	int		j;

	if (!head)
		return (NULL);
	total = calc_line_len(head);
	str = malloc(total + 1);
	if (!str)
		return (NULL);
	i = 0;
	while (head)
	{
		j = 0;
		while (head->raw[j] && !match_byte(head->raw[j], '\n'))
			str[i++] = head->raw[j++];
		if (match_byte(head->raw[j], '\n'))
			str[i++] = '\n';
		if (match_byte(head->raw[j], '\n'))
			break ;
		head = head->next;
	}
	str[i] = '\0';
	return (str);
}

char	*get_next_line(int fd)
{
	static t_chunk	*head;
	t_chunk			*last;
	char			*line;
	char			*rest;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	pull_data(fd, &head);
	if (!head)
		return (NULL);
	line = assemble_str(head);
	last = head;
	while (last->next)
		last = last->next;
	rest = preserve_tail(last);
	purge_chunks(&head);
	if (rest)
		push_chunk(&head, rest);
	return (line);
}
