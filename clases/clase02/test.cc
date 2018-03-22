#include <iostream>
#include <vector>
using namespace std;

void print(int arr[], int size) {
    for(int i=0; i < size; ++i) {
        cout << arr[i] << ' ';
    }
    cout << '\n';
}

int main() {
    int midpoint = 5;
    int lower[5], upper[5];
    int j=0, k=0; //indice para lower y upper
    for(int i = 0; i < 10; ++i) {
        if (i < midpoint) {
            lower[j] = i;
            j++;
        } else {
            upper[k] = i;
            k++;
        }
    }
    print(lower, 5);
    print(upper, 5);
    
    return 0;
}
