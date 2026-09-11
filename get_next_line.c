/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:36 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 19:28:00 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static char	*get_remaining(t_buf *last)
{
	char	*buf;
	int		i;
	int		j;

	i = 0;
	while (last->content[i] && !check_byte(last->content[i], '\n'))
		i++;
	if (check_byte(last->content[i], '\n'))
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
			if (bytes == -1)
				free_list(lst);
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
		while (lst->content[i] && !check_byte(lst->content[i], '\n'))
			line[j++] = lst->content[i++];
		if (check_byte(lst->content[i], '\n'))
			line[j++] = '\n';
		if (check_byte(lst->content[i], '\n'))
			break ;
		lst = lst->next;
	}
	line[j] = '\0';
	return (line);
}

char	*get_next_line(int fd)
{
	static t_buf	*lst;
	t_buf			*last;
	char			*line;
	char			*rem;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	fill_list(fd, &lst);
	if (!lst)
		return (NULL);
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
