"""Skill submissions and the skill seat (PLANNING.md §6): a student's skill played by the course agent."""

from .loader import EFFORT, MODELS, Skill, SkillError, is_skill_dir, load_skill

__all__ = ["EFFORT", "MODELS", "Skill", "SkillError", "is_skill_dir", "load_skill"]
