#!/usr/bin/env python3
"""
Coverage reporting and badge generation script for YFAS project.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any


def run_coverage() -> Dict[str, Any]:
    """Run tests with coverage and return coverage data."""
    print("Running tests with coverage...")
    
    # Run pytest with coverage
    result = subprocess.run(
        ["uv", "run", "pytest", "--cov=src", "--cov-report=json:coverage.json"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Tests failed with return code {result.returncode}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        sys.exit(1)
    
    # Load coverage data
    coverage_file = Path("coverage.json")
    if not coverage_file.exists():
        print("Coverage file not found!")
        sys.exit(1)
    
    with open(coverage_file) as f:
        coverage_data = json.load(f)
    
    return coverage_data


def generate_coverage_badge(coverage_percent: float) -> str:
    """Generate a coverage badge URL."""
    # Determine badge color based on coverage percentage
    if coverage_percent >= 95:
        color = "brightgreen"
    elif coverage_percent >= 90:
        color = "green"
    elif coverage_percent >= 80:
        color = "yellow"
    elif coverage_percent >= 70:
        color = "orange"
    else:
        color = "red"
    
    # Generate shields.io badge URL
    badge_url = f"https://img.shields.io/badge/coverage-{coverage_percent:.1f}%25-{color}"
    return badge_url


def generate_coverage_report(coverage_data: Dict[str, Any]) -> None:
    """Generate a detailed coverage report."""
    total_coverage = coverage_data["totals"]["percent_covered"]
    
    print(f"\n{'='*60}")
    print("COVERAGE REPORT")
    print(f"{'='*60}")
    print(f"Total Coverage: {total_coverage:.2f}%")
    print(f"Lines Covered: {coverage_data['totals']['covered_lines']}")
    print(f"Total Lines: {coverage_data['totals']['num_statements']}")
    print(f"Missing Lines: {coverage_data['totals']['missing_lines']}")
    print(f"Branch Coverage: {coverage_data['totals']['percent_covered_display']}%")
    
    print(f"\n{'File Coverage Details':<40} {'Coverage':<10} {'Missing'}")
    print("-" * 60)
    
    for file_path, file_data in coverage_data["files"].items():
        if file_path.startswith("src/"):
            coverage_pct = (file_data["summary"]["covered_lines"] / 
                          file_data["summary"]["num_statements"] * 100 
                          if file_data["summary"]["num_statements"] > 0 else 100)
            missing_lines = len(file_data["missing_lines"])
            print(f"{file_path:<40} {coverage_pct:>7.1f}% {missing_lines:>8}")
    
    # Generate badge
    badge_url = generate_coverage_badge(total_coverage)
    print(f"\nCoverage Badge URL:")
    print(badge_url)
    
    # Save badge URL to file for CI/CD
    with open("coverage_badge.txt", "w") as f:
        f.write(badge_url)
    
    print(f"\nBadge URL saved to coverage_badge.txt")


def validate_coverage_threshold(coverage_data: Dict[str, Any], threshold: float = 95.0) -> bool:
    """Validate that coverage meets the required threshold."""
    total_coverage = coverage_data["totals"]["percent_covered"]
    
    if total_coverage < threshold:
        print(f"\n❌ COVERAGE FAILURE: {total_coverage:.2f}% < {threshold}%")
        print("Coverage is below the required threshold!")
        return False
    else:
        print(f"\n✅ COVERAGE SUCCESS: {total_coverage:.2f}% >= {threshold}%")
        return True


def main():
    """Main function to run coverage reporting."""
    # Ensure we're in the project root
    if not Path("pyproject.toml").exists():
        print("Error: Must be run from project root directory")
        sys.exit(1)
    
    # Create scripts directory if it doesn't exist
    Path("scripts").mkdir(exist_ok=True)
    
    try:
        # Run coverage
        coverage_data = run_coverage()
        
        # Generate report
        generate_coverage_report(coverage_data)
        
        # Validate threshold
        threshold = 95.0  # Can be made configurable
        success = validate_coverage_threshold(coverage_data, threshold)
        
        if not success:
            sys.exit(1)
        
        print("\n🎉 Coverage reporting completed successfully!")
        
    except Exception as e:
        print(f"Error during coverage reporting: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()