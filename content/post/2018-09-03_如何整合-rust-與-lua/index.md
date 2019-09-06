---
title: "如何整合 Rust 與 Lua"
author: "poga"
date: 2018-09-03T23:30:04.764Z
lastmod: 2019-04-30T21:56:04+08:00

description: ""

subtitle: "在系統中遷入一個動態輕巧的 scripting language 一直是個常見的設計。像 Rust 這樣的系統語言，雖然效能好，但是上手門檻較高。這時若是能遷入一個像 Lua 一樣動態型別，簡單易懂的語言，便能大幅提高系統彈性。"
tags:
 - Rust
 - Lua
 - Actix

image: "/post/2018-09-03_如何整合-rust-與-lua/images/1.jpeg"
images:
 - "/post/2018-09-03_如何整合-rust-與-lua/images/1.jpeg"


aliases:
    - "/%E5%A6%82%E4%BD%95%E6%95%B4%E5%90%88-rust-%E8%88%87-lua-3cb38238dc72"
---

![image](/post/2018-09-03_如何整合-rust-與-lua/images/1.jpeg)

Photo by [Anders Jildén](https://unsplash.com/photos/4izt8TxQmEs?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/lua?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText)



在系統中遷入一個動態輕巧的 scripting language 一直是個常見的設計。像 [Rust](https://www.rust-lang.org/) 這樣的系統語言，雖然效能好，但是上手門檻較高。這時若是能遷入一個像 [Lua](https://www.lua.org/) 一樣動態型別，簡單易懂的語言，便能大幅提高系統彈性。

最近為了實做 [actix-lua](https://github.com/poga/actix-lua)，研究了一下 Rust 跟 Lua 之間的介接，順便學了不少 Rust 跟 Lua 的設計，筆記在此。

<!--more-->


#### Lua Binding 的選擇

Rust 現在有數套 Lua binding，比較常被人提到的是 [lua](https://crates.io/crates/lua), [hlua](https://github.com/tomaka/hlua) 與 [rlua](https://github.com/kyren/rlua) 。

[lua](https://crates.io/crates/lua) 基本上是直接把 Lua 的 C API 直接移植，沒有做多餘的包裝。所以需要絕對的效能的話，這可能是你的最佳選擇。不過安全性跟 UB 就要自己處理了。

[hlua](https://github.com/tomaka/hlua) 提供是比較高階的介面，不讓你直接存取 Lua Stack，可以視為 lua API 上的再一層包裝。彈性較低，可能不適合某些需求。

[rlua](https://github.com/kyren/rlua) 是由知名遊戲工作室 [chucklefish](https://blog.chucklefish.org/about/) 開發。延續 Rust 對安全性的要求，設計介面時也是以安全性為最高原則。在使用 rlua 的 API 時，不會產生任何 UB（由於 lua API 跟內部的運作方式，這種 API 真的很難做到…）也許犧牲了一點效能，不過對於 Rust 的使用者來說，這樣的 tradeoff 應該是蠻值得的。

最後我用的是 rlua。

#### 老問題：Lifetime &amp; ownership

剛開始用 rlua 的時候，很容易就撞到 lifetime 的問題。不過，就跟一般使用 Rust 一樣：如果遇到很難解的 lifetime 跟 ownership 問題，很可能架構設計上就錯了。

rlua 作者很詳盡的解釋了 rlua 許多的設計概念，也深入剖析了 Lua 本身設計帶來的影響。不過，這些解釋大多分散在各 github issue 之中。這邊稍微整理一下幾個重點：

1.  rlua 提供的所有的 reference type，像是 `Function`、 `Table` 這些指向 Lua 內部元素的參照，都不應該被另外存起來。
2.  rlua 提供的 reference type 也不應該被存到任何 Lua 內的 `userdata` 或是 Rust callback 之中。
3.  傳進 rlua 中的任何值都必須是 `Send` （因為 lua 本身是 `Send`）跟 `'static`（因為你沒辦法知道 Lua 何時會 GC 掉這些值，難以找出精確的 lifetime。）
4.  3 的限制讓傳值給 lua 變的複雜許多。rlua 提供了 `scope` API，可以用一個暫時的 scope 將不符合條件的值傳給 lua。傳過去的資料在 scope 結束後就會被銷毀，避免複雜的 lifetime 問題。

#### 最後的成果：actix-lua

[actix](https://actix.rs/) 是個 Rust 上的 actor framework，前陣子因為極高的效能而小有名氣。由於目前 Rust async/await 的支援還不算友善，actor model 算是能幫助簡化 async 程式的架構。

而 [actix-lua](https://github.com/poga/actix-lua) 便是將 actix 與 Lua 整合，讓人能用 Lua 實做系統中某些需要彈性、熱抽換、方便修改的部分。想法來自於 [openresty](https://openresty.org/en/) 這套整合 nginx 與 Lua 的軟體。目前主要被我用來處理即時資料的分析。

雖然寫的過程碰了蠻多壁，不過最後的成果我還算滿意。目前還在初步的階段，歡迎各種建議與回饋。
