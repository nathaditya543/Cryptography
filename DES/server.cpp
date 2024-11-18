#include <stdio.h> 
#include <netdb.h> 
#include <netinet/in.h> 
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <unistd.h> 
#include<bits/stdc++.h>
#define MAX 80 
#define PORT 8080 
#define SA struct sockaddr
using namespace std;

string round_keys[16];

string toBin(char ch){
	int val = ch;
	string str = "";
	while(val > 1){
		str += to_string(val % 2);
		val /= 2;
	}
	str += to_string(val);
}

string buffToString(char* buff){
	string str = "";
	for(int i = 0; i < sizeof(buff); i++){
		str += toBin(buff[i]);
	}	
	int val = sizeof(str) % 64;
	for(int i = 0; i <)
	return str;
}

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

// Function designed for chat between client and server. 
void chat(int connfd) 
{ 
	char buff[MAX]; 
	int n; 
	for (;;) { 
		bzero(buff, MAX); 
		read(connfd, buff, sizeof(buff));
		string msg = buffToString(buff);

		printf("Client: %sServer : ", buff); 
		bzero(buff, MAX); 
		n = 0;

		while ((buff[n++] = getchar()) != '\n'); 
	
		write(connfd, buff, sizeof(buff)); 
		if (strncmp("exit", buff, 4) == 0) { 
			printf("Server Exit...\n"); 
			break; 
		} 
	} 
} 

// Driver function 
int main() 
{ 
	int sockfd, connfd;
    socklen_t len; 
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
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY); 
	servaddr.sin_port = htons(PORT); 

	// Binding newly created socket to given IP and verification 
	if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) { 
		printf("socket bind failed...\n"); 
		exit(0); 
	} 
	else
		printf("Socket successfully binded..\n"); 

	// Now server is ready to listen and verification 
	if ((listen(sockfd, 5)) != 0) { 
		printf("Listen failed...\n"); 
		exit(0); 
	} 
	else
		printf("Server listening..\n"); 
	len = sizeof(cli); 

	// Accept the data packet from client and verification 
	connfd = accept(sockfd, (SA*)&cli, &len); 
	if (connfd < 0) { 
		printf("server accept failed...\n"); 
		exit(0); 
	} 
	else
		printf("server accept the client...\n"); 


	string key = "1010101010111011000010010001100000100111001101101100110011011101";
	generate_keys(key);
	// Function for chatting between client and server 
	chat(connfd);
	// After chatting close the socket 
	close(sockfd); 
}
