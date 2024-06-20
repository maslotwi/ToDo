#include <thread>
#include <ctime>

void count_days(std::time_t* daty, int size);

void count_n(std::time_t* daty, int* czasy, int size, int thread_id, int thread_count) {
    for(int i=thread_id; i<size; i+=thread_count) {
        czasy[i] = std::difftime(std::time(0),daty[0]);
    }
}