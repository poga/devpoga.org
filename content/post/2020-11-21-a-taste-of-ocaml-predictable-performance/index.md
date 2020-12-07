---
title: "A Taste of OCaml's Predictable Performance"
author: "poga"
date: 2020-11-21
tags:
  - OCaml
  - Compiler
  - Programming
  - Learn OCaml the Hard Way
categories:
  - Essays

summary: "![](/post/2020-11-21-a-taste-of-ocaml-predictable-performance/colour-logo.png) [eqaf](https://github.com/mirage/eqaf), a constant-time compare function implementation in [OCaml](https://ocaml.org/), is a great case to demonstrate the [predictable performance of OCaml's compiler](https://signalsandthreads.com/language-design/#0008401). Why?"
---

**[Learn OCaml the Hard Way](/tags/learn-ocaml-the-hard-way/) is a series about learning OCaml from the ground up:**

- [A taste of OCaml's predictable performance](/post/2020-11-21-a-taste-of-ocaml-predictable-performance/) **(You're here)**
- [Going through the OCaml compiler pipeline (manually)](/post/2020-11-30-ocaml-compiler-pipeline/)

---

![](/post/2020-11-21-a-taste-of-ocaml-predictable-performance/colour-logo.png)

[eqaf](https://github.com/mirage/eqaf), a constant-time compare function implementation in [OCaml](https://ocaml.org/), is a great case to demonstrate the [predictable performance of OCaml's compiler](https://signalsandthreads.com/language-design/#0008401). Why?

- The goal of a constant-time compare function is to avoid [timing attacks](https://en.wikipedia.org/wiki/Timing_attack), which requires fully deterministic and predictable runtime performance.
- Usually, cryptography functions are written in assembly to have total control of resulting binary and avoid unneeded optimization by the compiler.
- However, [eqaf](https://github.com/mirage/eqaf) showed us that you can write clean OCaml and get simple and predictable resulting assembly.

---

**This is the first issue of [Learn OCaml the Hard Way](https://learnocamlthehardway.substack.com/welcome). Subscribe to get notified when a new article is out.**

---

## About Garbage Collection

It's hard to have a stable runtime performance for languages that comes with a garbage collector. To have a predictable runtime performance characteristic in these languages, the following rules are usually required to be followed religiously:

- Avoid garbage collections by avoiding memory allocations.
- Avoid boxed values to generate assembly as low-level as possible.

Hence, the resulting code are usually unidiomatic and hard to maintain.

## Compiler Explorer

[Compiler Explorer](https://godbolt.org) is a handy tool for exploring compilers and its assembly output. It has built-in OCaml support and removes boilerplate automatically. I recommend you to test the following example with it.

---

## Code

Here’s the implementation of `eqaf`’s `equal`.

```ocaml
let[@inline] get x i = String.unsafe_get x i |> Char.code

external unsafe_get_int16 : string -> int -> int = "%caml_string_get16u"
let[@inline] get16 x i = unsafe_get_int16 x i

let equal ~ln a b =
  let l1 = ln asr 1 in
  let r = ref 0 in
  for i = 0 to pred l1 do r := !r lor (get16 a (i * 2) lxor get16 b (i * 2)) done ;
  for _ = 1 to ln land 1 do r := !r lor (get a (ln - 1) lxor get b (ln - 1)) done ;
  !r = 0

let equal a b =
  let al = String.length a in
  let bl = String.length b in
  if al <> bl
  then false
  else equal ~ln:al a b
```

Besides basic OCaml syntaxes[1], interesting bits in the example are:

- You can force OCaml to always inline a function via adding an attribute `[@inline]`
- `String.unsafe_get` works like `String.get` but without bound-checking. It's unsafe for most use-cases but it's used here to [avoid jumping to exception](https://github.com/mirage/eqaf/blob/master/lib/eqaf.ml#L3).
- OCaml provides a FFI `external` for [interfacing with C](https://caml.inria.fr/pub/docs/manual-ocaml/intfc.html). Here we use it to call a primitive function provided by OCaml's runtime `%caml_string_get16u`.

  - `external` is always unsafe and should be really take care about.
  - Primitives are not stable. For example: https://github.com/mirage/ocaml-base64/pull/36

- `n asr m` shifts `n` to the right by `m` bits. This is an arithmetic shift: the sign bit of `n` is replicated. The result is unspecified if `m < 0` or `m > Sys.int_size`.
- `ref` creates a [reference cell](https://dev.realworldocaml.org/imperative-programming.html) and allows in-place replacement with `:=`.
- `pred x` is `x - 1`.
- `lor`, `lxor`, and `land` are logical bit-wise `or`, `xor`, and `and`.

Although the OCaml code is quite low-level (and not very functional). It's still cleaner than most constant-time compare functions implemented in assembly.

## Read the asm

Here's the resulting assembly of the previous example, copied from the `eqaf` [source](https://github.com/mirage/eqaf/blob/master/lib/eqaf.ml). You can get the same output via [Compiler Explorer](https://godbolt.org).

```ocaml
let[@inline] get x i = String.unsafe_get x i |> Char.code
(* XXX(dinosaure): we use [unsafe_get] to avoid jump to exception:
        sarq    $1, %rbx
        movzbq  (%rax,%rbx), %rax
        leaq    1(%rax,%rax), %rax
        ret
*)
external unsafe_get_int16 : string -> int -> int = "%caml_string_get16u"
let[@inline] get16 x i = unsafe_get_int16 x i
(* XXX(dinosaure): same as [unsafe_get] but for [int16]:
        sarq    $1, %rbx
        movzwq  (%rax,%rbx), %rax
        leaq    1(%rax,%rax), %rax
        ret
*)
let equal ~ln a b =
  let l1 = ln asr 1 in
  (*
        sarq    $1, %rcx
        orq     $1, %rcx
  *)
  let r = ref 0 in
  (*
        movq    $1, %rdx
  *)
  for i = 0 to pred l1 do r := !r lor (get16 a (i * 2) lxor get16 b (i * 2)) done ;
  (*
        movq    $1, %rsi
        addq    $-2, %rcx
        cmpq    %rcx, %rsi
        jg      .L104
.L105:
        leaq    -1(%rsi,%rsi), %r8
        sarq    $1, %r8
        movzwq  (%rdi,%r8), %r9
        leaq    1(%r9,%r9), %r9
        movzwq  (%rbx,%r8), %r8
        leaq    1(%r8,%r8), %r8
     // [unsafe_get_int16 a i] and [unsafe_get_int6 b i]
        xorq    %r9, %r8
        orq     $1, %r8
        orq     %r8, %rdx
        movq    %rsi, %r8
        addq    $2, %rsi
        cmpq    %rcx, %r8
        jne     .L105
.L104:
  *)
  for _ = 1 to ln land 1 do r := !r lor (get a (ln - 1) lxor get b (ln - 1)) done ;
  (*
        movq    $3, %rsi
        movq    %rax, %rcx
        andq    $3, %rcx
        cmpq    %rcx, %rsi
        jg      .L102
.L103:
        movq    %rax, %r8
        addq    $-2, %r8
        sarq    $1, %r8
        movzbq  (%rdi,%r8), %r9
        leaq    1(%r9,%r9), %r9
        movzbq  (%rbx,%r8), %r8
        leaq    1(%r8,%r8), %r8
     // [unsafe_get a i] and [unsafe_get b i]
        xorq    %r9, %r8
        orq     $1, %r8
        orq     %r8, %rdx
        movq    %rsi, %r8
        addq    $2, %rsi
        cmpq    %rcx, %r8
        jne     .L103
.L102:
  *)
  !r = 0
(*
        cmpq    $1, %rdx
        sete    %al
        movzbq  %al, %rax
        leaq    1(%rax,%rax), %rax
        ret
*)
```

Each OCaml code is compiled to a cleanly separated section of assembly, The resulting assembly contains no garbage collection, no types information, and no advanced features but still pretty readable.

---

## Conclusion

`eqaf` allows us to have a basic understanding about OCaml's assembly output without inferences of GC, boxed values, and advanced syntaxes such as pattern matching. We will explore more in the future issues.

Like this post? [Subscribe](https://learnocamlthehardway.substack.com/welcome) to **Learn OCaml the Hard Way** to get more!

## References

1. For understanding OCaml's syntax (and everything OCaml), [Real World OCaml](https://dev.realworldocaml.org/) does way better job than I can.
