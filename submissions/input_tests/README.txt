To observe the running time difference between the two solutions, you need to add certain components to the code.
In the solution.py file, add the following:
  start_time = time.time() # Add this on line 7, between "M, N = map(int, input().split())" and "preferred_topics_list = list(input().split()) # Topics you are good at"
  return start_time # Update line 64, add start_time right after the return statement
  start_time = solve() # Update line 85, add start_time =, right after the solve() function call
  print("Process finished --- %s seconds ---" % (time.time() - start_time)) # Add this on the last line of the code

In the time_limit_exceeded.py file, add the following:
  start_time = time.time() # Add this on line 12, between "M, N = map(int, input().split())" and "preferred_topics_list = list(input().split()) # Topics you are good at"
  return start_time # Add this on line 89, right after "print(*(sorted(best_final_path)))"
  start_time = solve() # Update line 92, add start_time =, right after the solve() function call
  print("Process finished --- %s seconds ---" % (time.time() - start_time)) # Add this on the last line of the code

This should measure and print the time that the program takes to run.
