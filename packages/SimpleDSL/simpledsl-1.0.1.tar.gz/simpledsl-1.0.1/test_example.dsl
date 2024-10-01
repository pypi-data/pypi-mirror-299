// test_example.dsl

// Define a simple configuration
config {
    name = "Test Configuration"
    version = "1.0"
}

// Define a task
task exampleTask {
    description = "This is an example task"
    execute {
        print("Executing example task...")
    }
}

// Define another task with parameters
task parameterizedTask {
    description = "This task takes parameters"
    parameters {
        param1 = "value1"
        param2 = "value2"
    }
    execute {
        print("Executing parameterized task with param1: ${param1} and param2: ${param2}")
    }
}

// Define a sequence of tasks
sequence {
    exampleTask
    parameterizedTask
}
