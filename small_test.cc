#include<vector>
#include<iostream>
using namespace std;

int main() {
    vector<int>v_2(4);
    vector<int>v(1);
    for (int k = 1; k < 10; k++) {
		v_2.insert(v_2.begin(), 10);
        v.insert(v.end(), 10);
     }
    for (int k = 0; k < 13; k++) {
        cout << v[k] << " " << v_2[k] << "\n"  ;
    }
    return 0;
}
