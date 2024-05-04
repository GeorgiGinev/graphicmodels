// Import the Gaussian distribution function
function gaussianRandom(min, max) {
    // Generate a random number using the Box-Muller transform
    const u = 1 - Math.random();
    const v = 1 - Math.random();
    const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    return min + z * (max - min);
}

// Define the hypercube topology as an adjacency list
function createHypercubeTopology(dimension) {
    const size = Math.pow(2, dimension);
    const adjacencyList = new Map();

    // Initialize servers
    for (let i = 0; i < size; i++) {
        adjacencyList.set(i, []);
    }

    // Connect servers in the hypercube
    for (let i = 0; i < size; i++) {
        for (let j = 0; j < dimension; j++) {
            const neighbor = i ^ (1 << j);
            adjacencyList.get(i).push(neighbor);
        }
    }

    return adjacencyList;
}

// Define a function to balance load in the hypercube cluster
function balanceLoad(clusterSize, dimension, numTasks) {
    // Create the hypercube topology
    const adjacencyList = createHypercubeTopology(dimension);

    // Initialize server queues and tasks
    const serverQueues = Array(clusterSize).fill(0);

    // Assign tasks to server 0 initially
    serverQueues[0] = numTasks;

    // Process tasks and balance the load
    for (let server = 0; server < clusterSize; server++) {
        // If the server queue is over capacity, migrate tasks
        while (serverQueues[server] > 5) {
            // Find a neighbor with lower load
            const neighbors = adjacencyList.get(server);
            for (const neighbor of neighbors) {
                if (serverQueues[neighbor] < 5) {
                    // Migrate one task to the neighbor
                    serverQueues[server]--;
                    serverQueues[neighbor]++;
                }
            }
        }
    }

    // Calculate average load
    const averageLoad = numTasks / clusterSize;

    // Calculate percentage deviation from average load
    const deviations = serverQueues.map(queue => {
        return Math.abs(queue - averageLoad) / averageLoad * 100;
    });

    // Output results
    console.log('Server queues:', serverQueues);
    console.log('Average load:', averageLoad);
    console.log('Percentage deviation of each server:', deviations);
}

// Specify the parameters
const clusterSize = Math.pow(2, 4); // 4D hypercube
const dimension = 4;
const numTasks = 100;

// Balance load in the cluster
balanceLoad(clusterSize, dimension, numTasks);
