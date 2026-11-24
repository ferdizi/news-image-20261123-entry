# news-image-20261123-entry

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/ferdizi/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/ferdizi/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One broadsheet front page (1024×1024 PNG) summing up the world's news of
**Monday 23 November 2026**: 35 stories across 7 regions, every one of them
happened or first reported that Monday. Masthead names the day in the largest
type on the page; three drawn hero panels lead with the day's biggest stories
(COP31 ends with no deal, Ukraine sinks the Russian corvette Merkury off
Libya, Jensen Huang is back as Nvidia CEO); a dotted world map pins the 7
regions; a red DATE CHECK box names the near-miss stories left out because
they happened on other days.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` draws `entry.png` from code (Pillow + system fonts) at build
time; `main.ts` only copies the committed image to `/output/entry.png`, so
both grader runs write identical bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qgr0hfw9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
