/* BY SUBMITTING THIS FILE TO CARMEN, I CERTIFY THAT I HAVE PERFORMED ALL OF THE
** WORK TO CREATE THIS FILE AND/OR DETERMINE THE ANSWERS FOUND WITHIN THIS
** FILE MYSELF WITH NO ASSISTANCE FROM ANY PERSON (OTHER THAN THE INSTRUCTOR
** OR GRADERS OF THIS COURSE) AND I HAVE STRICTLY ADHERED TO THE TENURES OF THE
** OHIO STATE UNIVERSITY’S ACADEMIC INTEGRITY POLICY.
     */
#include "lab3.h"
#include <stdio.h>
#include <stdlib.h>

//Function to get the title names
void getTitles(char **titles, int titleNum) {
//Asks the user for the titles and stores them in a dynamically allocatted
//array
printf("Enter the %i book titles one to a line: ", titleNum);
int i = 0;
for(i; i < titleNum; i++){
titles[i] = malloc(60*sizeof(char));
scanf(" %[^\n]", titles[i]);
}
}
//Function to get the favorite book titles
void getFavorites(int *favorites, char **titles, int numFav) {
printf("Which numbers would you like to be your favorites?: \n");
//Obtians the title numbers that the user wants as their favorites
int i = 0;
for(i; i < numFav; i++){
scanf("%d", favorites);
}
//Stores those titles inside the titles array
int j = 0;
for(j; j < numFav; j++) {
titles[favorites[j]];
}
}
//Function to print out the book titles
void bookTitles( char** titles, int titleNum) {
getTitles(titles, titleNum);


printf("You've Entered: \n");
//Foor loop that prints out the book titles
int i = 0;
for(i; i < titleNum; i++) {
printf("%i. ", i);
printf("%s \n", *titles++);
}
}
//Function to print out the favorite titles
void bookFavorites(int *favorites, char **titles, int numFav) {
getFavorites(favorites, titles, numFav);

printf("Your favorites are: \n");
//For loop to print out the favorite titles
int i = 0;
for(i; i < numFav; i++){
printf("%i. ", i);
printf("%s \n", *titles++);
}
}
//Function to write to a file
void dataSave(char fileName,  char **titles, int titleNum) {
    //Initializes the open method and opens the file
FILE*out; 
out = fopen(&fileName, "w");
//Writes each title to the file and then closes the stream
int i = 0;
for(i; i < titleNum; i++) {
fputs(*titles++, out);
fclose(out);
}
}

int main() {
//Initialized necessary variables
int titleNum;
int numFav;
int userInput;
char fileName;
//Obtains the number of titles
printf("Please enter the number of book titles: ");
scanf("%i", &titleNum);
//Dynamically allocates an array to store the titles in
char **titles = malloc(titleNum * sizeof(char *));
//Prints out the book titles
bookTitles(titles, titleNum);
//Obtains the number of favorite titles
printf("Please enter the number of your favorite book titles: ");
scanf("%i", &numFav);

//Dynamically allocates an array for the favorites and prints 
//them out
int *favorites = malloc(numFav*sizeof(numFav));
bookFavorites(favorites, titles, numFav);
//Sees if the user wants to write to a file
printf("Please enter 1 for yes, and 2 for no if you want to save data to a file: \n");
scanf("%i", &userInput);
//Writes to the file if the user input is 1
if(userInput == 1) {
printf("What file name would you like to use?: \n");
scanf("%s", &fileName);
dataSave(fileName, titles, titleNum);
printf("Your data has been saved to %c. \n", fileName);
}

return 0;
}
