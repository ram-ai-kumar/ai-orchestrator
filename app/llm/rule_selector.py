import os
import yaml
import git
from pathlib import Path
from typing import List, Dict, Optional
from app.llm.rule_loader import RuleLoader


class RuleSelector:
    def __init__(self, config_path: str = "config/rules.yaml", project_path: str = "."):
        self.config_path = Path(config_path)
        self.project_path = Path(project_path)
        self.loader = RuleLoader()
        self._config: Optional[Dict] = None

    def get_current_branch(self) -> Optional[str]:
        """Get current git branch name."""
        try:
            repo = git.Repo(self.project_path, search_parent_directories=True)
            return repo.active_branch.name
        except Exception:
            return None

    def is_production_branch(self, branch: str) -> bool:
        """Check if branch is a production branch (main, release/*, develop)."""
        if branch in ["main", "develop"]:
            return True
        if branch and branch.startswith("release/"):
            return True
        return False

    def load_config(self) -> Dict:
        """Load config/rules.yaml, create default if missing."""
        if self._config is not None:
            return self._config

        if not self.config_path.exists():
            self._config = self._create_default_config()
            self.save_config(self._config)
        else:
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f)

        return self._config

    def _create_default_config(self) -> Dict:
        """Create default config with auto-detection values."""
        return {
            "mandatory": self.loader.get_mandatory_rules(),
            "optional": {
                "03-hipaa-compliance": False,
                "04-soc2-compliance": False,
                "05-iso27001-compliance": False,
                "10-backend-patterns": "auto",
                "11-frontend-patterns": "auto",
                "21-ruby-rails-patterns": "auto",
                "22-python-patterns": "auto",
                "23-typescript-patterns": "auto",
                "24-go-patterns": "auto"
            },
            "auto_detect": {
                "python": ["requirements.txt", "pyproject.toml", "setup.py"],
                "ruby": ["Gemfile", "Gemfile.lock"],
                "typescript": ["package.json", "tsconfig.json"],
                "go": ["go.mod", "go.sum"],
                "backend": ["requirements.txt", "Gemfile", "go.mod"],
                "frontend": ["package.json", "tsconfig.json"]
            }
        }

    def save_config(self, config: Dict):
        """Save config to config/rules.yaml."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        self._config = config

    def auto_recommend_rules(self) -> Dict[str, bool]:
        """Auto-detect project and recommend optional rules based on branch."""
        config = self.load_config()
        recommendations = {}

        # Check current branch
        current_branch = self.get_current_branch()

        # If on production branch, enable all optional rules
        if current_branch and self.is_production_branch(current_branch):
            for rule_name in self.loader.get_optional_rules():
                recommendations[rule_name] = True
            return recommendations

        # If on development branch or git detection fails, use auto-detection
        lang_detected = self.loader.detect_language_patterns(str(self.project_path))
        arch_detected = self.loader.detect_architecture_patterns(str(self.project_path))

        # Process optional rules
        for rule_name, value in config.get("optional", {}).items():
            if isinstance(value, bool):
                # Explicit true/false, use as-is
                recommendations[rule_name] = value
            elif value == "auto":
                # Auto-detect based on rule type
                if "python" in rule_name:
                    recommendations[rule_name] = lang_detected.get("python", False)
                elif "ruby" in rule_name:
                    recommendations[rule_name] = lang_detected.get("ruby", False)
                elif "typescript" in rule_name:
                    recommendations[rule_name] = lang_detected.get("typescript", False)
                elif "go" in rule_name:
                    recommendations[rule_name] = lang_detected.get("go", False)
                elif "backend" in rule_name:
                    recommendations[rule_name] = arch_detected.get("backend", False)
                elif "frontend" in rule_name:
                    recommendations[rule_name] = arch_detected.get("frontend", False)
                else:
                    # Security compliance rules default to false
                    recommendations[rule_name] = False
            else:
                recommendations[rule_name] = False

        return recommendations

    def select_rules_interactively(self, accept_defaults: bool = False) -> List[str]:
        """Display recommendations, allow override (optional)."""
        config = self.load_config()
        recommendations = self.auto_recommend_rules()

        # Get current branch
        current_branch = self.get_current_branch()
        branch_type = "production" if current_branch and self.is_production_branch(current_branch) else "development"

        if accept_defaults:
            # Save auto-recommendations to config
            config["optional"] = recommendations
            self.save_config(config)
            return self.get_active_rules()

        # Display recommendations
        print("\nCurrent branch:", current_branch or "Unknown")
        print("Branch type:", branch_type)
        print("\nAuto-detected project type:")
        lang_detected = self.loader.detect_language_patterns(str(self.project_path))
        arch_detected = self.loader.detect_architecture_patterns(str(self.project_path))
        print(f"  Languages: {', '.join([k for k, v in lang_detected.items() if v]) or 'None detected'}")
        print(f"  Architecture: {', '.join([k for k, v in arch_detected.items() if v]) or 'None detected'}")

        print("\nMandatory rules (always applied):")
        for rule in config.get("mandatory", []):
            print(f"  ✓ {rule}")

        print("\nRecommended optional rules:")
        for rule, enabled in recommendations.items():
            status = "✓" if enabled else "-"
            print(f"  {status} {rule}")

        print("\nPress Enter to accept, or edit config/rules.yaml to customize")
        input()

        # Save recommendations to config
        config["optional"] = recommendations
        self.save_config(config)

        return self.get_active_rules()

    def get_active_rules(self) -> List[str]:
        """Return mandatory + selected optional rules based on branch."""
        config = self.load_config()
        mandatory = config.get("mandatory", [])

        # Check current branch
        current_branch = self.get_current_branch()

        # If git detection fails, fallback to config-based selection
        if current_branch is None:
            optional_config = config.get("optional", {})
            recommendations = self.auto_recommend_rules()
            optional_enabled = [rule for rule, enabled in recommendations.items() if enabled]
            return mandatory + optional_enabled

        # Branch-based rule selection
        if self.is_production_branch(current_branch):
            # Production branches: apply all optional rules
            all_optional = self.loader.get_optional_rules()
            return mandatory + all_optional
        else:
            # Development branches: only apply mandatory rules
            return mandatory
