/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali < omadali@student.42kocaeli.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/09/11 15:34:32 by omadali           #+#    #+#             */
/*   Updated: 2026/09/11 16:48:03 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 10
# endif

typedef struct s_buf
{
	char			*content;
	struct s_buf	*next;
}	t_buf;

int		find_nl(t_buf *lst);
int		line_len(t_buf *lst);
void	append_node(t_buf **lst, char *buf);
void	free_list(t_buf **lst);

#endif
