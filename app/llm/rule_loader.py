import os
import re
from pathlib import Path
from typing import List, Dict, Optional


class RuleLoader:
    def __init__(self, rules_dir: str = "app/llm/rules"):
        self.rules_dir = Path(rules_dir)
        self._rules_cache: Optional[Dict[str, str]] = None

    def load_rules(self) -> Dict[str, str]:
        """Load all rule files and return a dictionary of rule name -> content."""
        if self._rules_cache is not None:
            return self._rules_cache

        rules = {}
        for rule_file in sorted(self.rules_dir.glob("*.md")):
            rule_name = rule_file.stem
            with open(rule_file, 'r') as f:
                content = f.read()
            rules[rule_name] = content

        self._rules_cache = rules
        return rules

    def get_mandatory_rules(self) -> List[str]:
        """Return list of mandatory rule file names (00, 01, 02, 12, 20)."""
        return [
            "00-zero-trust-policy",
            "01-saas-architecture-policy",
            "02-dpdpa-compliance",
            "12-data-persistence-patterns",
            "20-clean-code-standards"
        ]

    def get_optional_rules(self) -> List[str]:
        """Return list of optional rule file names."""
        all_rules = set(self.load_rules().keys())
        mandatory = set(self.get_mandatory_rules())
        return sorted(all_rules - mandatory)

    def detect_language_patterns(self, project_path: str) -> Dict[str, bool]:
        """Detect language patterns from project files."""
        detected = {
            "python": False,
            "ruby": False,
            "typescript": False,
            "go": False
        }

        project = Path(project_path)

        # Python detection
        python_indicators = ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]
        if any((project / indicator).exists() for indicator in python_indicators):
            detected["python"] = True

        # Ruby detection
        ruby_indicators = ["Gemfile", "Gemfile.lock"]
        if any((project / indicator).exists() for indicator in ruby_indicators):
            detected["ruby"] = True

        # TypeScript detection
        ts_indicators = ["package.json", "tsconfig.json"]
        if any((project / indicator).exists() for indicator in ts_indicators):
            detected["typescript"] = True

        # Go detection
        go_indicators = ["go.mod", "go.sum"]
        if any((project / indicator).exists() for indicator in go_indicators):
            detected["go"] = True

        return detected

    def detect_architecture_patterns(self, project_path: str) -> Dict[str, bool]:
        """Detect architecture patterns from project files."""
        detected = {
            "backend": False,
            "frontend": False
        }

        project = Path(project_path)

        # Backend detection (server-side languages)
        backend_indicators = ["requirements.txt", "Gemfile", "go.mod", "pom.xml", "build.gradle"]
        if any((project / indicator).exists() for indicator in backend_indicators):
            detected["backend"] = True

        # Frontend detection
        frontend_indicators = ["package.json", "tsconfig.json", "webpack.config.js", "vite.config.js"]
        if any((project / indicator).exists() for indicator in frontend_indicators):
            detected["frontend"] = True

        return detected

    def get_rule_content(self, rule_name: str) -> Optional[str]:
        """Get content of a specific rule file."""
        rules = self.load_rules()
        return rules.get(rule_name)

    def parse_frontmatter(self, content: str) -> Dict[str, str]:
        """Parse YAML frontmatter from rule content."""
        frontmatter = {}
        lines = content.split('\n')
        in_frontmatter = False

        for line in lines:
            if line.strip() == '---':
                if in_frontmatter:
                    break
                in_frontmatter = True
                continue

            if in_frontmatter:
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()

        return frontmatter
