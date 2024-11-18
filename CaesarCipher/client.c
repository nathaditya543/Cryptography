#include <arpa/inet.h> // inet_addr()
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h> // bzero()
#include <sys/socket.h>
#include <unistd.h> // read(), write(), close()
#define MAX 80
#define PORT 8080
#define SA struct sockaddr

void chat(int sockfd){
    char buff[MAX];
    int n;
    for(;;){
        bzero(buff, sizeof(buff));
        printf("Client: ");
        n = 0;
        while((buff[n++] = getchar())!= '\n');
        
        //encrypt
        for(int i = 0; i < n-1; i++){
            if((int)buff[i] < (int)'a')
                buff[i] = (char)((((int)buff[i] - (int)'A' + 3) % 26) + (int)'A');
            else
                buff[i] = (char)((((int)buff[i] - (int)'a' + 3) % 26) + (int)'a');
        }
        write(sockfd, buff, sizeof(buff));
        bzero(buff, sizeof(buff));

        read(sockfd, buff, sizeof(buff));
        
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

        printf("Server: %s", buff);

        if(strncmp(buff, "exit", 4) == 0){
            printf("Client exit\n");
            exit(0);
        }
    }
}

int main(){
    int sockfd, connfd;
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if(sockfd == -1){
        printf("Socket creation failed!\n");
        exit(0);
    }
    else    
        printf("Socket created succesfully!\n");

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);

    if(connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0){
        printf("Connection to server failed!\n");
        exit(0);
    }
    else
        printf("Connection to server succesfull!\n");
    
    chat(sockfd); 
    close(sockfd);
}