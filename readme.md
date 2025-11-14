# Stroll
***"A lightweight Lisp dialect implemented in Python."***

---

## ⚙️ Introduction
Stroll is a small, extensible Lisp dialect written in Python.
It’s designed to be simple, approachable, and ideal for learning, experimenting, and contributing.
Whether you’re new to Lisp or exploring interpreter design, Stroll provides a friendly environment to build and grow with the language.



If you’re new to Lisp, check out our  [introductory guide](https://en.wikipedia.org/wiki/Lisp_(programming_language)).

---

## 🧩 Features
Here are some of the things **Stroll** currently has to offer!:

### 🧮 Math & Comparisons:
- Basic arithmetic: `+`, `-`, `*`, `/`
- Comparison operators: `>`, `<`, `>=`, `<=`, `==`, `!=`
- Additional math functions: `mod`, `pow`, `sqrt`, `abs`  *(some untested)*

### 📦 Data & Collections:
- Variables: `let` to store values
- Lists: `list` to make lists, `append` to add elements
- List utilities: `len`, `reverse`, `index` to manage elements 

### 🔤 Strings & Text:
- Create strings using quotes
- String functions: `concat`, `strlen`, `substr`  *(some untested)*

### 🔁 Control Flow:
- Conditionals: `if`, `elif`, `else` (syntax differs from traditional Lisp — see docs)
- Loops: `while` loops
- Logic values & operators: `&` (and), `|` (or), `true`, `false`

### 🖨️ Input/Output:
- Print to console: `print`
- Read input: `scan`

###  👨‍💻 User defined functions:
- Define function with `fn`
- Set passed in arguments: `argone|argtwo|argthree`
- Call functions using `call`: call a user defined function

###  Quick Example:

```
(+ 1 2)

(let x 10)
(print x)

(fn square |argone| (* argone argone))
(call square 6)
```

---

## 🎯 Goals
We’re aiming for:
1. **Feature progression** — rapid growth and iteration  
2. **Good documentation** — clear, complete, and beginner-friendly  
3. **Open contributions** — an inviting community for all contributors  
4. **Clean code** — readable and structured

---

 ## 🤝 Contributing
 Interested in **Stroll** and want to help it grow?

 We welcome contributions of all kinds!
To get started, please review the contributing guide and explore open issues [contributing guide](docs/contributing.md) to get started! 

If you’d like to add features, improve documentation, or help refine the interpreter, your contributions are appreciated.



---
