/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:40 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 19:35:00 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	is_byte_eq(char a, char b)
{
	return (!((unsigned char)a ^ (unsigned char)b));
}

int	check_nl_in_chain(t_chunk *head)
{
	size_t	i;

	while (head)
	{
		i = head->offset;
		while (i < head->size)
		{
			if (is_byte_eq(head->raw[i], '\n'))
				return (1);
			i++;
		}
		head = head->next;
	}
	return (0);
}

size_t	measure_line_bytes(t_chunk *head)
{
	size_t	total;
	size_t	i;

	total = 0;
	while (head)
	{
		i = head->offset;
		while (i < head->size)
		{
			total++;
			if (is_byte_eq(head->raw[i], '\n'))
				return (total);
			i++;
		}
		head = head->next;
	}
	return (total);
}

void	append_stream_chunk(t_chunk **head, char *buf, size_t sz)
{
	t_chunk	*node;
	t_chunk	*tail;

	node = malloc(sizeof(t_chunk));
	if (!node)
		return ;
	node->raw = buf;
	node->size = sz;
	node->offset = 0;
	node->next = NULL;
	if (!*head)
	{
		*head = node;
		return ;
	}
	tail = *head;
	while (tail->next)
		tail = tail->next;
	tail->next = node;
}

void	clear_stream(t_chunk **head)
{
	t_chunk	*tmp;

	if (!head)
		return ;
	while (*head)
	{
		tmp = (*head)->next;
		free((*head)->raw);
		free(*head);
		*head = tmp;
	}
}
