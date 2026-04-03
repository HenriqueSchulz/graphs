import time
import tracemalloc
import statistics
import psutil
import os
import matplotlib.pyplot as plt
import numpy as np

from classes import Graph

class Benchmark:

    def __init__(self, graph: Graph, rounds=5):
        self.graph: Graph = graph
        self.rounds = rounds
        self.process = psutil.Process()

        self.algorithms = {
            "BFS": self.graph.bfs,
            "DFS": self.graph.dfs,
            "Dijkstra": self.graph.dijkstra
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
            "path_cost": result["cost"] if result["cost"] is not None else 0,
            "path_length": len(result["path"]) if result["path"] else 0
        }

    def _aggregate(self, rounds_data):
        return {
            "time_avg": round(statistics.mean([r["time"] for r in rounds_data]), 6),
            "memory_kb_avg": round(statistics.mean([r["memory_kb"] for r in rounds_data]), 2),
            "rss_kb_avg": round(statistics.mean([r["rss_diff_kb"] for r in rounds_data]), 2),
            "iterations_avg": round(statistics.mean([r["iterations"] for r in rounds_data]), 2),
            "expanded_avg": round(statistics.mean([r["expanded_nodes"] for r in rounds_data]), 2),
            "cost_avg": round(statistics.mean([r["path_cost"] for r in rounds_data]), 2),
            "path_len_avg": round(statistics.mean([r["path_length"] for r in rounds_data]), 2),
            "astar_time_avg": round(statistics.mean([r.get("astar_time", r["time"]) for r in rounds_data]), 6),
            "bfs_time_avg": round(statistics.mean([r.get("bfs_time", 0) for r in rounds_data]), 6)
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

    def _plot_a_star_time_breakdown(self, results, mode):
        names = list(results.keys())

        astar_times = [results[n]["astar_time_avg"] for n in names]
        bfs_times = [results[n]["bfs_time_avg"] for n in names]

        x = np.arange(len(names))

        plt.figure(figsize=(10, 6))

        # cores consistentes
        color_astar = "#4CAF50"   # verde (execução)
        color_bfs = "#FF9800"     # laranja (heurística)

        # barra base (A*)
        plt.bar(
            x,
            astar_times,
            label="A* execução",
            color=color_astar
        )

        # topo (BFS)
        plt.bar(
            x,
            bfs_times,
            bottom=astar_times,
            label="BFS heurística",
            color=color_bfs
        )

        # valores nas barras
        for i in range(len(x)):
            total = astar_times[i] + bfs_times[i]

            plt.text(
                x[i],
                total,
                f"{total:.4f}",
                ha="center",
                va="bottom",
                fontsize=8
            )

        plt.xticks(x, names)
        plt.ylabel("Tempo (s)")
        plt.title(f"A* Tempo de Execução + Heurística ({mode})")
        plt.legend()

        # melhora escala
        max_val = max([a + b for a, b in zip(astar_times, bfs_times)])
        plt.ylim(0, max_val * 1.2)

        plt.grid(axis="y", linestyle="--", alpha=0.4)

        filename = os.path.join(self.a_star_path, f"time_breakdown_{mode}.png")
        plt.savefig(filename, bbox_inches='tight', dpi=150)
        plt.close()

    def _generate_general_plots(self, results):
        metrics = [
            "time_avg",
            "memory_kb_avg",
            "rss_kb_avg",
            "iterations_avg",
            "expanded_avg",
            "cost_avg",
            "path_len_avg"
        ]

        for metric in metrics:
            self._plot_metric(
                results,
                metric,
                f"Comparação Geral - {metric}",
                self.general_path
            )

    def _generate_a_star_plots(self, results, mode):
        metrics = [
            "time_avg",
            "memory_kb_avg",
            "rss_kb_avg",
            "iterations_avg",
            "expanded_avg",
            "cost_avg",
            "path_len_avg"
        ]

        for metric in metrics:
            self._plot_metric(
                results,
                metric,
                f"A* ({mode}) - {metric}",
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
                    "path_cost": statistics.mean([c["path_cost"] for c in collected]),
                    "path_length": statistics.mean([c["path_length"] for c in collected]),
                })

            results[name] = self._aggregate(rounds_data)

        self._generate_general_plots(results)
        return results

    def run_a_star_test(self, start_node, target_nodes: list, mode="precomputed"):
        results = {}
        bfs_cache = {}

        heuristics_names = ["A*_Zero", "A*_Degree", "A*_BFS"]

        for h_name in heuristics_names:
            rounds_data = []

            for _ in range(self.rounds):
                collected = []

                for target in target_nodes:

                    bfs_time = 0

                    if h_name == "A*_Zero":
                        heuristic = self.graph.heuristic_zero

                    elif h_name == "A*_Degree":
                        heuristic = self.graph.heuristic_degree

                    elif h_name == "A*_BFS":

                        if mode == "precomputed":
                            if target not in bfs_cache:
                                bfs_cache[target] = self.graph.precompute_bfs_heuristic(target)
                            bfs_dist = bfs_cache[target]

                        elif mode == "on_the_fly":
                            bfs_start = time.perf_counter()
                            bfs_dist = self.graph.precompute_bfs_heuristic(target)
                            bfs_time = time.perf_counter() - bfs_start

                        heuristic = lambda n, g: self.graph.heuristic_bfs(n, g, bfs_dist)

                    func = lambda s, t: self.graph.a_star(s, t, heuristic)

                    data = self._run_once(func, start_node, target)

                    data["astar_time"] = data["time"]
                    data["bfs_time"] = bfs_time

                    collected.append(data)

                rounds_data.append({
                    "time": statistics.mean([c["time"] for c in collected]),
                    "memory_kb": statistics.mean([c["memory_kb"] for c in collected]),
                    "rss_diff_kb": statistics.mean([c["rss_diff_kb"] for c in collected]),
                    "iterations": statistics.mean([c["iterations"] for c in collected]),
                    "expanded_nodes": statistics.mean([c["expanded_nodes"] for c in collected]),
                    "path_cost": statistics.mean([c["path_cost"] for c in collected]),
                    "path_length": statistics.mean([c["path_length"] for c in collected]),
                    "astar_time": statistics.mean([c["astar_time"] for c in collected]),
                    "bfs_time": statistics.mean([c["bfs_time"] for c in collected]),
                })

            results[h_name] = self._aggregate(rounds_data)

        self._generate_a_star_plots(results, mode)
        self._plot_a_star_time_breakdown(results, mode)

        return results

    def display_table(self, results):
        print("\n===== BENCHMARK RESULTS =====\n")

        header = (
            f"{'Algoritmo':<12} | {'Tempo(s)':<10} | {'Mem(KB)':<10} | "
            f"{'RSS(KB)':<10} | {'Iterações':<10} | {'Expansão':<10} | "
            f"{'Custo':<10} | {'Comprimento':<10}"
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
                f"{data['cost_avg']:<10} | "
                f"{data['path_len_avg']:<10}"
            )