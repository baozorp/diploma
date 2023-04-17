using CSV
using DataFrames

using YAML

data = YAML.load_file("config.yaml")
path = data["paths"]["sources"]

#Define function create symmetric matrix costs
function create_symmetric_matrix(x::Vector{T}) where T<:Number
    n = length(x)
    A = zeros(Float64, n, n)
    A[1, 2:end] .= x[2:end]
    A[2:end, 1] .= x[2:end]
    A[1:n+1:end] .= 0

    for i in 2:n
        for j in 2:n
            A[i, j] = (x[i-1] + x[j-1]) / 2
        end
    end
    
    A[1:n+1:end] .= 0
    
    return A
end

data = DataFrame(CSV.File(path * "sorted_rec.csv"))
scores = data[!, "score"]

costs = create_symmetric_matrix(scores)
objects = data[!, "ID"]

times = DataFrame(CSV.File(path * "times.csv", header = false))
waits = DataFrame(CSV.File(path * "waits.csv", header = false))
distances =  DataFrame(CSV.File(path * "distances.csv", header = false))


#Define the generate start route function
function generateRoute(exhibits, max_exhibits)
  n = length(exhibits)
  route = zeros(Int, min(n, max_exhibits))
  visited = falses(n)
  for i in 1:min(n, max_exhibits)
    unvisited = filter(x -> !visited[x], 1:n)
    index = rand(1:length(unvisited))
    route[i] = unvisited[index]
    visited[route[i]] = true
  end
  return route
end

max_time = 7200
max_iterations = 150

# Call the generate start route function
start_solution = generateRoute(objects, 20)
node_count = length(start_solution)
println(start_solution)

using Random

function ILS(distances::DataFrame, times::DataFrame, costs::Matrix{Float64}, waits::DataFrame, node_count::Int64, max_time::Int64, max_iterations::Int64, start_solution::Vector{Int64})
    # Define a local search function
    function local_search(current_solution, current_time, current_cost)
        # Generate a random neighboring solution by swapping two randomly selected nodes
        next_solution = copy(current_solution)
        idx1 = rand(2:node_count)
        idx2 = rand(2:node_count)
        while idx2 == idx1 
            idx2 = rand(2:node_count)
        end
        next_solution[idx1], next_solution[idx2] = next_solution[idx2], next_solution[idx1]

        # Compute the time and cost of the new solution
        next_time = current_time
        next_cost = current_cost
        for i in 1:(node_count-1)
            next_time += times[next_solution[i], next_solution[i+1]]
            next_time += waits[next_solution[i], next_solution[i+1]]
            next_cost += costs[next_solution[i], next_solution[i+1]]
        end

        # Keep the new solution if it is better than the current solution
        if next_time <= max_time && next_cost > current_cost
            return next_solution, next_time, next_cost
        else
            return current_solution, current_time, current_cost
        end
    end
    
    

    # Initialize the best solution with the first node visited first
    best_solution = copy(start_solution)
    best_time = 0
    best_cost = 0

    # Initialize the current solution
    current_solution = best_solution
    current_time = best_time
    current_cost = best_cost
    
    
    # Create an array to store the total cost of each iteration
    total_costs = []

    # Start the iteration
    for i in 1:max_iterations
        # Use the local search function to get the next solution
        current_solution, current_time, current_cost = local_search(current_solution, current_time, current_cost)
        # Keep the best solution
        if current_cost > best_cost
            best_solution = copy(current_solution)
            best_time = current_time
            best_cost = current_cost
        end
        # Store the best cost of each iteration
        push!(total_costs, best_cost)
    end
    

    # Return the best solution
    return best_solution, best_time, best_cost
end


# Call the solve function
solution, time, cost = ILS(distances, times, costs, waits, node_count, max_time, max_iterations, start_solution)
solution