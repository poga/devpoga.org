---
author: "Poga Po"
date: 2018-10-12
linktitle: Analyze Streaming Data with Rust, Actix, and Lua
title: Analyze Streaming Data with Rust, Actix, and Lua
slug: parsing-streaming-data-actix-lua
tags:
  - rust
  - lua
  - actix
categories:
  - Programming
---

[`actix-lua`](https://github.com/poga/actix-lua) provides a safe scripting environment for the [actix](http://actix.rs) framework with the [Lua Programming Language](http://lua.org).

I want to share one of my use-case here to demostrate why you might need it. Hope you can try these ideas in your next project.

### Definitely not a world-changing project

[Path of Exile(PoE)](https://pathofexile.com) is an online multiplayer RPG. In PoE, players get powerful, unique items by killing monsters. Then, they put their items to the market and trade with others.

![Path of Exile Logo](/poe-logo.jpeg)

I was an avid player of the game. I spent hundreds of hours building my character, learning from other players, and trying to improve my efficiency. But I'm still nowhere near the top players. They are on a whole different level, and how they do it is mostly their trade secret.

### Revealing secrets via data processing

How do I reveal their secret? I want to know what item they're trading and how do they make profits. Fortunately, PoE provides a [public API](https://pathofexile.gamepedia.com/Public_stash_tab_API) about the items on the market.

Understanding a virtual market in a video game won't make me money (other than some virtual bucks). But hey, it's fun.

PoE has lots of players. The amount of items they put to the market is huge. And more importantly, **I don't know what I'm looking for.** I'm exploring the live data as it comes in, looking for interesting patterns, and learn from it.

### Asynchronous programming and Actor model

The task has two parts: reading the data and analyzing it. Reading the data is mostly IO-bound. It takes about 3 seconds to get a 5MB response from the API endpoint. By using an asynchronous model, we can delegate the IO to the OS, and process the data while we're waiting for the next batch of data, without resorting to multi-threading!

Actix is an actor framework that simplifies asynchronous programming. Actor model helps us design the control-flow of our program, and we can focus on the data-flow.

A control-flow is a program's order of execution. When writing an async program, it's easy to get lost in callbacks and futures. By using actors, we can separate different parts of the control-flow into different actors:

* an actor to bootstrap the program, fetch the latest "offset" from a 3rd-party API and begin our processing.
* an actor to poll the API with a specified offset, send the response to the processing actor, then poll the next offset.
* an actor to process the data with Lua scripts.

So, each actor only has its own simple control-flow. It's much easier to understand than multiple tangled futures.

### Exploring the data with the power of dynamic languages

So, what does Lua really gives us? By using Lua, we can write scripts like this:

{{< highlight Lua>}}
for i, item in pairs(data["items"]) do
    -- looking for an item called "Belly of the Beast"
    if string.find(item["name"], "Belly of the Beast") then
        -- print the seller's account and the price
        print(data["accountName"], item["note"])
    end
end
{{< / highlight >}}

Instead of figuring out types and fighting borrow checkers, we can express our idea in a simple language.

We can also change the script while the program is running! **We can explore the data WHILE PROCESSING THE DATA**, which is tremendously useful.

To achieve hot-reload, you need only four lines of codes thanks to the dynamic nature of Lua.

{{< highlight Lua>}}
-- assume -1 is the signal to reload lua scripts
if ctx.msg == -1 then
  -- remove "handler" package from cache
  -- next require will load the script from disk instead of cache
  package.loaded["handler"] = nil
end

-- load the package from disk or cache
local handler = require("handler")
{{< / highlight >}}

### Then I stopped playing the video game

It turns out that writing Rust and Lua is more fun than actually playing the video game. I'm really happy with [`actix-lua`](https://github.com/poga/actix-lua). I believe there's potential for the crate and I'm excited to explore it!

If you're interested, [Here's the full example mentioned in this post](https://github.com/poga/streaming-data-parsing-with-actix-lua).
