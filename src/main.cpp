/**
 * 
 * dependency order
 * 
 * 1. our own headers
 * 2. 3rd partys
 * 3. cpp level
 * 4. c level
 * 5. os level
 */
#include <rapidxml.hpp>
#include <nlohmann/json.hpp>

#include <iostream>
#include <fstream>
#include <vector>

using namespace std;

using namespace rapidxml;
using namespace nlohmann;

struct Point final {
    double lat;
    double lon;
    double ele;
    
    string time;
};

int main(int argc, char** argv){
    
    ifstream gpx("/home/mosdon/Desktop/berke/gpx-draw/data/kiran.gpx");

    if(!gpx.is_open()) {
        cerr << "File path is wrong!" << endl;
        return -1;
    }

    string str((istreambuf_iterator<char>(gpx)), istreambuf_iterator<char>());

    xml_document<> doc;
     doc.parse<0>(str.data()); 
   

    vector<Point> points;
     xml_node<>* rootNode = doc.first_node("gpx");
    if (rootNode) {

         xml_node<>* trksegNode = rootNode->first_node("trk")->first_node("trkseg");
         if (trksegNode) {

            for (xml_node<>* trkptNode = trksegNode->first_node("trkpt"); trkptNode; trkptNode = trkptNode->next_sibling("trkpt")) {
                Point pt;
                
                pt.lat = std::stod(trkptNode->first_attribute("lat")->value());
                pt.lon = std::stod(trkptNode->first_attribute("lon")->value());

                
                xml_node<>* eleNode = trkptNode->first_node("ele");
                if (eleNode) 
                    pt.ele = std::stod(eleNode->value());
                else 
                    pt.ele = 0.0;
   
                xml_node<>* timeNode = trkptNode->first_node("time");
                if (timeNode) 
                    pt.time = timeNode->value();
                else
                    pt.time = ""; 


                points.push_back(pt);
            }
        }
    }


  json jPoints;
    for (const auto& pt : points) {
        json jPoint;
        jPoint["lat"] = pt.lat;
        jPoint["lon"] = pt.lon;
        jPoint["ele"] = pt.ele;
        jPoint["time"] = pt.time;
        jPoints.push_back(jPoint);
    }

    ofstream outputFile("gpxoutput.json");
    outputFile << jPoints.dump(4); 
    cout << "JSON dosyası oluşturuldu: gpxoutput.json" << endl;        

    return 0;

}