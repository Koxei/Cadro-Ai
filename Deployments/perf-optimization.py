import time
import functools
import tracemalloc

class PerformanceOptimization:
    def __init__(self):
        """
        Initializes the Performance Optimization module.
        """
        self.execution_times = []
        self.memory_usage = []
    
    def time_execution(self, func):
        """
        Decorator to measure execution time of a function.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            exec_time = end_time - start_time
            self.execution_times.append(exec_time)
            print(f"Execution Time ({func.__name__}): {exec_time:.6f} seconds")
            return result
        return wrapper
    
    def measure_memory(self, func):
        """
        Decorator to measure memory usage of a function.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            result = func(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            self.memory_usage.append(peak)
            print(f"Memory Usage ({func.__name__}): {peak / 1024:.2f} KB")
            return result
        return wrapper
    
    def get_performance_report(self):
        """
        Returns a summary of execution times and memory usage.
        """
        avg_time = sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0
        avg_memory = sum(self.memory_usage) / len(self.memory_usage) if self.memory_usage else 0
        return {
            "average_execution_time": avg_time,
            "average_memory_usage_kb": avg_memory / 1024
        }

# Example Usage
if __name__ == "__main__":
    optimizer = PerformanceOptimization()
    
    @optimizer.time_execution
    @optimizer.measure_memory
    def sample_function(n):
        return sum(i ** 2 for i in range(n))
    
    sample_function(100000)
    sample_function(200000)
    
    print(optimizer.get_performance_report())
