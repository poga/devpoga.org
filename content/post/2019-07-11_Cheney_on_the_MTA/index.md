---
title: "Cheney on the M.T.A"
author: "poga"
date: 2019-07-12
tags:
  - Programming Language
  - Compiler
categories:
  - Essays
---

如果問軟體工程師他覺得簡潔又經典的文章，我想很多人會回答你這篇：[Cheney on the M.T.A](http://home.pipeline.com/~hbaker1/CheneyMTA.html).

<!--more-->

---


[Scheme](https://en.wikipedia.org/wiki/Scheme_(programming_language))，史上最不 portable 的語言，有著各種千奇百怪的實作，每個實作的特點，支援的語法都有微妙的不同。

[CHICKEN](https://www.call-cc.org/) 是一個 scheme 的實作，是個 scheme-to-c 的編譯器，主打的特性很類似 Lua：簡單、可攜、容易擴充、容易嵌入至其他程式中。

像 scheme 這類 lisp 方言，很多的功能都依賴 recursion 跟高效能的尾遞回（tail-recursion）來達成。傳統上，尾遞回的實作是透過一種叫「trampoline」的架構來處理：讓一個外層函式呼叫內部的尾遞回函式，內部的尾遞回函式回傳他要遞回的下一個 function 的位址，讓外層函式不停呼叫。這樣的作法避免了遞回把 stack 撐爆的問題，卻也因為透過了 function pointer，讓效能變差，也讓參數傳遞變複雜。

CHICKEN 的特色之一是用了 [cheney on the MTA](http://home.pipeline.com/~hbaker1/CheneyMTA.html) 來實作 tail-recursive，作法是把尾遞回編譯成 CSP 形式的 C，讓每個 function 結束時主動呼叫他的 continuation，把尾遞回編譯成一個永不 `return` 的函式。另外，所有的值也全都放在 stack 上。

既然永遠不會 `return`，自然得處理 stack overflow 的問題。解法也蠻單純的，在 stack 快要爆炸的時候，直接 `setjmp`/`longjmp` 跳到下一個 continuation，清空 stack 的同時也清空了用過的值，順便成為了一種 generational garbage collector！

---

用一個方法同時處理 tail-recursion 跟 GC 真是相當漂亮啊。
