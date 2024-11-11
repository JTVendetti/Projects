#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define BUFFER_SIZE 256
//use gcc - pedantic -O0 -Wformat -Wreturn-type -lm lab3-shell.c to compile
//use ./a/out to execute
static char buffer[BUFFER_SIZE];
char commands[10][BUFFER_SIZE];
int command_count = 0;
int MAX_COMMANDS = 10;


//Function to handle the caught signal and to print out the commands
void handle_sigint(int sig) {
printf("Caught signal %d \n", sig);

 
int left = 0, right = (command_count < MAX_COMMANDS) ? command_count - 1 : MAX_COMMANDS - 1;
        int index = 0;

	char temp[MAX_COMMANDS][BUFFER_SIZE];
        // Fill the temp array in Crescent-Diminishing Order
        while (left <= right) {
            if (index % 2 == 0) {
                strcpy(temp[index++], commands[left++]);  // Take from the start for even indices
            } else {
                strcpy(temp[index++], commands[right--]); // Take from the end for odd indices
            }
        }

        // Print the commands in the Crescent-Diminishing Order if there are any commands
      if(command_count > 0){
	for (int i = 0; i < command_count && i < MAX_COMMANDS; i++) {
            printf("%d: %s", i + 1, temp[i]);
        }
	}else{
		printf("No commands in command hsitory.");
    	}
		
}


void store_command(const char *command) {
    // Use a circular buffer to store the command in the commands array
    strcpy(commands[command_count % MAX_COMMANDS], command);
    commands[command_count % MAX_COMMANDS][BUFFER_SIZE - 1] = '\0';
    command_count++;
}

void execute_recent_command(char letter) {
    for (int i = command_count - 1; i >= 0; i--) {
        if (commands[i % MAX_COMMANDS][0] == letter) {
            printf("Executing: %s", commands[i % MAX_COMMANDS]);
            system(commands[i % MAX_COMMANDS]);
            store_command(commands[i % MAX_COMMANDS]); // Store only the executed command
            return;
        }
    }
    printf("No command found starting with '%c'.\n", letter);
}

void re_execute_most_recent_command() {
    if (command_count > 0) {
        printf("Re-executing: %s", commands[(command_count - 1) % MAX_COMMANDS]);
        system(commands[(command_count - 1) % MAX_COMMANDS]);
        store_command(commands[(command_count - 1) % MAX_COMMANDS]); // Store only the executed command
    } else {
        printf("No commands in history to re-execute.\n");
    }
}

int main() {
printf("Program running. Enter commands, or use 'r x' to re-run commands. Press Ctrl+C to display the last 10 commands.\n");
signal(SIGINT, handle_sigint);
char buffer[BUFFER_SIZE];
while(1){
	 printf("Enter a command: ");
      		fgets(buffer, sizeof(buffer), stdin);
            
    // Check for 'r' command shortcuts
	if(buffer[0] != '\n'){
        if (strncmp(buffer, "r ", 2) == 0 && buffer[2] != '\n' && buffer[3] == '\n') {
            char letter = buffer[2];
            execute_recent_command(letter); // Execute the command starting with 'letter'
        } else if (strcmp(buffer, "r\n") == 0) {
            re_execute_most_recent_command(); // Re-execute the most recent command
        } else {
            // Store and execute the entered command normally
            store_command(buffer);
	    
            printf("Executing: %s", buffer);
            system(buffer);
	    
       } 
	}else{
		printf("Please enter a command. \n");
           }
    
	}
return 0;
}
