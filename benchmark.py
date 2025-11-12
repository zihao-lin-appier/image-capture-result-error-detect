#!/usr/bin/env python3
"""
Benchmark script to run all five image detection solutions 10 times each
and calculate average analysis times.

This script extracts the internal analysis time (end_time - start_time) 
measured within each solution, which represents the actual image analysis 
time, not the total program execution time.
"""

import subprocess
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Define the solutions and their commands
SOLUTIONS = {
    'govips': {
        'command': ['./govips/govips', 'data'],
        'type': 'go',
        'fallback': ['go', 'run', 'govips/main.go', 'data']
    },
    'goimage': {
        'command': ['./goimage/goimage', 'data'],
        'type': 'go',
        'fallback': ['go', 'run', 'goimage/main.go', 'data']
    },
    'pillow': {
        'command': ['python3', 'pillow/main.py', 'data'],
        'type': 'python'
    },
    'cv2': {
        'command': ['python3', 'cv2/main.py', 'data'],
        'type': 'python'
    },
    'imageio': {
        'command': ['python3', 'imageio/main.py', 'data'],
        'type': 'python'
    }
}

# Number of runs per solution
NUM_RUNS = 10

# Pattern to extract processing time from output
TIME_PATTERN = re.compile(r'Total processing time: ([\d.]+) milliseconds')


def run_solution(name, config, run_num):
    """
    Run a solution once and return the output and analysis time.
    
    This function extracts the internal analysis time (end_time - start_time)
    measured within each solution, not the total program execution time.
    
    Args:
        name: Name of the solution
        config: Configuration dict with command and type
        run_num: Current run number (1-indexed)
        
    Returns:
        tuple: (output_text, analysis_time_ms) or (None, None) if failed
    """
    command = config['command']
    
    # Check if executable exists for Go solutions
    if config['type'] == 'go' and not Path(command[0]).exists():
        if 'fallback' in config:
            command = config['fallback']
        else:
            print(f"Error: {command[0]} not found and no fallback available")
            return None, None
    
    try:
        # Run the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
            timeout=60  # 60 second timeout
        )
        
        # Get output
        output = result.stdout + result.stderr
        
        # Extract the internal analysis time from output
        # This is the time measured by end_time - start_time within each solution
        match = TIME_PATTERN.search(output)
        if match:
            analysis_time = float(match.group(1))
            return output, analysis_time
        else:
            # If we can't find the time in output, this is an error
            print(f"  Run {run_num}: Could not extract analysis time from output")
            print(f"  Output: {output[:200]}...")  # Show first 200 chars for debugging
            return None, None
            
    except subprocess.TimeoutExpired:
        print(f"  Run {run_num}: Timeout after 60 seconds")
        return None, None
    except Exception as e:
        print(f"  Run {run_num}: Error - {e}")
        return None, None


def generate_markdown_report(all_results, solution_averages):
    """
    Generate a markdown report from the benchmark results.
    
    Args:
        all_results: Dictionary containing all run results
        solution_averages: List of tuples (solution_name, avg_time, successful_runs)
        
    Returns:
        str: Markdown formatted report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    md = []
    md.append("# Image Detection Solutions Benchmark Results\n")
    md.append(f"**Generated:** {timestamp}\n")
    md.append(f"**Runs per solution:** {NUM_RUNS}\n")
    md.append("\n---\n")
    
    # Final comparison table
    md.append("## Final Results - Average Analysis Times\n")
    md.append("\n| Solution | Avg Analysis Time (ms) | Successful Runs |")
    md.append("|----------|------------------------|-----------------|")
    for solution_name, avg_time, successful_runs in solution_averages:
        md.append(f"| {solution_name} | {avg_time:.2f} | {successful_runs}/{NUM_RUNS} |")
    md.append("\n")
    
    # Detailed results for each solution
    md.append("---\n")
    md.append("## Detailed Results by Solution\n")
    
    for solution_name, config in SOLUTIONS.items():
        if solution_name not in all_results or not all_results[solution_name]:
            continue
            
        results = all_results[solution_name]
        times = [r['time'] for r in results]
        
        if not times:
            continue
            
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        md.append(f"\n### {solution_name.upper()}\n")
        md.append(f"\n**Summary:**\n")
        md.append(f"- Successful runs: {len(times)}/{NUM_RUNS}\n")
        md.append(f"- Average analysis time: {avg_time:.2f} milliseconds\n")
        md.append(f"- Min analysis time: {min_time:.2f} milliseconds\n")
        md.append(f"- Max analysis time: {max_time:.2f} milliseconds\n")
        
        md.append(f"\n**Individual Run Results:**\n")
        md.append("\n| Run | Analysis Time (ms) |")
        md.append("|-----|-------------------|")
        for result in results:
            md.append(f"| {result['run']} | {result['time']:.2f} |")
        md.append("\n")
        
        # Include first run's full output as example
        if results:
            md.append(f"\n**Example Output (Run 1):**\n")
            md.append("```\n")
            md.append(results[0]['output'].rstrip())
            md.append("\n```\n")
    
    md.append("\n---\n")
    md.append("\n## Notes\n")
    md.append("\n- Analysis time is measured internally by each solution using `end_time - start_time`\n")
    md.append("- This represents the actual image analysis time, not the total program execution time\n")
    md.append("- Times are reported in milliseconds\n")
    
    return "\n".join(md)


def main():
    """Main function to run all benchmarks."""
    print("=" * 80)
    print("Image Detection Solutions Benchmark")
    print("=" * 80)
    print(f"Running each solution {NUM_RUNS} times...\n")
    
    # Store results for each solution
    all_results = defaultdict(list)
    
    # Run each solution
    for solution_name, config in SOLUTIONS.items():
        print(f"\n{'=' * 80}")
        print(f"Solution: {solution_name.upper()}")
        print(f"{'=' * 80}")
        
        times = []
        
        for run in range(1, NUM_RUNS + 1):
            print(f"\nRun {run}/{NUM_RUNS}:")
            output, exec_time = run_solution(solution_name, config, run)
            
            if output is not None and exec_time is not None:
                # Print the output
                print(output.rstrip())
                print(f"Analysis time (internal): {exec_time:.2f} milliseconds")
                times.append(exec_time)
                all_results[solution_name].append({
                    'run': run,
                    'output': output,
                    'time': exec_time
                })
            else:
                print(f"  Failed to run or extract time")
        
        # Print summary for this solution
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            print(f"\n--- {solution_name.upper()} Summary ---")
            print(f"  Successful runs: {len(times)}/{NUM_RUNS}")
            print(f"  Average analysis time: {avg_time:.2f} milliseconds")
            print(f"  Min analysis time: {min_time:.2f} milliseconds")
            print(f"  Max analysis time: {max_time:.2f} milliseconds")
    
    # Print final comparison
    print(f"\n{'=' * 80}")
    print("FINAL RESULTS - Average Analysis Times (Internal Measurement)")
    print(f"{'=' * 80}\n")
    
    # Sort solutions by average time
    solution_averages = []
    for solution_name, results in all_results.items():
        if results:
            times = [r['time'] for r in results]
            avg_time = sum(times) / len(times)
            solution_averages.append((solution_name, avg_time, len(times)))
    
    # Sort by average time (fastest first)
    solution_averages.sort(key=lambda x: x[1])
    
    print(f"{'Solution':<15} {'Avg Analysis Time (ms)':<25} {'Successful Runs':<15}")
    print("-" * 55)
    for solution_name, avg_time, successful_runs in solution_averages:
        print(f"{solution_name:<15} {avg_time:<25.2f} {successful_runs}/{NUM_RUNS}")
    
    print(f"\n{'=' * 80}")
    
    # Generate and save markdown report
    markdown_content = generate_markdown_report(all_results, solution_averages)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = Path(__file__).parent / f"benchmark_results_{timestamp}.md"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"\n✓ Benchmark results saved to: {output_file}")
    except Exception as e:
        print(f"\n✗ Error saving markdown report: {e}")


if __name__ == '__main__':
    main()

