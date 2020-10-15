---
title: "The Golden Age of New Programming Languages"
author: "poga"
date: 2019-11-03
tags:
  - Programming
categories:
  - Essays
---

2020 is going to be the golden age of new programming languages.

<!--more-->

---

For the longest time, creating and promoting new programming languages is impossible.

The new language needs to have good performance, which requires tremendous efforts to optimize your compiler.

The new language needs to have good editor support: syntax highlighting, auto-complete, and formatting.

If scientific programming is the target, you need to have good interactive programming support.

If security is the goal, you need to create a sandboxed virtual machine.

And most importantly, you need to provide benefit against existing language community, tooling, and culture.

---

Luckily, we have a better foundation than 30 years ago.

We have [LLVM](https://llvm.org/) and [MLIR](https://github.com/tensorflow/mlir), which give us a solid compiler backend and generate code with good performance.

We have [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), a standardized protocol for the communication between editors and developer tools. A single Language Server can be re-used in multiple development tools, which in turn can support multiple languages with minimal effort.

We have [The Jupyter Protocol](https://jupyter.org/). We can support millions of scientists, researchers with familiar interactive programming environment without reinventing everything.

Finally, we have [WebAssembly](https://webassembly.org/), which is designed to run insecure code inside everyone's browser and [edge data centers](https://webassembly.org/).

---

But still, why would people use our new language? **Because the landscape is different now.**

We have new problems: machine learning, differentiable programming, and software-defined network.

We have new hardware: GPU, TPU, and FPGAs.

We need more computing power, more developer, safer program, and friendlier culture. **The current paradigm is not enough.**



