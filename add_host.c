#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main(int argc, char ** const argv) {
	setuid(0);
	system("echo \"127.0.0.1      metadata.google.internal\" >> /etc/hosts");
	return 0;
}