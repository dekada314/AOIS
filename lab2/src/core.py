from __future__ import annotations

_ALLOWED_VARS = ("a", "b", "c", "d", "e")
_OPERATORS = {"!", "&", "|", "^", "->", "~"}
_PRECEDENCE = {"!": 5, "&": 4, "^": 3, "|": 2, "->": 1, "~": 0}
_RIGHT_ASSOC = {"!", "->"}


class CoreEngine:
    def __init__(self, expression: str):
        self.set_expression(expression)
        
    def set_expression(self, expression: str) -> None:
        normalized = self.normalize_expression(expression)
        tokens = self.tokenize(normalized)
        variables = [name for name in _ALLOWED_VARS if name in tokens]
        if len(variables) > 5:
            raise ValueError("Допускается не более 5 переменных")
        rpn = self.to_rpn(tokens)

        self.expression = expression
        self.normalized_expression = normalized
        self.tokens = tokens
        self.variables = variables
        self.rpn = rpn
        self.truth_vector = self._build_truth_vector()

    @staticmethod
    def normalize_expression(expression: str) -> str:
        normalized = expression.strip()
        replacements = {
            " ": "",
            "\t": "",
            "\n": "",
            "¬": "!",
            "∧": "&",
            "∨": "|",
            "→": "->",
            "↔": "~",
            "⊕": "^",
        }
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        return normalized

    @staticmethod
    def tokenize(expression: str) -> list[str]:
        if not expression:
            raise ValueError("Пустое выражение")

        tokens: list[str] = []
        i = 0
        while i < len(expression):
            ch = expression[i]
            if ch in _ALLOWED_VARS:
                tokens.append(ch)
                i += 1
                continue
            if ch in "01":
                tokens.append(ch)
                i += 1
                continue
            if ch in "()!&|^~":
                tokens.append(ch)
                i += 1
                continue
            if ch == "-" and i + 1 < len(expression) and expression[i + 1] == ">":
                tokens.append("->")
                i += 2
                continue
            if ch.isalpha() and ch.lower() in _ALLOWED_VARS:
                tokens.append(ch.lower())
                i += 1
                continue
            raise ValueError(f"Неизвестный символ: {ch}")

        return tokens

    @staticmethod
    def to_rpn(tokens: list[str]) -> list[str]:
        output: list[str] = []
        stack: list[str] = []
        prev_kind = "start"

        for token in tokens:
            if token in _ALLOWED_VARS or token in {"0", "1"}:
                output.append(token)
                prev_kind = "operand"
                continue

            if token == "(":
                stack.append(token)
                prev_kind = "lparen"
                continue

            if token == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                if not stack:
                    raise ValueError("Несогласованные скобки")
                stack.pop()
                prev_kind = "operand"
                continue

            if token in _OPERATORS:
                if token != "!" and prev_kind in {"start", "operator", "lparen"}:
                    raise ValueError("Некорректная позиция бинарного оператора")
                if token == "!" and prev_kind == "operand":
                    raise ValueError("Оператор ! должен стоять перед выражением")

                while stack and stack[-1] in _OPERATORS:
                    top = stack[-1]
                    if _PRECEDENCE[top] > _PRECEDENCE[token]:
                        output.append(stack.pop())
                    elif _PRECEDENCE[top] == _PRECEDENCE[token] and token not in _RIGHT_ASSOC:
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)
                prev_kind = "operator"
                continue

            raise ValueError(f"Неизвестный токен: {token}")

        if prev_kind == "operator":
            raise ValueError("Выражение не может заканчиваться оператором")

        while stack:
            current = stack.pop()
            if current == "(":
                raise ValueError("Несогласованные скобки")
            output.append(current)

        return output

    def _evaluate_rpn(self, assignment: dict[str, int]) -> int:
        stack: list[int] = []
        for token in self.rpn:
            if token in _ALLOWED_VARS:
                stack.append(int(assignment[token]))
                continue
            if token in {"0", "1"}:
                stack.append(int(token))
                continue
            if token == "!":
                if not stack:
                    raise ValueError("Недостаточно операндов для !")
                value = stack.pop()
                stack.append(0 if value else 1)
                continue

            if len(stack) < 2:
                raise ValueError("Недостаточно операндов")
            right = stack.pop()
            left = stack.pop()

            if token == "&":
                stack.append(1 if (left and right) else 0)
            elif token == "|":
                stack.append(1 if (left or right) else 0)
            elif token == "^":
                stack.append(left ^ right)
            elif token == "->":
                stack.append(1 if ((not left) or right) else 0)
            elif token == "~":
                stack.append(1 if left == right else 0)
            else:
                raise ValueError(f"Неизвестный оператор: {token}")

        if len(stack) != 1:
            raise ValueError("Некорректное выражение")
        return stack[0]

    def _build_truth_vector(self) -> list[int]:
        n = len(self.variables)
        if n == 0:
            return [self._evaluate_rpn({})]

        values: list[int] = []
        for index in range(1 << n):
            bits = format(index, f"0{n}b")
            assignment = {var: int(bits[i]) for i, var in enumerate(self.variables)}
            values.append(self._evaluate_rpn(assignment))
        return values

    def truth_table(self) -> list[dict[str, int]]:
        rows: list[dict[str, int]] = []
        n = len(self.variables)

        if n == 0:
            rows.append({"f": self.truth_vector[0]})
            return rows

        for index, value in enumerate(self.truth_vector):
            bits = format(index, f"0{n}b")
            row = {var: int(bits[i]) for i, var in enumerate(self.variables)}
            row["f"] = value
            rows.append(row)
        return rows
