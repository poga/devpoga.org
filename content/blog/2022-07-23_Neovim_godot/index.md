---
title: "Developing Godot Projects with Neovim"
author: "poga"
date: 2022-07-23
tags:
  - Godot
  - Neovim
categories:
  - Blog
---

When I started using [Godot Engine](https://godotengine.org/), what surprised me the most is the built-in [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) support. Thank to it, I can easily develop [GDScript](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html) with all my customized vim configs.

## Setup

Install [`vim-godot`](https://github.com/habamax/vim-godot).

```
Plug 'habamax/vim-godot'
```

Install [`neovim-remote`](https://github.com/mhinz/neovim-remote).

```
pip3 install neovim-remote
```

Setup Neovim as the external editor for Godot

1. Open menu Editor/Editor Settings/ then navigate to General/External/:
2. Tick `Use external editor`
3. Set nvr to Exec Path, use `which nvr` to get the absolute path.
4. Add `--servername godothost --remote-send "<C-\><C-N>:n {file}<CR>:call cursor({line},{col})<CR>"` to Exec Flags

Start Neovim and listening to remote commands:

```
nvim --listen godothost .
```

now when you click on a script in godot it will open it in a new buffer in Neovim.

## That's all

💜


