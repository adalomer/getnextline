/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:36 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 17:48:14 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static char	*get_remaining(t_buf *last)
{
	char	*buf;
	int		i;
	int		j;

	i = 0;
	while (last->content[i] && last->content[i] != '\n')
		i++;
	if (last->content[i] == '\n')
		i++;
	if (!last->content[i])
		return (NULL);
	j = 0;
	while (last->content[i + j])
		j++;
	buf = malloc(j + 1);
	if (!buf)
		return (NULL);
	buf[j] = '\0';
	while (j--)
		buf[j] = last->content[i + j];
	return (buf);
}

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

char	*get_next_line(int fd)
{
	static t_buf *lst;
	t_buf *last;
	char *line;
	char *rem;

	fill_list(fd, &lst);
	line = extract_line(lst);
	last = lst;
	while (last->next)
		last = last->next;
	rem = get_remaining(last);
	free_list(&lst);
	if (rem)
		append_node(&lst, rem);
	return (line);
}
