#include <arpa/inet.h> // inet_addr()
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h> // bzero()
#include <sys/socket.h>
#include <unistd.h> // read(), write(), close()
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

void chat(int sockfd) {
    char buff[MAX];
    int key = 3;
    int n;

    for (;;) {
        bzero(buff, sizeof(buff));
        printf("Client: ");
        n = 0;

        while ((buff[n++] = getchar()) != '\n');

        buff[n - 1] = '\0'; // Remove newline character

        // Encrypt 
        char ciphertext[MAX];
        encryptRailFence(buff, ciphertext, key);

        write(sockfd, ciphertext, sizeof(ciphertext));
        bzero(buff, sizeof(buff));

        read(sockfd, buff, sizeof(buff));

        // Decrypt
        char plaintext[MAX];
        decryptRailFence(buff, plaintext, key);

        printf("Server: %s\n", plaintext);

        if (strncmp(plaintext, "exit", 4) == 0) {
            printf("Client exit\n");
            exit(0);
        }
    }
}

int main() {
    int sockfd, connfd;
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("Socket creation failed!\n");
        exit(0);
    } else
        printf("Socket created successfully!\n");

    bzero(&servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);

    if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) {
        printf("Connection to server failed!\n");
        exit(0);
    } else
        printf("Connection to server successful!\n");

    chat(sockfd);
    close(sockfd);
}
