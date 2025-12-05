import java.io.*;
import java.util.*;

public class solution {

    static class Problem {
        int id;
        long points;
        int difficulty;
        int length;
        int topicRank;

        public Problem(int id, long points, int difficulty, int length, int topicRank) {
            this.id = id;
            this.points = points;
            this.difficulty = difficulty;
            this.length = length;
            this.topicRank = topicRank;
        }
    }

    // Class to use as a Key for the visitedStates HashMap
    static class StateKey {
        int diff;
        int count;
        int negRank;
        int len;

        public StateKey(int diff, int count, int negRank, int len) {
            this.diff = diff;
            this.count = count;
            this.negRank = negRank;
            this.len = len;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            StateKey stateKey = (StateKey) o;
            return diff == stateKey.diff &&
                   count == stateKey.count &&
                   negRank == stateKey.negRank &&
                   len == stateKey.len;
        }

        @Override
        public int hashCode() {
            return Objects.hash(diff, count, negRank, len);
        }
    }

    // Represents a node in the Heap
    static class State implements Comparable<State> {
        int totalDiff;
        int totalCount;
        int totalNegRank;
        int totalLen;
        long currentPoints;
        int currentIndex;
        List<Integer> path;

        public State(int d, int c, int r, int l, long p, int idx, List<Integer> path) {
            this.totalDiff = d;
            this.totalCount = c;
            this.totalNegRank = r;
            this.totalLen = l;
            this.currentPoints = p;
            this.currentIndex = idx;
            this.path = path;
        }

        @Override
        public int compareTo(State other) {
            if (this.totalDiff != other.totalDiff)
                return Integer.compare(this.totalDiff, other.totalDiff);
            if (this.totalCount != other.totalCount)
                return Integer.compare(this.totalCount, other.totalCount);
            if (this.totalNegRank != other.totalNegRank)
                return Integer.compare(this.totalNegRank, other.totalNegRank);
            return Integer.compare(this.totalLen, other.totalLen);
        }
    }

    public static void solve() throws IOException {
        // Fast I/O
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        
        String[] parts = line.trim().split("\\s+");
        long M = Long.parseLong(parts[0]);
        int N = Integer.parseInt(parts[1]);

        // Topics Line
        String[] topicParts = br.readLine().trim().split("\\s+");
        Map<String, Integer> topicMap = new HashMap<>();
        int rankCounter = topicParts.length;
        for (String t : topicParts) {
            topicMap.put(t, rankCounter);
            rankCounter--;
        }

        List<Problem> problems = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            String[] pParts = br.readLine().trim().split("\\s+");
            int id = Integer.parseInt(pParts[0]);
            long pts = Long.parseLong(pParts[1]);
            int diff = Integer.parseInt(pParts[2]);
            String topic = pParts[3];
            int len = Integer.parseInt(pParts[4]);

            int rank = topicMap.getOrDefault(topic, 0);
            problems.add(new Problem(id, pts, diff, len, rank));
        }

        // 1. Sort by Difficulty -> Length -> ID
        problems.sort((a, b) -> {
            if (a.difficulty != b.difficulty) return Integer.compare(a.difficulty, b.difficulty);
            if (a.length != b.length) return Integer.compare(a.length, b.length);
            return Integer.compare(a.id, b.id);
        });

        // Min-Heap
        PriorityQueue<State> pq = new PriorityQueue<>();
        
        // Initial State
        pq.add(new State(0, 0, 0, 0, 0, -1, new ArrayList<>()));

        // 2. Visited States Map (StateKey -> MaxPoints)
        Map<StateKey, Long> visitedStates = new HashMap<>();

        while (!pq.isEmpty()) {
            State current = pq.poll();

            // Check Goal
            if (current.currentPoints >= M) {
                Collections.sort(current.path);
                StringBuilder sb = new StringBuilder();
                for (int i = 0; i < current.path.size(); i++) {
                    sb.append(current.path.get(i));
                    if (i < current.path.size() - 1) sb.append(" ");
                }
                System.out.println(sb.toString());
                return;
            }

            // Branching
            for (int i = current.currentIndex + 1; i < N; i++) {
                Problem p = problems.get(i);

                // 10% Rule Pruning
                if (current.totalCount + 1 > 12) continue;

                int newDiff = current.totalDiff + p.difficulty;
                int newCount = current.totalCount + 1;
                int newNegRank = current.totalNegRank - p.topicRank;
                int newLen = current.totalLen + p.length;
                long newPts = current.currentPoints + p.points;

                // State Pruning Logic
                StateKey key = new StateKey(newDiff, newCount, newNegRank, newLen);
                if (visitedStates.containsKey(key)) {
                    if (visitedStates.get(key) >= newPts) {
                        continue;
                    }
                }
                visitedStates.put(key, newPts);

                // Create new path
                List<Integer> newPath = new ArrayList<>(current.path);
                newPath.add(p.id);

                pq.add(new State(newDiff, newCount, newNegRank, newLen, newPts, i, newPath));
            }
        }
    }

    public static void main(String[] args) {
        try {
            solve();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}