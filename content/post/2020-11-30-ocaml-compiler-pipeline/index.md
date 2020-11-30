---
title: "Going through the OCaml compiler pipeline (manually)"
author: "poga"
date: 2020-11-30
tags:
  - OCaml
  - Compiler
  - Programming
  - Learn OCaml the Hard Way
categories:
  - Essays
---

Modern compilers usually composed by multiple stages: parsers, optimizers, linkers, and assemblers. Here's the OCaml's compilation pipeline:

![](/post/2020-11-30-ocaml-compiler-pipeline/ocaml-pipeline.png)

<!--more-->

source: https://dev.realworldocaml.org/compiler-frontend.html

From Real World OCaml:

> Each source file represents a _compilation unit_ that is built separately. The compiler generates intermediate files with different filename extensions to use as it advances through the compilation stages. The linker takes a collection of compiled units and produces a standalone executable or library archive that can be reused by other applications.

We can easily go through intermediate representations via poking into these files.

---

## Abstract Syntax Tree (AST)

OCaml's metaprogramming ability relies on manipulating ASTs (Parsetrees). [ppx_tools](https://github.com/ocaml-ppx/ppx_tools) is a set of tools for people who want to write programs with such ability. We can use it to obtain the AST of a source code.

Assume we have the following OCaml code:

```ocaml
type t = | Alice | Bob | Charlie | David

let test v =
  match v with
  | Alice   -> 100
  | Bob     -> 101
  | Charlie -> 102
  | David   -> 103
```

We can get the AST of it via the following command:

```bash
$ $ ocamlfind ppx_tools/dumpast t.ml
t.ml
==>
[{pstr_desc =
   Pstr_type (Recursive,
    [{ptype_name = {txt = "t"}; ptype_params = []; ptype_cstrs = [];
      ptype_kind =
       Ptype_variant
        [{pcd_name = {txt = "Alice"}; pcd_args = Pcstr_tuple [];
          pcd_res = None};
         {pcd_name = {txt = "Bob"}; pcd_args = Pcstr_tuple [];
          pcd_res = None};
         {pcd_name = {txt = "Charlie"}; pcd_args = Pcstr_tuple [];
          pcd_res = None};
         {pcd_name = {txt = "David"}; pcd_args = Pcstr_tuple [];
          pcd_res = None}];
      ptype_private = Public; ptype_manifest = None}])};
 {pstr_desc =
   Pstr_value (Nonrecursive,
    [{pvb_pat = {ppat_desc = Ppat_var {txt = "test"}; ppat_loc_stack = []};
      pvb_expr =
       {pexp_desc =
         Pexp_fun (Nolabel, None,
          {ppat_desc = Ppat_var {txt = "v"}; ppat_loc_stack = []},
          {pexp_desc =
            Pexp_match
             ({pexp_desc = Pexp_ident {txt = Lident "v"};
               pexp_loc_stack = []},
             [{pc_lhs =
                {ppat_desc = Ppat_construct ({txt = Lident "Alice"}, None);
                 ppat_loc_stack = []};
               pc_guard = None;
               pc_rhs =
                {pexp_desc = Pexp_constant (Pconst_integer ("100", None));
                 pexp_loc_stack = []}};
              {pc_lhs =
                {ppat_desc = Ppat_construct ({txt = Lident "Bob"}, None);
                 ppat_loc_stack = []};
               pc_guard = None;
               pc_rhs =
                {pexp_desc = Pexp_constant (Pconst_integer ("101", None));
                 pexp_loc_stack = []}};
              {pc_lhs =
                {ppat_desc = Ppat_construct ({txt = Lident "Charlie"}, None);
                 ppat_loc_stack = []};
               pc_guard = None;
               pc_rhs =
                {pexp_desc = Pexp_constant (Pconst_integer ("102", None));
                 pexp_loc_stack = []}};
              {pc_lhs =
                {ppat_desc = Ppat_construct ({txt = Lident "David"}, None);
                 ppat_loc_stack = []};
               pc_guard = None;
               pc_rhs =
                {pexp_desc = Pexp_constant (Pconst_integer ("103", None));
                 pexp_loc_stack = []}}]);
           pexp_loc_stack = []});
        pexp_loc_stack = []}}])}]
=========
```

The output is pretty straight forward. The [Parsetree documentation](https://caml.inria.fr/pub/docs/manual-ocaml/compilerlibref/Parsetree.html) is a good reference to understand it.

---

## Typedtree

For the simplicity of the article, we will skip the detail of type inferencing and checking here. They will (hopefully) be explained in the future.

---

## Lambda

The first code generation phase in the OCaml pipeline is to create a **Lambda Form**. Lambda form discards higher-level constructs such as modules, pattern matching, and objects.

- Modules and objects are replaced with records and function pointers.
- Pattern Matchings are compiled into optimized automatas.
- Block and values are mapped to [the runtime memory model](https://dev.realworldocaml.org/runtime-memory-layout.html#memory-representation-of-values).

We can obtain the lambda form via the following command:

```bash
$ ocamlc -dlambda -c t.ml
(setglobal T!
  (let
    (test/85 =
       (function v/87 : int
         (switch* v/87
          case int 0: 100
          case int 1: 101
          case int 2: 102
          case int 3: 103)))
    (makeblock 0 test/85)))
```

Lambda Form is **explicitly undocumented** and can change across compiler revisions.

For more detail, see [The Compiler Backend: Bytecode and Native code - Real World OCaml](https://dev.realworldocaml.org/compiler-backend.html).

We can generate both **bytecodes** and **native binaries** from the Lambda Form.

---

## Bytecode and `js_of_ocaml`

We can obtain the bytecode with the following command:

```bash
$ ocamlc -dinstr t.ml
	branch L2
L1:	acc 0
	switch 6 5 4 3/
L6:	const 100
	return 1
L5:	const 101
	return 1
L4:	const 102
	return 1
L3:	const 103
	return 1
L2:	closure L1, 0
	push
	acc 0
	makeblock 1, 0
	pop 1
	setglobal T!
```

The bytecode can be executed with `ocamlrun`, a portable interpreter for OCaml's bytecode.

The OCaml bytecode is based on a stack-based VM. The instruction set of the Caml Virtual Machine is documented [here](http://cadmium.x9c.fr/distrib/caml-instructions.pdf).

Since the OCaml bytecode is quite stable. We can generate a target-specified code (such as Javascript for the web) from it without recompiling any library.

- [`js_of_ocaml`](https://ocsigen.org/js_of_ocaml/) is a compiler from OCaml bytecode programs to Javascript.
- [Caramel](https://github.com/AbstractMachinesLab/caramel) is an [Erlang](https://www.erlang.org/) backend to the OCaml compiler.

Here's a simple example of using `js_of_ocaml`:

```bash
$ ocamlfind ocamlc -package js_of_ocaml -package js_of_ocaml-ppx \
          -linkpkg -o t.byte t.ml
$ js_of_ocaml t.byte
```

---

## Native Compilation

Finally, we can generate native binaries with `ocamlopt t.ml`. You can get `ocamlopt` to output the assembly with the `-S` flag.

If we want the best performance (and we usually does). We should use the compiler with [flambda optimizers](https://caml.inria.fr/pub/docs/manual-ocaml/flambda.html). you can install a flambda-optimized OCaml with `opam switch`, such as:

```
$ opam switch create 4.11.1+flambda
```

---

## Extra: Top-level

The OCaml top-level supports loading both source code or bytecodes. To load a source code, use the `#mod_use` command. To load a bytecode, use `#load`.

---

## References

- [The OCaml Compiler Pipeline](https://sookocheff.com/post/ocaml/the-ocaml-compiler-pipeline/)
- [The Compiler Frontend: Parsing and Type Checking](https://dev.realworldocaml.org/compiler-frontend.html)
- [The Compiler Backend: Bytecode and Native code](https://dev.realworldocaml.org/compiler-backend.html)
- [An introduction to OCaml PPX ecosystem](https://tarides.com/blog/2019-05-09-an-introduction-to-ocaml-ppx-ecosystem)
