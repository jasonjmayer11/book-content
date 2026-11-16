"""Batch 4 storyboards."""
import json
T = "#firsttimehomebuyer #newhomeowner #howitworks #homeownertips #homemaintenance #engineering"
END = {"type": "end", "dur": 3.6}
BOOK = {"type": "book", "text": "That’s one page of the manual your house didn’t come with", "accent": ["manual"], "size": 96, "book_h": 700,
        "chips": ["34 CHAPTERS", "PAPERBACK + KINDLE"], "voice": "That's one page of the manual your house didn't come with. If this was news to you, the rest of the book will be too."}
L = lambda **k: k
def S(text, voice, els, cam, accent=(), **kw):
    d = {"type": "diagram", "diagram": "gx", "state": {"els": els}, "text": text, "voice": voice, "cam": cam, "accent": list(accent)}; d.update(kw); return d
def save(key, title, cover, cacc, hero, hero_t, scenes, why, cap, tag=""):
    scenes = scenes + [{"type": "quote", "label": "WHY IT MATTERS", "text": why[0], "voice": why[1], "accent": why[2], "size": 80, "hold": .5}, BOOK, END]
    v = {"slug": "house-x-how-it-works-" + key, "book": "house", "format": "X explainer", "title": title, "cover": cover, "cover_accent": cacc,
         "cover_sub": "How your house works", "hero": ["gx", hero], "hero_t": hero_t, "scenes": scenes, "caption": dict(cap, tags=T + tag)}
    json.dump(v, open(f"stories/{v['slug']}.json", "w"), indent=1, ensure_ascii=False)
FULL = [[0, .5, .5, 1.0], [1, .5, .5, 1.0]]

# ================================================================= AC
LOOP_IN = [[1500, 1250], [1320, 1250], [1320, 900], [880, 900], [880, 560]]
LOOP_OUT = [[960, 560], [960, 980], [1400, 980], [1400, 1180], [1560, 1180]]
def ac(extra, flow=True):
    e = [L(k="poly", pts=[[0, 1440], [1840, 1440], [1840, 1760], [0, 1760]], fill="soil", w=0), L(k="hatch", box=[0, 1480, 1840, 1760], c=[38, 50, 64], gap=46),
         L(k="poly", pts=[[60, 480], [620, 120], [1180, 480]], w=16), L(k="rect", box=[140, 480, 1100, 1440], w=16), L(k="text", text="INSIDE: 72°F", xy=[380, 1360], c="sky", size=40),
         L(k="text", text="OUTSIDE: 95°F", xy=[1500, 520], center=True, c="hot", size=44), L(k="rect", box=[200, 900, 380, 1120], w=8, c="dim"), L(k="line", pts=[[290, 900], [290, 1120]], c="dim", w=6),
         L(k="rect", box=[760, 500, 1080, 760], r=16, fill="panel", w=12), L(k="hatch", box=[790, 560, 1050, 700], c=[90, 160, 230], gap=18, w=5), L(k="text", text="INDOOR COIL", xy=[920, 440], center=True, c="ice", size=34),
         L(k="rect", box=[1440, 1060, 1780, 1420], r=20, fill="panel", w=14), L(k="hatch", box=[1460, 1080, 1760, 1400], c=[70, 90, 120], gap=16, w=4), L(k="circ", at_xy=[1610, 1240], r=120, c="dim", w=10),
         L(k="rot", pivot=[1610, 1240], len=105, a0=0, a1=3600, over=10, c="line", w=16), L(k="rot", pivot=[1610, 1240], len=105, a0=120, a1=3720, over=10, c="line", w=16), L(k="rot", pivot=[1610, 1240], len=105, a0=240, a1=3840, over=10, c="line", w=16),
         L(k="text", text="OUTDOOR UNIT", xy=[1610, 1500], center=True, c="sky", size=32),
         L(k="pipe", pts=LOOP_IN, w=40), L(k="pipe", pts=LOOP_OUT, w=40)]
    if flow: e += [L(k="dots", pts=LOOP_IN, c="ice", n=6, speed=360, r=12), L(k="dots", pts=LOOP_OUT, c="hot", n=6, speed=360, r=12)]
    return e + extra
ROOMAIR = [L(k="dots", pts=[[200, 640], [740, 640]], c="hot", n=5, speed=300, r=14), L(k="dots", pts=[[1080, 690], [1100, 690]], c="ice", n=1, speed=60, r=1),
           L(k="dots", pts=[[760, 740], [500, 900], [300, 1300]], c="ice", n=5, speed=300, r=14)]
DUMP = [L(k="rise", at_xy=[1610, 1040], c="hot", n=4, h=320, gap=80)]
DRIP = [L(k="drops", at_xy=[920, 770], c="water", n=4, spread=8, fall=60, rate=1.2, r=10), L(k="line", pts=[[860, 790], [980, 790]], w=10), L(k="line", pts=[[980, 790], [1080, 790], [1100, 1440]], c="water", w=12, draw=1.2)]
save("ac", "Your AC doesn’t make cold air", "AC doesn’t make cold", ["cold"], 1, 3.0, [
    S("Your air conditioner doesn’t make cold air. It moves heat from inside your house to the outside.", "Your air conditioner doesn't make cold air. It moves heat, from inside your house, to the outside.",
      ac(ROOMAIR + DUMP), FULL, ["moves", "heat"]),
    S("Inside, warm air from your rooms blows across a cold coil. The refrigerant in that coil soaks up the heat.", "Inside, warm air from your rooms blows across a cold coil. The refrigerant in that coil soaks up the heat.",
      ac(ROOMAIR + [L(k="label", text="REFRIGERANT", xy=[1150, 760], anchor=[1100, 900], c="ice", at=2.2)]), [[0, .5, .5, 1.0], [1, .42, .36, 1.6]], ["cold", "coil."]),
    S("A pump sends that refrigerant outside, where a big fan blows the heat into the yard.", "A pump sends that refrigerant outside, where a big fan blows the heat into the yard.",
      ac(DUMP + [L(k="label", text="HEAT OUT", xy=[1180, 820], anchor=[1560, 1000], c="hot", at=1.4), L(k="hud", text="MOVING HEAT, NOT MAKING COLD", c="yel")]), [[0, .42, .36, 1.6], [1, .82, .68, 1.6]], ["fan", "heat"]),
    S("It also pulls water out of the air. That drips into a pan and out a small drain line. When algae clogs it, the water goes into your ceiling.", "It also pulls water out of the air. That drips into a pan, and out a small drain line. When algae clogs it, the water goes into your ceiling.",
      ac(ROOMAIR + DRIP + [L(k="label", text="CONDENSATE LINE", xy=[1130, 1140], anchor=[1094, 1180], c="water", at=2.2), L(k="hud", text="CLOGGED LINE = WET CEILING", c="red", at=4.2)]),
      [[0, .82, .68, 1.6], [.3, .5, .4, 1.9], [1, .55, .6, 1.4]], ["water", "ceiling."]),
    S("So keep two feet of clear space around the outdoor unit, and change your filter. Both help it move heat.", "So keep two feet of clear space around the outdoor unit, and change your filter. Both help it move heat.",
      ac(DUMP + [L(k="dim", a=[1440, 1000], b=[1780, 1000], text="2 FT CLEAR", c="yel", dy=-60), L(k="hud", text="KEEP IT CLEAR", c="green")]), [[0, .55, .6, 1.4], [1, .82, .66, 1.55]], ["two", "feet"], label="THE FIX", hold=.6)],
    ("ENERGY STAR says heating and cooling is almost half of the average home’s energy bill.", "Energy Star says heating and cooling is almost half of the average home's energy bill. Knowing how it works helps you keep it efficient.", ["half"]),
    {"hook": "Your air conditioner doesn’t make cold air.", "feel": "It’s a heat mover, and once you get that, its upkeep makes sense.",
     "shows": "How heat moves from your rooms to the outdoor unit, where the water goes, and the two-foot rule.", "ask": "When did you last clear around your outdoor unit?"}, " #hvac")

# ================================================================= sump pump
PIT = [760, 1180, 1080, 1620]
def sp(level0, level1, run, extra, over=3):
    e = [L(k="rect", box=[0, 0, 1840, 1760], fill="soil", w=0, shadow=False), L(k="hatch", box=[0, 0, 1840, 1760], c=[34, 46, 60], gap=46),
         L(k="level", box=[0, 900, 1840, 1760], c=[30, 70, 120], v0=.6, v1=.6),
         L(k="rect", box=[300, 0, 1540, 1120], fill="navy", w=0, shadow=False), L(k="line", pts=[[300, 1120], [1540, 1120]], w=24), L(k="line", pts=[[300, 0], [300, 1120]], w=24), L(k="line", pts=[[1540, 0], [1540, 1120]], w=24),
         L(k="text", text="BASEMENT", xy=[920, 980], center=True, c="dim", size=44), L(k="text", text="GROUNDWATER", xy=[160, 1280], c="water", size=36),
         L(k="level", box=[772, 1192, 1068, 1608], c="water", v0=level0, v1=level1, over=over), L(k="rect", box=PIT, w=14), L(k="text", text="SUMP PIT", xy=[1140, 1560], c="dim", size=34),
         L(k="rect", box=[860, 1460, 980, 1600], r=14, fill="panel", w=10), L(k="line", pts=[[920, 1460], [920, 400], [1540, 400], [1840, 400]], w=26)]
    for x in (200, 500, 1300, 1700): e.append(L(k="dots", pts=[[x, 1700], [x, 1400], [880 if x < 920 else 960, 1300]], c="water", n=3, speed=140, r=10))
    if run: e += [L(k="dots", pts=[[920, 1460], [920, 400], [1840, 400]], c="water", n=10, speed=700, r=13), L(k="text", text="PUMP ON", xy=[920, 1420], center=True, c="green", size=30)]
    return e + extra
save("sump-pump", "The pump keeping your basement dry", "Your basement’s last defense", ["last"], 2, 2.0, [
    S("If your basement has a pit in the floor with a pump in it, that pump is all that stands between a rainstorm and a flooded basement.", "If your basement has a pit in the floor, with a pump in it, that pump is all that stands between a rainstorm, and a flooded basement.",
      sp(.3, .6, False, [L(k="label", text="SUMP PUMP", xy=[1130, 1300], anchor=[985, 1520], c="yel", at=2)]), [[0, .5, .5, 1.0], [1, .5, .78, 1.4]], ["flooded", "basement."]),
    S("Groundwater collects in the pit. When it rises, a float switches the pump on, and it pushes the water outside.", "Groundwater collects in the pit. When it rises, a float switches the pump on, and it pushes the water outside.",
      sp(.6, .2, True, [L(k="hud", text="FLOAT UP: PUMP ON", c="green")]), [[0, .5, .78, 1.4], [.6, .5, .55, 1.0], [1, .6, .3, 1.2]], ["float", "outside."]),
    S("But the storms that flood basements also knock out power. No power, no pump.", "But the storms that flood basements also knock out power. No power, no pump.",
      sp(.6, 1, False, [L(k="level", box=[312, 1060, 1528, 1108], c="water", v0=0, v1=1, over=2, at=2.5), L(k="hud", text="POWER OUT", c="red"), L(k="rain", box=[0, 0, 300, 880], c="water", n=10)]),
      [[0, .6, .3, 1.2], [1, .5, .7, 1.3]], ["power.", "pump."], hold=.8),
    S("Test it a few times a year with a bucket of water. Add a battery backup and a water alarm, and replace it every 7 to 10 years.", "Test it a few times a year with a bucket of water. Add a battery backup, and a water alarm. And replace it every seven to ten years.",
      sp(.2, .5, True, [L(k="rect", box=[1180, 1380, 1380, 1600], r=14, fill="green", w=0), L(k="text", text="BACKUP", xy=[1280, 1470], center=True, c="navy", size=34),
         L(k="hud", text="TEST · BACKUP · ALARM", c="green")]), [[0, .5, .7, 1.3], [1, .55, .78, 1.45]], ["bucket", "backup", "7", "10"], label="THE FIX", hold=.6)],
    ("Standard home insurance generally won’t cover sump pump failure unless you add water backup coverage.", "Standard home insurance generally won't cover a failed sump pump, unless you add water backup coverage. Check your policy.", ["won’t"]),
    {"hook": "One pump decides whether your basement floods.", "feel": "And it fails right when you need it, during a storm with the power out.",
     "shows": "How a sump pump works, why storms beat it, and the test, backup and alarm that protect you.", "ask": "Have you ever tested yours?"})

# ================================================================= radon
def rd(extra, lvl=0.0, lvl1=None, fan=False):
    lvl1 = lvl if lvl1 is None else lvl1
    e = [L(k="rect", box=[0, 1280, 1840, 1760], fill="soil", w=0, shadow=False), L(k="hatch", box=[0, 1300, 1840, 1760], c=[38, 50, 64], gap=46), L(k="text", text="SOIL", xy=[120, 1640], c="dim", size=36),
         L(k="poly", pts=[[260, 560], [920, 160], [1580, 560]], w=16), L(k="rect", box=[340, 560, 1500, 1280], w=16), L(k="rect", box=[340, 1280, 1500, 1540], w=16),
         L(k="line", pts=[[340, 1000], [1500, 1000]], c="dim", w=8), L(k="text", text="BASEMENT", xy=[920, 1400], center=True, c="dim", size=36),
         L(k="line", pts=[[700, 1540], [720, 1500], [700, 1460]], c="yel", w=6), L(k="line", pts=[[1240, 1540], [1260, 1500], [1240, 1470]], c="yel", w=6),
         L(k="level", box=[352, 1292, 1488, 1528], c=[160, 200, 80], v0=lvl, v1=lvl1, over=3)]
    if fan:
        e += [L(k="pipe", pts=[[1100, 1600], [1100, 1300], [1100, 1100], [1100, 80]], w=56), L(k="rect", box=[1050, 620, 1150, 720], r=12, fill="green", w=0),
              L(k="dots", pts=[[400, 1620], [1100, 1620], [1100, 80]], c=[160, 200, 80], n=10, speed=520, r=12)]
    return e + extra
SEEP = [L(k="dots", pts=[[710, 1740], [710, 1500], [760, 1360]], c=[160, 200, 80], n=4, speed=120, r=13), L(k="dots", pts=[[1250, 1740], [1250, 1500], [1180, 1360]], c=[160, 200, 80], n=4, speed=120, r=13),
        L(k="dots", pts=[[960, 1740], [960, 1560], [960, 1420]], c=[160, 200, 80], n=3, speed=100, r=13)]
save("radon", "The invisible gas in a lot of basements", "The gas you can’t smell", ["can’t"], 1, 3.0, [
    S("Radon is a radioactive gas that seeps up from the ground and collects indoors. You can’t see it or smell it.", "Radon is a radioactive gas that seeps up from the ground, and collects indoors. You can't see it, or smell it.",
      rd(SEEP + [L(k="label", text="RADON", xy=[160, 1180], anchor=[700, 1500], c=[160, 200, 80], at=1)], 0, .5), [[0, .5, .5, 1.0], [1, .5, .78, 1.4]], ["radioactive", "smell"]),
    S("It gets in through cracks in the floor, gaps around pipes, and the joints in your foundation.", "It gets in through cracks in the floor, gaps around pipes, and the joints in your foundation.",
      rd(SEEP + [L(k="ring", at_xy=[710, 1500], r=80, c="yel"), L(k="ring", at_xy=[1250, 1500], r=80, c="yel", at=1.2), L(k="label", text="CRACKS", xy=[150, 1460], anchor=[640, 1500], c="yel")], .5),
      [[0, .5, .78, 1.4], [1, .55, .82, 1.7]], ["cracks"]),
    S("The only way to know your level is to test. A kit costs about $15 to $25 including the lab fee. Fix it at 4 picocuries or higher.", "The only way to know your level is to test. A kit costs about fifteen to twenty five dollars, including the lab fee. Fix it at four picocuries, or higher.",
      rd(SEEP + [L(k="rect", box=[820, 1440, 1020, 1520], r=10, fill=[236, 230, 214], w=0), L(k="text", text="TEST KIT", xy=[920, 1460], center=True, c="navy", size=28),
         L(k="count", fmt="{:.1f} pCi/L", v0=0, v1=6.2, over=3, xy=[920, 1080], center=True, c="red", size=80, at=2.5), L(k="hud", text="EPA: FIX AT 4+", c="red", at=4)], .5), [[0, .55, .82, 1.7], [1, .5, .68, 1.4]], ["test.", "4"]),
    S("The fix is a pipe from under the floor to above the roof, with a small fan that pulls the gas out before it gets in.", "The fix is a pipe from under the floor to above the roof, with a small fan that pulls the gas out before it gets in.",
      rd([L(k="label", text="FAN", xy=[1200, 560], anchor=[1150, 670], c="green", at=2), L(k="hud", text="MITIGATION SYSTEM", c="green")], .5, 0, fan=True), [[0, .5, .68, 1.4], [1, .55, .45, 1.0]], ["pipe", "fan"], label="THE FIX", hold=.6)],
    ("The EPA estimates radon causes about 21,000 lung cancer deaths a year, and about 1 in 15 homes has elevated levels.", "The E P A estimates radon causes about twenty one thousand lung cancer deaths a year. And about one in fifteen homes has elevated levels.", ["21,000", "1", "15"]),
    {"hook": "There may be a gas in your basement you can’t see or smell.", "feel": "Your neighbor’s test tells you nothing about your house. Only yours does.",
     "shows": "Where radon comes from, how it gets in, what level to act on, and how mitigation works. Readings shown are examples.", "ask": "Have you ever tested your home?"}, " #radon")

# ================================================================= main line vs single clog
TUB, TOILET, SINK = [520, 600], [920, 820], [1320, 600]
def ml(extra, clog_at=None):
    e = [L(k="rect", box=[0, 1300, 1840, 1760], fill="soil", w=0, shadow=False), L(k="hatch", box=[0, 1320, 1840, 1760], c=[38, 50, 64], gap=46), L(k="text", text="TO SEWER", xy=[1700, 1600], center=True, c="sky", size=34),
         L(k="rect", box=[400, 520, 640, 660], r=30, w=12), L(k="text", text="TUB", xy=[520, 460], center=True, c="dim", size=34),
         L(k="rect", box=[850, 700, 990, 880], r=40, w=12), L(k="text", text="TOILET", xy=[920, 640], center=True, c="dim", size=34),
         L(k="rect", box=[1240, 520, 1400, 640], r=14, w=12), L(k="text", text="SINK", xy=[1320, 460], center=True, c="dim", size=34),
         L(k="pipe", pts=[[520, 660], [520, 1200], [920, 1200]], w=50), L(k="pipe", pts=[[920, 880], [920, 1200]], w=60), L(k="pipe", pts=[[1320, 640], [1320, 1200], [920, 1200]], w=50),
         L(k="pipe", pts=[[920, 1200], [920, 1500], [1840, 1500]], w=84), L(k="rect", box=[620, 1440, 700, 1560], r=8, fill="line", w=0), L(k="text", text="CLEANOUT", xy=[440, 1580], c="dim", size=30)]
    return e + extra
FLOW_ALL = [L(k="dots", pts=[[520, 660], [520, 1200], [920, 1200], [920, 1500], [1840, 1500]], c="water", n=8, speed=520, r=12),
            L(k="dots", pts=[[1320, 640], [1320, 1200], [920, 1200], [920, 1500], [1840, 1500]], c="water", n=8, speed=520, r=12)]
save("main-line", "One slow drain vs. every drain backing up", "One clog, or the main line?", ["main"], 2, 3.0, [
    S("Every drain in your house flows into one main line that carries everything to the sewer.", "Every drain in your house flows into one main line that carries everything to the sewer.",
      ml(FLOW_ALL + [L(k="label", text="MAIN LINE", xy=[1100, 1340], anchor=[1300, 1480], c="yel", at=1.5)]), [[0, .5, .5, 1.0], [1, .6, .74, 1.3]], ["one", "main", "line"]),
    S("One slow drain is a local clog, usually hair or grease in that drain’s own pipe. That’s a plunger job.", "One slow drain is a local clog. Usually hair, or grease, in that drain's own pipe. That's a plunger job.",
      ml([L(k="rect", box=[496, 880, 544, 960], r=10, fill="brown", w=0), L(k="dots", pts=[[1320, 640], [1320, 1200], [920, 1200], [920, 1500], [1840, 1500]], c="water", n=8, speed=520, r=12),
          L(k="level", box=[412, 532, 628, 648], c="water", v0=0, v1=.6, over=3), L(k="hud", text="ONE DRAIN: LOCAL CLOG", c="yel")]), [[0, .6, .74, 1.3], [1, .32, .45, 1.6]], ["One", "local"]),
    S("But if several drains back up at once, or flushing makes water rise in the tub, the clog is in the main line.", "But if several drains back up at once, or flushing makes water rise in the tub, the clog is in the main line.",
      ml([L(k="rect", box=[1180, 1458, 1260, 1542], r=12, fill="brown", w=0), L(k="level", box=[412, 532, 628, 648], c=[140, 120, 60], v0=0, v1=.7, over=3, at=1.5),
          L(k="level", box=[1252, 532, 1388, 628], c=[140, 120, 60], v0=0, v1=.6, over=3, at=2), L(k="dots", pts=[[920, 880], [920, 1500], [1180, 1500]], c=[140, 120, 60], n=5, speed=300, r=12),
          L(k="hud", text="EVERYTHING BACKING UP", c="red", at=1.5), L(k="ring", at_xy=[1220, 1500], r=110, c="red", at=1)]), [[0, .32, .45, 1.6], [.5, .66, .8, 1.6], [1, .5, .5, 1.0]], ["several", "main", "line."]),
    S("Stop running water and call a plumber. They’ll clear it through the cleanout, so find yours now.", "Stop running water, and call a plumber. They'll clear it through the cleanout. So find yours now.",
      ml([L(k="ring", at_xy=[660, 1500], r=110, c="yel"), L(k="dots", pts=[[660, 1440], [660, 1500], [1840, 1500]], c="yel", n=6, speed=420, r=10, at=1.4), L(k="hud", text="FIND YOUR CLEANOUT", c="green")]),
      [[0, .5, .5, 1.0], [1, .38, .84, 1.7]], ["Stop", "cleanout,"], label="WHAT TO DO", hold=.6)],
    ("Standard home insurance doesn’t cover sewer backup. It’s a separate add-on, and most people don’t have it.", "Standard home insurance doesn't cover sewer backup. It's a separate add on. Ask your agent about it.", ["doesn’t"]),
    {"hook": "One slow drain is a plunger job. Every drain backing up is not.", "feel": "Knowing the difference saves you from making it worse.",
     "shows": "How your drains feed one main line, the signs of a main line clog, and why you find the cleanout now.", "ask": "Do you know where your cleanout is?"}, " #plumbing101")

# ================================================================= garage door safety
def door(a, b, over, back):
    Y = lambda v: 340 + 1220 * v
    out = [L(k="rect", box=[240, 340, 1600, Y(a)], box1=[240, 340, 1600, Y(b)], over=over, fill=[44, 64, 96], w=6, c="dim", to=(over + .25) if back else 999)]
    if back: out.append(L(k="rect", box=[240, 340, 1600, Y(b)], box1=[240, 340, 1600, Y(a)], over=1.4, fill=[44, 64, 96], w=6, c="dim", at=over + .25))
    return out
def gd(door0, door1, extra, over=3, beam=True, back=False):
    e = [L(k="rect", box=[0, 1560, 1840, 1760], fill="soil", w=0, shadow=False), L(k="line", pts=[[0, 1560], [1840, 1560]], c="dim", w=10),
         L(k="rect", box=[200, 300, 1640, 1560], w=18), L(k="line", pts=[[200, 300], [920, 80], [1640, 300]], w=16),
         ] + door(door0, door1, over, back) + [
         L(k="rect", box=[240, 1460, 300, 1500], fill="line", w=0), L(k="rect", box=[1540, 1460, 1600, 1500], fill="line", w=0), L(k="text", text="PHOTO EYES", xy=[920, 1600], center=True, c="sky", size=32)]
    if beam: e.append(L(k="line", pts=[[300, 1480], [1540, 1480]], c="red", w=4))
    return e + extra
save("garage-door", "The safety test your garage door needs", "Test this every month", ["month"], 1, 2.5, [
    S("A garage door weighs a lot. Two safety systems keep it from closing on a person, a pet, or your car.", "A garage door weighs a lot. Two safety systems keep it from closing on a person, a pet, or your car.",
      gd(.2, .2, [L(k="label", text="PHOTO EYE BEAM", xy=[620, 1300], anchor=[900, 1480], c="red", at=2)]), FULL, ["Two", "safety"]),
    S("First, the photo eyes. Two small sensors near the floor send a beam across the opening. Break the beam, and the door should reverse.", "First, the photo eyes. Two small sensors near the floor send a beam across the opening. Break the beam, and the door should reverse.",
      gd(.2, .75, [L(k="line", pts=[[880, 1380], [960, 1560]], c="yel", w=18, at=3.2), L(k="text", text="BROOM", xy=[980, 1360], c="yel", size=30, at=3.2), L(k="hud", text="BEAM BROKEN: REVERSE", c="green", at=3.3)], over=3, back=True),
      [[0, .5, .5, 1.0], [1, .5, .78, 1.5]], ["photo", "eyes.", "reverse."]),
    S("Second, auto-reverse. Lay a 2×4 flat in the door’s path and close it. It should hit the board and go back up.", "Second, auto reverse. Lay a two by four flat in the door's path, and close it. It should hit the board, and go back up.",
      gd(.2, .93, [L(k="rect", box=[820, 1520, 1020, 1560], fill="brown", w=0), L(k="text", text="2×4", xy=[920, 1480], center=True, c="brown", size=34), L(k="hud", text="HIT THE BOARD: REVERSE", c="green", at=3.6)], over=3.4, beam=False, back=True),
      [[0, .5, .78, 1.5], [1, .5, .82, 1.8]], ["2×4", "back", "up."]),
    S("If it doesn’t reverse, stop using the opener until it’s fixed. Then test both every month.", "If it doesn't reverse, stop using the opener until it's fixed. Then test both, every month.",
      gd(.93, .93, [L(k="rect", box=[820, 1520, 1020, 1560], fill="brown", w=0), L(k="hud", text="NO REVERSE = STOP USING IT", c="red"), L(k="hud", text="TEST MONTHLY", c="green", at=3)], beam=False),
      [[0, .5, .82, 1.8], [1, .5, .5, 1.0]], ["stop", "month."], label="DO THIS", hold=.6)],
    ("Federal rules have required this protection on openers made since 1993, but sensors get dirty and knocked out of line.", "Federal rules have required this protection on openers made since nineteen ninety three. But sensors get dirty, and knocked out of line.", ["1993,"]),
    {"hook": "Your garage door has two safety systems. Have you tested either one?", "feel": "Both can quietly stop working, and the door doesn’t tell you.",
     "shows": "How the photo eyes and auto-reverse work, the broom test, the 2×4 test, and what to do if it fails.", "ask": "When did you last test yours?"}, " #homesafety")
