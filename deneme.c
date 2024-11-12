#include <stdio.h>
#include <fcntl.h>
#include "get_next_line.h"

int main()
{
	int fd_4 = open("deneme.txt", O_RDONLY);
	printf("%s", get_next_line(fd_4));
	printf("%s\n", get_next_line(fd_4));
	printf("%s\n", get_next_line(fd_4));
}
