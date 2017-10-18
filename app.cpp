/*
Profilepal

This is a skeleton for the project with focus on front-end and back-end communication.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <vector>
#include <string>
#include <fstream>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <algorithm>
using namespace std;

#define	MAXLINE	8192
#define  SA struct sockaddr
#define	GROUP		"hs2685@code.engineering.nyu.edu"	// replace with the server address
#define PORT_NUM        9001	//replace with the port you are using

vector<string> EXED;

// sends back an indicator indicating if the username has been used before. if username has not been used, create entry in database for the user.
void signUp(string& info, int& fd, fstream& fs, struct sockaddr_in& addr, string& uid) {
	size_t n = info.find("\n");
	string username = info.substr(0, n);
	string password = info.substr(n + 1, info.length() - n);
	if (-1 == -1) { // placeholder. username doesn't already exist
		string tmp = uid + "t";
		char* t = (char *)tmp.c_str();
		sendto(fd, t, sizeof(t), 0, (struct sockaddr *) &addr, sizeof(addr));

		// create entry in DB



	}
	else {
		string tmp = uid + "f";
		char* f = (char *)tmp.c_str();
		sendto(fd, f, sizeof(f), 0, (struct sockaddr *) &addr, sizeof(addr));
	}
}

// checks if the username exists and if the password is correct.
void logIn(string& info, int& fd, fstream& fs, struct sockaddr_in& addr, string& uid) {
	size_t n = info.find("\n");
	string username = info.substr(0, n);
	string password = info.substr(n + 1, info.length() - n);
	if (-1 == -1) { // placeholder. if username doean't exist
		string tmp = uid + "0";
		char* zero = (char *)tmp.c_str();
		sendto(fd, zero, sizeof(zero), 0, (struct sockaddr *) &addr, sizeof(addr));
	}
	else {
		// check password
		

		if (1 == 1) { //placeholder. password correct
			string tmp = uid + "3";
			char* three = (char *)tmp.c_str();
			sendto(fd, three, sizeof(three), 0, (struct sockaddr *) &addr, sizeof(addr));
		}
		else {
			string tmp = uid + "2";
			char* two = (char *)tmp.c_str();
			sendto(fd, two, sizeof(two), 0, (struct sockaddr *) &addr, sizeof(addr));
		}
	}
}

void handleRequest(int& fd, string buff, struct sockaddr_in& addr) {
	fstream fs;
	string uid = buff.substr(0, 32);	// unique identifier
	if (find(EXED.begin(), EXED.end(), uid) != EXED.end()) return; // request already processed
	EXED.push_back(uid);
	buff = buff.substr(32, buff.length() - 32);
	string cmd = buff.substr(0, 2);		// action to take
	int n = buff.length();
	string info = buff.substr(2, n - 2);

	if (cmd == "SU") { //sign up. 
		signUp(info, fd, fs, addr, uid);
	}
	else if (cmd == "LI") { // log in. 
		logIn(info, fd, fs, addr, uid);
	}
	else if (cmd == "DA") { // delete account. remove from DB
		


	}
	//else if ... other functions


}

int main() {
	struct sockaddr_in addr;
	int fd, nbytes;
	struct ip_mreq mreq;
	char buff[MAXLINE];

	unsigned yes = 1;

	if ((fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) { // create the socket
		perror("socket");
		exit(1);
	}


	if (setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) < 0) { // allow multiple sockets to use the same PORT number
		perror("Reusing ADDR failed");
		exit(1);
	}

	// set up destination address
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	addr.sin_addr.s_addr = htonl(INADDR_ANY);
	addr.sin_port = htons(PORT_NUM);

	// bind to receive address
	if (bind(fd, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
		perror("bind");
		exit(1);
	}

	// use setsockopt() to request that the kernel join a multicast group
	mreq.imr_multiaddr.s_addr = inet_addr(GROUP);
	mreq.imr_interface.s_addr = htonl(INADDR_ANY);
	if (setsockopt(fd, IPPROTO_IP, IP_ADD_MEMBERSHIP, &mreq, sizeof(mreq)) < 0) {
		perror("setsockopt");
		exit(1);
	}

	for (; ; ) {
		unsigned addrlen = sizeof(addr);
		if ((nbytes = recvfrom(fd, buff, MAXLINE, 0,
			(struct sockaddr *) &addr, &addrlen)) < 0) {
			perror("recvfrom");
			exit(1);
		}

		handleRequest(fd, string(buff), addr);
	}
}