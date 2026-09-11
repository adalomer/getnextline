/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:36 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 17:22:39 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static void	fill_list(int fd, t_buf **lst)
{
	char	*buf;
	int		bytes;

	while (!find_nl(*lst))
	{
		buf = malloc((BUFFER_SIZE + 1) * sizeof(char));
		if (!buf)
			return ;
		bytes = read(fd, buf, BUFFER_SIZE);
		if (bytes <= 0)
		{
			free(buf);
			return ;
		}
		buf[bytes] = '\0';
		append_node(lst, buf);
	}
}

static char	*extract_line(t_buf *lst)
{
	char	*line;
	int		i;
	int		j;

	if (!lst)
		return (NULL);
	line = malloc(sizeof(char) * (line_len(lst) + 1));
	if (!line)
		return (NULL);
	j = 0;
	while (lst)
	{
		i = 0;
		while (lst->content[i] && lst->content[i] != '\n')
			line[j++] = lst->content[i++];
		lst = lst->next;
	}
	line[j] = '\0';
	return (line);
}
