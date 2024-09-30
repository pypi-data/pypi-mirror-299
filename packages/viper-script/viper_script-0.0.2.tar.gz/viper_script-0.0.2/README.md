# ParselTongue Programming Language

ParselTongue is a simple, lightweight programming language built with the goal of providing an easy-to-understand syntax and a streamlined programming experience. It is ideal for both beginners learning how to code and advanced users who want to explore new concepts or experiment with programmatic logic in a clean, minimal environment.

**Core Philosophy**

The core philosophy behind ParselTongue is simplicity and accessibility. It strips away the complexities often found in other languages, offering a more straightforward and intuitive syntax. This makes it especially suitable for educational purposes, allowing users to focus on problem-solving and logical thinking rather than the intricacies of the language itself.

**Designed for Learning and Experimentation**

ParselTongue was designed to be approachable, yet powerful enough to accommodate real-world programming tasks. It allows beginners to get started without being overwhelmed by complex syntax, while still offering enough features to keep advanced users engaged. By focusing on core programming constructs, it ensures that users can quickly grasp fundamental concepts such as loops, conditionals, and function calls.

**Why ParselTongue?**

- **Beginner-Friendly:** ParselTongue minimizes boilerplate code, making it easy to write and understand even for those new to programming. The language syntax is designed to be close to natural language, ensuring that newcomers can get started with minimal friction.

- **Experimentation-Ready:** For more advanced users or educators, ParselTongue offers a simple and flexible environment to experiment with programming logic. Its REPL (Read-Eval-Print Loop) allows users to immediately see the results of their code, fostering a rapid development and learning process.

- **Built-in Error Handling:** As a part of its user-friendly design, ParselTongue incorporates basic error handling. This helps developers quickly identify mistakes and learn how to correct them, further enhancing the learning experience.

**Current Status: Alpha Stage**
ParselTongue is currently in its alpha stage, meaning it's open for community testing and feedback. As an alpha release, the language already includes the essential programming constructs, but it will continue to evolve based on user input. We encourage users to try it out, report bugs, suggest new features, and share their experience so we can improve the language together.

This early stage is a great time for users to contribute to shaping ParselTongue into a robust and versatile programming language. As we move forward, we plan to introduce more features, expand functionality, and enhance the language’s capabilities based on the feedback we receive.

**The Vision**

ParselTongue aims to bridge the gap between learning and applying programming concepts. It’s not just a language but a learning tool designed to help users understand how code works without unnecessary complexity. In future iterations, we hope to make ParselTongue a full-fledged language for hobbyists, educators, and professionals alike.

Whether you’re just starting out or looking for a simple platform to prototype and explore, ParselTongue provides the tools you need to get coding quickly. We look forward to the community’s feedback and involvement as we continue developing this unique programming language.

## Installation
To install ParselTongue, you can use pip, the Python package manager. Run the command 

### Using pip
You can easily install ParselTongue using pip:

```bash
pip install parsel_tongue
```
After installation, you can start the REPL by running:

```bash 
parsel_tongue --repl
```

Or run a specific program by passing a file:

```bash
parsel_tongue path_to_your_file.pt
```

### From Source 
To install from source: 

1. Clone the repository using git: `git clone https://github.com/shiv3679/parsel_tongue`

2. Navigate to the directory:
```bash
cd parsel_tongue
```
3. Install the dependencies using pip:
```bash
pip install .
```

---
## Quick Start Guide

Once you've installed ParselTongue, follow these steps to get started with your first program:

1. **Open the REPL**:
   Run the following command in your terminal:
   ```bash
   parsel_tongue --repl
    ```
    This will open the REPL, where you can write and execute ParselTongue code.

2. **Write a Simple Program:**
In the REPL, type the following code and press Enter:
```bash
>> print "Hello, ParselTongue!"
```
This will print "Hello, ParselTongue!" to the console.
 
 3. **Declare Variables:**

 ```bash
 >> x = 10
>> print x
```

4. **If-Else Condition:**

```bash
>> if x > 5:
..    print "x is greater than 5"
.. else:
..    print "x is not greater than 5"
```

5. **Loops**
```bash
>> i = 0
>> while i < 3:
..    print i
..    i = i + 1
```

6. **Functions**
```bash
>> function greet(name):
..    print "Hello, " + name
>> greet("Alice")
```
## Language Features

### 1. Variables
In ParselTongue, variables are declared using `=`:
```bash
x = 10
y = 5
```
You can use variables in expressions:

```bash
sum = x + y
print sum
```

### 2. Conditionals

ParselTongue supports `if`,`else` statements:

```bash
if x > y:
    print "x is greater than y"
else:
    print "x is not greater than y"
```
### 3. Expressions

ParselTongue supports basic arithmetic expressions:

- `+` (Addition)
- `-` (Subtraction)
- `*` (Multiplication)
- `/` (Division)

## Contributing and Feedback

We welcome feedback and contributions from the community!

### Reporting Issues
If you find any bugs or have feature requests, please create an issue on our [GitHub Issues](https://github.com/shiv3679/parsel_tongue/issues) page.

### Contributing
If you'd like to contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature_branch`)
3. Make your changes
4. Submit a pull request

For more detailed guidelines, check our `CONTRIBUTING.md`.