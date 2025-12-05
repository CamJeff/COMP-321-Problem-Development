import heapq

def solve():
    # Required point value to get a full score, Number of total problems, Number of topics you are good at
    M, N = map(int, input().split()) 
    preferred_topics_list = list(input().split()) # Topics you are good at
    
    # Higher rank value = Better topic.
    # If input is "A B C", A is best.
    # We assign A=3, B=2, C=1.
    topic_map = {}
    rank_counter = len(preferred_topics_list)
    for t in preferred_topics_list:
        topic_map[t] = rank_counter
        rank_counter -= 1
    
    problems = []
    for _ in range(N):
        parts = list(input().split())
        
        p_id = int(parts[0]) # Problem id number
        points = int(parts[1]) # Problem point value
        difficulty = int(parts[2]) # Problem difficulty
        topic = parts[3] # Problem type
        length = int(parts[4]) # Problem text length

        # Get rank (0 if not in preferred list)
        rank = topic_map.get(topic, 0)
        problems.append((p_id, points, difficulty, length, rank))

    # Sort by difficulty, then length
    problems.sort(key=lambda x: x[0])

    # Priority Queue (Min-Heap): relies on tuple comparison. When Python compares two tuples, 
    # it does so element-by-element (lexicographically). It compares the first item. If they're 
    # different, the tuple with the smaller item is "smaller." If the first items are equal, it moves to the second item, etc
    # Index 0: Total Difficulty (Minimize)
    # Index 1: Count of problems (Minimize)
    # Index 2: Negative Total Topic Score (Minimize negative -> Maximize score)
    # Index 3: Total Length (Minimize)

    # The following items in the tuple do not affect the decision of which problem to choose (unless everything else is somehow equal)
    # Index 4: Current Points (how many points we have so far)
    # Index 5: Current Index in problem list (where we are in the list (to add the next problem))
    # Index 6: Path (which problems we actually picked (to print the answer))
    
    # Initial state: 0 diff, 0 count, 0 rank, 0 len, 0 pts, index -1, empty path
    pq = [(0, 0, 0, 0, 0, -1, ())] # Start the search with a "blank slate"
    
    # Implement memoization to prevent waisting time and memory on wrong paths
    # visited_states prevents the heap from exploring millions of identical "decoy" combinations.
    # Key: (diff, count, neg_rank, len) -> Value: max_points_found
    visited_states = {}

    # Best-First Search: explores the "cheapest" possible combinations of problems first, which guarantees
    #  that the moment it finds a valid solution, it is the best one
    while pq:
        # heappop pops the item with the lowest priority value from the heap. The heap always gives the combination 
        # that currently has the lowest total difficulty (or fewest problems if difficulties are equal, etc)
        total_diff, total_count, total_neg_rank, total_len, total_pts, idx, path = heapq.heappop(pq)
        # Check if we met the point requirement
        if total_pts >= M:
            # Since this is a Best-First Search (Dijkstra) on our specific costs,
            # the first valid node we expand is guaranteed to be the optimal one.
            print(*(sorted(path))) # The * prints the list content separated by spaces
            return

        # This loop tries to create new combinations by adding one more problem to the current set
        for i in range(idx + 1, N):
            p_pid, p_pts, p_diff, p_len, p_rank = problems[i]
            # Computing the potential new totals if we add problem idx+1
            new_pts = total_pts + p_pts
            new_diff = total_diff + p_diff
            new_count = total_count + 1
            new_neg_rank = total_neg_rank - p_rank  # Subtracting positive rank makes it more negative
            new_len = total_len + p_len

            # Have we reached this exact cost state before?
            state_key = (new_diff, new_count, new_neg_rank, new_len)
            if state_key in visited_states:
                # If the previous way to get here had MORE or EQUAL points, 
                # this current path is redundant
                if visited_states[state_key] >= new_pts:
                    continue
            
            # Record this new best state
            visited_states[state_key] = new_pts
            
            new_path = path + (p_pid,)
            
            # We add this new, slightly larger combination back into the pile
            # The heap sorts it. If this new combination is very difficult, it sinks to the bottom. If it's easy,
            # it floats to the top, ready to be popped in the next iteration.
            heapq.heappush(pq, (new_diff, new_count, new_neg_rank, new_len, new_pts, i, new_path))

if __name__ == "__main__":
    solve()
