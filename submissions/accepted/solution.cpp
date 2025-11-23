#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <map>
#include <queue>
#include <algorithm>
#include <tuple>

using namespace std;

// Use __int128 for point values as M > 10^20
// This is supported by GCC/Clang (standard in CP environments)
typedef __int128_t big_int;

// Helper to read big_int
big_int read_big_int() {
    string s;
    cin >> s;
    big_int res = 0;
    for (char c : s) res = res * 10 + (c - '0');
    return res;
}

struct Problem {
    int id;
    big_int points;
    int difficulty;
    string topic;
    int length;
    int rank_score; // Higher is better
};

// The State represents a node in our search tree
struct State {
    long long total_diff;
    int count;
    long long neg_rank_sum; // Minimize negative rank
    long long total_len;
    big_int current_pts;
    int last_index; // To prevent permutations, only look forward
    vector<int> path;

    // Priority Queue in C++ is a Max-Heap by default.
    // To make it a Min-Heap (smallest diff first), we must return TRUE
    // if "this" is GREATER than "other".
    bool operator>(const State& other) const {
        if (total_diff != other.total_diff) return total_diff > other.total_diff;
        if (count != other.count) return count > other.count;
        if (neg_rank_sum != other.neg_rank_sum) return neg_rank_sum > other.neg_rank_sum;
        return total_len > other.total_len;
    }
};

int main() {
    // Parse M and N
    big_int M = read_big_int();
    int N;
    cin >> N;

    // Parse Topics
    // We need to consume the rest of the line after N before reading topics
    string line; 
    getline(cin >> ws, line); 
    stringstream ss(line);
    string temp_topic;
    vector<string> preferred_topics;
    while (ss >> temp_topic) {
        preferred_topics.push_back(temp_topic);
    }

    // Map topics to rank score (Higher score = better preference)
    // First topic in list = Highest Score
    map<string, int> topic_map;
    int rank_counter = preferred_topics.size();
    for (const string& t : preferred_topics) {
        topic_map[t] = rank_counter;
        rank_counter--;
    }

    // Parse Problems
    vector<Problem> problems;
    for (int i = 0; i < N; ++i) {
        int p_id;
        int difficulty, length;
        string p_topic;
        // We read points as string first to convert to big_int
        string pts_str;
        
        cin >> p_id >> pts_str >> difficulty >> p_topic >> length;
        
        big_int pts = 0;
        for (char c : pts_str) pts = pts * 10 + (c - '0');

        int r = 0;
        if (topic_map.find(p_topic) != topic_map.end()) {
            r = topic_map[p_topic];
        }

        problems.push_back({p_id, pts, difficulty, p_topic, length, r});
    }

    // Sort by ID (consistency in path)
    sort(problems.begin(), problems.end(), [](const Problem& a, const Problem& b) {
        return a.id < b.id;
    });

    // Priority Queue Search
    // stores State, container is vector<State>, comparator is greater<State> (Min Heap)
    priority_queue<State, vector<State>, greater<State>> pq;

    // Initial state: 0 costs, index -1, empty path
    pq.push({0, 0, 0, 0, 0, -1, {}});

    while (!pq.empty()) {
        State current = pq.top();
        pq.pop();

        // Check solution
        if (current.current_pts >= M) {
            // Print path
            for (size_t i = 0; i < current.path.size(); ++i) {
                cout << current.path[i] << (i == current.path.size() - 1 ? "" : " ");
            }
            cout << endl;
            return 0;
        }

        // Branch out
        // Iterate through all problems AFTER the last one we added
        for (int i = current.last_index + 1; i < N; ++i) {
            const Problem& p = problems[i];

            State next_state;
            next_state.total_diff = current.total_diff + p.difficulty;
            next_state.count = current.count + 1;
            next_state.neg_rank_sum = current.neg_rank_sum - p.rank_score;
            next_state.total_len = current.total_len + p.length;
            next_state.current_pts = current.current_pts + p.points;
            next_state.last_index = i;
            
            // Copy path and add new ID
            next_state.path = current.path;
            next_state.path.push_back(p.id);

            pq.push(next_state);
        }
    }

    // If no solution found (though typically -1 output is handled here)
    cout << -1 << endl;

    return 0;
}
