import sys

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"{self.token_type:20} {self.value}"

class Scanner:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.length = len(code)

        self.keywords = {
            "int", "float", "char", "if", "else", "for", "while",
            "return", "break", "continue", "void", "main"
        }

        self.special_chars = set("(){}[],;")
        self.operators = {
            "+", "-", "*", "/", "=", "==", "<", ">", "<=", ">=", "!="
        }

    def scan(self):
        tokens = []
        while self.position < self.length:
            ch = self.code[self.position]

            if ch.isspace():
                self.position += 1
                continue

            if ch == '/':
                token = self.check_comment()
                if token:
                    tokens.append(token)
                    continue

            if ch.isalpha() or ch == '_':
                token = self.check_identifier_or_keyword()
                tokens.append(token)
                continue

            if ch.isdigit():
                token = self.check_number()
                tokens.append(token)
                continue

            if ch == "'":
                token = self.check_char_constant()
                tokens.append(token)
                continue

            op = self.check_operator()
            if op:
                tokens.append(op)
                continue

            if ch in self.special_chars:
                tokens.append(Token("Special characters", ch))
                self.position += 1
                continue

            self.position += 1

        return tokens
    
    def check_identifier_or_keyword(self):
        start = self.position
        while (self.position < self.length and
               (self.code[self.position].isalnum() or self.code[self.position] == '_')):
            self.position += 1
        word = self.code[start:self.position]
        if word in self.keywords:
            return Token("Keywords", word)
        else:
            return Token("Identifiers", word)

    def check_number(self):
        start = self.position
        has_dot = False
        while self.position < self.length:
            c = self.code[self.position]
            if c.isdigit():
                self.position += 1
            elif c == '.' and not has_dot:
                has_dot = True
                self.position += 1
            else:
                break
        return Token("Numeric constants", self.code[start:self.position])

    def check_char_constant(self):
        start = self.position
        self.position += 1 

        if self.position < self.length and self.code[self.position] == '\\':
            self.position += 1
            if self.position < self.length:
                self.position += 1
        else:
            if self.position < self.length:
                self.position += 1

        if self.position < self.length and self.code[self.position] == "'":
            self.position += 1
        return Token("Character constants", self.code[start:self.position])

    def check_operator(self):
        for op in sorted(self.operators, key=lambda x: -len(x)):
            end = self.position + len(op)
            if self.code[self.position:end] == op:
                self.position = end
                return Token("Operators", op)
        return None

    def check_comment(self):
        if self.position + 1 < self.length and self.code[self.position + 1] == '/':
            start = self.position
            self.position += 2
            while self.position < self.length and self.code[self.position] != '\n':
                self.position += 1
            return Token("Comments", self.code[start:self.position])
        
        if self.position + 1 < self.length and self.code[self.position + 1] == '*':
            start = self.position
            self.position += 2
            while (self.position + 1 < self.length and
                   not (self.code[self.position] == '*' and self.code[self.position + 1] == '/')):
                self.position += 1

            if self.position + 1 < self.length:
                self.position += 2
            return Token("Comments", self.code[start:self.position])

        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scan.py <filename.c>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    scanner = Scanner(code)
    tokens = scanner.scan()

    print(f"{'Token Type':20} {'Lexeme'}")
    print("-" * 40)
    for token in tokens:
        print(token)
