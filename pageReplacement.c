#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <ctype.h>

#define MAX_FRAMES 20
#define MAX_REF_STR_LEN 80
//use gcc - pedantic -O0 -Wformat -Wreturn-type -lm minilab5.c to compile
//use ./a.out #-of-fames policy-id text-file to run
int is_in_frames(int frames[], int page, int num_frames) {
	for(int i = 0; i < num_frames; i++){
		if(frames[i] == page){
		return 1;
		}
	}
	return 0;
}

int find_fifo_index(int queue[], int num_frames, int *fifo_index) {
	int replace_index = *fifo_index;
	*fifo_index = (*fifo_index + 1) % num_frames;
	return replace_index;
}

int find_lru_index(int frames[], int last_used[], int num_frames){
	int lru_index = 0, min_last_used = last_used[0];
	for(int i = 1; i < num_frames; i++){
		if(last_used[i] < min_last_used){
			min_last_used = last_used[i];
			lru_index = i;
		}
	}
	return lru_index;
}

int find_optimal_index(int frames[], int num_frames, int ref_str[], int ref_len, int current_index, int last_used[]) {
	int farthest_index = -1, optimal_index = -1;
	int never_used_again_count = 0, no_future_access[MAX_FRAMES];

	for(int i = 0; i < num_frames; i++){
	int found = 0;
	for(int j = current_index + 1; j < ref_len; j++){
		if(frames[i] == ref_str[j]){
			if(j > farthest_index){
				farthest_index = j;
				optimal_index = i;
			}
			found = 1;
			break;
		}
	}
	if(!found){
		no_future_access[never_used_again_count++] = i;
	}
	}
	
	if(never_used_again_count > 0){
	int lru_index = no_future_access[0];
        int min_last_used = last_used[lru_index];
        for (int i = 1; i < never_used_again_count; i++) {
            int index = no_future_access[i];
            if (last_used[index] < min_last_used) {
                min_last_used = last_used[index];
                lru_index = index;
            }
        }
        return lru_index;
    }
	return optimal_index;
}

int map_letter_to_page(char letter) {
    // Mapping A = 0, B = 1, C = 2, ... Z = 25
    if (isalpha(letter)) {
	
        return toupper(letter) - 'A';  // Returns 0 for A, 1 for B, and so on
    }
    return -1; // Invalid mapping
}

void page_replacement(int ref_str[], int ref_len, int num_frames, int policy_id){
	int frames[MAX_FRAMES], queue[MAX_FRAMES], last_used[MAX_FRAMES];
	int fifo_index = 0, page_faults = 0;
	int time = 0;
	int page = 0;

	const char *policy_name;
	switch(policy_id){
	case 0: policy_name = "Optimal"; break;
	case 1: policy_name = "FIFO"; break;
	case 2: policy_name = "LRU"; break;
	default: printf("Invalid policy ID \n"); exit(1);
	}

	for(int i = 0; i < num_frames; i++){
	frames[i] = -1;
	}

	printf("Using %s policy \n", policy_name);

	for(int i = 0; i < ref_len; i++){
	page = ref_str[i];
	time++;
	
	if(!is_in_frames(frames, page, num_frames)){
		page_faults++;
				
		int replace_index;
		if(policy_id == 1){
		replace_index = find_fifo_index(queue, num_frames, &fifo_index);
		} else if(policy_id == 2){
		replace_index = find_lru_index(frames, last_used, num_frames); 
		} else if(policy_id == 0){
		replace_index = find_optimal_index(frames, num_frames, ref_str, ref_len, i, last_used); 
		}
		frames[replace_index] = page;
	}
	}
	for(int j = 0; j < num_frames; j++){
		if(frames[j] == page){
			last_used[j] = time;
			break;
		}
	}

	printf("Page %d -> Frames: ", page);
	for(int j = 0; j < num_frames; j++) {
		if(frames[j] != -1){
		char letter = (char)(frames[j] + 'A');
		printf("%c ", letter);
		}else {
			printf(". ");
		}
		printf("\n");
	}
	printf("Total Page Faults: %d\n", page_faults);
	printf("Total Page References: %d\n", ref_len);
    printf("Final State of Memory: \n");
    for (int i = 0; i < num_frames; i++) {
        if (frames[i] != -1) {
        char letter = (char)(frames[i] + 'A');
	printf("%c ", letter);
        }else{
            printf(". ");
    }

}
}

int main(int argc, char *argv[]) { 
	

	int num_frames = atoi(argv[1]);
    	int policy_id = atoi(argv[2]);
    	const char *filename = argv[3];

	if (num_frames <= 0 || num_frames > MAX_FRAMES) {
        printf("Error: Number of frames must be between 1 and %d.\n", MAX_FRAMES);
        return 1;
    	}

	FILE *file = fopen(filename, "r");
	if(!file){
	perror("Error opening file.");
	return 1;
	}

	int ref_str[MAX_REF_STR_LEN], ref_len = 0;
	char page_input[10];
	printf("Reading reference string from file '%s':\n", filename);

	while (fscanf(file, "%c", page_input) == 1 && ref_len < MAX_REF_STR_LEN) {
        int page;
        if (isalpha(page_input[0])) {  // If it's a letter
            page = map_letter_to_page(page_input[0]);
        } else {  // If it's a number
            page = atoi(page_input);
        }

        if (page >= 0) {  // Only add valid pages
            ref_str[ref_len] = page;
	    
        } else {
            printf("Invalid page reference: %s\n", page_input);
        }
	ref_len++;
    }
    fclose(file);

    printf("Number of Frames: %d\n", num_frames);
    printf("Policy ID: %d\n", policy_id);
    printf("Reference String Length: %d\n", ref_len);
    printf("Reference String: \n");
    for (int i = 0; i < ref_len; i++) {
        char letter = (char)(ref_str[i] + 'A');
	printf("%c \n", letter);
    }
    printf("\n");

    // Run the chosen page replacement policy
    page_replacement(ref_str, ref_len, num_frames, policy_id);

    return 0;
}
