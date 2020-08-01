---
title: "在 iPad 上布置軟體開發環境"
author: "poga"
date: 2020-08-01
tags:
  - iPad
  - Programming
categories:
  - Programming
---

五月買了 [iPad Pro](https://www.apple.com/tw/ipad-pro/) 跟 [巧控鍵盤](https://www.apple.com/tw/ipad-keyboards/) 後，大部分的需求 iPad Pro 都能直接滿足，除了寫程式以外。摸索了一陣子之後總算找到順手又省錢的寫程式方式了，這篇簡單記錄一下。

<!--more-->

### 基地

首先準備一台便宜的 VPS，我原本就有一台 [Digital Ocean](https://www.digitalocean.com/) $5/m 的小機器用來掛 IRC，跑各式 cronjob，正好作為基地使用。

iPad 透過 [Blink Shell](https://blink.sh/)，靠著 [mosh-server](https://mosh.org/) 的威能永遠掛在基地上，隨時打開就能用，不用重新登入。

### Development environment

$5 的小機器自然是不夠拿來寫程式，也沒辦法編譯一些肥大的專案（像是 LLVM）。

我把整個開發環境包進 Docker container，需要的時候從 Base 跑個 script 透過 [doctl](https://github.com/digitalocean/doctl) 在 Digital Ocean Tokyo 開台 CPU-optimized, 4vCPU, 8G RAM 的機器起來用，小時計費每小時只要 $0.119。

Docker container 裡面就是標準的 [tmux](https://github.com/tmux/tmux)、[Neovim](https://neovim.io/)、跟各種編譯開發工具。啟動完成後直接從基地跳過去開發機。

iPad 上 Shell 用起來長這樣：

![](/post/2020-08-01_ipad_programming_environment/shell.png)

東京的 DO 機房平常 ping 大概 50ms，用起來算是順暢。

### Worker

有些工作（像是編譯 LLVM...）對於 8G RAM 的小機器來說負擔還是太重，這些工作我另外寫了 script 去開更強力的機器起來跑。

經過一番調查，最後選的是 [Hetzner cloud](https://www.hetzner.com/cloud)，德國機房的 CCX31。規格是 dedicate vCPU(AMD Epyc), 8vCPU, 32G ram，除了 ping 較高（~300ms）所以不太適合平常使用之外，拿來跑程式綽綽有餘。價錢更是每小時只要 $0.12！

### 其他

原本有想說用 kubernetes 或是 nomad 來管環境。實驗後覺得直接寫 script 最簡單也最省錢。

另外也試過用 terraform 開 aws spot instances 來用，最後算算價錢而言差不多，又多了一堆麻煩，就直接用單純的 VPS 了。

現在沒事就開台機器起來編 LLVM 相當愉快（？）
