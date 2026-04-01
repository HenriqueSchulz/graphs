import time
import tracemalloc
import statistics
import psutil


class Benchmark:

    def __init__(self, graph, rounds=5):
        self.graph = graph
        self.rounds = rounds
        self.process = psutil.Process()

        self.algorithms = {
            "BFS": graph.bfs,
            "DFS": graph.dfs,
            "Dijkstra": graph.dijkstra,
            "A*": graph.a_star
        }

    def _run_once(self, func, start, end):
        tracemalloc.start()

        mem_before = self.process.memory_info().rss
        start_time = time.perf_counter()

        result = func(start, end)

        end_time = time.perf_counter()
        mem_after = self.process.memory_info().rss

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "time": end_time - start_time,
            "memory_kb": peak / 1024,
            "rss_diff_kb": (mem_after - mem_before) / 1024,
            "iterations": result["iterations"],
            "expanded_nodes": result["expanded_nodes"],
            "path_cost": result["cost"] if result["cost"] is not None else 0,
            "path_length": len(result["path"]) if result["path"] else 0
        }

    def run(self, start_node, target_nodes: list):
        results = {}

        for name, func in self.algorithms.items():

            times = []
            mems = []
            rss = []
            iterations = []
            expanded = []
            costs = []
            lengths = []

            for _ in range(self.rounds):

                round_times = []
                round_mems = []
                round_rss = []
                round_iterations = []
                round_expanded = []
                round_costs = []
                round_lengths = []

                # Execute each target node and collect metrics
                for target in target_nodes:
                    data = self._run_once(func, start_node, target)

                    round_times.append(data["time"])
                    round_mems.append(data["memory_kb"])
                    round_rss.append(data["rss_diff_kb"])
                    round_iterations.append(data["iterations"])
                    round_expanded.append(data["expanded_nodes"])
                    round_costs.append(data["path_cost"])
                    round_lengths.append(data["path_length"])

                # Mean of rounds
                times.append(statistics.mean(round_times))
                mems.append(statistics.mean(round_mems))
                rss.append(statistics.mean(round_rss))
                iterations.append(statistics.mean(round_iterations))
                expanded.append(statistics.mean(round_expanded))
                costs.append(statistics.mean(round_costs))
                lengths.append(statistics.mean(round_lengths))

            # Final mean of all rounds
            results[name] = {
                "time_avg": round(statistics.mean(times), 6),
                "memory_kb_avg": round(statistics.mean(mems), 2),
                "rss_kb_avg": round(statistics.mean(rss), 2),
                "iterations_avg": round(statistics.mean(iterations), 2),
                "expanded_avg": round(statistics.mean(expanded), 2),
                "cost_avg": round(statistics.mean(costs), 2),
                "path_len_avg": round(statistics.mean(lengths), 2)
            }

        return results

    def display_table(self, results):
        print("\n===== BENCHMARK RESULTS =====\n")

        header = (
            f"{'Algoritmo':<10} | {'Tempo(s)':<10} | {'Mem(KB)':<10} | "
            f"{'RSS(KB)':<10} | {'Iterações':<10} | {'Expansão':<10} | "
            f"{'Custo':<10} | {'Comprimento do Caminho':<10}"
        )
        print(header)
        print("-" * len(header))

        for name, data in results.items():
            print(
                f"{name:<10} | "
                f"{data['time_avg']:<10} | "
                f"{data['memory_kb_avg']:<10} | "
                f"{data['rss_kb_avg']:<10} | "
                f"{data['iterations_avg']:<10} | "
                f"{data['expanded_avg']:<10} | "
                f"{data['cost_avg']:<10} | "
                f"{data['path_len_avg']:<10}"
            )