#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <list>
#include <unordered_map>
#include <random>
#include <ctime>
#include <algorithm>
#include <sstream>

struct Node {
    int data;
    Node* next;
    Node(int data) : data(data), next(nullptr) {}
};

class LinkedList {
public:
    Node* head;
    LinkedList() : head(nullptr) {}

    void append(int data) {
        Node* new_node = new Node(data);
        if (!head) {
            head = new_node;
        } else {
            Node* current = head;
            while (current->next) {
                current = current->next;
            }
            current->next = new_node;
        }
    }

    friend std::ostream& operator<<(std::ostream& os, const LinkedList& list) {
        Node* current = list.head;
        while (current) {
            os << current->data << " -> ";
            current = current->next;
        }
        return os << "NULL";
    }
};

std::vector<std::vector<double>> readPointsFromFile(const std::string& filename) {
    std::vector<std::vector<double>> points;
    std::ifstream file(filename);
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::vector<double> point;
        double coord;
        while (iss >> coord) {
            point.push_back(coord);
        }
        points.push_back(point);
    }
    return points;
}

std::vector<double> chooseReferencePoint(const std::vector<std::vector<double>>& points) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(0, points.size() - 1);
    return points[distrib(gen)];
}

double distance(const std::vector<double>& a, const std::vector<double>& b) {
    double dist = 0.0;
    for (size_t i = 0; i < a.size(); ++i) {
        dist += (a[i] - b[i]) * (a[i] - b[i]);
    }
    return std::sqrt(dist);
}

std::unordered_map<int, LinkedList> radiusQuery(const std::vector<std::vector<double>>& points, double radius, const std::vector<double>& reference, const std::vector<int>& queryIndices) {
    std::vector<std::pair<double, int>> dist(points.size());
    for (size_t i = 0; i < points.size(); ++i) {
        dist[i] = {distance(reference, points[i]), i};
    }
    std::sort(dist.begin(), dist.end());

    std::unordered_map<int, LinkedList> hashTable;
    for (auto& p : dist) {
        hashTable[p.second] = LinkedList();
    }

    for (size_t i = 0; i < dist.size(); ++i) {
        for (size_t j = i + 1; j < dist.size() && (dist[j].first - dist[i].first) <= radius; ++j) {
            if (distance(points[dist[i].second], points[dist[j].second]) <= radius) {
                hashTable[dist[i].second].append(dist[j].second);
                hashTable[dist[j].second].append(dist[i].second);
            }
        }
    }

    std::unordered_map<int, LinkedList> result;
    for (int idx : queryIndices) {
        result[idx] = hashTable[idx];
    }
    return result;
}

void writeResultToFile(const std::unordered_map<int, LinkedList>& hashTable, const std::string& filename) {
    std::ofstream file(filename);
    file << "===============================================================\n";
    std::string queryFilename = "lsh_query_points.txt";
    auto queryPoints = readPointsFromFile(queryFilename);
    int i = queryPoints.size();
    for (auto& pair : hashTable) {
        file << "Result[" << i << "]: " << pair.second << "\n";
        i--;
    }
}

int main() {
    std::string normalizedPointsFilename = "lsh_normalized_points.txt";
    std::string queryFilename = "lsh_query_points.txt";
    double radius = 0.6;

    auto normalizedPoints = readPointsFromFile(normalizedPointsFilename);
    auto queryPoints = readPointsFromFile(queryFilename);

    std::vector<int> queryIndices;
    for (size_t i = normalizedPoints.size(); i < normalizedPoints.size() + queryPoints.size(); ++i) {
        queryIndices.push_back(i);
    }
    normalizedPoints.insert(normalizedPoints.end(), queryPoints.begin(), queryPoints.end());

    auto reference = chooseReferencePoint(normalizedPoints);
    
    clock_t start = clock();
    auto hashTable = radiusQuery(normalizedPoints, radius, reference, queryIndices);
    clock_t end = clock();

    std::string resultFilename = "result.txt";
    writeResultToFile(hashTable, resultFilename);

    double elapsed_time = static_cast<double>(end - start) / CLOCKS_PER_SEC;
    std::cout << "Result is available in \"" << resultFilename << "\" file.\n";
    std::cout << "========================================================\n";
    std::cout << "Time taken: " << elapsed_time << " seconds.\n";

    return 0;
}