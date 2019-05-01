---
title: "萬事萬物皆是 LOG — 參考資料"
author: "poga"
date: 2016-08-27T05:06:01.256Z
lastmod: 2019-04-30T21:55:51+08:00

subtitle: "這是 COSCUP 2016 的講題的延伸參考資料"
tags:
 - Coscup
 - 科普
 - 系統架構
 - Log

---


之前在 COSCUP 2016 榮幸講了一場 [萬事萬物皆是 Log — 系統架構也來點科普](https://devpoga.org/post/2016-08-20_%E8%90%AC%E4%BA%8B%E8%90%AC%E7%89%A9%E7%9A%86%E6%98%AF-log-%E7%B3%BB%E7%B5%B1%E6%9E%B6%E6%A7%8B%E4%B9%9F%E4%BE%86%E9%BB%9E%E7%A7%91%E6%99%AE/)。結束後被詢問有沒有一些靈感來源、延伸讀物、參考資料等等，這裡就把我有記下來的參考資料整理在此。一些時間關係沒有帶到的主題就也一起放在這了。

* Linkedin 工程師寫的關於 LOG 架構的長篇好文，強烈推薦閱讀。
https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying

* Microservice:
http://blog.christianposta.com/microservices/the-hardest-part-about-microservices-data/
http://blog.christianposta.com/microservices/why-microservices-should-be-event-driven-autonomy-vs-authority/

* 講 Apache Samza 如何用 LOG 整個拆解掉 Database。很精彩，大推薦！
http://www.confluent.io/blog/turning-the-database-inside-out-with-apache-samza/

* Stream Processing：
Spark: https://spark.apache.org/
Storm: https://storm.apache.org/
Kafka: https://kafka.apache.org/

* Immutable Database — Datomic: http://www.datomic.com/rationale.html

* Lamport Timestamp：所有對分散式系統有興趣的人都一定要瞭解一下。
http://www.goodmath.org/blog/2016/03/16/time-in-distributed-systems-lamport-timestamps/

* CRDT：這也是我最近很有興趣的主題，條列一些參考資料在此。
https://swarmjs.github.io/articles/papoc/

* A comprehensive study of Convergent and Commutative Replicated Data Types: http://hal.upmc.fr/inria-00555588/document
http://underscore.io/blog/posts/2013/12/20/crdts-for-fun-and-eventual-profit.html

* Google Spanner：
https://static.googleusercontent.com/external_content/untrusted_dlcp/research.google.com/en/us/archive/spanner-osdi2012.pdf

* Martin 大叔介紹的 Event Sourcing 架構 http://martinfowler.com/eaaDev/EventSourcing.html
An Introduction to Distributed System
https://github.com/aphyr/distsys-class

* Lambda/Kappa Architecture
https://www.oreilly.com/ideas/questioning-the-lambda-architecture
http://milinda.pathirage.org/kappa-architecture.com/

* Consistent Hashing/CAP/Merkle Tree 三個分散式系統常見元素的系列介紹文：
https://loveforprogramming.quora.com/Distributed-Systems-Part-1-A-peek-into-consistent-hashing
https://loveforprogramming.quora.com/Distributed-Systems-Part-2-Consistency-versus-Availability-A-Pragmatic-Examplehttps://loveforprogramming.quora.com/Distributed-Systems-Part-3-Managing-Anti-Entropy-using-Merkle-Trees

* 最後又一個集大成文… WHAT WE TALK ABOUT WHEN WE TALK ABOUT DISTRIBUTED SYSTEMS
https://videlalvaro.github.io/2015/12/learning-about-distributed-systems.html

對任何主題有興趣的話都歡迎來討論 XD

