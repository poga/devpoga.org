---
author: "Poga Po"
date: 2019-04-29
linktitle: Go，七年後
title: Go，七年後
slug: golang-7-years-later
tags:
  - go
  - editor
  - Programming Languages
categories:
  - Programming
---

從[開始接觸 Go](https://blog.golang.org/go-version-1-is-released) 到現在也已經過了 7 年了啊... 最近又有機會拿出 Go 出來寫寫，隨手寫一下感受。

## 編輯器

`vim` 還是很好用。

這幾年微軟提出的 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 相當受到社群歡迎，也算是解決了程式語言跟編輯器社群長久以來的困境，成長相當快速。vim plugin 也跟風從 `vim-go` 換成基於 Language Server Protocol 的 [LanguageClient-neovim](https://github.com/autozimu/LanguageClient-neovim) 配上 [bingo](https://github.com/saibing/bingo)。有點小不穩但是功能算齊全。

tagbar 一樣是用 `gotags` 沒變

## Dependency Management

當年被這問題惹毛好幾次，2019 年的今天似乎 Go 社群終於要收斂到一個比較好的作法上了... 目前 go module 用起來有些陽春，有些怪異，不過堪用。

終於不用再處理 `GOPATH` 的鳥事了... 真是令人感動啊。

## Sync Map

當初堅持說不需要，最後還是提供 [sync.Map](https://golang.org/pkg/sync/#Map) 了嘛。

--

好像就這樣了。

雖然這語言還是有很多我不喜歡的地方，不過，一個語言可以經過這麼久都沒啥改變的堅持跟說服力，我也是相當欽佩。
