#include <arpa/inet.h> // inet_addr()
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h> // bzero()
#include <sys/socket.h>
#include <unistd.h> // read(), write(), close()
#include<bits/stdc++.h>
#define MAX 80
#define PORT 8080
#define SA struct sockaddr
using namespace std;

string round_keys[16];  
string shift_left_once(string key_chunk){  
	string shifted="";  
	for(int i = 1; i < 28; i++)
		shifted += key_chunk[i];  
	
	shifted += key_chunk[0];  
	return shifted;  
}

string shift_left_twice(string key_chunk){  
	string shifted="";  
	for(int i = 0; i < 2; i++){  
		for(int j = 1; j < 28; j++){  
			shifted += key_chunk[j];  
		}  
		shifted += key_chunk[0];  
		key_chunk= shifted;  
		shifted ="";  
	}  
	return key_chunk;  
} 

void generate_keys(string key){  
	int pc1[56] = {  
	57,49,41,33,25,17,9,  
	1,58,50,42,34,26,18,  
	10,2,59,51,43,35,27,  
	19,11,3,60,52,44,36,  
	63,55,47,39,31,23,15,  
	7,62,54,46,38,30,22,  
	14,6,61,53,45,37,29,  
	21,13,5,28,20,12,4};

	int pc2[48] = {  
	14,17,11,24,1,5,  
	3,28,15,6,21,10,  
	23,19,12,4,26,8,  
	16,7,27,20,13,2,  
	41,52,31,37,47,55,  
	30,40,51,45,33,48,  
	44,49,39,56,34,53,  
	46,42,50,36,29,32}; 

	string perm_key ="";  
	for(int i = 0; i < 56; i++)
		perm_key+= key[pc1[i]-1];  

	string left= perm_key.substr(0, 28);  
	string right= perm_key.substr(28, 28);  
	for(int i=0; i<16; i++){  
		if(i == 0 || i == 1 || i==8 || i==15 ){  
			left= shift_left_once(left);  
			right= shift_left_once(right);  
		}  
		else{  
			left= shift_left_twice(left);  
			right= shift_left_twice(right);  
		}  
		string combined_key = left + right;  
		string round_key = "";  
		for(int i = 0; i < 48; i++)
			round_key += combined_key[pc2[i]-1];

		round_keys[i] = round_key;  
		cout<<"Key "<<i+1<<": "<<round_keys[i]<<endl;  
	}  
} 

void chat(int sockfd){
	char buff[MAX];
	int n;
	for (;;) {
		bzero(buff, sizeof(buff));
		printf("Client: ");
		n = 0;
		while ((buff[n++] = getchar()) != '\n');
		write(sockfd, buff, sizeof(buff));

		bzero(buff, sizeof(buff));
		read(sockfd, buff, sizeof(buff));
		printf("Server : %s", buff);
		if ((strncmp(buff, "exit", 4)) == 0) {
			printf("Client Exit...\n");
			break;
		}
	}
}

int main(){
	int sockfd, connfd;
	struct sockaddr_in servaddr, cli;

	// socket create and verification
	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if (sockfd == -1) {
		printf("socket creation failed...\n");
		exit(0);
	}
	else
		printf("Socket successfully created..\n");
	bzero(&servaddr, sizeof(servaddr));

	// assign IP, PORT
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	servaddr.sin_port = htons(PORT);

	// connect the client socket to server socket
	if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr))
		!= 0) {
		printf("connection with the server failed...\n");
		exit(0);
	}
	else
		printf("connected to the server..\n");

	string key = "1010101010111011000010010001100000100111001101101100110011011101";
	generate_keys(key);
	// function for chat
	chat(sockfd);
	// close the socket
	close(sockfd);

}
