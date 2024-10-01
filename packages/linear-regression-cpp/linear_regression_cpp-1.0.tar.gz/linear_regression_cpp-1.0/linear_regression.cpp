#include <iostream>
#include <string>
#include <fstream>
#include <vector>

using namespace std;

vector<string> getRowVector(string line){
    vector<string> row;
    string word = "";
    for (auto x : line) {
        if (x == ',') {
            row.push_back(word);
            word = "";
        }
        else {
            word = word + x;
        }
    }
    row.push_back(word);
    return row;
};


class Model {
private :
    float m=0;
    float c=0;
public : 
    void train(string filepath, string x_column, string y_column) {
        ifstream file(filepath);
        if (!file.is_open()) {
            cout << "File not found" << endl;
            return;
        }
        string line;
        getline(file, line);

        int column_x_index;
        int column_y_index;

        vector<string> row;
        row = getRowVector(line);

        for (int i = 0; i < row.size(); i++) {
            if (row[i] == x_column) {
                column_x_index = i;
            }
            if (row[i] == y_column) {
                column_y_index = i;
            }
        }

        float x_sum = 0;
        float y_sum = 0;
        float x_y_sum = 0;
        float x_square_sum = 0;
        int n = 0;


        while (getline(file, line)) {
            row = getRowVector(line);
            float x = stof(row[column_x_index]);
            float y = stof(row[column_y_index]);
            x_sum += x;
            y_sum += y;
            x_y_sum += x*y;
            x_square_sum += x*x;
            n++;
            cout << x << " " << y << endl;
        }

        m = (n*x_y_sum - x_sum*y_sum) / (n*x_square_sum - x_sum*x_sum);
        c = (y_sum - m*x_sum) / n;
    };

    float predict(float x) {
        return m*x + c;
    };
};


int main(){
    Model model;
    model.train("./myFile.csv", "my_x", "my_y");
    float prediction = model.predict(10);
    cout <<"prediction : " <<prediction << endl;
    return 0;
}