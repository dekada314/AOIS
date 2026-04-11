from __future__ import annotations

from itertools import combinations


class MinimizationMixin:
    @staticmethod
    def _combine_terms(a: tuple[str, ...], b: tuple[str, ...]) -> tuple[str, ...] | None:
        diff = 0
        result: list[str] = []

        for left, right in zip(a, b):
            if left == right:
                result.append(left)
                continue
            if left in {"0", "1"} and right in {"0", "1"}:
                diff += 1
                result.append("-")
                continue
            return None

        if diff == 1:
            return tuple(result)
        return None

    @staticmethod
    def _pattern(term: tuple[str, ...]) -> str:
        return "".join(term)

    def _glue_stages(self, indices: list[int]) -> tuple[list[list[tuple[str, ...]]], list[tuple[str, ...]]]:
        n = len(self.variables)
        current = {tuple(format(i, f"0{n}b")) for i in indices}
        stages: list[list[tuple[str, ...]]] = [sorted(current)]
        prime_implicants: set[tuple[str, ...]] = set()

        while True:
            used: set[tuple[str, ...]] = set()
            next_terms: set[tuple[str, ...]] = set()
            current_list = sorted(current)

            for i in range(len(current_list)):
                for j in range(i + 1, len(current_list)):
                    combined = self._combine_terms(current_list[i], current_list[j])
                    if combined is not None:
                        used.add(current_list[i])
                        used.add(current_list[j])
                        next_terms.add(combined)

            for term in current:
                if term not in used:
                    prime_implicants.add(term)

            if not next_terms:
                break

            stages.append(sorted(next_terms))
            current = next_terms

        return stages, sorted(prime_implicants)

    def _covers(self, term: tuple[str, ...], index: int) -> bool:
        bits = format(index, f"0{len(self.variables)}b")
        for i, symbol in enumerate(term):
            if symbol != "-" and symbol != bits[i]:
                return False
        return True

    @staticmethod
    def _literal_count(term: tuple[str, ...]) -> int:
        return sum(1 for x in term if x != "-")

    def _select_cover(self, prime_implicants: list[tuple[str, ...]], indices: list[int]) -> list[tuple[str, ...]]:
        if not indices:
            return []

        coverage: dict[int, list[int]] = {}
        cover_sets: list[set[int]] = []

        for term in prime_implicants:
            covered = {idx for idx in indices if self._covers(term, idx)}
            cover_sets.append(covered)

        for idx in indices:
            holders: list[int] = []
            for i, covered in enumerate(cover_sets):
                if idx in covered:
                    holders.append(i)
            coverage[idx] = holders

        essential: set[int] = set()
        for idx, holders in coverage.items():
            if len(holders) == 1:
                essential.add(holders[0])

        covered_by_essential: set[int] = set()
        for i in essential:
            covered_by_essential |= cover_sets[i]

        uncovered = set(indices) - covered_by_essential
        remaining = [i for i in range(len(prime_implicants)) if i not in essential]

        best_combo: tuple[int, ...] = tuple()
        if uncovered:
            best_cost: tuple[int, int] | None = None
            for size in range(len(remaining) + 1):
                found_here: list[tuple[int, ...]] = []
                for combo in combinations(remaining, size):
                    covered = set(covered_by_essential)
                    for idx in combo:
                        covered |= cover_sets[idx]
                    if uncovered <= covered:
                        found_here.append(combo)
                if found_here:
                    for combo in found_here:
                        all_terms = [prime_implicants[i] for i in sorted(set(essential) | set(combo))]
                        cost = (len(all_terms), sum(self._literal_count(term) for term in all_terms))
                        if best_cost is None or cost < best_cost:
                            best_cost = cost
                            best_combo = combo
                    break

        selected_ids = sorted(set(essential) | set(best_combo))
        return [prime_implicants[i] for i in selected_ids]

    def _term_to_dnf(self, term: tuple[str, ...]) -> str:
        literals: list[str] = []
        for i, symbol in enumerate(term):
            if symbol == "1":
                literals.append(self.variables[i])
            elif symbol == "0":
                literals.append(f"!{self.variables[i]}")

        if not literals:
            return "1"
        if len(literals) == 1:
            return literals[0]
        return "(" + "&".join(literals) + ")"

    def _term_to_knf_clause_from_zero_cube(self, term: tuple[str, ...]) -> str:
        literals: list[str] = []
        for i, symbol in enumerate(term):
            if symbol == "1":
                literals.append(f"!{self.variables[i]}")
            elif symbol == "0":
                literals.append(self.variables[i])

        if not literals:
            return "0"
        if len(literals) == 1:
            return literals[0]
        return "(" + "|".join(literals) + ")"

    def _build_prime_table(
        self,
        prime_implicants: list[tuple[str, ...]],
        columns: list[int],
    ) -> dict[str, object]:
        rows = []
        for term in prime_implicants:
            rows.append(
                {
                    "pattern": self._pattern(term),
                    "term": self._term_to_dnf(term),
                    "marks": [self._covers(term, index) for index in columns],
                }
            )

        return {
            "columns": columns,
            "rows": rows,
        }

    def _minimize_dnf(self, minterms: list[int], include_table: bool) -> dict[str, object]:
        if not minterms:
            return {
                "stages": [["0"]],
                "prime_implicants": [],
                "selected_implicants": [],
                "result_expression": "0",
                "table": {"columns": [], "rows": []},
            }

        if len(minterms) == (1 << len(self.variables)):
            return {
                "stages": [["1"]],
                "prime_implicants": ["-" * len(self.variables)],
                "selected_implicants": ["-" * len(self.variables)],
                "result_expression": "1",
                "table": {"columns": minterms, "rows": []},
            }

        stages, primes = self._glue_stages(minterms)
        selected_terms = self._select_cover(primes, minterms)

        pieces = [self._term_to_dnf(term) for term in selected_terms]
        expression = "|".join(pieces) if pieces else "0"

        table = self._build_prime_table(primes, minterms) if include_table else {"columns": [], "rows": []}

        return {
            "stages": [[self._pattern(term) for term in stage] for stage in stages],
            "prime_implicants": [self._pattern(term) for term in primes],
            "selected_implicants": [self._pattern(term) for term in selected_terms],
            "result_expression": expression,
            "table": table,
        }

    def _minimize_knf(self, maxterms: list[int], include_table: bool) -> dict[str, object]:
        if not maxterms:
            return {
                "stages": [["1"]],
                "prime_implicants": [],
                "selected_implicants": [],
                "result_expression": "1",
                "table": {"columns": [], "rows": []},
            }

        if len(maxterms) == (1 << len(self.variables)):
            return {
                "stages": [["0"]],
                "prime_implicants": ["-" * len(self.variables)],
                "selected_implicants": ["-" * len(self.variables)],
                "result_expression": "0",
                "table": {"columns": maxterms, "rows": []},
            }

        stages, primes = self._glue_stages(maxterms)
        selected_terms = self._select_cover(primes, maxterms)

        clauses = [self._term_to_knf_clause_from_zero_cube(term) for term in selected_terms]
        expression = "&".join(clauses) if clauses else "1"

        table = self._build_prime_table(primes, maxterms) if include_table else {"columns": [], "rows": []}

        return {
            "stages": [[self._pattern(term) for term in stage] for stage in stages],
            "prime_implicants": [self._pattern(term) for term in primes],
            "selected_implicants": [self._pattern(term) for term in selected_terms],
            "result_expression": expression,
            "table": table,
        }

    def minimize_calculation(self) -> dict[str, object]:
        forms = self.canonical_forms()
        return {
            "dnf": self._minimize_dnf(forms["minterms"], include_table=False),
            "knf": self._minimize_knf(forms["maxterms"], include_table=False),
        }

    def minimize_calculation_table(self) -> dict[str, object]:
        forms = self.canonical_forms()
        return {
            "dnf": self._minimize_dnf(forms["minterms"], include_table=True),
            "knf": self._minimize_knf(forms["maxterms"], include_table=True),
        }

    @staticmethod
    def _gray_codes(bits: int) -> list[int]:
        if bits == 0:
            return [0]
        return [i ^ (i >> 1) for i in range(1 << bits)]

    def _index_from_assignment(self, assignment: dict[str, int]) -> int:
        bits = "".join(str(assignment[var]) for var in self.variables)
        return int(bits, 2) if bits else 0

    @staticmethod
    def _bits_of(value: int, width: int) -> list[int]:
        if width == 0:
            return []
        return [int(ch) for ch in format(value, f"0{width}b")]

    def _karnaugh_table(self) -> dict[str, object]:
        n = len(self.variables)

        if n == 0:
            return {
                "type": "single",
                "row_vars": [],
                "col_vars": [],
                "rows": [[self.truth_vector[0]]],
                "row_labels": [""],
                "col_labels": [""],
            }

        if n <= 4:
            row_bits = n // 2
            col_bits = n - row_bits
            row_vars = self.variables[:row_bits]
            col_vars = self.variables[row_bits:]

            row_codes = self._gray_codes(row_bits)
            col_codes = self._gray_codes(col_bits)

            row_labels = [format(code, f"0{row_bits}b") if row_bits else "" for code in row_codes]
            col_labels = [format(code, f"0{col_bits}b") if col_bits else "" for code in col_codes]

            grid: list[list[int]] = []
            for r in row_codes:
                row_bits_values = self._bits_of(r, row_bits)
                row: list[int] = []
                for c in col_codes:
                    col_bits_values = self._bits_of(c, col_bits)
                    assignment: dict[str, int] = {}
                    for i, var in enumerate(row_vars):
                        assignment[var] = row_bits_values[i]
                    for i, var in enumerate(col_vars):
                        assignment[var] = col_bits_values[i]
                    index = self._index_from_assignment(assignment)
                    row.append(self.truth_vector[index])
                grid.append(row)

            return {
                "type": "single",
                "row_vars": row_vars,
                "col_vars": col_vars,
                "rows": grid,
                "row_labels": row_labels,
                "col_labels": col_labels,
            }

        layer_var = self.variables[0]
        row_vars = self.variables[1:3]
        col_vars = self.variables[3:5]

        row_codes = self._gray_codes(len(row_vars))
        col_codes = self._gray_codes(len(col_vars))
        row_labels = [format(code, f"0{len(row_vars)}b") for code in row_codes]
        col_labels = [format(code, f"0{len(col_vars)}b") for code in col_codes]

        maps: dict[int, list[list[int]]] = {}
        for layer in [0, 1]:
            grid: list[list[int]] = []
            for r in row_codes:
                row_bits_values = self._bits_of(r, len(row_vars))
                row: list[int] = []
                for c in col_codes:
                    col_bits_values = self._bits_of(c, len(col_vars))
                    assignment = {layer_var: layer}
                    for i, var in enumerate(row_vars):
                        assignment[var] = row_bits_values[i]
                    for i, var in enumerate(col_vars):
                        assignment[var] = col_bits_values[i]
                    index = self._index_from_assignment(assignment)
                    row.append(self.truth_vector[index])
                grid.append(row)
            maps[layer] = grid

        return {
            "type": "double",
            "layer_var": layer_var,
            "row_vars": row_vars,
            "col_vars": col_vars,
            "row_labels": row_labels,
            "col_labels": col_labels,
            "maps": maps,
        }

    def minimize_karnaugh(self) -> dict[str, object]:
        forms = self.canonical_forms()
        return {
            "map": self._karnaugh_table(),
            "dnf": self._minimize_dnf(forms["minterms"], include_table=False),
            "knf": self._minimize_knf(forms["maxterms"], include_table=False),
        }
