"""Batch 2 storyboards (data-driven 'gx' diagrams). Run once: python3 scripts/make_batch2.py"""
import json
T = "#firsttimehomebuyer #newhomeowner #howitworks #homeownertips #homemaintenance #engineering"
END = {"type": "end", "dur": 3.6}
BOOK = {"type": "book", "text": "That’s one page of the manual your house didn’t come with", "accent": ["manual"], "size": 96, "book_h": 700,
        "chips": ["34 CHAPTERS", "PAPERBACK + KINDLE"], "voice": "That's one page of the manual your house didn't come with. If this was news to you, the rest of the book will be too."}
def S(text, voice, els, cam, accent=(), **kw):
    d = {"type": "diagram", "diagram": "gx", "state": {"els": els}, "text": text, "voice": voice, "cam": cam, "accent": list(accent)}; d.update(kw); return d
WHY = {
 "water-heater": ("When a tank finally rusts through, the water ends up on your floor. Know its age, and you replace it on your schedule.", "When a tank finally rusts through, the water ends up on your floor. Know its age, and you replace it on your schedule, not its schedule.", ["your", "schedule."]),
 "breaker": ("That switch is what stands between an overloaded wire and a fire inside your wall.", "That little switch is what stands between an overloaded wire, and a fire inside your wall. Know your panel before you need it in the dark.", ["fire"]),
 "running-toilet": ("The EPA says a running toilet can waste 200 gallons a day. That’s on your water bill.", "The E P A says a running toilet can waste two hundred gallons a day. That's on your water bill, for one inexpensive rubber part.", ["200", "gallons"]),
 "gutters": ("One inch of rain on a 1,000 sq ft roof is about 620 gallons. Gutters move it, or your foundation soaks it up.", "One inch of rain on a thousand square foot roof is about six hundred and twenty gallons. Either your gutters move it, or your foundation soaks it up.", ["620", "gallons."]),
 "frozen-pipes": ("Water damage and freezing claims average over $13,000. A dripping faucet costs pennies.", "Water damage and freezing insurance claims average over thirteen thousand dollars. A dripping faucet costs pennies.", ["$13,000."])}
def save(key, title, cover, cacc, hero, hero_t, scenes, cap, tag=""):
    w = WHY[key]; scenes = scenes + [{"type": "quote", "label": "WHY IT MATTERS", "text": w[0], "voice": w[1], "accent": w[2], "size": 80, "hold": .5}]
    v = {"slug": "house-x-how-it-works-" + key, "book": "house", "format": "X explainer", "title": title, "cover": cover, "cover_accent": cacc,
         "cover_sub": "How your house works", "hero": ["gx", hero], "hero_t": hero_t, "scenes": scenes + [BOOK, END], "caption": dict(cap, tags=T + tag)}
    json.dump(v, open(f"stories/{v['slug']}.json", "w"), indent=1, ensure_ascii=False)
L = lambda **k: k

# ---------------------------------------------------------------- water heater
TANK = [614, 414, 1226, 1426]
def wh(mid):
    return [L(k="line", pts=[[240, 1530], [1620, 1530]], c="dim", w=10), L(k="hatch", box=[240, 1536, 1620, 1600], c=[30, 48, 78], gap=30),
            L(k="rect", box=[380, 40, 520, 190], r=60, fill="panel", w=10), L(k="text", text="EXPANSION TANK", xy=[540, 60], c="dim", size=30), L(k="line", pts=[[450, 190], [450, 205]], w=14),
            L(k="pipe", pts=[[200, 220], [760, 220], [760, 420]], w=80, water="water"), L(k="pipe", pts=[[1080, 420], [1080, 220], [1700, 220]], w=80, water="hot"),
            L(k="circ", at_xy=[300, 220], r=40, fill="line", w=0), L(k="line", pts=[[300, 190], [300, 120], [370, 120]], c="yel", w=18),
            L(k="rect", box=[660, 1440, 710, 1486], fill="line", w=0, shadow=False), L(k="rect", box=[1130, 1440, 1180, 1486], fill="line", w=0, shadow=False),
            L(k="rect", box=[588, 388, 1252, 1452], r=70, fill=[18, 30, 50], w=0), L(k="hatch", box=[596, 470, 612, 1380], c=[90, 110, 140], gap=18), L(k="hatch", box=[1228, 470, 1244, 1380], c=[90, 110, 140], gap=18),
            L(k="level", box=TANK, c=[40, 110, 180], v0=1, v1=1)] + mid + [
            L(k="rect", box=[600, 400, 1240, 1440], r=60, w=16), L(k="rect", box=[624, 424, 1216, 1416], r=40, w=4, c="dim"),
            L(k="line", pts=[[760, 420], [760, 1250]], w=10), L(k="line", pts=[[745, 1250], [775, 1250]], w=10),
            L(k="bolts", pts=[[660, 400], [860, 400], [980, 400], [1180, 400]], c="line"),
            L(k="rect", box=[520, 1340, 600, 1400], fill="line", w=0), L(k="circ", at_xy=[520, 1370], r=26, fill="yel", w=0),
            L(k="rect", box=[1240, 520, 1310, 570], fill="line", w=0), L(k="line", pts=[[1310, 545], [1360, 545], [1360, 1430]], w=14), L(k="text", text="RELIEF VALVE", xy=[1384, 524], c="dim", size=30),
            L(k="rect", box=[1240, 1160, 1350, 1290], r=14, fill="panel", w=8), L(k="circ", at_xy=[1295, 1225], r=34, c="yel", w=8), L(k="line", pts=[[1295, 1225], [1315, 1203]], c="yel", w=8),
            L(k="text", text="THERMOSTAT", xy=[1384, 1200], c="dim", size=30), L(k="line", pts=[[1295, 1290], [1295, 1500], [1140, 1500]], c=[190, 160, 40], w=10),
            L(k="rect", box=[810, 560, 1030, 700], r=8, fill=[236, 230, 214], w=0), L(k="text", text="MFG DATE", xy=[920, 574], c="navy", size=28, center=True),
            L(k="line", pts=[[830, 630], [1010, 630]], c=[120, 120, 120], w=5), L(k="line", pts=[[830, 660], [960, 660]], c=[120, 120, 120], w=5),
            L(k="rect", box=[700, 1480, 1140, 1520], fill="line", w=0), L(k="text", text="COLD IN", xy=[210, 268], c="sky"), L(k="text", text="HOT OUT", xy=[1440, 268], c="hot")]
HOT = L(k="level", box=TANK, c="hot", dir="top", v0=.55, v1=.55)
save("water-heater", "How your water heater works, and what kills it", "What kills a water heater", ["kills"], 2, 3.0, [
    S("Your water heater sits in a corner doing its job, until the day it doesn’t.", "Your water heater sits in a corner doing its job, until the day it doesn't.",
      wh([]) + [L(k="label", text="WATER HEATER", xy=[1300, 640], anchor=[1244, 760], c="yel", at=.4, size=48)], [[0, .5, .5, 1.0], [1, .5, .52, 1.25]], ["doesn’t."]),
    S("Cold water goes down a tube to the bottom. A burner heats it, and the hot water rises to the top, ready for your shower.",
      "Cold water goes down a tube to the bottom. A burner heats it, and the hot water rises to the top, ready for your shower.",
      wh([L(k="level", box=TANK, c="hot", dir="top", v0=0, v1=.55, over=4, at=1.5)]) + [L(k="dots", pts=[[200, 220], [760, 220], [760, 1250]], c="ice", n=7, speed=420),
          L(k="flame", at_xy=[920, 1478], at=1.2), L(k="dots", pts=[[1080, 420], [1080, 220], [1700, 220]], c="white", n=4, speed=420, at=4)],
      [[0, .42, .2, 1.5], [.4, .45, .75, 1.5], [1, .5, .4, 1.3]], ["hot", "rises"]),
    S("Over the years, sediment settles at the bottom. It makes the heater work harder, and rumble.", "Over the years, sediment settles at the bottom. It makes the heater work harder, and rumble.",
      wh([HOT, L(k="level", box=TANK, c="brown", v0=0, v1=.1, over=3)]) + [L(k="flame", at_xy=[920, 1478]), L(k="hud", text="SEDIMENT BUILDING UP", c="red", at=1),
          L(k="label", text="SEDIMENT", xy=[1320, 1250], anchor=[1180, 1380], c="brown", at=1.2)], [[0, .5, .4, 1.3], [1, .52, .8, 1.7]], ["sediment"]),
    S("Inside, a metal rod sacrifices itself so the tank doesn’t rust. Having it checked every few years can add years to the tank.",
      "Inside, a metal rod sacrifices itself so the tank doesn't rust. Having it checked every few years can add years to the tank.",
      wh([HOT, L(k="level", box=TANK, c="brown", v0=.1, v1=.1), L(k="level", box=[935, 420, 965, 1050], c="line", dir="top", v0=1, v1=.35, over=4)]) +
      [L(k="label", text="ANODE ROD", xy=[1320, 560], anchor=[965, 520], c="yel", at=.5)], [[0, .52, .8, 1.7], [.3, .6, .4, 1.4], [1, .6, .42, 1.45]], ["rod"]),
    S("Tanks commonly last 8 to 12 years. Find the date on the sticker, and drain a few gallons from the bottom once a year.",
      "Tanks commonly last eight to twelve years. Find the date on the sticker, and drain a few gallons from the bottom once a year.",
      wh([HOT, L(k="level", box=TANK, c="brown", v0=.1, v1=.03, over=2, at=3)]) + [L(k="count", fmt="AGE: {:.0f} YRS", v0=1, v1=12, over=3, xy=[300, 800], center=True, c="white", size=64), L(k="ring", at_xy=[920, 630], r=150, c="yel", at=1.4, to=3.4),
          L(k="label", text="DRAIN VALVE", xy=[220, 1560], anchor=[540, 1400], c="yel", at=2.6), L(k="drops", at_xy=[510, 1400], c="water", n=8, spread=30, fall=300, at=3),
          L(k="hud", text="LASTS ABOUT 8 TO 12 YEARS", c="yel")], [[0, .5, .45, 1.3], [.55, .4, .78, 1.5], [1, .38, .8, 1.6]], ["8", "12", "years."], label="KEEP IT ALIVE", hold=.6)],
    {"hook": "Your water heater is aging quietly in a corner.", "feel": "It works until the day it doesn’t, and that day usually involves water on the floor.",
     "shows": "How a tank heater works, what sediment and rust do to it, and the yearly flush. If yours is old and has never been flushed, ask a plumber first.",
     "ask": "Do you know how old yours is?"}, " #plumbing101")

# ---------------------------------------------------------------- breaker
ROWS = [420 + i * 150 for i in range(6)]
def bk(wire, toggle, extra):
    e = [L(k="hatch", box=[660, 420, 1780, 620], c=[26, 44, 74], gap=44), L(k="text", text="INSIDE THE WALL", xy=[1500, 380], c="dim", size=32),
         L(k="line", pts=[[1060, 1190], [1780, 1190]], c="dim", w=10), L(k="hatch", box=[1060, 1196, 1780, 1250], c=[30, 48, 78], gap=30),
         L(k="rect", box=[140, 300, 640, 1340], r=30, fill="panel", w=16), L(k="rect", box=[168, 328, 612, 1312], r=18, w=4, c="dim"), L(k="text", text="BREAKER PANEL", xy=[390, 215], center=True),
         L(k="bolts", pts=[[190, 350], [590, 350], [190, 1290], [590, 1290]], c="line"), L(k="rect", box=[300, 345, 480, 395], r=8, fill="line", w=0, shadow=False), L(k="text", text="MAIN", xy=[390, 352], c="navy", size=28, center=True),
         L(k="rect", box=[1210, 780, 1290, 826], fill="line", w=0, shadow=False), L(k="rect", box=[1540, 780, 1620, 826], fill="line", w=0, shadow=False)]
    for i, nm in enumerate(("KITCHEN", "LAUNDRY", "BATH", "BEDROOM", "GARAGE", "LIVING")): e.append(L(k="text", text=nm, xy=[232, ROWS[i] + 30], c="dim", size=24))
    for i, y in enumerate(ROWS):
        e.append(L(k="rect", box=[220, y, 560, y + 90], w=8, r=10))
        if i != 2: e.append(L(k="rect", box=[400, y + 15, 520, y + 75], fill="dim", w=0, r=8))
    e += [L(k="rect", box=[1110, 820, 1390, 1180], r=30, w=14), L(k="text", text="SPACE HEATER", xy=[1250, 1205], center=True, size=40),
          L(k="rect", box=[1440, 820, 1720, 1180], r=30, w=14), L(k="text", text="HAIR DRYER", xy=[1580, 1205], center=True, size=40)]
    return e + wire + toggle + extra
def wire(c, w=20, **k): return [L(k="line", pts=[[640, 765], [1000, 765], [1000, 520], [1720, 520]], c=c, w=w, **k), L(k="line", pts=[[1250, 520], [1250, 820]], c=c, w=w, **k), L(k="line", pts=[[1580, 520], [1580, 820]], c=c, w=w, **k)]
ON = [L(k="rect", box=[400, 735, 520, 795], fill="yel", w=0, r=8)]
P1 = [[640, 765], [1000, 765], [1000, 520], [1250, 520], [1250, 820]]; P2 = [[640, 765], [1000, 765], [1000, 520], [1580, 520], [1580, 820]]
LIM = L(k="text", text="WIRE LIMIT: 15 A", xy=[1000, 215], center=True, c="sky")
H1 = L(k="rect", box=[1150, 880, 1350, 1120], fill="hot", w=0, r=16); H2 = L(k="rect", box=[1480, 880, 1680, 1120], fill="hot", w=0, r=16)
save("breaker", "What a breaker actually does", "Why the power cut out", ["cut"], 2, 2.5, [
    S("A breaker is a safety switch. Every circuit in your house has one.", "A breaker is a safety switch. Every circuit in your house has one.",
      bk(wire("line"), ON, [L(k="ring", at_xy=[460, 765], r=150, c="yel", at=.8)]), [[0, .5, .5, 1.0], [1, .22, .45, 1.8]], ["safety", "switch."]),
    S("Its wires can only carry so much current, safely.", "Its wires can only carry so much current, safely.",
      bk(wire("yel"), ON, [L(k="dots", pts=P1, c="white", n=6, speed=420), H1, LIM, L(k="count", fmt="{:.0f} A", v0=0, v1=12, over=1.5, xy=[1000, 300], center=True, c="yel", size=120)]),
      [[0, .22, .45, 1.8], [1, .62, .4, 1.3]], ["so", "much"], hold=.8),
    S("Run a space heater and a hair dryer on the same circuit, and it pulls more than the wires can carry.", "Run a space heater and a hair dryer on the same circuit, and it pulls more than the wires can carry.",
      bk(wire("red", 28), ON, [L(k="dots", pts=P1, c="white", n=6, speed=560), L(k="dots", pts=P2, c="white", n=6, speed=560), H1, H2, LIM,
          L(k="count", fmt="{:.0f} A", v0=12, v1=24, over=1.5, xy=[1000, 300], center=True, c="red", size=120), L(k="hud", text="WIRES OVERHEATING", c="red", at=1.2)]),
      [[0, .62, .4, 1.3], [1, .75, .5, 1.45]], ["more"]),
    S("So the breaker trips, and cuts the power before the wires overheat inside your walls.", "So the breaker trips, and cuts the power, before the wires overheat inside your walls.",
      bk(wire("red", 28, to=.6) + wire("dim", at=.6), [L(k="rect", box=[400, 735, 520, 795], fill="yel", w=0, r=8, to=.6), L(k="rect", box=[400, 735, 520, 795], box1=[340, 735, 460, 795], over=.25, fill="red", w=0, r=8, at=.6)],
         [LIM, L(k="text", text="24 A", xy=[1000, 300], center=True, c="red", size=120, to=.6), L(k="text", text="0 A", xy=[1000, 300], center=True, c="dim", size=120, at=.6),
          L(k="hud", text="TRIPPED: POWER CUT", c="green", at=.6), L(k="ring", at_xy=[400, 765], r=150, c="yel", at=1.2)]),
      [[0, .75, .5, 1.45], [.3, .22, .45, 1.9], [1, .22, .45, 1.9]], ["trips,"], hold=.8),
    S("To reset it, push it fully off first, then on. And move one thing to another circuit.", "To reset it, push it fully off first, then on. And move one thing to another circuit.",
      bk(wire("dim", to=2.6) + wire("yel", at=2.6), [L(k="rect", box=[340, 735, 460, 795], box1=[250, 735, 370, 795], over=.7, fill="red", w=0, r=8, at=.3, to=1.6),
          L(k="rect", box=[340, 735, 460, 795], fill="red", w=0, r=8, to=.3), L(k="rect", box=[250, 735, 370, 795], box1=[400, 735, 520, 795], over=.7, fill="yel", w=0, r=8, at=1.6)],
         [L(k="hud", text="OFF FIRST, THEN ON", c="yel"), L(k="hud", text="ONE BIG APPLIANCE PER CIRCUIT", c="green", at=2.6), L(k="dots", pts=P1, c="white", n=6, speed=420, at=2.6),
          L(k="rect", box=[1150, 880, 1350, 1120], fill="hot", w=0, r=16, at=2.6)]),
      [[0, .22, .45, 1.9], [.55, .22, .45, 1.9], [1, .5, .45, 1.1]], ["off", "first,"], label="THE FIX", hold=1.0),
    S("A breaker that keeps tripping is telling you something. The answer is never a bigger breaker.", "A breaker that keeps tripping is telling you something. The answer is never a bigger breaker.",
      bk(wire("yel"), ON, [L(k="dots", pts=P1, c="white", n=6, speed=420), H1, L(k="hud", text="NEVER A BIGGER BREAKER", c="red")]), [[0, .5, .45, 1.1], [1, .22, .45, 1.6]], ["never"], label="ONE RULE")],
    {"hook": "A tripped breaker isn’t the problem.", "feel": "It’s the thing protecting you from the problem.",
     "shows": "What a breaker does, why a heater plus a hair dryer trips it, and how to reset it properly.", "ask": "Which two appliances always trip yours?"}, " #electrical101")

# ---------------------------------------------------------------- running toilet
WT = [308, 308, 1332, 1192]
def tl(v0, v1, flap, extra, over=2.5):
    return [L(k="hatch", box=[60, 240, 150, 1740], c=[30, 48, 78], gap=34), L(k="line", pts=[[150, 240], [150, 1740]], c="dim", w=10),
            L(k="rect", box=[700, 1450, 1300, 1740], r=120, w=14, c="dim"), L(k="text", text="BOWL", xy=[1180, 1560], c="dim", size=34),
            L(k="line", pts=[[465, 1192], [465, 1330], [150, 1330]], c="dim", w=18), L(k="circ", at_xy=[270, 1330], r=34, fill="yel", w=0), L(k="text", text="SUPPLY VALVE", xy=[180, 1380], c="dim", size=30),
            L(k="level", box=WT, c="water", v0=v0, v1=v1, over=over), L(k="rect", box=[300, 300, 1340, 1200], w=16), L(k="rect", box=[280, 270, 1360, 300], fill="line", w=0, shadow=False),
            L(k="line", pts=[[500, 500], [640, 450], [815, 505]], c="dim", w=8), L(k="line", pts=[[300, 400], [560, 400]], w=12), L(k="bolts", pts=[[600, 1200], [1240, 1200]], c="line"), L(k="rect", box=[780, 520, 850, 1192], w=10, fill="navy"),
            L(k="rect", box=[430, 460, 500, 1192], fill="line", w=0), L(k="circ", at_xy=[465, 560], r=62, fill="line", w=0), L(k="pipe", pts=[[1000, 1200], [1000, 1700]], w=120),
            L(k="line", pts=[[900, 1198], [1100, 1198]], c="navy", w=22), L(k="line", pts=[[300, 400], [200, 400]], w=26), L(k="line", pts=[[330, 400], [1090, 1160]], c="dim", w=6),
            L(k="text", text="TOILET TANK, LID OFF", xy=[820, 200], center=True, c="sky")] + flap + extra
FL = lambda c="red", a0=0, a1=0, **k: [L(k="rot", pivot=[880, 1182], len=230, a0=a0, a1=a1, c=c, w=30, **k)]
save("running-toilet", "Why your toilet keeps running", "Why it keeps running", ["running"], 1, 3.0, [
    S("A running toilet? Lift the tank lid. There are only two parts that fail.", "A running toilet? Lift the tank lid. There are only two parts that fail.",
      tl(.7, .7, FL(), [L(k="label", text="FLAPPER", xy=[1150, 980], anchor=[1010, 1172], c="red", at=1.5), L(k="label", text="FILL VALVE", xy=[560, 350], anchor=[470, 470], c="yel", at=2.2)]),
      [[0, .45, .42, 1.1], [1, .45, .45, 1.3]], ["two", "parts"]),
    S("The flapper is the rubber seal at the bottom. When it wears out, water leaks into the bowl, and the tank keeps refilling.",
      "The flapper is the rubber seal at the bottom. When it wears out, water leaks into the bowl, and the tank keeps refilling.",
      tl(.7, .62, FL(a1=9, over=1.5), [L(k="dots", pts=[[1000, 1190], [1000, 1700]], c="water", n=5, speed=420, r=16, at=1.2), L(k="hud", text="LEAKING INTO THE BOWL", c="red", at=1.2),
          L(k="label", text="FLAPPER", xy=[1150, 980], anchor=[1010, 1160], c="red")], over=5), [[0, .45, .45, 1.3], [1, .56, .74, 1.8]], ["flapper", "leaks"]),
    S("The fill valve is the tower on the left. If the water level is set too high, it trickles into the overflow tube, nonstop.",
      "The fill valve is the tower on the left. If the water level is set too high, it trickles into the overflow tube, nonstop.",
      tl(.7, .8, FL(), [L(k="dots", pts=[[815, 530], [815, 1180]], c="water", n=5, speed=380, r=13, at=2.6), L(k="ring", at_xy=[815, 520], r=90, c="red", at=2.6),
          L(k="hud", text="SPILLING INTO THE OVERFLOW TUBE", c="red", at=2.6), L(k="label", text="FILL VALVE", xy=[560, 350], anchor=[470, 470], c="yel")]),
      [[0, .56, .74, 1.8], [.35, .32, .3, 1.7], [1, .42, .3, 1.8]], ["fill", "valve", "overflow"]),
    S("Swap the flapper for a matching new one, and set the float so the water stops about an inch below the top of the tube.",
      "Swap the flapper for a matching new one, and set the float so the water stops about an inch below the top of the tube.",
      tl(.8, .7, FL("green"), [L(k="line", pts=[[700, 573], [940, 573]], c="yel", w=8, at=2.6), L(k="label", text="1 INCH BELOW", xy=[900, 400], anchor=[850, 546], c="yel", at=2.6),
          L(k="hud", text="QUIET AGAIN", c="green", at=2.6)]), [[0, .42, .3, 1.8], [.3, .56, .72, 1.6], [.6, .46, .3, 1.7], [1, .45, .45, 1.2]], ["inch"], label="THE FIX", hold=.8)],
    {"hook": "That hissing toilet is water you’re paying for.", "feel": "There are only two parts in the tank that fail, and both are a cheap swap.",
     "shows": "What the flapper and the fill valve do, how each one fails, and the fix for both.", "ask": "How long has yours been running?"}, " #plumbing101")

# ---------------------------------------------------------------- gutters
def gt(gfill, extra):
    return [L(k="poly", pts=[[0, 1380], [600, 1380], [600, 1700], [1300, 1700], [1300, 1380], [1840, 1380], [1840, 1760], [0, 1760]], fill="soil", w=0),
            L(k="hatch", box=[0, 1420, 590, 1760], c=[38, 50, 64], gap=46), L(k="hatch", box=[1310, 1420, 1840, 1760], c=[38, 50, 64], gap=46),
            L(k="hatch", box=[0, 1384, 600, 1410], c=[70, 150, 80], gap=14, w=5), L(k="hatch", box=[1300, 1384, 1840, 1410], c=[70, 150, 80], gap=14, w=5),
            L(k="rect", box=[1130, 330, 1210, 520], w=12, fill="navy", shadow=False)] + extra[0] + [
            L(k="rect", box=[690, 800, 880, 1010], w=8, c="dim"), L(k="line", pts=[[785, 800], [785, 1010]], c="dim", w=6), L(k="line", pts=[[690, 905], [880, 905]], c="dim", w=6),
            L(k="rect", box=[1030, 1040, 1200, 1380], w=8, c="dim"), L(k="circ", at_xy=[1060, 1220], r=12, fill="dim", w=0),
            L(k="line", pts=[[560, 600], [950, 306], [1340, 600]], c="dim", w=6), L(k="line", pts=[[600, 1100], [1300, 1100]], c=[40, 60, 96], w=6),
            L(k="rect", box=[600, 1380, 1300, 1690], w=16), L(k="rect", box=[600, 640, 1300, 1380], w=16), L(k="poly", pts=[[500, 640], [950, 300], [1400, 640]], w=16),
            L(k="text", text="BASEMENT", xy=[950, 1600], center=True, c="dim", size=44), L(k="rect", box=[1390, 630, 1470, 684], w=10, fill=gfill),
            L(k="line", pts=[[1440, 684], [1440, 1330], [1500, 1380]], w=22), L(k="rain", box=[300, 0, 1700, 290], c="water")] + extra[1]
RR = [L(k="dots", pts=[[950, 300], [1400, 640]], c="water", n=7, speed=520, r=15), L(k="dots", pts=[[950, 300], [500, 640]], c="water", n=7, speed=520, r=15)]
DS = [[1440, 650], [1440, 1330], [1500, 1380]]
save("gutters", "What your gutters are actually for", "Gutters protect the basement", ["basement"], 2, 3.5, [
    S("A roof sheds hundreds of gallons in a single rainstorm.", "A roof sheds hundreds of gallons in a single rainstorm.",
      gt("navy", [[], RR + [L(k="count", fmt="{:.0f} GALLONS", v0=0, v1=620, over=3.5, xy=[950, 840], center=True, c="water", size=64), L(k="text", text="1 INCH OF RAIN, 1,000 SQ FT ROOF", xy=[950, 950], center=True, c="sky", size=34)]]),
      [[0, .5, .4, 1.0], [1, .54, .32, 1.4]], ["hundreds"], hold=.8),
    S("Gutters catch it, and downspouts carry it away from the house.", "Gutters catch it, and downspouts carry it away from the house.",
      gt("water", [[], RR + [L(k="dots", pts=DS + [[1830, 1396]], c="water", n=9, speed=560, r=14), L(k="label", text="GUTTER", xy=[1500, 470], anchor=[1436, 636], c="yel", at=.4),
          L(k="label", text="DOWNSPOUT", xy=[1040, 1000], anchor=[1430, 1000], c="line", at=1.2)]]), [[0, .54, .32, 1.4], [1, .76, .56, 1.45]], ["away"], hold=.6),
    S("When they clog, that water pours down the siding, pools at the foundation, and ends up in your basement.", "When they clog, that water pours down the siding, pools at the foundation, and ends up in your basement.",
      gt("brown", [[L(k="level", box=[1300, 1340, 1720, 1380], c="water", v0=0, v1=1, over=2, at=.8), L(k="level", box=[608, 1388, 1292, 1682], c="water", v0=0, v1=.3, over=3, at=2.2)],
          RR + [L(k="dots", pts=[[1400, 640], [1335, 700], [1335, 1380]], c="water", n=10, speed=560, r=14), L(k="hud", text="WATER AT THE FOUNDATION", c="red", at=1),
          L(k="label", text="CLOGGED", xy=[1500, 470], anchor=[1436, 636], c="brown")]]), [[0, .78, .38, 1.6], [.45, .72, .76, 1.5], [1, .55, .86, 1.6]], ["clog,", "basement."]),
    S("Clean them twice a year, and extend the downspouts 4 to 6 feet from the foundation. A $12 extension is the cheapest basement waterproofing ever invented.",
      "Clean them twice a year, and extend the downspouts four to six feet from the foundation. A twelve dollar extension is the cheapest basement waterproofing ever invented.",
      gt("water", [[], RR + [L(k="line", pts=[[1500, 1380], [1830, 1394]], c="yel", w=30, draw=1.0, at=.8), L(k="dots", pts=DS + [[1830, 1396]], c="water", n=9, speed=560, r=14),
          L(k="label", text="4 TO 6 FEET AWAY", xy=[1040, 1500], anchor=[1680, 1404], c="yel", at=1.8), L(k="hud", text="$12 EXTENSION", c="green", at=1.8)]]),
      [[0, .55, .86, 1.6], [.3, .8, .8, 1.6], [1, .6, .6, 1.1]], ["4", "6", "feet", "$12"], label="THE FIX")],
    {"hook": "Your gutters aren’t there to keep you dry at the front door.", "feel": "They’re there to keep hundreds of gallons away from your foundation.",
     "shows": "Where roof water goes when gutters work, where it goes when they clog, and the $12 fix.", "ask": "When were yours last cleaned?"})

# ---------------------------------------------------------------- frozen pipes
PIPE = [[560, 900], [1640, 900], [1640, 1250]]
def fz(extra_pre, extra):
    return [L(k="rect", box=[0, 0, 480, 1760], fill="panel", w=0, shadow=False), L(k="hatch", box=[500, 0, 640, 1760], c=[40, 60, 96], gap=34), L(k="line", pts=[[640, 0], [640, 1760]], c="dim", w=8),
            L(k="text", text="INSULATION", xy=[520, 1620], c="dim", size=26), L(k="poly", pts=[[0, 1700], [200, 1620], [470, 1660], [470, 1760], [0, 1760]], fill="ice", w=0),
            L(k="rect", box=[84, 440, 124, 700], r=20, w=8), L(k="circ", at_xy=[104, 724], r=36, fill="ice", w=0), L(k="line", pts=[[1640, 1250], [1640, 1180], [1700, 1180]], w=16),
            L(k="line", pts=[[480, 0], [480, 1760]], w=30), L(k="text", text="OUTSIDE", xy=[240, 180], center=True, c="sky"),
            L(k="text", text="INSIDE THE WALL", xy=[1160, 180], center=True, c="sky"), L(k="rain", box=[0, 470, 470, 1720], c="ice", n=24),
            L(k="pipe", pts=PIPE, w=130, water="water"), L(k="line", pts=[[1560, 1250], [1720, 1250]], w=30)] + extra_pre + extra
ICE = [700, 848, 1180, 952]; CRACK = L(k="line", pts=[[1230, 838], [1252, 880], [1224, 922], [1254, 962]], c="yel", w=14)
save("frozen-pipes", "Why frozen pipes burst", "Why frozen pipes burst", ["burst"], 1, 2.5, [
    S("Water expands when it freezes. Inside a pipe, it has nowhere to go.", "Water expands when it freezes. Inside a pipe, it has nowhere to go.",
      fz([L(k="rect", box=[700, 848, 720, 952], box1=ICE, over=3, fill="ice", w=0, at=.8)], [L(k="count", fmt="{:.0f}°F", v0=40, v1=10, over=3, xy=[240, 300], center=True, c="ice", size=120),
          L(k="label", text="ICE", xy=[860, 640], anchor=[940, 850], c="ice", at=1.8)]), [[0, .4, .5, 1.0], [1, .5, .5, 1.6]], ["expands"]),
    S("So a frozen pipe can split.", "So a frozen pipe can split.",
      fz([L(k="rect", box=ICE, fill="ice", w=0)], [L(k="text", text="10°F", xy=[240, 300], center=True, c="ice", size=120), dict(CRACK, draw=.5, at=.6),
          L(k="ring", at_xy=[1240, 900], r=130, c="yel", at=.6), L(k="hud", text="THE PIPE SPLITS", c="red", at=.6)]), [[0, .5, .5, 1.6], [1, .66, .5, 1.9]], ["split."], hold=1.2),
    S("And you won’t know until it thaws, and starts spraying.", "And you won't know until it thaws, and starts spraying.",
      fz([L(k="rect", box=ICE, box1=[700, 848, 720, 952], over=2.2, fill="ice", w=0), L(k="level", box=[700, 1700, 1740, 1750], c="water", v0=0, v1=1, over=1.5, at=2.2)],
         [L(k="count", fmt="{:.0f}°F", v0=10, v1=45, over=2.2, xy=[240, 300], center=True, c="hot", size=120), CRACK, L(k="drops", at_xy=[1240, 965], c="water", n=22, spread=280, fall=720, at=2.0),
          L(k="hud", text="NOW IT SPRAYS", c="red", at=2.0)]), [[0, .66, .5, 1.9], [.5, .66, .55, 1.6], [1, .66, .68, 1.3]], ["thaws,", "spraying."], hold=1.0),
    S("On freezing nights, let faucets on outside walls drip. Moving water resists freezing. And never set the heat below about 55 degrees.",
      "On freezing nights, let faucets on outside walls drip. Moving water resists freezing. And never set the heat below about fifty five degrees.",
      fz([], [L(k="text", text="10°F", xy=[240, 300], center=True, c="ice", size=120), L(k="dots", pts=PIPE, c="white", n=6, speed=170, r=13),
          L(k="drops", at_xy=[1640, 1300], c="water", n=4, spread=6, fall=380, rate=.9, r=13), L(k="label", text="LET IT DRIP", xy=[1020, 1420], anchor=[1630, 1340], c="yel", at=.6),
          L(k="text", text="HEAT: 55°F MINIMUM", xy=[1160, 420], center=True, c="hot", size=70, at=-3.2), L(k="hud", text="MOVING WATER RESISTS FREEZING", c="green", at=2.2)]),
      [[0, .6, .5, 1.2], [.45, .85, .72, 1.6], [1, .6, .42, 1.2]], ["drip.", "55"], label="PREVENT IT")],
    {"hook": "A frozen pipe doesn’t flood your house when it freezes.", "feel": "It floods it when it thaws.",
     "shows": "Why ice splits a pipe, why you only find out later, and what to do on a freezing night.", "ask": "Has this ever happened to you?"}, " #winterprep")
