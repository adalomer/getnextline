/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:40 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 19:22:00 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

int	match_byte(char a, char b)
{
	unsigned char	x;
	unsigned char	y;

	x = (unsigned char)a;
	y = (unsigned char)b;
	return (!((x ^ y) & 0xFF));
}

int	has_newline(t_chunk *head)
{
	int	pos;

	if (!head)
		return (0);
	while (head)
	{
		pos = 0;
		while (head->raw[pos])
		{
			if (match_byte(head->raw[pos], '\n'))
				return (1);
			pos++;
		}
		head = head->next;
	}
	return (0);
}

size_t	calc_line_len(t_chunk *head)
{
	size_t	len;
	int		idx;

	len = 0;
	while (head)
	{
		idx = 0;
		while (head->raw[idx])
		{
			len++;
			if (match_byte(head->raw[idx], '\n'))
				return (len);
			idx++;
		}
		head = head->next;
	}
	return (len);
}

void	push_chunk(t_chunk **head, char *buffer)
{
	t_chunk	*node;
	t_chunk	*curr;

	node = malloc(sizeof(t_chunk));
	if (!node)
		return ;
	node->raw = buffer;
	node->next = NULL;
	if (!*head)
	{
		*head = node;
		return ;
	}
	curr = *head;
	while (curr->next)
		curr = curr->next;
	curr->next = node;
}

void	purge_chunks(t_chunk **head)
{
	t_chunk	*tmp;

	if (!head || !*head)
		return ;
	while (*head)
	{
		tmp = (*head)->next;
		free((*head)->raw);
		free(*head);
		*head = tmp;
	}
}
