"""Visualization tools for cognitive patterns."""
from typing import List, Dict
from termcolor import colored
from datetime import datetime

class PatternVisualizer:
    """Tracks and evolves pattern understanding over time."""
    
    @staticmethod
    def show_pattern_evolution(pattern_history: List[Dict]) -> None:
        """Show how patterns evolve over time."""
        try:
            print(colored("\n📈 Pattern Evolution Tree:", "cyan"))
            
            # Group by category
            categories = {}
            for entry in pattern_history:
                cat = entry.get('category', 'unknown')
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(entry)
            
            # Show evolution by category
            for category, entries in categories.items():
                print(colored(f"\n{category.title()} Patterns:", "yellow"))
                for i, entry in enumerate(entries):
                    prefix = "├──" if i < len(entries) - 1 else "└──"
                    theme = entry.get('theme', 'unknown')
                    confidence = entry.get('confidence', 0)
                    thought = entry.get('thought', '')
                    
                    print(f"{prefix} {theme} ({confidence:.2f})")
                    print(f"    └── \"{thought}\"")
                    
        except Exception as e:
            print(colored(f"Error visualizing pattern evolution: {str(e)}", "red"))
    
    @staticmethod
    def show_correlations(correlations: List[Dict]) -> None:
        """Visualize pattern correlations."""
        try:
            print(colored("\n🔗 Pattern Correlations:", "magenta"))
            
            if not correlations:
                print(colored("  No correlations found", "yellow"))
                return
            
            for i, corr in enumerate(correlations, 1):
                pattern = corr.get('pattern', 'unknown')
                outcome = corr.get('outcome', 'unknown')
                confidence = corr.get('confidence', 0)
                evidence = corr.get('evidence', [])
                
                print(colored(f"\nCorrelation {i}:", "yellow"))
                print(f"  {pattern} → {outcome}")
                print(f"  Confidence: {confidence:.2f}")
                if evidence:
                    print("  Evidence:")
                    for e in evidence:
                        print(f"    • {e}")
                print("  " + "─" * 40)
                
        except Exception as e:
            print(colored(f"Error visualizing correlations: {str(e)}", "red"))
    
    @staticmethod
    def show_pattern_summary(patterns: List[Dict]) -> None:
        """Show current pattern summary."""
        try:
            print(colored("\n📊 Pattern Summary:", "cyan"))
            
            if not patterns:
                print(colored("  No patterns to summarize", "yellow"))
                return
            
            # Count by category
            categories = {}
            for pattern in patterns:
                cat = pattern.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            # Show distribution
            total = len(patterns)
            for category, count in categories.items():
                percentage = (count / total) * 100
                bar = "█" * int(percentage / 5)
                print(f"\n{category.title()}: {count}")
                print(f"{bar} {percentage:.1f}%")
                
        except Exception as e:
            print(colored(f"Error in pattern summary: {str(e)}", "red"))