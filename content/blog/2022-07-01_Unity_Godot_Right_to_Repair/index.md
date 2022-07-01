---
title: "Unity, Godot, and Right to Repair"
author: "poga"
date: 2022-07-01
tags:
  - Unity
  - Godot
  - Opensource
categories:
  - Blog
---

Some years ago, [Unity](https://unity.com/) dominated the game engine market. Everyone would recommend Unity to fellow game developers [without needing to think](https://alextardif.com/LearningGraphics.html).

However, Unity (as a game engine) is [**not in a great shape**](https://garry.blog/unity-2022/) right now:

- Deprecating features while the replacement isn’t ready,
- Creating multiple new implementations of features from scratch instead of improving what’s there.
- Abandoning their own features in favour of acquiring community made versions, and then abandoning them,
- Splitting the whole render system into two incompatible, contrary versions, deprecating the previous render system.
- Splitting the UI system into two/three and trying to use them all at the same time,
- ...and the worst: shutting down Unity Answers and redirecting it to the Unity Forums. (Although [they walked back the decision](https://forum.unity.com/threads/unity-answers-shutdown-canceled.1293360/))

It's pretty obvious that Unity (as a company) are **oblivious about their product and their customer**. The stock price and shareholders' value becomes more important than game developers.

## Is Godot an alternative?

[Godot](https://godotengine.org/) is an open-sourced game engine with a permissive license (MIT). No strings attached, no royalties, nothing. Your game is yours, down to the last line of engine code.

Right now, Godot might not be able to compete with the convenience of [Unity Asset Store](https://assetstore.unity.com/). It's already a solid foundation for hobbists, 2d games, or [advanced GUI applications](https://medium.com/swlh/what-makes-godot-engine-great-for-advance-gui-applications-b1cfb941df3b).

## Right to Repair

But the biggest benefit of using Godot (or any open-sourced game engine) is about the [Right to Repair](https://en.wikipedia.org/wiki/Right_to_repair). Without engine source code, you are not in control of your own game. One apple policy change can [put you in a rough spot](https://9to5mac.com/2022/04/24/apple-now-removing-outdated-apps-from-the-app-store-developers-complain/) and remove your creation from the storefront.

**Open source game engines allows you to actually "finish" your game.** Unlike most software projects, games are something that can be "finished". You might think the game is good enough as it is, and can be called "done".  But if you don't control the engine. One day you won't be able to reproduce the game again.

[If you start seeing open-source as "right-to-repair", any frustration or entitlement you feel will be replaced with gratitude](https://twitter.com/adamwathan/status/1535989815778463746). It's better for  both the maintainer and for you.

I'm using Godot for my creative works and so far it's an enjoyable experience. I'm a software developer who's taking a break from startups and products to work on something I love. Knowing that I can put my hand on the whole stack of rendering pipeline and tweak the engine if I need to  is liberating.
