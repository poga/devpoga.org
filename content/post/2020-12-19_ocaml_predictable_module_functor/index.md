---
title: "Predictable Performance of OCaml's Module System"
author: "poga"
date: 2020-12-19
tags:
  - OCaml
  - Compiler
  - Programming
  - Learn OCaml the Hard Way
categories:
  - Essays

summary: "![](/post/2020-12-19_ocaml_predictable_module_functor/camel.jpg) OCaml's [module system](https://dev.realworldocaml.org/files-modules-and-programs.html) can be a powerful tool for building generic code and structuring systems. Functors are functions from modules to modules and they server an important role for the power of module system. However, I want to know if functors (and the module system) can be optimized away by the OCaml compiler."
---

**[Learn OCaml the Hard Way](/tags/learn-ocaml-the-hard-way/) is a series about learning OCaml from the ground up:**

- [A taste of OCaml's predictable performance](/post/2020-11-21-a-taste-of-ocaml-predictable-performance/)
- [Going through the OCaml compiler pipeline (manually)](/post/2020-11-30-ocaml-compiler-pipeline/)
- [Predictable Performance of OCaml's module system](/post/2020-12-19_ocaml_predictable_module_functor/) **(You're here)**

---

![](/post/2020-12-19_ocaml_predictable_module_functor/camel.jpg)

OCaml's module system can be a powerful tool for building generic code and structuring systems. Functors are functions from modules to modules and they server an important role for the power of module system.

Some common usages of functors [are](https://dev.realworldocaml.org/functors.html):

- Dependency Injection
- Autoextension of Modules
- Instantiating modules with state

However, I want to know if functors (and the module system) can be optimized away by the OCaml compiler.

The following codes are compiled with OCaml 4.11.1 with [flambda](https://caml.inria.fr/pub/docs/manual-ocaml/flambda.html) enabled, running on [Compiler Explorer](https://godbolt.org/).

---

## Modules

First, I wonder if a simple module layer can break OCaml's claim of predictable performance. Here's a trivial function to compare two strings:

```ocaml
let eq x y =
  compare x y
(* camlExample__eq_29:
        subq    $8, %rsp
        movq    %rax, %rdi
        movq    %rbx, %rsi
        movq    caml_compare@GOTPCREL(%rip), %rax
        call    caml_c_call@PLT
.L100:
        movq    (%r14), %r15
        addq    $8, %rsp
        ret *)
```

If we wrap the type and the `compare` function with a module `ID`, the compiler still product the same assembly:

```ocaml
module type ID = sig
    type t
    val (=): t -> t -> int
end

module StringID = struct
    type t = string
    let (=) = compare
end

module Username: ID = StringID

let eqUser x y =
    Username.(=) x y

(* camlExample__eqUser_48:
        subq    $8, %rsp
        movq    %rax, %rdi
        movq    %rbx, %rsi
        movq    caml_compare@GOTPCREL(%rip), %rax
        call    caml_c_call@PLT
.L104:
        movq    (%r14), %r15
        addq    $8, %rsp
        ret *)
```

In this example, we put the actual implementation of comparing two string behind a module `ID` and its implementation `StringID`.

We can see that the compiler removed all module infomations and produced exact same assembly for `eqUser` and `eq`. Quite impressive!

---

## Functors

The above example is way too trivial, what if we try some functors?

Here's a functor example copied from [Real world's OCaml](https://dev.realworldocaml.org/functors.html):

```ocaml
module type JustAnInt = sig
    val x: int
end

(* a functor which takes a JustAnInt and return a JustAnInt *)
module Increment (M: JustAnInt) : JustAnInt = struct
    let x = M.x + 1
end

let inc x =
    x + 1

(* camlExample__inc_71:
        addq    $2, %rax
        ret
        *)

module One = struct
    let x = 1
end

module Two = Increment(One)

let add_two y =
    Two.x + y

(* camlExample__add_two_86:
        addq    $4, %rax
        ret
        *)
```

Here, we can see that the `add_two` function (which operate on top of a functor `Increment`) produces the same assembly as a trivial `inc` function.

---

The above examples are trivial but build up my confidence to OCaml's predictable performance. I guess the simplicity of OCaml's syntax and semantics helped the compiler a lot?

---

## References

- [Files, Modules, and Programs](https://dev.realworldocaml.org/files-modules-and-programs.html)
- [Functors](https://dev.realworldocaml.org/functors.html)

<span>Photo by <a href="https://unsplash.com/@iaminbaltal?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Inbal Malca</a> on <a href="https://unsplash.com/@iaminbaltal?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText">Unsplash</a></span>

---

Like this post? [Subscribe](https://learnocamlthehardway.substack.com/welcome) to **Learn OCaml the Hard Way** to get more!
