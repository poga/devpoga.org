---
title: "軟體設計模式 — Data-Oriented Design"
author: "poga"
date: 2018-07-16T06:19:38.744Z
lastmod: 2019-04-30T21:56:04+08:00

description: ""

subtitle: "遊戲開發對很多開發者來說是個陌生的領域。遊戲對於效能的極高要求跟規格的不確定性，產生出了許多特有的系統架構。Data-Oriented Design 便是個有趣的設計模式。"
tags:
 - 遊戲開發
 - 科普
 - 系統架構

image: "/post/2018-07-16_軟體設計模式-dataoriented-design/images/1.jpeg"
images:
 - "/post/2018-07-16_軟體設計模式-dataoriented-design/images/1.jpeg"


aliases:
    - "/data-oriented-design-9288178d3ea5"
---

![image](/post/2018-07-16_軟體設計模式-dataoriented-design/images/1.jpeg)

Photo by [Rebecca Oliver](https://unsplash.com/photos/BpqDaDxG48w?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/game?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText)



遊戲開發對很多開發者來說是個陌生的領域。遊戲對於效能的極高要求跟規格的不確定性，產生出了許多特有的系統架構。Data-Oriented Design 便是個有趣的設計模式。

相較於其他設計模式，Data-Oriented Design 深受硬體快取（cache）架構影響。對於現代的高度 pipeline、高速的 CPU 架構而言，資料的存取方式對效能有非常大的影響。比起 L1、L2 cache，對主記憶體的一次存取帶來的是數百倍的效能損耗。為了避免太過抽象，就用個實際的例子來解釋吧。

<!--more-->


假設我們的遊戲中有許多的球，每個球有顏色、位置、半徑等等資訊。對於學過物件導向的人而言，很可能直覺的設計成這樣：

```
class Ball {
 Point position;
 Color color;
 double radius;
}
```

這樣的作法很符合人對世界的理解：每個球是獨立的個體，有自己的屬性。

不過，如果遊戲中有數百萬個球在移動，這樣的作法的效能就不太好了。每個球的座標都經過物件導向的層層封裝，分散在記憶體四處，spatial locality 非常差，在更新的過程中產生了大量的 cache miss。

#### There’s no ball

如果採用 Data-Oriented Design 的話，作法會變成：

```
class Balls {
 vector<Point> positions;
 vector<Color> color;
 vector<double> radius;
}
```

於是我們的程式中不再有「獨立的球」這個設計存在，所謂的球，只是透過一個 index，含蓄的存在遊戲世界中。

這樣的作法，對人而言並不直覺，但是對硬體而言，效能好上許多。大多數的 vector 實做，都會將其中的內容放在一段連續的記憶體空間中。因此 spatial locality 很好，對 CPU 而言，他能很輕易的猜到接下來要存取的記憶體位址，省下許多猜錯而損失的 CPU cycle。

#### SoA 與 AoS

這兩種作法又分別被稱做 Array of Structs 跟 Structs of Arrays。前者是用一個陣列存放許多獨立的 struct（class），後者是用一個 struct（class）存放許多陣列。

實際開發時，很難臨時在這兩種模式中轉換。對程式而言，model 遊戲世界的方式完全不同。所以常常一開始用了直覺的 AoS 開發，發現效能不好，需要換成 SoA 時卻無從下手。遊戲開發在介面設計跟系統架構上，都有很多很經典的範例啊…
