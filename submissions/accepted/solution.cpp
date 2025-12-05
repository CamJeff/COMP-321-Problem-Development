#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <unordered_map> // Changed to unordered_map for O(1) speed
#include <algorithm>
#include <queue>
#include <tuple>

using namespace std;

// Use long long for Points and M (up to 10^15)
typedef long long ll;

struct Problem {
    int id;
    ll points;
    int difficulty;
    int length;
    int topic_rank;
};

// Represents a state in our Search
struct State {
    int total_diff;
    int total_count;
    int total_neg_rank; 
    int total_len;
    ll current_points;
    int current_index; 
    vector<int> path; 

    // Optimized Constructor: Uses std::move to avoid deep copying the vector
    State(int d, int c, int r, int l, ll p, int idx, vector<int> pa)
        : total_diff(d), total_count(c), total_neg_rank(r), total_len(l),
          current_points(p), current_index(idx), path(std::move(pa)) {}

    // Priority Queue Operator (Min-Heap logic)
    bool operator>(const State& other) const {
        if (total_diff != other.total_diff) return total_diff > other.total_diff;
        if (total_count != other.total_count) return total_count > other.total_count;
        if (total_neg_rank != other.total_neg_rank) return total_neg_rank > other.total_neg_rank;
        return total_len > other.total_len;
    }
};

// Hash Key for visited_states
struct StateKey {
    int diff, count, neg_rank, len;

    bool operator==(const StateKey& other) const {
        return diff == other.diff && count == other.count && 
               neg_rank == other.neg_rank && len == other.len;
    }
};

// Custom Hash Function for StateKey
struct StateKeyHash {
    size_t operator()(const StateKey& k) const {
        // Simple hash combination
        size_t h1 = hash<int>{}(k.diff);
        size_t h2 = hash<int>{}(k.count);
        size_t h3 = hash<int>{}(k.neg_rank);
        size_t h4 = hash<int>{}(k.len);
        return h1 ^ (h2 << 1) ^ (h3 << 2) ^ (h4 << 3);
    }
};

void solve() {
    // Optimization for faster I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    ll M;
    int N;
    if (!(cin >> M >> N)) return;

    unordered_map<string, int> topic_map;
    
    // Consume newline after N
    string line;
    getline(cin >> ws, line); 
    stringstream ss(line);
    string temp_topic;
    vector<string> preferred_topics;
    while (ss >> temp_topic) {
        preferred_topics.push_back(temp_topic);
    }

    int rank_counter = preferred_topics.size();
    for (const string& t : preferred_topics) {
        topic_map[t] = rank_counter;
        rank_counter--;
    }

    vector<Problem> problems;
    problems.reserve(N); // Reserve memory
    for (int i = 0; i < N; ++i) {
        int id;
        ll pts;
        int diff, len;
        string top;
        cin >> id >> pts >> diff >> top >> len;

        int rank = 0;
        if (topic_map.find(top) != topic_map.end()) {
            rank = topic_map[top];
        }
        problems.push_back({id, pts, diff, len, rank});
    }

    // 1. Sort by Difficulty -> Length -> ID
    sort(problems.begin(), problems.end(), [](const Problem& a, const Problem& b) {
        if (a.difficulty != b.difficulty) return a.difficulty < b.difficulty;
        if (a.length != b.length) return a.length < b.length;
        return a.id < b.id;
    });

    priority_queue<State, vector<State>, greater<State>> pq;
    pq.push(State(0, 0, 0, 0, 0, -1, {}));

    // Visited States Pruning: Using unordered_map (Hash Map) instead of std::map (Tree)
    // This changes lookup from O(log N) to O(1)
    unordered_map<StateKey, ll, StateKeyHash> visited_states;

    while (!pq.empty()) {
        // Construct 'current' locally. Since pq.top() returns const ref, we must copy or 
        // rely on the fact we are popping immediately.
        // To avoid copy, we can use const_cast or just standard copy (cheap enough for members, expensive for vector).
        // Standard pattern:
        State current = pq.top(); 
        pq.pop();

        if (current.current_points >= M) {
            sort(current.path.begin(), current.path.end());
            for (size_t k = 0; k < current.path.size(); ++k) {
                cout << current.path[k] << (k == current.path.size() - 1 ? "" : " ");
            }
            cout << endl;
            return;
        }

        for (int i = current.current_index + 1; i < N; ++i) {
            const Problem& p = problems[i];

            if (current.total_count + 1 > 12) continue;

            int new_diff = current.total_diff + p.difficulty;
            int new_count = current.total_count + 1;
            int new_neg_rank = current.total_neg_rank - p.topic_rank;
            int new_len = current.total_len + p.length;
            ll new_pts = current.current_points + p.points;

            // State Pruning Check with Hash Map
            StateKey state_key = {new_diff, new_count, new_neg_rank, new_len};
            auto it = visited_states.find(state_key);
            
            if (it != visited_states.end()) {
                if (it->second >= new_pts) {
                    continue;
                }
            }
            visited_states[state_key] = new_pts;

            // Create new path vector
            vector<int> new_path = current.path; // Copy 
            new_path.reserve(12); // Optimization: Prevent multiple reallocations
            new_path.push_back(p.id);

            // Use std::move to transfer ownership of the vector to the State struct
            pq.push(State(new_diff, new_count, new_neg_rank, new_len, new_pts, i, std::move(new_path)));
        }
    }
}

int main() {
    solve();
    return 0;
}