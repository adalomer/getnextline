#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include "get_next_line.h"

int	main(int argc, char **argv)
{
	int		fd;
	char	*line;
	int		line_count;

	// Eğer argüman olarak dosya yolu verilmişse onu açar, yoksa "test.txt" dosyasını açar
	if (argc > 1)
		fd = open(argv[1], O_RDONLY);
	else
		fd = open("test.txt", O_RDONLY);

	if (fd < 0)
	{
		perror("Dosya acma hatasi");
		return (1);
	}

	line_count = 1;
	printf("=== GET NEXT LINE TEST BASLADI ===\n");
	while ((line = get_next_line(fd)) != NULL)
	{
		printf("[%02d]: %s", line_count++, line);
		free(line); // get_next_line malloc kullandığı için her satır free edilmelidir!
	}
	printf("\n=== DOSYA SONUNA ULASILDI (EOF) ===\n");

	close(fd);
	return (0);
}
