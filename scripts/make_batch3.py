"""Batch 3 storyboards. python3 scripts/make_batch3.py"""
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

# ================================================================= dryer vent
DUCT = [[760, 1100], [1100, 1100], [1100, 500], [1560, 500]]
def dv(lint, extra, spd=520, n=8):
    e = [L(k="line", pts=[[100, 1506], [1560, 1506]], c="dim", w=10), L(k="hatch", box=[100, 1512, 1560, 1580], c=[30, 48, 78], gap=30),
         L(k="rect", box=[1560, 160, 1640, 1580], fill="panel", w=0, shadow=False), L(k="hatch", box=[1560, 160, 1640, 1580], c=[44, 70, 110], gap=40), L(k="text", text="OUTSIDE", xy=[1740, 300], c="sky", center=True, size=40),
         L(k="pipe", pts=DUCT, w=110), L(k="poly", pts=[[1640, 440], [1780, 470], [1780, 560], [1640, 560]], fill="line", w=0)] + lint + [
         L(k="rect", box=[200, 880, 760, 1500], r=30, fill="panel", w=16), L(k="circ", at_xy=[480, 1230], r=190, w=16), L(k="circ", at_xy=[480, 1230], r=150, c="dim", w=8),
         L(k="rot", pivot=[480, 1230], len=140, a0=0, a1=1440, over=9, c="dim", w=14), L(k="rot", pivot=[480, 1230], len=140, a0=120, a1=1560, over=9, c="dim", w=14), L(k="rot", pivot=[480, 1230], len=140, a0=240, a1=1680, over=9, c="dim", w=14),
         L(k="rect", box=[240, 910, 720, 990], r=12, w=6, c="dim"), L(k="circ", at_xy=[300, 950], r=24, c="yel", w=8), L(k="rect", box=[420, 925, 600, 975], r=8, fill="yel", w=0, shadow=False),
         L(k="text", text="LINT SCREEN", xy=[510, 936], c="navy", size=24, center=True), L(k="text", text="DRYER", xy=[480, 1440], center=True, c="dim", size=40),
         L(k="dots", pts=DUCT + [[1760, 500]], c="hot", n=n, speed=spd, r=13)]
    return e + extra
def lint(v, v1=None, over=4):
    v1 = v if v1 is None else v1
    return [L(k="level", box=[790, 1059, 1060, 1141], c="brown", v0=v, v1=v1, over=over), L(k="level", box=[1059, 540, 1141, 1060], c="brown", dir="right", v0=v, v1=v1, over=over), L(k="level", box=[1140, 459, 1540, 541], c="brown", v0=v, v1=v1, over=over)]
save("dryer-vent", "Why your dryer takes longer and longer", "Why the dryer got slow", ["slow"], 1, 4.0, [
    S("Your dryer pushes hot, wet air and lint out through a duct to the outside.", "Your dryer pushes hot, wet air, and lint, out through a duct to the outside.",
      dv([], [L(k="label", text="VENT DUCT", xy=[1180, 800], anchor=[1150, 760], c="yel", at=1.0)]), [[0, .35, .65, 1.3], [1, .6, .5, 1.25]], ["duct"]),
    S("Lint that gets past the screen builds up in that duct. Air slows down, so clothes take longer and longer to dry.", "Lint that gets past the screen builds up in that duct. Air slows down, so clothes take longer and longer to dry.",
      dv(lint(0, .7), [L(k="hud", text="LINT BUILDING UP", c="yel"), L(k="count", fmt="DRY TIME: {:.0f} MIN", v0=45, v1=95, over=5, xy=[480, 720], center=True, c="white", size=60)], spd=180, n=4),
      [[0, .6, .5, 1.25], [.5, .62, .42, 1.6], [1, .45, .55, 1.25]], ["longer", "lint"]),
    S("Now the heat can’t escape. And lint is highly flammable.", "Now the heat can't escape. And lint is highly flammable.",
      dv(lint(.7), [L(k="hud", text="HEAT TRAPPED", c="red"), L(k="rise", at_xy=[930, 1040], c="hot", n=4, h=240, gap=60), L(k="flame", at_xy=[930, 1100], size=46, n=3, at=1.6), L(k="ring", at_xy=[930, 1080], r=150, c="red", at=1.6),
         L(k="text", text="DRY TIME: 95 MIN", xy=[480, 720], center=True, c="red", size=60)], spd=90, n=3), [[0, .45, .55, 1.25], [1, .52, .62, 1.9]], ["flammable."], hold=1.0),
    S("Clean the lint screen every single load. And clean the full duct to the outside once a year.", "Clean the lint screen every single load. And clean the full duct to the outside once a year.",
      dv(lint(.7, 0, over=2.5), [L(k="ring", at_xy=[510, 950], r=130, c="yel", to=2.4), L(k="hud", text="SCREEN: EVERY LOAD", c="yel", to=2.4), L(k="hud", text="FULL DUCT: ONCE A YEAR", c="green", at=2.4)]),
      [[0, .3, .56, 1.9], [.45, .3, .56, 1.9], [1, .58, .5, 1.2]], ["every", "year."], label="THE FIX", hold=.6)],
    ("About 2,900 home dryer fires are reported in the U.S. every year. The leading cause: failure to clean.", "About twenty nine hundred home dryer fires are reported in the U.S. every year. The leading cause? Failure to clean them.", ["2,900", "clean."]),
    {"hook": "If your dryer takes two cycles, it’s probably not the dryer.", "feel": "It’s the duct behind it, and a clogged duct is a fire risk.",
     "shows": "Where the lint goes, why drying slows down, and the two cleanings that fix it.", "ask": "When was your dryer duct last cleaned?"}, " #firesafety")

# ================================================================= escrow
GRN, BLU = [90, 200, 130], [58, 160, 255]
def es(pay, extra, jar=.5, jar1=None, over=3):
    jar1 = jar if jar1 is None else jar1
    bars = [("PRINCIPAL", 360, "dim"), ("INTEREST", 560, "dim"), ("PROPERTY TAX", 760, GRN), ("INSURANCE", 960, BLU)]
    e = [L(k="text", text="YOUR MONTHLY PAYMENT", xy=[430, 250], center=True, size=44), L(k="rect", box=[130, 320, 730, 1180], r=30, w=12, c="dim")]
    for nm, y, c in bars: e += [L(k="rect", box=[170, y, 690, y + 160], r=18, fill=c, w=0), L(k="text", text=nm, xy=[430, y + 56], center=True, c="navy", size=40)]
    e += [L(k="text", text="ESCROW ACCOUNT", xy=[1340, 430], center=True, size=44), L(k="level", box=[1112, 512, 1568, 1088], c=GRN, v0=jar, v1=jar1, over=over),
          L(k="rect", box=[1100, 500, 1580, 1100], r=30, w=16), L(k="rect", box=[1060, 1320, 1380, 1500], r=18, fill="panel", w=10), L(k="text", text="TAX BILL", xy=[1220, 1384], center=True, size=38),
          L(k="rect", box=[1440, 1320, 1780, 1500], r=18, fill="panel", w=10), L(k="text", text="INSURANCE BILL", xy=[1610, 1384], center=True, size=32)]
    return e + pay + extra
PAY = lambda a, b, c="white", **k: [L(k="count", fmt="${:,.0f} / MONTH", v0=a, v1=b, over=1.5, xy=[430, 1230], center=True, c=c, size=64, **k)]
IN = [L(k="dots", pts=[[690, 840], [900, 840], [900, 700], [1100, 700]], c=GRN, n=5, speed=380, r=14), L(k="dots", pts=[[690, 1040], [960, 1040], [960, 860], [1100, 860]], c=BLU, n=5, speed=380, r=14)]
OUT = [L(k="dots", pts=[[1220, 1100], [1220, 1320]], c=GRN, n=3, speed=300, r=14, at=2.5), L(k="dots", pts=[[1500, 1100], [1610, 1320]], c=BLU, n=3, speed=300, r=14, at=2.5)]
save("escrow", "Why your fixed mortgage payment went up", "Fixed rate. Payment went up.", ["up."], 3, 3.5, [
    S("You got a fixed-rate mortgage so the payment would never change. Then a letter says it’s going up.", "You got a fixed rate mortgage so the payment would never change. Then a letter says it's going up.",
      es(PAY(2000, 2000, to=2.5) + PAY(2000, 2240, "red", at=2.5), [L(k="hud", text="PAYMENT INCREASE NOTICE", c="red", at=2.5)]), [[0, .5, .5, 1.0], [1, .26, .48, 1.5]], ["up."]),
    S("Your payment is four things. Principal and interest are fixed. Taxes and insurance are not.", "Your payment is four things. Principal and interest are fixed. Taxes and insurance, are not.",
      es(PAY(2000, 2000), [L(k="label", text="FIXED", xy=[790, 500], anchor=[700, 520], c="line", at=1.2), L(k="label", text="CAN CHANGE", xy=[790, 900], anchor=[700, 930], c="yel", at=2.6), L(k="ring", at_xy=[430, 940], r=330, c="yel", at=2.6)]),
      [[0, .26, .48, 1.5], [1, .3, .46, 1.45]], ["four", "not."]),
    S("Your lender collects one-twelfth of those bills every month, holds it in escrow, and pays them for you.", "Your lender collects one twelfth of those bills every month, holds it in escrow, and pays them for you.",
      es(PAY(2000, 2000), IN + OUT + [L(k="hud", text="1/12 EVERY MONTH", c="green")], jar=.2, jar1=.6), [[0, .3, .46, 1.45], [.5, .62, .48, 1.4], [1, .72, .62, 1.4]], ["escrow,"]),
    S("Once a year they re-check the math. If your taxes or insurance went up, there’s a shortage.", "Once a year they recheck the math. If your taxes or insurance went up, there's a shortage.",
      es(PAY(2000, 2000), IN + [L(k="line", pts=[[1090, 700], [1590, 700]], c="yel", w=8), L(k="text", text="NEEDED", xy=[1620, 680], c="yel", size=34), L(k="hud", text="SHORTAGE", c="red", at=2.2),
         L(k="count", fmt="${:,.0f}", v0=3600, v1=4400, over=2, xy=[1220, 1436], center=True, c="red", size=44), L(k="count", fmt="${:,.0f}", v0=1800, v1=2600, over=2, xy=[1610, 1436], center=True, c="red", size=44)], jar=.6, jar1=.42),
      [[0, .72, .62, 1.4], [1, .74, .55, 1.45]], ["shortage."]),
    S("So your payment rises for two reasons: to cover the higher bills, and to pay back last year’s gap.", "So your payment rises for two reasons. To cover the higher bills, and to pay back last year's gap.",
      es(PAY(2000, 2240, "red"), IN + [L(k="rect", box=[170, 1300, 690, 1400], r=14, fill="red", w=0, at=.8), L(k="text", text="+ HIGHER BILLS", xy=[430, 1330], center=True, c="navy", size=36, at=.8),
         L(k="rect", box=[170, 1420, 690, 1520], r=14, fill="yel", w=0, at=2.2), L(k="text", text="+ LAST YEAR’S GAP", xy=[430, 1450], center=True, c="navy", size=36, at=2.2)], jar=.42),
      [[0, .74, .55, 1.45], [.3, .26, .7, 1.5], [1, .26, .72, 1.5]], ["two", "reasons:"], hold=.6),
    S("When the escrow statement arrives, read it. It shows exactly which bill went up.", "When the escrow statement arrives, read it. It shows exactly which bill went up.",
      es(PAY(2240, 2240, "red"), IN + [L(k="hud", text="READ THE ESCROW STATEMENT", c="green")], jar=.5), [[0, .26, .72, 1.5], [1, .5, .5, 1.0]], ["read", "it."], label="WHAT TO DO")],
    ("Fixed rate does not mean fixed payment. Your taxes and insurance can move it every year.", "Fixed rate does not mean fixed payment. Your taxes and insurance can move it, every single year.", ["not"]),
    {"hook": "Fixed-rate mortgage. Payment went up anyway.", "feel": "You weren’t lied to. You just met your escrow account.",
     "shows": "The four parts of a mortgage payment, what escrow does, and why a shortage raises your payment twice. Dollar figures are examples.", "ask": "Did your payment jump this year?"}, " #mortgage #escrow")

# ================================================================= heat loss
GAPS = [700, 920, 1140]
def hl(extra, ins=0.0, ins1=None, sealed=False):
    ins1 = ins if ins1 is None else ins1
    e = [L(k="poly", pts=[[0, 1500], [1840, 1500], [1840, 1760], [0, 1760]], fill="soil", w=0), L(k="hatch", box=[0, 1540, 1840, 1760], c=[38, 50, 64], gap=46),
         L(k="rain", box=[0, 0, 400, 1400], c="ice", n=14), L(k="rain", box=[1440, 0, 1840, 1400], c="ice", n=14), L(k="text", text="20°F OUTSIDE", xy=[200, 1560], center=True, c="ice", size=40),
         L(k="poly", pts=[[420, 700], [920, 280], [1420, 700]], w=16), L(k="rect", box=[500, 700, 1340, 1500], w=16), L(k="text", text="ATTIC", xy=[920, 470], center=True, c="dim", size=40),
         L(k="level", box=[512, 640, 1328, 692], c=[236, 170, 200], dir="right", v0=ins, v1=ins1, over=2.5),
         L(k="rect", box=[600, 1180, 800, 1500], w=8, c="dim"), L(k="rect", box=[1000, 900, 1220, 1120], w=8, c="dim"), L(k="line", pts=[[1110, 900], [1110, 1120]], c="dim", w=6),
         L(k="rect", box=[860, 1300, 1000, 1480], r=10, fill="hot", w=0), L(k="text", text="FURNACE", xy=[930, 1250], center=True, c="dim", size=28), L(k="text", text="68°F", xy=[1180, 1320], center=True, c="hot", size=70)]
    for x in GAPS:
        e.append(L(k="line", pts=[[x - 30, 700], [x + 30, 700]], c="navy", w=22))
        if sealed: e.append(L(k="rect", box=[x - 44, 684, x + 44, 716], r=8, fill="yel", w=0, shadow=False, at=.8))
    return e + extra
UP = [L(k="dots", pts=[[x, 1280], [x, 700], [x + (x - 920) * .3, 420]], c="hot", n=5, speed=330, r=14) for x in GAPS]
COLD = [L(k="dots", pts=[[300, 1470], [500, 1470], [760, 1440]], c="ice", n=4, speed=260, r=13), L(k="dots", pts=[[1540, 1470], [1340, 1470], [1100, 1440]], c="ice", n=4, speed=260, r=13)]
save("heat-loss", "Where your heat actually goes", "Where your heat goes", ["heat"], 1, 3.0, [
    S("Warm air rises. In winter it pushes up through every gap in your ceiling.", "Warm air rises. In winter it pushes up through every gap in your ceiling.",
      hl(UP + [L(k="label", text="GAPS IN THE CEILING", xy=[1000, 560], anchor=[1140, 690], c="yel", at=1.5)]), [[0, .5, .55, 1.0], [1, .5, .38, 1.5]], ["rises.", "gap"]),
    S("And cold air gets pulled in down low to replace it.", "And cold air gets pulled in, down low, to replace it.",
      hl(UP + COLD + [L(k="label", text="COLD AIR IN", xy=[130, 1300], anchor=[420, 1462], c="ice", at=.6), L(k="hud", text="YOUR HOUSE IS A CHIMNEY", c="red", at=1.2)]), [[0, .5, .38, 1.5], [1, .4, .78, 1.5]], ["cold"], hold=.8),
    S("Two things fight this. Air sealing stops air moving through holes. Insulation slows heat moving through surfaces.", "Two things fight this. Air sealing stops air moving through holes. Insulation slows heat moving through surfaces.",
      hl(UP + COLD + [L(k="label", text="INSULATION", xy=[1420, 600], anchor=[1300, 664], c=[236, 170, 200], at=3.2)], ins=0, ins1=1), [[0, .4, .78, 1.5], [.4, .5, .4, 1.4], [1, .56, .38, 1.5]], ["sealing", "Insulation"]),
    S("Insulation without air sealing is a wool sweater in a windstorm.", "Insulation without air sealing, is a wool sweater in a windstorm.",
      hl(UP + COLD + [L(k="hud", text="STILL LEAKING", c="red")], ins=1), [[0, .56, .38, 1.5], [1, .5, .4, 1.7]], ["sweater", "windstorm."], hold=.8),
    S("So seal first, then insulate.", "So seal first. Then insulate.",
      hl([L(k="dots", pts=[[930, 1300], [930, 800], [640, 800], [640, 1140], [930, 1300]], c="hot", n=6, speed=300, r=14, at=.8), L(k="dots", pts=[[930, 1300], [930, 800], [1260, 800], [1260, 1240], [930, 1300]], c="hot", n=6, speed=300, r=14, at=.8),
          L(k="hud", text="SEAL FIRST, THEN INSULATE", c="green", at=.8)] + [dict(d, to=.8) for d in UP], ins=1, sealed=True), [[0, .5, .4, 1.7], [1, .5, .55, 1.1]], ["seal", "first,"], label="THE FIX", hold=1.6)],
    ("The EPA estimates that sealing and insulating saves the average home about 15% on heating and cooling.", "The E P A estimates that air sealing and insulating saves the average home about fifteen percent on heating and cooling.", ["15%"]),
    {"hook": "Your house is a chimney, and you’re paying to heat the sky.", "feel": "Most people add insulation and wonder why the bill didn’t move.",
     "shows": "Why warm air leaves through the ceiling, why cold air comes in low, and why you seal before you insulate.", "ask": "Is your upstairs always the wrong temperature?"}, " #energysaving")

# ================================================================= smoke / CO alarm dates
def al(extra, bar=0.0, bar1=None, red=0.0, red1=None, over=3):
    bar1 = bar if bar1 is None else bar1; red1 = red if red1 is None else red1
    e = [L(k="rect", box=[0, 0, 1840, 200], fill="panel", w=0, shadow=False), L(k="hatch", box=[0, 0, 1840, 200], c=[44, 70, 110], gap=40), L(k="text", text="CEILING", xy=[920, 220], center=True, c="dim", size=32),
         L(k="circ", at_xy=[520, 620], r=250, fill="panel", w=16), L(k="circ", at_xy=[520, 620], r=170, c="dim", w=8)]
    for i in range(8): e.append(L(k="rot", pivot=[520, 620], len=150, a0=i * 45, a1=i * 45, c="dim", w=8))
    e += [L(k="circ", at_xy=[520, 620], r=56, fill="line", w=0), L(k="circ", at_xy=[660, 480], r=16, fill="green", w=0), L(k="text", text="FRONT", xy=[520, 900], center=True, c="dim", size=36),
          L(k="circ", at_xy=[1300, 620], r=250, fill="panel", w=16), L(k="rect", box=[1140, 540, 1460, 700], r=10, fill=[236, 230, 214], w=0), L(k="text", text="MFG DATE", xy=[1300, 556], center=True, c="navy", size=30),
          L(k="text", text="2011 MAR 08", xy=[1300, 610], center=True, c="navy", size=44), L(k="bolts", pts=[[1160, 470], [1440, 470], [1160, 780], [1440, 780]], c="line"), L(k="text", text="BACK", xy=[1300, 900], center=True, c="dim", size=36),
          L(k="level", box=[204, 1204, 1164, 1276], c="green", dir="right", v0=bar, v1=bar1, over=over), L(k="level", box=[1164, 1204, 1636, 1276], c="red", dir="right", v0=red, v1=red1, over=1.5, at=over if red1 != red else 0),
          L(k="rect", box=[200, 1200, 1640, 1280], r=10, w=10), L(k="text", text="SMOKE ALARM AGE", xy=[200, 1120], size=40)]
    for yr, x in ((0, 200), (5, 680), (10, 1160), (15, 1640)): e += [L(k="line", pts=[[x, 1280], [x, 1320]], w=8), L(k="text", text=f"{yr} YRS", xy=[x, 1336], center=True, c="sky", size=34)]
    return e + extra
save("alarm-dates", "Your smoke alarm has an expiration date", "Your alarm expired", ["expired"], 2, 3.0, [
    S("Every smoke alarm has an expiration date. Almost nobody knows that.", "Every smoke alarm has an expiration date. Almost nobody knows that.",
      al([L(k="ring", at_xy=[660, 480], r=50, c="green")]), [[0, .5, .45, 1.0], [1, .3, .36, 1.7]], ["expiration", "date."]),
    S("The sensor inside loses sensitivity over time. After about 10 years, it may not respond quickly, or at all.", "The sensor inside loses sensitivity over time. After about ten years, it may not respond quickly, or at all.",
      al([L(k="label", text="REPLACE HERE", xy=[980, 1440], anchor=[1160, 1290], c="yel", at=3), L(k="hud", text="PAST ITS DATE", c="red", at=3.4), L(k="rise", at_xy=[520, 1060], c="dim", n=4, h=160, gap=70, at=3.4)], bar=0, bar1=1, red=0, red1=1),
      [[0, .3, .36, 1.7], [.35, .5, .7, 1.3], [1, .52, .7, 1.35]], ["10", "years,"]),
    S("Take it down and look at the back. The manufacture date is printed right there.", "Take it down and look at the back. The manufacture date is printed right there.",
      al([L(k="ring", at_xy=[1300, 620], r=210, c="yel", at=1.4)], bar=1, red=1), [[0, .52, .7, 1.35], [.4, .7, .36, 1.8], [1, .7, .36, 1.9]], ["back."]),
    S("Smoke alarms: replace about every 10 years. Carbon monoxide alarms often sooner, typically 5 to 10 years depending on the model.",
      "Smoke alarms, replace about every ten years. Carbon monoxide alarms, often sooner. Typically five to ten years, depending on the model.",
      al([L(k="text", text="CO ALARM: 5 TO 10 YRS, CHECK THE MODEL", xy=[200, 1440], c="yel", size=40, at=2.8), L(k="hud", text="SMOKE: 10 YEARS", c="yel"), L(k="hud", text="CO: 5 TO 10 YEARS", c="yel", at=2.8)], bar=1, red=0),
      [[0, .7, .36, 1.9], [.3, .5, .72, 1.3], [1, .5, .74, 1.3]], ["10", "5"]),
    S("If the house came with a 15-year-old alarm, it’s decor, not protection.", "If the house came with a fifteen year old alarm, it's decor. Not protection.",
      al([L(k="hud", text="DECOR, NOT PROTECTION", c="red"), L(k="ring", at_xy=[1640, 1240], r=90, c="red")], bar=1, red=1), [[0, .5, .74, 1.3], [1, .5, .5, 1.0]], ["decor,"], label="CHECK YOURS", hold=.8)],
    ("NFPA: 3 out of 5 home fire deaths happen in homes with no working smoke alarm.", "The N F P A says three out of five home fire deaths happen in homes with no working smoke alarm.", ["3", "5"]),
    {"hook": "Your smoke alarm has an expiration date.", "feel": "It can beep when you test it and still be too old to trust.",
     "shows": "Why alarms wear out, where the date is printed, and when to replace smoke and CO alarms.", "ask": "Go look. What year is on the back of yours?"}, " #firesafety")

# ================================================================= the four ages
ITEMS = [("ROOF", [920, 330], "2008"), ("FURNACE", [520, 1300], "2011"), ("WATER HEATER", [820, 1300], "2014"), ("AC", [1580, 1280], "2016")]
def fa(extra):
    e = [L(k="poly", pts=[[0, 1100], [380, 1100], [380, 1560], [1300, 1560], [1300, 1100], [1840, 1100], [1840, 1760], [0, 1760]], fill="soil", w=0), L(k="hatch", box=[0, 1140, 370, 1760], c=[38, 50, 64], gap=46), L(k="hatch", box=[1310, 1140, 1840, 1760], c=[38, 50, 64], gap=46),
         L(k="rect", box=[380, 1100, 1300, 1550], w=16), L(k="rect", box=[380, 560, 1300, 1100], w=16), L(k="poly", pts=[[300, 560], [840, 200], [1380, 560]], w=24, c="yel"),
         L(k="rect", box=[480, 700, 680, 920], w=8, c="dim"), L(k="rect", box=[980, 700, 1180, 920], w=8, c="dim"), L(k="text", text="BASEMENT", xy=[1120, 1480], center=True, c="dim", size=32),
         L(k="rect", box=[440, 1180, 600, 1540], r=14, fill="panel", w=12), L(k="flame", at_xy=[520, 1520], size=30, n=3), L(k="line", pts=[[520, 1180], [520, 1104]], w=20),
         L(k="rect", box=[760, 1200, 880, 1540], r=50, fill=[40, 110, 180], w=12), L(k="line", pts=[[800, 1200], [800, 1104]], w=12),
         L(k="rect", box=[1460, 880, 1700, 1100], r=14, fill="panel", w=12), L(k="circ", at_xy=[1580, 990], r=76, c="dim", w=8), L(k="rot", pivot=[1580, 990], len=70, a0=0, a1=2880, over=10, c="dim", w=12), L(k="rot", pivot=[1580, 990], len=70, a0=180, a1=3060, over=10, c="dim", w=12),
         L(k="line", pts=[[1460, 1040], [1300, 1040]], c="dim", w=14)]
    return e + extra
RINGS = [L(k="ring", at_xy=[840, 360], r=150, c="yel", at=.4), L(k="ring", at_xy=[520, 1360], r=210, c="yel", at=1.0), L(k="ring", at_xy=[820, 1370], r=200, c="yel", at=1.6), L(k="ring", at_xy=[1580, 990], r=180, c="yel", at=2.2)]
NAMES = [L(k="text", text="ROOF", xy=[1100, 300], c="yel", size=44, at=.4), L(k="text", text="FURNACE", xy=[420, 950], c="yel", size=36, at=1.0), L(k="text", text="WATER HEATER", xy=[700, 950], c="yel", size=36, at=1.6), L(k="text", text="AC", xy=[1550, 780], c="yel", size=44, at=2.2)]
YEARS = [L(k="count", fmt="{:.0f}", v0=2026, v1=2008, over=2, xy=[1100, 360], c="white", size=60), L(k="count", fmt="{:.0f}", v0=2026, v1=2011, over=2, xy=[440, 1000], c="white", size=44),
         L(k="count", fmt="{:.0f}", v0=2026, v1=2014, over=2, xy=[760, 1000], c="white", size=44), L(k="count", fmt="{:.0f}", v0=2026, v1=2016, over=2, xy=[1540, 830], c="white", size=50)]
save("four-ages", "The four ages that decide your next big bills", "4 numbers to know", ["4"], 1, 3.0, [
    S("Four things in your house decide your next decade of big bills.", "Four things in your house decide your next decade of big bills.", fa(RINGS + NAMES), [[0, .5, .45, 1.0], [1, .5, .48, 1.05]], ["Four", "big", "bills."], hold=.8),
    S("Your furnace, your AC, your water heater, and your roof. Each one has a birthday.", "Your furnace. Your A C. Your water heater. And your roof. Each one has a birthday.",
      fa(NAMES + YEARS + [L(k="hud", text="YEAR INSTALLED", c="yel")]), [[0, .5, .48, 1.05], [.5, .36, .72, 1.6], [1, .6, .5, 1.2]], ["birthday."]),
    S("The date is on a sticker, usually hidden in the serial number. Search the brand name plus “serial number date” to decode it.", "The date is on a sticker, usually hidden in the serial number. Search the brand name, plus serial number date, to decode it.",
      fa([L(k="rect", box=[770, 1290, 870, 1350], r=6, fill=[236, 230, 214], w=0), L(k="line", pts=[[782, 1310], [858, 1310]], c=[120, 120, 120], w=4), L(k="line", pts=[[782, 1330], [840, 1330]], c=[120, 120, 120], w=4),
          L(k="ring", at_xy=[820, 1320], r=90, c="yel", at=.6), L(k="label", text="SERIAL NO. STICKER", xy=[930, 1230], anchor=[872, 1316], c="yel", at=.8, size=40)]), [[0, .6, .5, 1.2], [1, .5, .75, 2.2]], ["sticker,", "serial"]),
    S("Tank water heaters commonly last around 8 to 12 years. Past 10, you’re not in trouble, but you’re on the clock.", "Tank water heaters commonly last around eight to twelve years. Past ten, you're not in trouble. But you're on the clock.",
      fa([L(k="rect", box=[900, 1260, 1260, 1300], r=8, w=6), L(k="level", box=[904, 1264, 1256, 1296], c="red", dir="right", v0=0, v1=1, over=4), L(k="text", text="0", xy=[900, 1316], c="sky", size=28), L(k="text", text="12 YRS", xy=[1180, 1316], c="sky", size=28),
          L(k="hud", text="ON THE CLOCK", c="red", at=3.5)]), [[0, .5, .75, 2.2], [1, .56, .75, 2.0]], ["8", "12", "clock."]),
    S("Write all four ages down, and start saving before the oldest one quits.", "Write all four ages down, and start saving before the oldest one quits.",
      fa(NAMES + [L(k="text", text="2008", xy=[1100, 360], c="red", size=60), L(k="text", text="2011", xy=[440, 1000], c="white", size=44), L(k="text", text="2014", xy=[760, 1000], c="white", size=44), L(k="text", text="2016", xy=[1540, 830], c="white", size=50),
          L(k="hud", text="WRITE THEM DOWN", c="green"), L(k="ring", at_xy=[840, 360], r=150, c="red", at=1.2)]), [[0, .56, .75, 2.0], [1, .5, .45, 1.0]], ["four", "ages"], label="DO THIS", hold=.8)],
    ("Replacing any one of these costs thousands. Knowing the ages turns an emergency into a plan.", "Replacing any one of these costs thousands. Knowing their ages turns an emergency, into a plan.", ["plan."]),
    {"hook": "Four numbers decide your next ten years of repair bills.", "feel": "Most homeowners can’t tell you a single one of them.",
     "shows": "The four big-ticket systems, where to find each one’s age, and why you write them down. Years shown are examples.", "ask": "Do you know how old your roof is?"})
