---
title: "OCaml Quickstart"
author: "poga"
date: 2020-03-17
tags:
  - Programming
  - OCaml
categories:
  - Programming
---

![](/post/2020-03-17_ocaml_quickstart/vim.png)

[OCaml](https://ocaml.org/) is a great language. However, the tooling for newbies is kinda confusing. Here's a guide to setup a working OCaml development environment in [neovim](https://neovim.io/) on MacOS.

<!--more-->

### Install opam

```
$ brew install opam
```

### Install ocaml 4.09.0

```
$ opam switch create 4.09.0 4.09.0
# follow the instructions to setup bash env
```

### Install utop(REPL) and dune(build system)

```
$ opam install utop dune
```


### Setup editor

* Install [ocaml-lsp](https://github.com/ocaml/ocaml-lsp)
* Setup LSP in neovim with coc.nvim https://github.com/neoclide/coc.nvim/wiki/Language-servers

You need to install all dependencies (with dune) and build it once to get a working LSP.

### Build a project

Let's test our environment on an existing project.


```
$ git clone git@github.com:inhabitedtype/httpaf.git
$ cd httpaf

# install dependencies
$ opam pin add -n httpaf .
$ opam install --deps-only httpaf

# run tests
$ dune runtest
```
