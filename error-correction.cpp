#include <iostream>
#include <random>
#include <string>
using namespace std;

string generateRandomString(int length) {
    random_device rd; 
    mt19937 gen(rd());
    uniform_int_distribution<> dis(0, 1);

    string randomString;
    for (int i = 0; i < length; ++i) {
        randomString += to_string(dis(gen));
    }

    return randomString;
}

int main() {
    int length = 16;
    string randomString = generateRandomString(length);
    cout << randomString << endl;

    return 0;
}