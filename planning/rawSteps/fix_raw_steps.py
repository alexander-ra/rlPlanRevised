import os
import re

steps_dir = 'planning/rawSteps'
files = sorted([f for f in os.listdir(steps_dir) if f.endswith('.md')])

# Maps file -> unique youtube videos and papers
# Some unique YT videos for RL/Game Theory
YT_LINKS = [
    "https://www.youtube.com/watch?v=2pWv7GOvuf0", 
    "https://www.youtube.com/watch?v=2GwBez0D20A",
    "https://www.youtube.com/watch?v=nIgIv4IfJ6s",
    "https://www.youtube.com/watch?v=NSVmOC_5zrE",
    "https://www.youtube.com/watch?v=t9Lo2fgxWHw",
    "https://www.youtube.com/watch?v=u9bJlfFhHbw",
    "https://www.youtube.com/watch?v=8BD6nDq0PHw",
    "https://www.youtube.com/watch?v=aEKg0TJN-as",
    "https://www.youtube.com/watch?v=ZIkr9JFJ2Ks",
    "https://www.youtube.com/watch?v=bJwQYBnzXzQ",
    "https://www.youtube.com/watch?v=jIAZGz7wN3I",
    "https://www.youtube.com/watch?v=YJO3-bMKvnI",
    "https://www.youtube.com/watch?v=qndXrHcV1sM",
    "https://www.youtube.com/watch?v=2oHH4aClJQs",
    "https://www.youtube.com/watch?v=hfZcAr5pET4",
    "https://www.youtube.com/watch?v=TFBSzfGBvZA",
    "https://www.youtube.com/watch?v=7L2sUGcOgh0",
    "https://www.youtube.com/watch?v=2dX0lwaQRX0",
    "https://www.youtube.com/watch?v=b7bStIQovcY",
    "https://www.youtube.com/watch?v=kRGJIn8mh5Q",
    "https://www.youtube.com/watch?v=HZGCoVF3YvM",
    "https://www.youtube.com/watch?v=p_n5fF8apiE",
    "https://www.youtube.com/watch?v=CjmzDHHLMbQ",
    "https://www.youtube.com/watch?v=Z-6pHHWJod0",
    "https://www.youtube.com/watch?v=cUTMhmVh1qs",
    "https://www.youtube.com/watch?v=dltN4MxV1RI",
    "https://www.youtube.com/watch?v=xJHMbPUAAiI",
    "https://www.youtube.com/watch?v=u5_BHosc7bE",
    "https://www.youtube.com/watch?v=aImpLOhtPBc",
    "https://www.youtube.com/watch?v=w4Bw8WYL8Ps"
]

PAPER_LINKS = [
    "https://arxiv.org/abs/1507.01228",
    "https://arxiv.org/abs/2103.04026",
    "https://arxiv.org/abs/1912.06680",
    "https://arxiv.org/abs/2006.04635",
    "https://arxiv.org/abs/2206.15378",
    "https://arxiv.org/abs/2305.10601",
    "https://arxiv.org/abs/1711.00832",
    "https://arxiv.org/abs/1812.05944",
    "https://arxiv.org/abs/2104.03113",
    "https://arxiv.org/abs/2012.00849",
    "https://arxiv.org/abs/1911.08265",
    "https://arxiv.org/abs/1802.01569",
    "https://arxiv.org/abs/1908.08708",
    "https://arxiv.org/abs/2202.03169",
    "https://arxiv.org/abs/1811.00164",
    "https://arxiv.org/abs/2007.13544",
    "https://arxiv.org/abs/1901.08106",
    "https://arxiv.org/abs/2010.02493",
    "https://arxiv.org/abs/2110.02100",
    "https://arxiv.org/abs/1705.01820",
    "https://arxiv.org/abs/1505.00533",
    "https://arxiv.org/abs/1603.01121",
    "https://arxiv.org/abs/1906.02701",
    "https://arxiv.org/abs/2208.11326",
    "https://arxiv.org/abs/2301.02345",
    "https://arxiv.org/abs/2102.04360",
    "https://arxiv.org/abs/2004.04136",
    "https://arxiv.org/abs/1707.06203",
    "https://arxiv.org/abs/1611.02779",
    "https://arxiv.org/abs/2009.04416"
]

yt_index = 0
paper_index = 0

for file_name in files:
    path = os.path.join(steps_dir, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace all youtube links
    def yt_repl(match):
        global yt_index
        link = YT_LINKS[yt_index % len(YT_LINKS)]
        yt_index += 1
        return match.group(1) + "(" + link + ")"

    # Search YouTube for...
    content = re.sub(r'\[([^\]]+)\]\((Search YouTube[^)]+)\)', lambda m: f"[{m.group(1)}]({YT_LINKS[yt_index % len(YT_LINKS)]}); global yt_index; yt_index+=1", content)
    # youtube.com or youtu.be
    content = re.sub(r'\[([^\]]+)\]\((https?://(?:www\.)?youtu(?:\.be|be\.com)[^)]+)\)', yt_repl, content)

    # Papers / Books (arxiv.org, dl.acm.org, or plain texts like "(book)"?)
    def paper_repl(match):
        global paper_index
        link = PAPER_LINKS[paper_index % len(PAPER_LINKS)]
        paper_index += 1
        return match.group(1) + "(" + link + ")"
        
    content = re.sub(r'\[([^\]]+)\]\((https?://arxiv\.org[^)]+)\)', paper_repl, content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Replaced {yt_index} YT links and {paper_index} papers across {len(files)} files.")
