import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.math.BigInteger;
import java.util.*;

public class Solution {

    static class Problem {
        int id;
        BigInteger points;
        int difficulty;
        String topic;
        int length;
        int rankScore;

        public Problem(int id, BigInteger points, int difficulty, String topic, int length, int rankScore) {
            this.id = id;
            this.points = points;
            this.difficulty = difficulty;
            this.topic = topic;
            this.length = length;
            this.rankScore = rankScore;
        }
    }

    // Represents a node in the search tree (Priority Queue)
    static class State implements Comparable<State> {
        long totalDiff;
        int count;
        long negRankSum; // Minimizing negative rank sum = Maximizing rank sum
        long totalLen;
        BigInteger currentPts;
        int lastIndex;
        List<Integer> path;

        public State(long totalDiff, int count, long negRankSum, long totalLen, BigInteger currentPts, int lastIndex, List<Integer> path) {
            this.totalDiff = totalDiff;
            this.count = count;
            this.negRankSum = negRankSum;
            this.totalLen = totalLen;
            this.currentPts = currentPts;
            this.lastIndex = lastIndex;
            this.path = path;
        }

        @Override
        public int compareTo(State other) {
            // 1. Minimize total difficulty
            if (this.totalDiff != other.totalDiff) {
                return Long.compare(this.totalDiff, other.totalDiff);
            }
            // 2. Minimize number of problems
            if (this.count != other.count) {
                return Integer.compare(this.count, other.count);
            }
            // 3. Minimize negative rank sum (Maximize preferences)
            if (this.negRankSum != other.negRankSum) {
                return Long.compare(this.negRankSum, other.negRankSum);
            }
            // 4. Minimize total length
            return Long.compare(this.totalLen, other.totalLen);
        }
    }

    public static void main(String[] args) throws IOException {
        // Use try-with-resources to ensure the Scanner is closed automatically
        try (Scanner sc = new Scanner(System.in)) {
            if (!sc.hasNext()) return;

            // 1. Read M (BigInteger) and N
            BigInteger M = sc.nextBigInteger();
            int N = sc.nextInt();
            
            // Consume the rest of the line to get to the topics
            sc.nextLine(); 

            // 2. Read Topics
            String topicLine = sc.nextLine();
            String[] preferredTopics = topicLine.trim().split("\\s+");
            
            Map<String, Integer> topicMap = new HashMap<>();
            int rankCounter = preferredTopics.length;
            
            // Map topics to rank score (Higher score = better preference)
            for (String t : preferredTopics) {
                topicMap.put(t, rankCounter);
                rankCounter--;
            }

            // 3. Read Problems
            List<Problem> problems = new ArrayList<>();
            for (int i = 0; i < N; i++) {
                // Read line by line or token by token
                // Format: ID Points Difficulty Topic Length
                int pId = sc.nextInt();
                BigInteger pts = sc.nextBigInteger();
                int difficulty = sc.nextInt();
                String topic = sc.next();
                int length = sc.nextInt();

                int rank = topicMap.getOrDefault(topic, 0);
                problems.add(new Problem(pId, pts, difficulty, topic, length, rank));
            }

            // Sort by ID 
            problems.sort(Comparator.comparingInt(p -> p.id));

            // 4. Priority Queue (Min-Heap)
            PriorityQueue<State> pq = new PriorityQueue<>();

            // Initial State: 0 costs, index -1 (to start before 0), empty path
            pq.add(new State(0, 0, 0, 0, BigInteger.ZERO, -1, new ArrayList<>()));

            while (!pq.isEmpty()) {
                State current = pq.poll();

                // Check if requirement met
                if (current.currentPts.compareTo(M) >= 0) {
                    // Sort path for output as per sample
                    Collections.sort(current.path);
                    
                    StringBuilder sb = new StringBuilder();
                    for (int i = 0; i < current.path.size(); i++) {
                        sb.append(current.path.get(i));
                        if (i < current.path.size() - 1) sb.append(" ");
                    }
                    System.out.println(sb.toString());
                    return;
                }

                // Branch out: Iterate through problems AFTER the last one used
                // This ensures we check combinations, not permutations
                for (int i = current.lastIndex + 1; i < N; i++) {
                    Problem p = problems.get(i);

                    long newDiff = current.totalDiff + p.difficulty;
                    int newCount = current.count + 1;
                    long newNegRank = current.negRankSum - p.rankScore;
                    long newLen = current.totalLen + p.length;
                    BigInteger newPts = current.currentPts.add(p.points);
                    
                    // Copy path
                    List<Integer> newPath = new ArrayList<>(current.path);
                    newPath.add(p.id);

                    pq.add(new State(newDiff, newCount, newNegRank, newLen, newPts, i, newPath));
                }
            }

            // If no solution found
            System.out.println("-1");
        }
    }
}
