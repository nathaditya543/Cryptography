#include <stdio.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <ctype.h>

#define MAX 80
#define PORT 8080
#define SA struct sockaddr

void encryptRailFence(char *plaintext, char *ciphertext, int key) {
    int len = strlen(plaintext);
    int k = 0;
    char rail[key][len];

    for (int i = 0; i < key; i++)
        for (int j = 0; j < len; j++)
            rail[i][j] = '\n';

    int row = 0;
    int dir = -1;
    for (int i = 0; i < len; i++) {
        rail[row][i] = plaintext[i];
        if (row == 0 || row == key - 1)
            dir *= -1;
        row += dir;
    }

    for (int i = 0; i < key; i++) {
        for (int j = 0; j < len; j++) {
            if (rail[i][j] != '\n') {
                ciphertext[k++] = rail[i][j];
            }
        }
    }
    ciphertext[k] = '\0';
}

void decryptRailFence(char *ciphertext, char *plaintext, int key) {
    int len = strlen(ciphertext);
    char rail[key][len];
    int k = 0;

    for (int i = 0; i < key; i++)
        for (int j = 0; j < len; j++)
            rail[i][j] = '\n';

    int row = 0;
    int dir = -1;
    for (int i = 0; i < len; i++) {
        rail[row][i] = '*';
        if (row == 0 || row == key - 1)
            dir *= -1;
        row += dir;
    }

    for (int i = 0; i < key; i++)
        for (int j = 0; j < len; j++)
            if (rail[i][j] == '*')
                rail[i][j] = ciphertext[k++];

    row = 0;
    dir = -1;
    k = 0;
    for (int i = 0; i < len; i++) {
        plaintext[i] = rail[row][i];
        if (row == 0 || row == key - 1)
            dir *= -1;
        row += dir;
    }
    plaintext[len] = '\0';
}

void chat(int connfd) {
    int key = 3;
    char buff[MAX];
    int n;
    int flag = 0;
    for (;;) {
        bzero(buff, MAX);
        read(connfd, buff, sizeof(buff));

        char decrypted[MAX];
        decryptRailFence(buff, decrypted, key);

        printf("Client: %s\nServer: ", decrypted);

        bzero(buff, MAX);
        n = 0;
        while ((buff[n++] = getchar()) != '\n');

        if (strncmp(buff, "exit", 4) == 0) {
            printf("Server exit\n");
            flag = 1;
        }

        char encrypted[MAX];
        encryptRailFence(buff, encrypted, key);

        write(connfd, encrypted, sizeof(encrypted));
        if (flag)
            break;
    }
}

int main() {
    int sockfd, connfd, len;
    struct sockaddr_in servaddr, cli;

    // Create socket and verify
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("Socket creation failed\n");
        exit(0);
    } else
        printf("Socket created successfully\n");

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);

    if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) {
        printf("Socket bind failed\n");
        exit(0);
    } else
        printf("Socket bound successfully!\n");

    if ((listen(sockfd, 5)) != 0) {
        printf("Listen failed\n");
        exit(0);
    } else
        printf("Server listening\n");

    len = sizeof(cli);
    connfd = accept(sockfd, (SA*)&cli, &len);
    if (connfd < 0) {
        printf("Server failed to accept the client\n");
        exit(0);
    } else
        printf("Server has accepted the client.\n");

    chat(connfd);
    close(sockfd);
}
