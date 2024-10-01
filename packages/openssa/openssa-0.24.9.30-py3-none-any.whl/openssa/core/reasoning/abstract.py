"""
===========================
ABSTRACT REASONER INTERFACE
===========================

`AbstractReasoner` is `OpenSSA`'s abstract base class for reasoning.

A reasoner has an LM and can `.reason(...)` through a given task (which can come with assigned informational resources),
optionally leveraging some given domain-specific knowledge and/or some other results from elsewhere,
and return a conclusion in string.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from openssa.core.util.lm.openai import OpenAILM

if TYPE_CHECKING:
    from openssa.core.knowledge.abstract import Knowledge
    from openssa.core.task import Task
    from openssa.core.util.lm.abstract import AbstractLM
    from openssa.core.util.misc import AskAnsPair


@dataclass
class AbstractReasoner(ABC):
    """Abstract Reasoner."""

    # language model for reasoning
    lm: AbstractLM = field(default_factory=OpenAILM.from_defaults,
                           init=True,
                           repr=True,
                           hash=None,
                           compare=True,
                           metadata=None,
                           kw_only=False)

    @abstractmethod
    def reason(self, task: Task, *,
               knowledge: set[Knowledge], other_results: list[AskAnsPair] | None = None, n_words: int = 1000) -> str:
        """Work through Task and return conclusion in string."""
