from typing import List
from app.llm.rule_loader import RuleLoader


class PromptBuilder:
    def __init__(self):
        self.loader = RuleLoader()

    def build_system_prompt(self, active_rules: List[str]) -> str:
        """Build system prompt from active rules."""
        # Load base system prompt
        base_prompt = self._load_base_system_prompt()

        # Load rule contents
        rule_contents = []
        for rule_name in active_rules:
            content = self.loader.get_rule_content(rule_name)
            if content:
                # Remove frontmatter
                lines = content.split('\n')
                content_lines = []
                in_frontmatter = False
                for line in lines:
                    if line.strip() == '---':
                        if in_frontmatter:
                            continue
                        in_frontmatter = True
                        continue
                    if not in_frontmatter:
                        content_lines.append(line)
                rule_content = '\n'.join(content_lines)
                rule_contents.append(f"## {rule_name}\n\n{rule_content}")

        # Combine base prompt with rules
        rules_section = "\n\n".join(rule_contents)
        full_prompt = f"{base_prompt}\n\n{rules_section}"

        return full_prompt

    def _load_base_system_prompt(self) -> str:
        """Load base system prompt from file."""
        try:
            with open("app/llm/prompts/system.txt", 'r') as f:
                return f.read()
        except FileNotFoundError:
            return self._get_default_base_prompt()

    def _get_default_base_prompt(self) -> str:
        """Return default base system prompt if file not found."""
        return """You are an AI Orchestrator agent working on an enterprise software project.

PROJECT CONTEXT:
- Zero Trust Architecture enforced
- Local-only processing (no external APIs)
- Docker sandboxed execution
- Git worktree isolation

APPLICABLE POLICIES:
{rules}

Follow all applicable policies strictly when generating code, making architectural decisions, or reviewing changes."""
