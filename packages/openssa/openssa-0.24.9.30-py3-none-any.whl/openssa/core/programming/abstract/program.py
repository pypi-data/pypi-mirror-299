"""
==========================
ABSTRACT PROGRAM INTERFACE
==========================

`AbstractProgram` is `OpenSSA`'s abstract base class for problem-solving Programs.

A Program has a target Task,
which encapsulates a posed Problem to solve and a set of Resources to help solve it.

A Program can be executed through its own `.execute(...)` method,
which optionally takes into account some given domain-specific Knowledge,
and which returns a string result.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Self as SameType, TYPE_CHECKING

if TYPE_CHECKING:
    from openssa.core.knowledge.abstract import Knowledge
    from openssa.core.task import Task
    from .programmer import AbstractProgrammer


@dataclass
class AbstractProgram(ABC):
    """Abstract Program."""

    # target Task to solve
    task: Task

    # Programmer that has created this
    programmer: AbstractProgrammer | None = None

    @abstractmethod
    def adapt(self, **kwargs: Any) -> SameType:
        """Return adapted copy."""

    @abstractmethod
    def execute(self, knowledge: set[Knowledge] | None = None, **kwargs: Any) -> str:
        """Execute and return string result.

        Execution also optionally takes into account domain-specific Knowledge.
        """
