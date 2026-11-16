"""Batch 5 storyboards."""
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
GRN, RED_ = [90, 200, 130], [255, 96, 80]
def tag(x, y, text, ok, at=0.0, w=420):
    c = GRN if ok else RED_
    return [L(k="rect", box=[x, y, x + w, y + 110], r=18, fill="panel", w=8, c=c, at=at), L(k="circ", at_xy=[x + 56, y + 55], r=34, fill=c, w=0, at=at),
            *([L(k="line", pts=[[x + 38, y + 56], [x + 52, y + 72], [x + 76, y + 40]], c="navy", w=9, at=at)] if ok else
              [L(k="line", pts=[[x + 40, y + 39], [x + 72, y + 71]], c="navy", w=9, at=at), L(k="line", pts=[[x + 40, y + 71], [x + 72, y + 39]], c="navy", w=9, at=at)]), L(k="text", text=text, xy=[x + 110, y + 34], c="line", size=38, at=at)]
def house(x0=520, x1=1320, y0=700, y1=1380, top=360):
    return [L(k="poly", pts=[[x0 - 80, y0], [(x0 + x1) / 2, top], [x1 + 80, y0]], w=16), L(k="rect", box=[x0, y0, x1, y1], w=16),
            L(k="rect", box=[x0 + 80, y0 + 120, x0 + 260, y0 + 300], w=8, c="dim"), L(k="rect", box=[x1 - 260, y1 - 300, x1 - 120, y1], w=8, c="dim")]
GROUND = [L(k="rect", box=[0, 1380, 1840, 1760], fill="soil", w=0, shadow=False), L(k="hatch", box=[0, 1400, 1840, 1760], c=[38, 50, 64], gap=46)]
SHIELD = [L(k="poly", pts=[[920, 230], [1460, 360], [1420, 1100], [920, 1440], [420, 1100], [380, 360]], w=10, c="green")]

# ================================================================= insurance gaps
save("insurance-gaps", "What your home insurance doesn’t cover", "Insurance won’t pay for this", ["won’t"], 2, 3.0, [
    S("Home insurance covers sudden accidents. A pipe that bursts out of nowhere is usually covered.", "Home insurance covers sudden accidents. A pipe that bursts out of nowhere, is usually covered.",
      GROUND + house() + SHIELD + [L(k="drops", at_xy=[1000, 900], c="water", n=16, spread=180, fall=420), L(k="line", pts=[[860, 880], [1140, 880]], w=24)] + tag(1180, 520, "BURST PIPE", True, at=2.4, w=520),
      [[0, .5, .5, 1.0], [1, .58, .42, 1.25]], ["sudden", "covered."]),
    S("But a pipe that dripped for six months? That’s wear, and it generally isn’t.", "But a pipe that dripped for six months? That's wear. And it generally isn't.",
      GROUND + house() + [L(k="line", pts=[[860, 880], [1140, 880]], w=24), L(k="drops", at_xy=[1000, 900], c="water", n=3, spread=4, fall=300, rate=.6), L(k="rect", box=[860, 1220, 1140, 1380], fill="brown", w=0, at=.5),
         L(k="count", fmt="MONTH {:.0f}", v0=1, v1=6, over=2.5, xy=[1000, 1100], center=True, c="white", size=52)] + tag(1180, 520, "SLOW LEAK", False, at=2.6, w=520), [[0, .58, .42, 1.25], [1, .55, .55, 1.3]], ["wear,", "isn’t."]),
    S("Flood from outside is excluded from standard policies. Flood insurance is separate, and a new policy usually takes 30 days to start.", "Flood from outside is excluded from standard policies. Flood insurance is separate. And a new policy usually takes thirty days to start.",
      GROUND + [L(k="level", box=[0, 1100, 1840, 1760], c=[40, 110, 180], v0=0, v1=.55, over=4)] + house() + tag(1240, 260, "FLOOD", False, at=1.0, w=420) +
      [L(k="count", fmt="WAIT: {:.0f} DAYS", v0=0, v1=30, over=3, xy=[300, 300], center=True, c="yel", size=60, at=3.5)], [[0, .55, .55, 1.3], [1, .5, .5, 1.0]], ["Flood", "30", "days"]),
    S("Sewer backup is excluded too, unless you add an endorsement. The book’s advice: add it.", "Sewer backup is excluded too, unless you add an endorsement. The book's advice? Add it.",
      GROUND + house() + [L(k="pipe", pts=[[920, 1380], [920, 1600], [1840, 1600]], w=70), L(k="rect", box=[860, 1300, 980, 1380], r=14, w=8),
         L(k="level", box=[528, 1300, 1312, 1372], c=[140, 120, 60], v0=0, v1=1, over=3), L(k="dots", pts=[[1840, 1600], [920, 1600], [920, 1360]], c=[140, 120, 60], n=6, speed=260, r=13)] +
      tag(1180, 520, "SEWER BACKUP", False, at=1.0, w=560) + tag(1180, 680, "+ ENDORSEMENT", True, at=3.6, w=560), [[0, .5, .5, 1.0], [1, .62, .6, 1.25]], ["Sewer", "add", "it."]),
    S("Earthquakes, pests and mold usually aren’t covered either. Read your exclusions before you need them.", "Earthquakes, pests, and mold, usually aren't covered either. Read your exclusions, before you need them.",
      GROUND + house() + tag(120, 180, "EARTHQUAKE", False, w=500) + tag(120, 330, "TERMITES / PESTS", False, at=.6, w=600) + tag(1180, 180, "MOLD (OFTEN)", False, at=1.2, w=560) +
      [L(k="hud", text="READ YOUR EXCLUSIONS", c="green", at=2.6)], [[0, .5, .5, 1.0], [1, .5, .3, 1.15]], ["exclusions"], label="DO THIS", hold=.6)],
    ("FEMA says most standard homeowners policies don’t cover flood damage. Most people find out after the water arrives.", "FEMA says most standard homeowners policies don't cover flood damage. Most people find out after the water arrives.", ["don’t"]),
    {"hook": "Your home insurance has holes. Do you know where they are?", "feel": "Most people find out the day they file a claim.",
     "shows": "What a standard policy covers, the big exclusions (flood, sewer backup, wear, earthquake, pests, mold), and what to add. Policies vary, so read yours.", "ask": "Do you have sewer backup coverage?"}, " #homeinsurance")

# ================================================================= equity
BX0, BX1, BY0, BY1 = 560, 1280, 300, 1500
def eq(owed0, owed1, top0=0.0, top1=None, extra=(), over=4):
    top1 = top0 if top1 is None else top1
    Y = lambda f: BY1 - (BY1 - BY0) * f
    return [L(k="text", text="WHAT YOUR HOUSE IS WORTH", xy=[920, 200], center=True, size=40),
            L(k="rect", box=[BX0, Y(.8 + top0), BX1, BY1], box1=[BX0, Y(.8 + top1), BX1, BY1], over=over, fill=GRN, w=0, r=10),
            L(k="rect", box=[BX0, Y(owed0), BX1, BY1], box1=[BX0, Y(owed1), BX1, BY1], over=over, fill=[70, 86, 112], w=0, r=10),
            L(k="line", pts=[[BX0 - 20, BY1], [BX1 + 20, BY1]], w=10)] + list(extra)
save("equity", "What home equity actually is", "Equity, explained simply", ["Equity,"], 0, 2.0, [
    S("Equity is the part of your house you actually own. It’s the home’s value, minus what you still owe.", "Equity is the part of your house you actually own. It's the home's value, minus what you still owe.",
      eq(.64, .64, extra=[L(k="text", text="OWED: $320,000", xy=[920, 1180], center=True, c="white", size=52), L(k="text", text="EQUITY: $80,000", xy=[920, 610], center=True, c="navy", size=52, at=2),
         L(k="text", text="VALUE: $400,000", xy=[1320, 260], c="line", size=40), L(k="hud", text="EXAMPLE NUMBERS", c="yel")]), FULL, ["own.", "minus"]),
    S("It grows two ways. First, every payment chips away at the loan. Early on, most of each payment is interest, so this part starts slow.", "It grows two ways. First, every payment chips away at the loan. Early on, most of each payment is interest, so this part starts slow.",
      eq(.64, .56, extra=[L(k="count", fmt="OWED: ${:,.0f}", v0=320000, v1=280000, over=4, xy=[920, 1180], center=True, c="white", size=52), L(k="hud", text="PAYING IT DOWN", c="green", at=1.2)], over=6), [[0, .5, .5, 1.0], [1, .5, .6, 1.2]], ["two", "slow."]),
    S("Second, if your home’s value rises, your equity rises with it, without you paying a cent more.", "Second, if your home's value rises, your equity rises with it, without you paying a cent more.",
      eq(.56, .56, 0, .14, extra=[L(k="count", fmt="VALUE: ${:,.0f}", v0=400000, v1=470000, over=4, xy=[1320, 260], c="line", size=40), L(k="hud", text="VALUE GOING UP (NOT GUARANTEED)", c="yel")]), [[0, .5, .6, 1.2], [1, .5, .38, 1.2]], ["value", "rises,"]),
    S("You can borrow against it with a home equity loan or line of credit. But your house becomes the collateral.", "You can borrow against it, with a home equity loan, or line of credit. But your house becomes the collateral.",
      eq(.56, .72, .14, .14, extra=[L(k="rect", box=[1380, 700, 1720, 900], r=16, fill="yel", w=0, at=1.2), L(k="text", text="BORROWED", xy=[1550, 770], center=True, c="navy", size=40, at=1.2),
         L(k="hud", text="YOUR HOUSE IS THE COLLATERAL", c="red", at=3.6)]), [[0, .5, .38, 1.2], [1, .58, .5, 1.1]], ["borrow", "collateral."], label="CAREFUL", hold=.6)],
    ("In the Federal Reserve’s 2016 survey, the primary residence was the largest asset on household balance sheets nationwide.", "In the Federal Reserve's twenty sixteen survey, the primary home was the largest asset on household balance sheets nationwide. Understand it, before you borrow against it.", ["largest"]),
    {"hook": "Equity is the part of your house you actually own.", "feel": "It’s most people’s biggest asset, and most people can’t explain it.",
     "shows": "What equity is, the two ways it grows, and the catch with borrowing against it. All figures are examples, not advice.", "ask": "Do you know roughly how much equity you have?"}, " #personalfinance")

# ================================================================= repair fund
JAR = [700, 560, 1140, 1360]
def rf(v0, v1, extra=(), over=4):
    return [L(k="text", text="REPAIR FUND", xy=[920, 470], center=True, size=44), L(k="level", box=[712, 572, 1128, 1348], c=GRN, v0=v0, v1=v1, over=over),
            L(k="rect", box=JAR, r=40, w=16), L(k="rect", box=[760, 520, 1080, 560], r=10, fill="line", w=0)] + list(extra)
save("repair-fund", "How much to save for home repairs", "Save this much for repairs", ["this", "much"], 1, 3.0, [
    S("The mortgage is the predictable part of owning a home. What breaks people is everything else, arriving at once, with no money set aside.", "The mortgage is the predictable part of owning a home. What breaks people is everything else, arriving at once, with no money set aside.",
      rf(.05, .05, [L(k="rect", box=[200, 900, 460, 1100], r=14, fill="panel", w=8, c="red", at=2), L(k="text", text="FURNACE", xy=[330, 980], center=True, c="red", size=36, at=2),
         L(k="rect", box=[1380, 900, 1640, 1100], r=14, fill="panel", w=8, c="red", at=2.6), L(k="text", text="WATER HEATER", xy=[1510, 980], center=True, c="red", size=30, at=2.6), L(k="hud", text="NO FUND", c="red", at=3.2)]),
      FULL, ["everything", "else,"]),
    S("The classic rule: set aside 1 to 3 percent of your home’s value every year. On a $400,000 house, that’s $4,000 to $12,000 a year.", "The classic rule. Set aside one to three percent of your home's value, every year. On a four hundred thousand dollar house, that's four thousand to twelve thousand dollars a year.",
      rf(.05, .6, [L(k="dots", pts=[[400, 300], [920, 300], [920, 600]], c=GRN, n=6, speed=420, r=14), L(k="count", fmt="${:,.0f} / YEAR", v0=0, v1=4000, over=3, xy=[920, 1420], center=True, c="white", size=56, at=2.5),
         L(k="hud", text="1–3% OF VALUE PER YEAR", c="yel")], over=6), [[0, .5, .5, 1.0], [1, .5, .62, 1.15]], ["1", "3", "percent"]),
    S("Newer homes, closer to 1 percent. 10 to 30 years old, around 2. Older homes, or systems near the end of their lives, 3 or more.", "Newer homes, closer to one percent. Ten to thirty years old, around two. Older homes, or systems near the end of their lives, three or more.",
      [L(k="rect", box=[300, 1300, 600, 1460], fill="green", w=0, r=10), L(k="rect", box=[770, 1140, 1070, 1460], fill="yel", w=0, r=10, at=1.4), L(k="rect", box=[1240, 980, 1540, 1460], fill="red", w=0, r=10, at=2.8),
       L(k="text", text="1%", xy=[450, 1220], center=True, size=60), L(k="text", text="2%", xy=[920, 1060], center=True, size=60, at=1.4), L(k="text", text="3%+", xy=[1390, 900], center=True, size=60, at=2.8),
       L(k="text", text="UNDER 10 YRS", xy=[450, 1490], center=True, c="sky", size=32), L(k="text", text="10–30 YRS", xy=[920, 1490], center=True, c="sky", size=32, at=1.4), L(k="text", text="OLDER", xy=[1390, 1490], center=True, c="sky", size=32, at=2.8),
       L(k="line", pts=[[240, 1460], [1600, 1460]], w=10)], [[0, .5, .72, 1.3], [1, .5, .68, 1.2]], ["1", "2.", "3"]),
    S("You won’t spend it every year. Then one year takes the furnace and the water heater, and the fund makes that year annoying instead of catastrophic.", "You won't spend it every year. Then one year takes the furnace and the water heater. And the fund makes that year annoying, instead of catastrophic.",
      rf(.8, .25, [L(k="dots", pts=[[920, 1360], [920, 1500], [330, 1500]], c=GRN, n=5, speed=380, r=14, at=2), L(k="dots", pts=[[920, 1360], [920, 1500], [1510, 1500]], c=GRN, n=5, speed=380, r=14, at=2.6),
         L(k="rect", box=[200, 1420, 460, 1600], r=14, fill="panel", w=8, c="green", at=2), L(k="text", text="FURNACE", xy=[330, 1490], center=True, c="green", size=36, at=2),
         L(k="rect", box=[1380, 1420, 1640, 1600], r=14, fill="panel", w=8, c="green", at=2.6), L(k="text", text="WATER HEATER", xy=[1510, 1490], center=True, c="green", size=30, at=2.6), L(k="hud", text="PAID FROM THE FUND", c="green", at=3.4)], over=5),
      [[0, .5, .62, 1.15], [1, .5, .6, 1.0]], ["annoying", "catastrophic."], hold=.6)],
    ("Angi’s 2025 report: the average homeowner spent $2,041 on maintenance and $1,143 on emergency repairs in a single year.", "Angi's twenty twenty five report found the average homeowner spent two thousand forty one dollars on maintenance, and eleven hundred forty three on emergency repairs, in a single year.", ["$2,041", "$1,143"]),
    {"hook": "How much should you save for home repairs?", "feel": "The mortgage is the easy part. It’s everything else that breaks budgets.",
     "shows": "The 1–3% rule, where your house falls in that range, and why the fund exists. The $400,000 home is an example.", "ask": "Do you have a separate repair fund?"}, " #personalfinance #budgeting")

# ================================================================= ice dams
ROOF = [[160, 1100], [920, 420], [1680, 1100]]
def idm(extra, heat=True):
    e = [L(k="rect", box=[300, 1100, 1540, 1700], w=16), L(k="text", text="WARM ROOMS", xy=[920, 1450], center=True, c="hot", size=40), L(k="text", text="ATTIC", xy=[920, 900], center=True, c="dim", size=40),
         L(k="line", pts=[[300, 1100], [1540, 1100]], c="dim", w=8), L(k="line", pts=ROOF, w=20), L(k="line", pts=[[160, 1100], [60, 1190]], w=20), L(k="line", pts=[[1680, 1100], [1780, 1190]], w=20),
         L(k="line", pts=[[182, 1060], [920, 395], [1658, 1060]], c="ice", w=26), L(k="text", text="COLD EAVE", xy=[80, 1220], c="ice", size=34), L(k="rain", box=[0, 0, 1840, 380], c="ice", n=26)]
    if heat: e += [L(k="rise", at_xy=[920, 1080], c="hot", n=4, h=520, gap=120), L(k="dots", pts=[[700, 1100], [700, 900], [600, 700]], c="hot", n=3, speed=200, r=12)]
    return e + extra
save("ice-dams", "How ice dams leak into your ceiling", "Ice on the roof, water inside", ["water"], 2, 3.0, [
    S("In snowy climates, heat leaking from the house warms the roof and melts the snow from underneath.", "In snowy climates, heat leaking from the house warms the roof, and melts the snow from underneath.",
      idm([L(k="dots", pts=[[700, 620], [400, 890], [230, 1040]], c="water", n=5, speed=160, r=11, at=2.2)]), [[0, .5, .5, 1.0], [1, .42, .45, 1.2]], ["heat", "melts"]),
    S("The water runs down to the cold overhang, refreezes, and builds a ridge of ice.", "The water runs down to the cold overhang, refreezes, and builds a ridge of ice.",
      idm([L(k="dots", pts=[[700, 620], [400, 890], [230, 1040]], c="water", n=5, speed=160, r=11), L(k="circ", at_xy=[175, 1060], r=10, fill="ice", w=0),
           L(k="poly", pts=[[110, 1120], [180, 1030], [260, 1000], [250, 1080]], fill="ice", w=0, at=1.5), L(k="label", text="ICE DAM", xy=[320, 1240], anchor=[220, 1060], c="ice", at=2.2)]),
      [[0, .42, .45, 1.2], [1, .2, .62, 1.9]], ["refreezes,", "ice."]),
    S("More meltwater backs up behind the ice, works under the shingles, and drips into your walls and ceilings.", "More meltwater backs up behind the ice, works under the shingles, and drips into your walls and ceilings.",
      idm([L(k="poly", pts=[[110, 1120], [180, 1030], [260, 1000], [250, 1080]], fill="ice", w=0), L(k="level", box=[230, 980, 420, 1030], c="water", v0=0, v1=1, over=2),
           L(k="drops", at_xy=[360, 1110], c="water", n=10, spread=60, fall=420, at=2.4), L(k="hud", text="LEAKING INSIDE", c="red", at=2.6)]), [[0, .2, .62, 1.9], [1, .25, .68, 1.7]], ["backs", "up", "ceilings."]),
    S("The real fix is in the attic: air sealing, insulation and ventilation. Short term, pull snow off the lower roof with a roof rake, from the ground.", "The real fix is in the attic. Air sealing, insulation, and ventilation. Short term, pull snow off the lower roof with a roof rake, from the ground.",
      idm([L(k="level", box=[312, 1040, 1528, 1092], c=[236, 170, 200], dir="right", v0=0, v1=1, over=2), L(k="line", pts=[[60, 1700], [300, 1080]], c="yel", w=12, at=3.6),
           L(k="hud", text="SEAL · INSULATE · VENTILATE", c="green")], heat=False), [[0, .25, .68, 1.7], [.5, .5, .55, 1.0], [1, .3, .6, 1.3]], ["attic:", "rake,"], label="THE FIX", hold=.6)],
    ("Don’t climb up and hack at the ice. You’ll wreck the shingles, and you can fall. Ice dams are a symptom of heat escaping.", "Don't climb up and hack at the ice. You'll wreck the shingles, and you can fall. Ice dams are a symptom of heat escaping your house.", ["symptom"]),
    {"hook": "Those icicles look pretty. They might be leaking into your walls.", "feel": "An ice dam is your house telling you heat is escaping through the roof.",
     "shows": "How heat, snow and a cold overhang build an ice dam, how the water gets inside, and the real fix.", "ask": "Do you get big icicles on your gutters?"}, " #winterprep")

# ================================================================= washer hoses
def wh(state_extra, burst=False):
    e = [L(k="rect", box=[0, 1560, 1840, 1760], fill="soil", w=0, shadow=False), L(k="line", pts=[[0, 1560], [1840, 1560]], c="dim", w=10),
         L(k="rect", box=[300, 300, 760, 560], r=14, fill="panel", w=10), L(k="circ", at_xy=[420, 430], r=40, fill="red", w=0), L(k="circ", at_xy=[640, 430], r=40, fill=[58, 160, 255], w=0),
         L(k="text", text="VALVES", xy=[530, 240], center=True, c="dim", size=32),
         L(k="rect", box=[900, 700, 1560, 1560], r=30, fill="panel", w=16), L(k="circ", at_xy=[1230, 1160], r=230, w=14), L(k="circ", at_xy=[1230, 1160], r=170, c="dim", w=8),
         L(k="rect", box=[940, 740, 1520, 840], r=12, w=6, c="dim"), L(k="text", text="WASHER", xy=[1230, 1470], center=True, c="dim", size=36)]
    if not burst:
        e += [L(k="line", pts=[[420, 470], [420, 900], [940, 900]], c="red", w=26), L(k="line", pts=[[640, 470], [640, 820], [940, 820]], c=[58, 160, 255], w=26)]
    return e + state_extra
save("washer-hoses", "The $25 part behind a lot of flooded laundry rooms", "The $25 flood prevention", ["$25"], 1, 2.0, [
    S("Behind your washer are two supply hoses under constant water pressure, 24 hours a day.", "Behind your washer are two supply hoses, under constant water pressure, twenty four hours a day.",
      wh([L(k="label", text="SUPPLY HOSES", xy=[60, 1000], anchor=[420, 900], c="yel", at=1.4), L(k="hud", text="ALWAYS UNDER PRESSURE", c="yel", at=2.4)]), [[0, .5, .5, 1.0], [1, .35, .4, 1.6]], ["constant", "pressure,"]),
    S("Plain rubber hoses get brittle over time. One day one bursts, and it runs at full pressure until someone notices.", "Plain rubber hoses get brittle over time. One day one bursts, and it runs at full pressure until someone notices.",
      wh([L(k="line", pts=[[420, 470], [420, 900], [700, 900]], c="red", w=26), L(k="line", pts=[[780, 900], [940, 900]], c="red", w=26), L(k="line", pts=[[640, 470], [640, 820], [940, 820]], c=[58, 160, 255], w=26),
          L(k="circ", at_xy=[600, 900], r=34, fill="red", w=0, to=2.6), L(k="drops", at_xy=[740, 900], c="water", n=26, spread=420, fall=640, at=2.6), L(k="level", box=[0, 1500, 1840, 1560], c="water", v0=0, v1=1, over=2, at=3),
          L(k="hud", text="BURST", c="red", at=2.6)], burst=True), [[0, .35, .4, 1.6], [.6, .4, .55, 1.6], [1, .5, .65, 1.1]], ["brittle", "bursts,"]),
    S("State Farm says a failed hose can release around 650 gallons an hour. That’s a second-floor laundry room emptying into your kitchen.", "State Farm says a failed hose can release around six hundred fifty gallons an hour. That's a second floor laundry room, emptying into your kitchen.",
      wh([L(k="line", pts=[[420, 470], [420, 900], [700, 900]], c="red", w=26), L(k="line", pts=[[640, 470], [640, 820], [940, 820]], c=[58, 160, 255], w=26), L(k="drops", at_xy=[740, 900], c="water", n=26, spread=420, fall=640),
          L(k="level", box=[0, 1300, 1840, 1560], c="water", v0=.25, v1=1, over=4), L(k="count", fmt="{:.0f} GALLONS", v0=0, v1=650, over=4, xy=[920, 160], center=True, c="water", size=80), L(k="hud", text="ONE HOUR", c="red")], burst=True),
      [[0, .5, .65, 1.1], [1, .5, .45, 1.0]], ["650", "gallons"]),
    S("The fix: swap them for braided stainless hoses, about $25, and put a $15 leak sensor on the floor behind the washer.", "The fix. Swap them for braided stainless hoses, about twenty five dollars, and put a fifteen dollar leak sensor on the floor behind the washer.",
      wh([L(k="line", pts=[[420, 470], [420, 900], [940, 900]], c=[200, 200, 210], w=30), L(k="hatch", box=[400, 480, 440, 900], c=[120, 120, 130], gap=12, w=4), L(k="line", pts=[[640, 470], [640, 820], [940, 820]], c=[200, 200, 210], w=30),
          L(k="hatch", box=[620, 480, 660, 820], c=[120, 120, 130], gap=12, w=4), L(k="label", text="BRAIDED: ~$25", xy=[60, 1000], anchor=[420, 880], c="yel", at=.5),
          L(k="rect", box=[760, 1500, 860, 1556], r=20, fill="yel", w=0, at=3.2), L(k="label", text="LEAK SENSOR: ~$15", xy=[200, 1300], anchor=[800, 1500], c="yel", at=3.4), L(k="hud", text="$40 OF PREVENTION", c="green", at=4)], burst=True),
      [[0, .5, .45, 1.0], [.4, .32, .45, 1.5], [1, .4, .7, 1.4]], ["braided", "$25,", "$15"], label="THE FIX", hold=.6)],
    ("State Farm paid nearly $30 million in 2020 on washing machine hose claims. The average claim was about $10,200.", "State Farm paid nearly thirty million dollars in twenty twenty on washing machine hose claims. The average claim was about ten thousand two hundred dollars.", ["$30", "million", "$10,200."]),
    {"hook": "The cheapest flood insurance you can buy costs about $40.", "feel": "Rubber washer hoses don’t warn you before they burst.",
     "shows": "Why washer hoses fail, how much water a burst one releases, and the braided-hose plus leak-sensor fix. Prices are approximate.", "ask": "Are your washer hoses rubber or braided?"}, " #laundryroom")
