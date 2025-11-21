"""
Time Limit Exceeded Solution - DP
This solution tries to solve the problem using a knapsack-style dp approach.
However, the magnitude of the points (integers of size 10^15), the dp table
will grow exponentially because almost every combination of problems produces a unique 
point total. Iterating through this massive table for every single problem becomes too slow.
"""
import time
def solve():
    # Required point value to get a full score, Number of total problems
    M, N = map(int, input().split())
    preferred_topics_list = list(input().split()) # Topics you are good at
    
    topic_map = {}
    rank_counter = len(preferred_topics_list)
    for t in preferred_topics_list:
        topic_map[t] = rank_counter
        rank_counter -= 1

    # Parse Problems
    problems = []
    for _ in range(N):
        parts = list(input().split())
        
        p_id = int(parts[0]) # Problem id number
        points = int(parts[1]) # Problem point value
        difficulty = int(parts[2]) # Problem difficulty
        topic = parts[3] # Problem type
        length = int(parts[4]) # Problem text length
        rank = topic_map.get(topic, 0)
        
        # Tuple: (Difficulty, Count, -TopicRank, Length, ProblemID)
        # Note: We include ProblemID to reconstruct the path later if needed,
        # though standard knapsack usually just stores the value. 
        # For this demo, we store the cost tuple.
        cost = (difficulty, 1, -rank, length)
        problems.append((p_id, points, cost))
    
    # MAP-BASED KNAPSACK (Iterative DP)
    
    # dp[points] = best_cost_tuple
    # We want to minimize cost for a specific point total.
    # Initial state: 0 points costs nothing.
    # We also store the path in the dictionary value: (cost_tuple, [list_of_ids])
    
    # Initial: {0 points: ((0 diff, 0 count, 0 rank, 0 len), [])}
    dp = {0: ((0, 0, 0, 0), [])}

    # Iterate through every problem (Standard Knapsack Outer Loop)
    for pid, p_pts, p_cost in problems:
        
        # Create a copy of items to iterate because we can't modify the dictionary while iterating over it.
        # This copying step becomes incredibly expensive as dp grows
        current_states = list(dp.items())
        
        for curr_pts, (curr_cost, curr_path) in current_states:
            new_pts = curr_pts + p_pts
            
            # Calculate new cost
            # (diff + p_diff, count + 1, rank + p_rank, len + p_len)
            new_cost = (
                curr_cost[0] + p_cost[0], # Diff
                curr_cost[1] + p_cost[1], # Count
                curr_cost[2] + p_cost[2], # Rank (already negative)
                curr_cost[3] + p_cost[3]  # Length
            )
            
            # If we haven't reached this point total before, OR
            # if this new way of reaching it is cheaper (lower cost tuple), update dp.
            if new_pts not in dp or new_cost < dp[new_pts][0]:
                dp[new_pts] = (new_cost, curr_path + [pid])

    # After checking all problems, find the best result among all states 
    # that meet the minimum point requirement.
    
    best_final_cost = None
    best_final_path = []

    for pts, (cost, path) in dp.items():
        if pts >= M:
            if best_final_cost is None or cost < best_final_cost:
                best_final_cost = cost
                best_final_path = path

    # Output
    if best_final_path:
        print(*(sorted(best_final_path)))

if __name__ == "__main__":
    solve()
