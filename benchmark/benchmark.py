import time
import tracemalloc
import statistics
import psutil
import os
import matplotlib.pyplot as plt

from classes import Graph

class Benchmark:

    def __init__(self, graph: Graph, rounds=5):
        self.graph: Graph = graph
        self.rounds = rounds
        self.process = psutil.Process()

        self.algorithms = {
            "BFS": self.graph.bfs,
            "DFS": self.graph.dfs,
            "Dijkstra": self.graph.dijkstra,
            "A*": self.graph.a_star
        }

        self._create_dirs()

    def _create_dirs(self):
        base = "results"
        self.general_path = os.path.join(base, "general")
        self.a_star_path = os.path.join(base, "a_star")

        os.makedirs(self.general_path, exist_ok=True)
        os.makedirs(self.a_star_path, exist_ok=True)

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
            "path_length": len(result["path"]) if result["path"] else 0
        }

    def _aggregate(self, rounds_data):
        return {
            "time_avg": round(statistics.mean([r["time"] for r in rounds_data]), 6),
            "memory_kb_avg": round(statistics.mean([r["memory_kb"] for r in rounds_data]), 2),
            "rss_kb_avg": round(statistics.mean([r["rss_diff_kb"] for r in rounds_data]), 2),
            "iterations_avg": round(statistics.mean([r["iterations"] for r in rounds_data]), 2),
            "expanded_avg": round(statistics.mean([r["expanded_nodes"] for r in rounds_data]), 2),
            "path_len_avg": round(statistics.mean([r["path_length"] for r in rounds_data]), 2),
        }

    def _plot_metric(self, results, metric_key, title, path):
        names = list(results.keys())
        values = [results[n][metric_key] for n in names]

        plt.figure()
        plt.bar(names, values)
        plt.title(title)
        plt.xlabel("Algoritmo")
        plt.ylabel(metric_key)
        plt.xticks(rotation=30)

        filename = os.path.join(path, f"{metric_key}.png")
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

    def _generate_general_plots(self, results):
        metrics = [
            "time_avg",
            "memory_kb_avg",
            "rss_kb_avg",
            "iterations_avg",
            "expanded_avg",
            "path_len_avg"
        ]

        for metric in metrics:
            self._plot_metric(
                results,
                metric,
                f"Comparação Geral - {metric}",
                self.general_path
            )

    def _generate_a_star_plots(self, results):
        metrics = [
            "time_avg",
            "memory_kb_avg",
            "rss_kb_avg",
            "iterations_avg",
            "expanded_avg",
            "path_len_avg"
        ]

        for metric in metrics:
            self._plot_metric(
                results,
                metric,
                f"A* - {metric}",
                self.a_star_path
            )

    def run(self, start_node, target_nodes: list):
        results = {}

        for name, func in self.algorithms.items():
            rounds_data = []

            for _ in range(self.rounds):
                collected = []

                for target in target_nodes:
                    data = self._run_once(func, start_node, target)
                    collected.append(data)

                rounds_data.append({
                    "time": statistics.mean([c["time"] for c in collected]),
                    "memory_kb": statistics.mean([c["memory_kb"] for c in collected]),
                    "rss_diff_kb": statistics.mean([c["rss_diff_kb"] for c in collected]),
                    "iterations": statistics.mean([c["iterations"] for c in collected]),
                    "expanded_nodes": statistics.mean([c["expanded_nodes"] for c in collected]),
                    "path_length": statistics.mean([c["path_length"] for c in collected]),
                })

            results[name] = self._aggregate(rounds_data)

        self._generate_general_plots(results)
        return results

    def run_a_star_test(self, start_node, target_nodes: list):
        results = {}

        heuristics = {
            "A*_Zero": self.graph.heuristic_zero,
            "A*_Degree": self.graph.heuristic_degree,
            "A*_Geo": self.graph.heuristic_geo
        }

        for h_name, heuristic in heuristics.items():
            rounds_data = []

            for _ in range(self.rounds):
                collected = []

                for target in target_nodes:
                    func = lambda s, t: self.graph.a_star(s, t, heuristic)
                    data = self._run_once(func, start_node, target)
                    collected.append(data)

                rounds_data.append({
                    "time": statistics.mean([c["time"] for c in collected]),
                    "memory_kb": statistics.mean([c["memory_kb"] for c in collected]),
                    "rss_diff_kb": statistics.mean([c["rss_diff_kb"] for c in collected]),
                    "iterations": statistics.mean([c["iterations"] for c in collected]),
                    "expanded_nodes": statistics.mean([c["expanded_nodes"] for c in collected]),
                    "path_length": statistics.mean([c["path_length"] for c in collected]),
                })

            results[h_name] = self._aggregate(rounds_data)

        self._generate_a_star_plots(results)
        return results

    def display_table(self, results):
        print("\n===== BENCHMARK RESULTS =====\n")

        header = (
            f"{'Algoritmo':<12} | {'Tempo(s)':<10} | {'Mem(KB)':<10} | "
            f"{'RSS(KB)':<10} | {'Iterações':<10} | {'Expansão':<10} | "
            f"{'Comprimento':<10}"
        )
        print(header)
        print("-" * len(header))

        for name, data in results.items():
            print(
                f"{name:<12} | "
                f"{data['time_avg']:<10} | "
                f"{data['memory_kb_avg']:<10} | "
                f"{data['rss_kb_avg']:<10} | "
                f"{data['iterations_avg']:<10} | "
                f"{data['expanded_avg']:<10} | "
                f"{data['path_len_avg']:<10}"
            )