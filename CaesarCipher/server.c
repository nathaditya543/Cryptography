#include<stdio.h>
#include<netdb.h>
#include<netinet/in.h>
#include<stdlib.h>
#include<string.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<unistd.h>

#define MAX 80
#define PORT 8080
#define SA struct sockaddr


void chat(int connfd){
    char buff[MAX];
    int n;
    int flag = 0;
    for(;;){
        bzero(buff,MAX);
        read(connfd, buff, sizeof(buff));
        //decrypt
        for(int i = 0; i < sizeof(buff); i++){
            if(buff[i] == '\n')
                break;

            char x = 'a';
            if((int)buff[i] < (int)'a')
                x = 'A';

            int val = ((int)buff[i] - (int)x - 3);
            if(val < 0)
                val = ((val % 26) + 26);
            buff[i] = (char)((val % 26) + (int)x);
        }
        printf("Client: %sServer: ", buff);

        bzero(buff, MAX);
        n = 0;
        while((buff[n++] = getchar()) != '\n');
        if(strncmp(buff, "exit", 4) == 0){
            printf("Server exit\n");
            flag = 1;
        }
        //decrypt
        for(int i = 0; i < n-1; i++){
            if((int)buff[i] < (int)'a')
                buff[i] = (char)((((int)buff[i] - (int)'A' + 3) % 26) + (int)'A');
            else
                buff[i] = (char)((((int)buff[i] - (int)'a' + 3) % 26) + (int)'a');
        }
        write(connfd, buff, sizeof(buff));
        if(flag)
            break;
    }
}

int main(){
    int sockfd, connfd, len;
    struct sockaddr_in servaddr, cli;
    
    //create socket and verif
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd == -1){
        printf("socket creation failed\n");
        exit(0);
    }
    else
        printf("Socket created succesfully\n");
    
    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);
    
    if((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0){
        printf("socket bind failed\n");
        exit(0);
    }
    else
        printf("Socket bound succesfully!\n");

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