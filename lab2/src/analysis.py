from __future__ import annotations

from itertools import combinations


class AnalysisMixin:
    @staticmethod
    def _term_from_bits(bits: str, variables: list[str]) -> str:
        literals: list[str] = []
        for i, bit in enumerate(bits):
            if bit == "1":
                literals.append(variables[i])
            else:
                literals.append(f"!{variables[i]}")
        if not literals:
            return "1"
        if len(literals) == 1:
            return literals[0]
        return "(" + "&".join(literals) + ")"

    @staticmethod
    def _clause_from_bits(bits: str, variables: list[str]) -> str:
        literals: list[str] = []
        for i, bit in enumerate(bits):
            if bit == "1":
                literals.append(f"!{variables[i]}")
            else:
                literals.append(variables[i])
        if not literals:
            return "1"
        if len(literals) == 1:
            return literals[0]
        return "(" + "|".join(literals) + ")"

    def _forms_for_vector(self, vector: list[int]) -> dict[str, object]:
        n = len(self.variables)

        if n == 0:
            value = vector[0]
            return {
                "sdnf": "1" if value == 1 else "0",
                "sknf": "1" if value == 1 else "0",
                "minterms": [0] if value == 1 else [],
                "maxterms": [0] if value == 0 else [],
            }

        minterms = [i for i, v in enumerate(vector) if v == 1]
        maxterms = [i for i, v in enumerate(vector) if v == 0]

        if minterms:
            terms = [self._term_from_bits(format(i, f"0{n}b"), self.variables) for i in minterms]
            sdnf = "|".join(terms)
        else:
            sdnf = "0"

        if maxterms:
            clauses = [self._clause_from_bits(format(i, f"0{n}b"), self.variables) for i in maxterms]
            sknf = "&".join(clauses)
        else:
            sknf = "1"

        return {
            "sdnf": sdnf,
            "sknf": sknf,
            "minterms": minterms,
            "maxterms": maxterms,
        }

    def canonical_forms(self) -> dict[str, object]:
        return self._forms_for_vector(self.truth_vector)

    def numeric_forms(self) -> dict[str, object]:
        canonical = self.canonical_forms()
        minterms = canonical["minterms"]
        maxterms = canonical["maxterms"]

        sigma = "Σ(" + ",".join(str(x) for x in minterms) + ")"
        pi = "Π(" + ",".join(str(x) for x in maxterms) + ")"
        return {
            "sdnf_numbers": minterms,
            "sknf_numbers": maxterms,
            "sdnf_numeric": sigma,
            "sknf_numeric": pi,
        }

    def index_form(self) -> dict[str, object]:
        vector = "".join(str(v) for v in self.truth_vector)
        return {
            "vector": vector,
            "index": int(vector, 2) if vector else 0,
        }

    def _anf_coefficients(self) -> list[int]:
        coefficients = self.truth_vector[:]
        n = len(self.variables)
        size = len(coefficients)
        for bit in range(n):
            step = 1 << bit
            for mask in range(size):
                if mask & step:
                    coefficients[mask] ^= coefficients[mask ^ step]
        return coefficients

    @staticmethod
    def _popcount(value: int) -> int:
        return value.bit_count()

    def _mask_for_var_indices(self, indices: tuple[int, ...]) -> int:
        n = len(self.variables)
        mask = 0
        for idx in indices:
            mask |= 1 << (n - 1 - idx)
        return mask

    def zhegalkin_polynomial(self) -> dict[str, object]:
        coefficients = self._anf_coefficients()
        n = len(self.variables)

        terms: list[str] = []
        if coefficients and coefficients[0] == 1:
            terms.append("1")

        for degree in range(1, n + 1):
            for idx_tuple in combinations(range(n), degree):
                mask = self._mask_for_var_indices(idx_tuple)
                if mask < len(coefficients) and coefficients[mask] == 1:
                    term_vars = [self.variables[i] for i in idx_tuple]
                    terms.append("&".join(term_vars))

        polynomial = " ^ ".join(terms) if terms else "0"
        return {
            "coefficients": coefficients,
            "polynomial": polynomial,
        }

    def post_classes(self) -> dict[str, bool]:
        n = len(self.variables)
        size = len(self.truth_vector)
        all_ones_index = (1 << n) - 1 if n > 0 else 0

        t0 = self.truth_vector[0] == 0
        t1 = self.truth_vector[all_ones_index] == 1

        self_dual = True
        for idx in range(size):
            inv = (size - 1) ^ idx
            if self.truth_vector[idx] == self.truth_vector[inv]:
                self_dual = False
                break

        monotone = True
        if n > 0:
            for x in range(size):
                bx = format(x, f"0{n}b")
                for y in range(size):
                    by = format(y, f"0{n}b")
                    leq = True
                    for i in range(n):
                        if int(bx[i]) > int(by[i]):
                            leq = False
                            break
                    if leq and self.truth_vector[x] > self.truth_vector[y]:
                        monotone = False
                        break
                if not monotone:
                    break

        coefficients = self._anf_coefficients()
        linear = True
        for mask, value in enumerate(coefficients):
            if value == 1 and self._popcount(mask) > 1:
                linear = False
                break

        return {
            "T0": t0,
            "T1": t1,
            "S": self_dual,
            "M": monotone,
            "L": linear,
        }

    def fictive_variables(self) -> list[str]:
        n = len(self.variables)
        if n == 0:
            return []

        fictive: list[str] = []
        for i, var in enumerate(self.variables):
            bit = 1 << (n - 1 - i)
            is_fictive = True
            for mask in range(1 << n):
                if mask & bit:
                    continue
                if self.truth_vector[mask] != self.truth_vector[mask | bit]:
                    is_fictive = False
                    break
            if is_fictive:
                fictive.append(var)

        return fictive

    def _derivative_reduced_forms(
        self,
        values: list[int],
        derivative_vars: list[str],
    ) -> dict[str, object]:
        derivative_set = set(derivative_vars)
        reduced_variables = [var for var in self.variables if var not in derivative_set]

        if not reduced_variables:
            value = values[0]
            return {
                "variables": reduced_variables,
                "truth_vector": [value],
                "sdnf": "1" if value == 1 else "0",
                "sknf": "1" if value == 1 else "0",
                "minterms": [0] if value == 1 else [],
                "maxterms": [0] if value == 0 else [],
            }

        reduced_vector: list[int] = []
        reduced_minterms: list[int] = []
        reduced_maxterms: list[int] = []

        for reduced_index in range(1 << len(reduced_variables)):
            reduced_bits = format(reduced_index, f"0{len(reduced_variables)}b")
            assignment: dict[str, int] = {}
            bit_pos = 0
            for var in self.variables:
                if var in derivative_set:
                    assignment[var] = 0
                else:
                    assignment[var] = int(reduced_bits[bit_pos])
                    bit_pos += 1

            full_index = self._index_from_assignment(assignment)
            value = values[full_index]
            reduced_vector.append(value)
            if value == 1:
                reduced_minterms.append(reduced_index)
            else:
                reduced_maxterms.append(reduced_index)

        if reduced_minterms:
            original_variables = self.variables
            try:
                self.variables = reduced_variables
                engine = self._minimize_dnf(reduced_minterms, include_table=False)
            finally:
                self.variables = original_variables
            sdnf = engine["result_expression"]
        else:
            sdnf = "0"

        if reduced_maxterms:
            clauses = [self._clause_from_bits(format(i, f"0{len(reduced_variables)}b"), reduced_variables) for i in reduced_maxterms]
            sknf = "&".join(clauses)
        else:
            sknf = "1"

        return {
            "variables": reduced_variables,
            "truth_vector": reduced_vector,
            "sdnf": sdnf,
            "sknf": sknf,
            "minterms": reduced_minterms,
            "maxterms": reduced_maxterms,
        }

    def boolean_derivative(self, derivative_vars: list[str]) -> dict[str, object]:
        if not derivative_vars:
            raise ValueError("Нужно передать хотя бы одну переменную")
        if len(derivative_vars) > 4:
            raise ValueError("Допускаются производные от 1 до 4 переменных")

        for name in derivative_vars:
            if name not in self.variables:
                raise ValueError(f"Переменной {name} нет в функции")

        values = self.truth_vector[:]
        n = len(self.variables)
        size = len(values)

        for name in derivative_vars:
            idx = self.variables.index(name)
            bit = 1 << (n - 1 - idx)
            new_values = [0] * size
            for mask in range(size):
                new_values[mask] = values[mask] ^ values[mask ^ bit]
            values = new_values

        reduced_forms = self._derivative_reduced_forms(values, derivative_vars)
        return {
            "variables": derivative_vars,
            "truth_vector": values,
            "sdnf": reduced_forms["sdnf"],
            "sknf": reduced_forms["sknf"],
            "minterms": reduced_forms["minterms"],
            "maxterms": reduced_forms["maxterms"],
            "result_variables": reduced_forms["variables"],
            "result_truth_vector": reduced_forms["truth_vector"],
        }
