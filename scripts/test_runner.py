#!/usr/bin/env python3
"""
Test execution and validation script for YFAS project.
Provides comprehensive test running with coverage reporting and result formatting.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional


class TestRunner:
    """Main test runner class with coverage and reporting capabilities."""
    
    def __init__(self, verbose: bool = False, fail_fast: bool = False):
        self.verbose = verbose
        self.fail_fast = fail_fast
        self.project_root = Path.cwd()
        
    def run_tests(
        self, 
        test_path: Optional[str] = None,
        markers: Optional[str] = None,
        coverage: bool = True,
        html_report: bool = False
    ) -> Dict[str, Any]:
        """Run tests with optional coverage reporting."""
        print("🧪 Running tests...")
        start_time = time.time()
        
        # Build pytest command
        cmd = ["uv", "run", "pytest"]
        
        # Add test path if specified
        if test_path:
            cmd.append(test_path)
        
        # Add markers if specified
        if markers:
            cmd.extend(["-m", markers])
        
        # Add fail-fast option
        if self.fail_fast:
            cmd.append("-x")
        
        # Add verbosity
        if self.verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")
        
        # Add coverage options
        if coverage:
            cmd.extend([
                "--cov=src",
                "--cov-report=term-missing:skip-covered",
                "--cov-report=json:coverage.json",
                "--cov-fail-under=95",
                "--cov-branch"
            ])
            
            if html_report:
                cmd.append("--cov-report=html:htmlcov")
        
        # Run the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration,
            "command": " ".join(cmd)
        }
    
    def format_test_results(self, result: Dict[str, Any]) -> None:
        """Format and display test results."""
        print(f"\n{'='*60}")
        print("TEST EXECUTION RESULTS")
        print(f"{'='*60}")
        print(f"Command: {result['command']}")
        print(f"Duration: {result['duration']:.2f}s")
        print(f"Exit Code: {result['returncode']}")
        
        if result['returncode'] == 0:
            print("✅ Tests PASSED")
        else:
            print("❌ Tests FAILED")
        
        # Display output
        if result['stdout']:
            print(f"\n{'STDOUT':-^60}")
            print(result['stdout'])
        
        if result['stderr']:
            print(f"\n{'STDERR':-^60}")
            print(result['stderr'])
    
    def generate_coverage_summary(self) -> Optional[Dict[str, Any]]:
        """Generate coverage summary from coverage.json if it exists."""
        coverage_file = self.project_root / "coverage.json"
        
        if not coverage_file.exists():
            return None
        
        try:
            with open(coverage_file) as f:
                coverage_data = json.load(f)
            
            total_coverage = coverage_data["totals"]["percent_covered"]
            
            print(f"\n{'COVERAGE SUMMARY':-^60}")
            print(f"Total Coverage: {total_coverage:.2f}%")
            print(f"Lines Covered: {coverage_data['totals']['covered_lines']}")
            print(f"Total Lines: {coverage_data['totals']['num_statements']}")
            print(f"Missing Lines: {coverage_data['totals']['missing_lines']}")
            
            # Show per-file coverage for source files
            print(f"\n{'File':<30} {'Coverage':<10} {'Missing Lines'}")
            print("-" * 60)
            
            for file_path, file_data in coverage_data["files"].items():
                if file_path.startswith("src/"):
                    summary = file_data["summary"]
                    if summary["num_statements"] > 0:
                        file_coverage = (summary["covered_lines"] / summary["num_statements"]) * 100
                        missing_count = len(file_data["missing_lines"])
                        print(f"{file_path:<30} {file_coverage:>7.1f}% {missing_count:>12}")
            
            return coverage_data
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error reading coverage data: {e}")
            return None
    
    def run_linting(self) -> Dict[str, Any]:
        """Run code linting with ruff."""
        print("🔍 Running linting...")
        
        result = subprocess.run(
            ["uv", "run", "ruff", "check", "src", "tests"],
            capture_output=True,
            text=True
        )
        
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    def run_type_checking(self) -> Dict[str, Any]:
        """Run type checking with mypy."""
        print("🔎 Running type checking...")
        
        result = subprocess.run(
            ["uv", "run", "mypy", "src"],
            capture_output=True,
            text=True
        )
        
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    def run_full_validation(self) -> bool:
        """Run complete validation suite: linting, type checking, and tests."""
        print("🚀 Running full validation suite...")
        
        all_passed = True
        
        # Run linting
        lint_result = self.run_linting()
        if lint_result["returncode"] != 0:
            print("❌ Linting failed:")
            print(lint_result["stdout"])
            print(lint_result["stderr"])
            all_passed = False
        else:
            print("✅ Linting passed")
        
        # Run type checking
        type_result = self.run_type_checking()
        if type_result["returncode"] != 0:
            print("❌ Type checking failed:")
            print(type_result["stdout"])
            print(type_result["stderr"])
            all_passed = False
        else:
            print("✅ Type checking passed")
        
        # Run tests
        test_result = self.run_tests(coverage=True)
        self.format_test_results(test_result)
        
        if test_result["returncode"] != 0:
            all_passed = False
        
        # Generate coverage summary
        self.generate_coverage_summary()
        
        return all_passed


def run_with_coverage():
    """Entry point for coverage testing (used by project.scripts)."""
    runner = TestRunner(verbose=True)
    result = runner.run_tests(coverage=True, html_report=True)
    runner.format_test_results(result)
    runner.generate_coverage_summary()
    sys.exit(result["returncode"])


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="YFAS Test Runner")
    parser.add_argument(
        "--path", 
        help="Specific test path to run"
    )
    parser.add_argument(
        "--markers", "-m",
        help="Test markers to filter by (e.g., 'not slow')"
    )
    parser.add_argument(
        "--no-coverage",
        action="store_true",
        help="Skip coverage reporting"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--fail-fast", "-x",
        action="store_true",
        help="Stop on first failure"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full validation suite (lint, type check, tests)"
    )
    
    args = parser.parse_args()
    
    # Ensure we're in the project root
    if not Path("pyproject.toml").exists():
        print("Error: Must be run from project root directory")
        sys.exit(1)
    
    runner = TestRunner(verbose=args.verbose, fail_fast=args.fail_fast)
    
    if args.full:
        success = runner.run_full_validation()
        sys.exit(0 if success else 1)
    else:
        result = runner.run_tests(
            test_path=args.path,
            markers=args.markers,
            coverage=not args.no_coverage,
            html_report=args.html
        )
        
        runner.format_test_results(result)
        
        if not args.no_coverage:
            runner.generate_coverage_summary()
        
        sys.exit(result["returncode"])


if __name__ == "__main__":
    main()