#include<stdio.h>
#include<netdb.h>
#include<netinet/in.h>
#include<stdlib.h>
#include<string.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<unistd.h>
#include <ctype.h>

#define MAX 80
#define PORT 8080
#define SA struct sockaddr


void chat(int connfd){
    char key[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    int kl = sizeof(key); 
    char buff[MAX];
    int n;
    int flag = 0;
    for(;;){
        bzero(buff,MAX);
        read(connfd, buff, sizeof(buff));
        // Decrypt using Vernam cipher
        for(int i = 0, j = 0; i < sizeof(buff); i++){
            if(buff[i] == '\n')
                break;
            // if(!isalpha(buff[i]))
            //     continue;

            int shift = key[j % kl] - 'A';
            buff[i] = buff[i] ^ shift;
            j++;
        }

        printf("Client: %sServer: ", buff);

        bzero(buff, MAX);
        n = 0;
        while((buff[n++] = getchar()) != '\n');

        if(strncmp(buff, "exit", 4) == 0){
            printf("Server exit\n");
            flag = 1;
        }

        // Encrypt using Vernam cipher
        for(int i = 0, j = 0; i < n - 1; i++){
            // if(!isalpha(buff[i]))
            //     continue;

            int shift = key[j % kl] - 'A';
            buff[i] = buff[i] ^ shift;
            j++;
        }
        write(connfd, buff, sizeof(buff));
        if(flag)
            break;
    }
}

int main(){
    int sockfd, connfd, len;
    struct sockaddr_in servaddr, cli;

    // Create socket and verify
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd == -1){
        printf("Socket creation failed\n");
        exit(0);
    }
    else
        printf("Socket created successfully\n");

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);

    if((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0){
        printf("Socket bind failed\n");
        exit(0);
    }
    else
        printf("Socket bound successfully!\n");

    if((listen(sockfd, 5)) != 0 ){
        printf("Listen failed\n");
        exit(0);   
    }
    else
        printf("Server listening\n");

    len = sizeof(cli);
    connfd = accept(sockfd, (SA*)&cli, &len);
    if(connfd < 0){
        printf("Server failed to accept the client\n");
        exit(0);
    }
    else
        printf("Server has accepted the client.\n");

    chat(connfd);
    close(sockfd);
}
