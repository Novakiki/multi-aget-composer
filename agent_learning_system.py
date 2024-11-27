from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Set
from termcolor import colored
from collections import defaultdict

class AgentLearningSystem:
    """Integrates agent coordination with Bayesian learning."""
    
    def __init__(self):
        self.data_dir = Path("monitor_data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize learning data structures
        self.agent_patterns = self._load_data("agent_patterns.json") or {
            "successful_workflows": defaultdict(int),
            "agent_interactions": defaultdict(list),
            "quality_impacts": defaultdict(list),
            "adaptation_history": []
        }
        
        # Track active learning
        self.active_agents: Set[str] = set()
        self.current_workflows: Dict[str, List[str]] = defaultdict(list)
        
        print(colored("Agent Learning System initialized", "green"))

    def register_agent_action(self, agent_id: str, action: str, context: Dict):
        """Record and learn from agent actions."""
        timestamp = datetime.now().isoformat()
        
        # Track action in workflow
        self.current_workflows[agent_id].append({
            "timestamp": timestamp,
            "action": action,
            "context": context
        })
        
        # Update agent interactions
        self._update_interactions(agent_id, action, context)
        
        # Learn from patterns
        if self._is_successful_action(context):
            self._learn_successful_pattern(agent_id, action, context)
        
        # Save updated patterns
        self._save_data("agent_patterns.json", self.agent_patterns)

    def get_agent_suggestions(self, agent_id: str, context: Dict) -> List[Dict]:
        """Provide learned suggestions for agent actions."""
        suggestions = []
        
        # Check successful patterns
        relevant_patterns = self._find_relevant_patterns(agent_id, context)
        if relevant_patterns:
            suggestions.append({
                "type": "PATTERN",
                "message": "Similar successful patterns found",
                "patterns": relevant_patterns
            })
        
        # Check quality impacts
        quality_insights = self._analyze_quality_impact(agent_id)
        if quality_insights:
            suggestions.append({
                "type": "QUALITY",
                "message": "Quality impact insights",
                "insights": quality_insights
            })
        
        return suggestions

    def update_quality_impact(self, agent_id: str, quality_report: Dict):
        """Learn from quality check results."""
        self.agent_patterns["quality_impacts"][agent_id].append({
            "timestamp": datetime.now().isoformat(),
            "report": quality_report,
            "workflow": self.current_workflows[agent_id].copy()
        })
        
        # Analyze and adapt
        self._adapt_to_quality_feedback(agent_id, quality_report)

    def _update_interactions(self, agent_id: str, action: str, context: Dict):
        """Track and learn from agent interactions."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_id,
            "action": action,
            "context": context
        }
        
        self.agent_patterns["agent_interactions"][agent_id].append(interaction)
        
        # Look for emerging patterns
        self._analyze_interaction_patterns()

    def _learn_successful_pattern(self, agent_id: str, action: str, context: Dict):
        """Learn from successful agent actions."""
        pattern_key = f"{agent_id}:{action}:{self._context_to_key(context)}"
        self.agent_patterns["successful_workflows"][pattern_key] += 1

    def _adapt_to_quality_feedback(self, agent_id: str, quality_report: Dict):
        """Adapt behavior based on quality results."""
        adaptation = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_id,
            "quality_metrics": quality_report,
            "adaptations": []
        }
        
        # Analyze quality trends
        if self._should_adapt(agent_id, quality_report):
            new_adaptations = self._generate_adaptations(agent_id, quality_report)
            adaptation["adaptations"] = new_adaptations
            
            self.agent_patterns["adaptation_history"].append(adaptation)

    def _analyze_interaction_patterns(self):
        """Identify emerging patterns in agent interactions."""
        recent_interactions = [
            interaction 
            for interactions in self.agent_patterns["agent_interactions"].values()
            for interaction in interactions[-10:]  # Look at recent history
        ]
        
        # Look for repeated successful sequences
        self._identify_successful_sequences(recent_interactions)

    def _should_adapt(self, agent_id: str, quality_report: Dict) -> bool:
        """Determine if adaptation is needed based on quality trends."""
        recent_impacts = self.agent_patterns["quality_impacts"][agent_id][-5:]
        if not recent_impacts:
            return False
        
        # Check for declining quality trends
        quality_scores = [self._calculate_quality_score(impact["report"]) 
                        for impact in recent_impacts]
        
        return sum(quality_scores) / len(quality_scores) < 0.8  # Threshold

    def _generate_adaptations(self, agent_id: str, quality_report: Dict) -> List[Dict]:
        """Generate specific adaptations based on quality feedback."""
        adaptations = []
        
        # Analyze quality issues
        if quality_report.get("issues"):
            for issue in quality_report["issues"]:
                adaptation = self._create_adaptation_for_issue(issue)
                if adaptation:
                    adaptations.append(adaptation)
        
        return adaptations

    def _create_adaptation_for_issue(self, issue: Dict) -> Dict:
        """Create specific adaptation for a quality issue."""
        return {
            "type": issue["type"],
            "target": issue["category"],
            "adjustment": self._determine_adjustment(issue),
            "confidence": self._calculate_confidence(issue)
        }

    def _load_data(self, filename: str) -> Dict:
        """Load learning data from file."""
        try:
            file_path = self.data_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(colored(f"Could not load {filename}: {e}", "yellow"))
        return None

    def _save_data(self, filename: str, data: Dict):
        """Save learning data to file."""
        try:
            with open(self.data_dir / filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(colored(f"Could not save {filename}: {e}", "red"))

    def _context_to_key(self, context: Dict) -> str:
        """Convert context dict to stable string key."""
        return ":".join(f"{k}={v}" for k, v in sorted(context.items()))

    def _calculate_quality_score(self, report: Dict) -> float:
        """Calculate normalized quality score from report."""
        if not report:
            return 0.0
            
        weights = {
            "CRITICAL": 0.5,
            "IMPORTANT": 0.3,
            "STYLE": 0.2
        }
        
        issues = report.get("issues", [])
        if not issues:
            return 1.0
            
        weighted_sum = sum(weights[issue["type"]] for issue in issues)
        return 1.0 - (weighted_sum / len(issues)) 