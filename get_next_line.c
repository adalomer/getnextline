/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: omadali <adalomer60@gmail.com>             +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/11/07 21:51:50 by omadali           #+#    #+#             */
/*   Updated: 2024/11/07 23:51:02 by omadali          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char *get_next_line(int fd)
{
	char *a;
	static char *f;
	int b;
	int c;

	b = 0;
	c = 0;
	a = malloc((BUFFER_SIZE +1)*sizeof(char));
	read(fd,a,BUFFER_SIZE);
	
	while(a[c] != '\n')
		c++;
	if(a[c] == '\n')
	{
		f = malloc((c + 1)*sizeof(char));
		while(c-- >= 0)
		{
			f[b] = a[b];
			b++;
		}
	}
	f[b] = '\0';
	//printf("%d",b);
	return(f);
}
int main()
{
	int fd = open("deneme.txt", O_RDONLY,111);
	for(int i = 0;i < 4; i++ )
	printf("%s",get_next_line(fd));
	
}
