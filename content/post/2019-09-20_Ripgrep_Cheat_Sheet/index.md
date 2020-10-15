---
title: "Ripgrep Cheat Sheet"
author: "poga"
date: 2019-09-20
tags:
  - Programming
  - Productivity
categories:
  - Notes
---

<!--more-->

Based on [the ripgrep user guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md) and [Ripgrep Cheatsheet](https://www.philipdaniels.com/blog/2019/ripgrep-cheatsheet/).

Syntax    | Description
--------|------
`rg -l clap`     | List matching files only
`rg -c clap`   | List matching files, including a count
`rg -i clap` | Search case-insensitively
`rg --no-filename clap` | Don’t print filenames
`rg -v clap` | Invert matching: show lines that do not match
`rg -c –sort path|modified|accessed|created clap` | Sort the results (`-sortr` to reverse)
`rg -g '*.c' clap` | Only search in `*.c` files (can use multiple `-g`)
`rg -g '!*.c' clap` | Search in everything but `*.c` files
`rg -e clap1 -e clap2` | Search for multiple patterns
`rg -z clap` | Search in gzip, bzip2, xz, LZ4, LZMA, Brotli and Zstd compressed files
`rg -trust -tconfig` | Search in file types `rust` and `config`
`rg -Tconfig`| **Don’t** search in file type config
`rg --type-add 'web:*.html' --type-add 'web:*.css' --type-add 'web:*.js' -tweb title` | Search with custom types
`rg fast README.md -r FAST` | Replace
`rg fast README.md -or FAST` | Replace the whole matching line
