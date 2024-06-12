#include <rapidxml/rapidxml.hpp>

#include <iostream>
#include <fstream>

using namespace std;

using namespace rapidxml;

int main(int argc, char** argv){
    
    ifstream gpx("/home/mosdon/Desktop/berke/data/kiran.gpx");

    if(!gpx.is_open()) {
        cerr << "File path is wrong!" << endl;
        return -1;
    }

    string str((istreambuf_iterator<char>(gpx)), istreambuf_iterator<char>());

    xml_document<> doc;
    doc.parse<0>(str.data());


    return 0;

}