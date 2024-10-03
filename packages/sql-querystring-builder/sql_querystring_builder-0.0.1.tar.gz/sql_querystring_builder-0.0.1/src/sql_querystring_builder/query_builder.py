from __future__ import annotations
from operator import attrgetter

from .abstract_clause import Clause


class QueryBuilder:
    def __init__(self, *initial_clauses:list[Clause]) -> None:
        self.clauses: list[Clause] = []
        if initial_clauses:
            self.extend(initial_clauses)

    def add(self, clause: Clause) -> QueryBuilder:
        self.clauses.append(clause)
        return self

    def extend(self, clauses: list[Clause]) -> QueryBuilder:
        self.clauses.extend(clauses)
        return self

    def build(self) -> str:
        sorted_clauses: list[Clause] = sorted(self.clauses, key=attrgetter("place"))
        return "\n".join(clause.build() for clause in sorted_clauses)
