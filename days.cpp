#include <cstdint>
#include <thread>
#include <ctime>
#include <cmath>
#include <vector>
#include <stdint.h>



void calculate_n(std::time_t* daty, int64_t* czasy, int64_t size, int  thread_id, int thread_count) {
    for(int i=thread_id; i<size; i+=thread_count) {
        if(daty[i] == 0)
            czasy[i] = -1;
        else
            czasy[i] = std::ceil(std::difftime(daty[i],std::time(0)) / 3600 / 24);
    }
}

extern "C"
int64_t* calculate_days(std::time_t* daty, int64_t size) {
    int64_t* czasy = new int64_t[size];
    int thread_count = std::thread::hardware_concurrency();
    std::vector<std::thread> watki;
    for(int i=0;i<thread_count;i++)
        watki.push_back(std::thread(calculate_n,daty,czasy,size,i,thread_count));
    for(int i=0;i<thread_count;i++)
        watki[i].join();
    return czasy;
}

extern "C"
void free_days(int64_t* czasy){
    delete czasy;
}