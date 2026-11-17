"""Batch 6: illustrated cutaways with a cover-off reveal (furnace, panel, toilet, attic, septic)."""
import json, re
S = 1.7
def P(x, y): return [round(x * S), round(y * S)]
def B(b): return [round(v * S) for v in b]
def C(t, x, y, z): return [t, x / 1080, y / 1920, z]
def wi(voice, word, after=0):
    ws = [re.sub(r"[^a-z0-9']", "", w.lower()) for w in voice.split()]
    for i in range(after, len(ws)):
        if ws[i] == word: return i
    raise ValueError((word, voice))
def ov(name, span, xs, **k): return dict({"k": "overlay", "img": f"assets/book/{name}-cover.png", "span": [round(span[0] * S), round(span[1] * S)], "xs": [round(xs[0] * S), round(xs[1] * S)]}, **k)
from PIL import ImageFont
_F = ImageFont.truetype("fonts/Inter-SemiBold.otf", 50)
def fit_tags(els, cam):                     # keep every label pill inside the frame the camera ends on
    _, cx, cy, z = cam[-1]; cx *= 1080; cy *= 1920
    vx0, vx1 = cx - 540 / z, cx + 540 / z
    for e in els:
        if e.get("k") != "tag": continue
        pw = (_F.getlength(e["text"]) + .06 * 50 * (len(e["text"]) - 1) + 90) / S; ph = 100 / S
        x, y = e["xy"][0] / S, e["xy"][1] / S
        x = min(max(x, vx0 + 30 / z), vx1 - pw - 30 / z)
        ylo, yhi = cy + (330 - 960) / z, cy + (1420 - 960) / z - ph
        y = min(max(y, ylo), yhi)
        e["xy"] = P(x, y)
    return els
def photo(name, els, text, cam, accent, voice=None):
    els = fit_tags(els, cam)
    return {"type": "photo", "state": {"img": f"assets/book/{name}.png", "scale": S, "els": els}, "text": text, "voice": voice or text, "cam": cam, "accent": accent}
def tag(text, xy, tgt, c, at, to=None, size=50):
    e = {"k": "tag", "text": text, "xy": P(*xy), "target": P(*tgt), "c": c, "at_word": at, "size": size}
    if to is not None: e["to_word"] = to
    return e
def focus(box, at, to=None):
    e = {"k": "focus", "box": B(box), "at_word": at}
    if to is not None: e["to_word"] = to
    return e
def flow(pts, c, at, n=8, speed=420):
    return {"k": "flow", "pts": [P(*p) for p in pts], "c": c, "n": n, "speed": speed, "size": 30, "at_word": at}
def hud(text, c, at): return {"k": "hud", "text": text, "c": c, "at_word": at}
def glow(xy, c, a, r=150, sy=.6, **k): return dict({"k": "glow", "at_xy": P(*xy), "r": r, "c": c, "a": a, "sy": sy}, **k)
BOOK = {"type": "book", "text": "That’s one page of the manual your house didn’t come with", "accent": ["manual"], "size": 96, "book_h": 700,
        "chips": ["34 CHAPTERS", "PAPERBACK + KINDLE"], "voice": "That's one page of the manual your house didn't come with. If this was news to you, the rest of the book will be too."}
TAGS = "#firsttimehomebuyer #newhomeowner #howitworks #homeownertips #homemaintenance #engineering"
def story(slug, title, cover, cacc, scenes, why, caption, hero_els):
    sc = scenes + [{"type": "quote", "label": "WHY IT MATTERS", "text": why[0], "voice": why[1], "accent": why[2], "count": why[3], "size": 78, "hold": .6}, BOOK, {"type": "end", "dur": 3.6}]
    d = {"slug": slug, "book": "house", "format": "X explainer (illustrated)", "title": title, "cover": cover, "cover_accent": cacc, "cover_sub": "How your house works",
         "hero": ["gx", {"img": scenes[0]["state"]["img"], "scale": S, "els": hero_els}], "hero_t": 2.0, "scenes": sc, "caption": caption}
    json.dump(d, open(f"stories/{slug}.json", "w"), indent=1); print(slug, len(sc))
BLUE, HOT, AIR = [120, 190, 255], [255, 150, 60], [170, 220, 255]

# ---------------- furnace
V = lambda s: s
F = "furnace"; o = lambda **k: ov(F, (395, 1760), (260, 835), **k); fl = glow((505, 905), [80, 140, 255], .8, r=170, sy=.45)
v3 = "Burners heat a sealed metal box called the heat exchanger. The flame and its exhaust stay inside it, and get vented outside."
v4 = "Below, a blower pulls in house air through the filter, pushes it across the hot exchanger, and up into your ducts."
v5 = "If that exchanger cracks, exhaust can leak into the air you breathe, including carbon monoxide."
v6 = "So get it inspected every year, change the filter, and keep a carbon monoxide alarm near the bedrooms."
story("house-ill-furnace", "How your furnace works, and the crack that matters", "The crack you can’t see", ["crack"], [
    photo(F, [o()], "This box in your basement lights a gas fire every time your heat kicks on.", [C(0, 540, 1000, 1.0), C(1, 540, 960, 1.08)], ["fire"]),
    photo(F, [fl, o(wipe_word=1, wipe_over=1.6)], "Here’s what’s inside.", [C(0, 540, 960, 1.08), C(1, 540, 1000, 1.0)], ["inside."], "Here's what's inside."),
    photo(F, [fl, focus((310, 820, 700, 1010), 0, wi(v3, "box")), tag("BURNERS", (720, 960), (600, 905), [120, 180, 255], 0, wi(v3, "box")),
              focus((295, 420, 710, 830), wi(v3, "box")), tag("HEAT EXCHANGER", (560, 330), (520, 520), "hot", wi(v3, "heat"))],
          v3, [C(0, 505, 900, 1.5), C(.3, 505, 640, 1.45), C(1, 505, 620, 1.5)], ["sealed", "exhaust"]),
    photo(F, [fl, focus((280, 1220, 710, 1710), 0, wi(v4, "through")), tag("BLOWER", (690, 1360), (520, 1460), AIR, wi(v4, "blower"), wi(v4, "through")),
              focus((280, 1100, 710, 1210), wi(v4, "through"), wi(v4, "pushes")), tag("FILTER", (700, 1020), (560, 1150), "yel", wi(v4, "filter"), wi(v4, "pushes")),
              flow([(470, 1600), (470, 1250), (650, 1150), (655, 820), (655, 450), (515, 330), (515, 40)], AIR, wi(v4, "pushes"), n=10),
              tag("WARM AIR TO DUCTS", (40, 160), (500, 200), HOT, wi(v4, "up"))],
          v4, [C(0, 480, 1450, 1.5), C(.35, 480, 1160, 1.5), C(.7, 500, 700, 1.1), C(1, 520, 560, 1.0)], ["blower", "filter", "ducts."]),
    photo(F, [fl, focus((295, 420, 710, 830), 0), glow((520, 620), [255, 70, 50], .7, r=120, sy=.8, at_word=wi(v5, "cracks")), hud("CRACKED EXCHANGER = CO RISK", "hot", wi(v5, "exhaust"))],
          "If that exchanger cracks, exhaust can leak into the air you breathe, including carbon monoxide (CO).", [C(0, 505, 620, 1.4), C(1, 505, 640, 1.6)], ["cracks,", "carbon", "monoxide"], v5),
    photo(F, [fl, hud("YEARLY TUNE-UP + CO ALARM", "green", 0)], "So get it inspected every year, change the filter, and keep a CO alarm near the bedrooms.",
          [C(0, 540, 1000, 1.05), C(1, 540, 960, 1.0)], ["every", "year,", "alarm"], v6)],
    ("Accidental carbon monoxide poisoning kills more than 400 Americans a year. You can’t see it or smell it.",
     "Accidental carbon monoxide poisoning kills more than four hundred Americans a year. You can't see it, and you can't smell it.", ["400", "see", "smell"], "SOURCE: CDC"),
    {"hook": "Your furnace lights a gas fire every time the heat kicks on.", "feel": "One part keeps that fire’s exhaust out of the air you breathe, and most people never think about it.",
     "shows": "How a gas furnace works: burners, heat exchanger, blower, filter. Plus the yearly check that matters. If a CO alarm ever goes off, get out and call 911.", "ask": "When was yours last inspected?", "tags": TAGS + " #hvac"},
    [fl, focus((295, 420, 710, 1010), 0)])

# ---------------- electrical panel
E_ = "panel"; o = lambda **k: ov(E_, (45, 1845), (185, 875), **k)
cover30 = [{"k": "rect", "box": B(b), "fill": [22, 22, 25], "w": 0, "shadow": False} for b in ((498, 279, 560, 309), (498, 420, 560, 450))]
lug = glow((528, 240), [140, 220, 255], .55, r=120, sy=.5)
v3 = "Power from the street comes in at the top and hits the main breaker, which can shut off the whole house."
v4 = "From there, metal bus bars carry power down to every breaker. Each breaker feeds one circuit in your house."
v5 = "Pull too much current and the wire heats up. The breaker trips first, before that wire can start a fire."
v6 = "If one keeps tripping, don't just keep flipping it back on. That's the circuit telling you something's wrong."
story("house-ill-panel", "How your breaker panel works", "What a breaker actually does", ["breaker"], [
    photo(E_, cover30 + [o()], "Every light, outlet and appliance in your house runs through this one gray box.", [C(0, 530, 960, 1.0), C(1, 530, 940, 1.08)], ["gray", "box."]),
    photo(E_, cover30 + [lug, o(wipe_word=1, wipe_over=1.6)], "Here’s what’s behind the door.", [C(0, 530, 940, 1.08), C(1, 530, 960, 1.0)], ["door."], "Here's what's behind the door."),
    photo(E_, cover30 + [lug, flow([(528, 0), (528, 250)], [140, 220, 255], 0, n=5, speed=300), focus((400, 180, 660, 480), wi(v3, "hits")),
                         tag("MAIN BREAKER", (690, 300), (600, 365), "yel", wi(v3, "main"))],
          v3, [C(0, 530, 260, 1.6), C(1, 530, 340, 1.7)], ["main", "breaker,", "whole"]),
    photo(E_, cover30 + [lug, focus((455, 460, 605, 1650), wi(v4, "metal"), wi(v4, "each")), flow([(530, 480), (530, 1600)], [255, 170, 80], wi(v4, "metal"), n=10),
                         tag("BUS BARS", (660, 700), (560, 800), [255, 170, 80], wi(v4, "bus"), wi(v4, "each")),
                         focus((415, 770, 645, 890), wi(v4, "each")), tag("ONE CIRCUIT", (690, 700), (620, 830), "green", wi(v4, "one"))],
          v4, [C(0, 530, 700, 1.3), C(.5, 530, 1000, 1.25), C(1, 530, 830, 1.6)], ["bus", "one", "circuit"]),
    photo(E_, cover30 + [lug, focus((415, 770, 645, 890), 0), glow((600, 830), [255, 60, 40], .75, r=110, sy=.7, at_word=wi(v5, "heats")),
                         hud("TRIPS BEFORE WIRES OVERHEAT", "yel", wi(v5, "trips"))],
          v5, [C(0, 530, 830, 1.6), C(1, 530, 830, 1.8)], ["too", "much", "first,"]),
    photo(E_, cover30 + [lug, hud("KEEPS TRIPPING? CALL AN ELECTRICIAN", "hot", 0)], "If one keeps tripping, don’t just keep flipping it back on. That’s the circuit telling you something’s wrong.",
          [C(0, 530, 900, 1.05), C(1, 530, 960, 1.0)], ["telling", "wrong."], v6)],
    ("Wiring, outlets, cords and lights start about 32,000 home fires a year.", "Wiring, outlets, cords and lights start about thirty-two thousand home fires a year.", ["32,000"], "SOURCE: NFPA, 2015–2019 AVERAGE"),
    {"hook": "Every outlet in your house runs through one gray box.", "feel": "Most people only open it when the power’s already out.",
     "shows": "How a breaker panel works: main breaker, bus bars, one breaker per circuit, and why a breaker that keeps tripping is a warning, not a nuisance. Panel work is a job for a licensed electrician.", "ask": "Is your panel labeled?", "tags": TAGS + " #electrical"},
    cover30 + [lug])

# ---------------- toilet
T = "toilet"; o = lambda **k: ov(T, (30, 960), (140, 1080), **k)
v3 = "The handle pulls a chain that lifts the flapper, and the tank's water rushes into the bowl."
v4 = "As the water drops, the float drops with it and opens the fill valve, which refills the tank."
v5 = "If the water gets too high, it spills into the overflow tube and down into the bowl, not onto your floor."
v6 = "When a toilet keeps running, it's usually a worn-out flapper. That's a cheap part you can swap yourself."
story("house-ill-toilet", "How your toilet works, and why it keeps running", "Why your toilet keeps running", ["running"], [
    photo(T, [o()], "You use it every day. But what actually happens when you push the handle?", [C(0, 540, 900, 1.0), C(1, 540, 780, 1.12)], ["handle?"]),
    photo(T, [o(wipe_word=1, wipe_over=1.4)], "Let’s take the lid off.", [C(0, 540, 780, 1.12), C(1, 540, 620, 1.25)], ["off."], "Let's take the lid off."),
    photo(T, [focus((200, 300, 650, 940), wi(v3, "chain")), tag("FLAPPER", (640, 960), (535, 885), "yel", wi(v3, "flapper")),
              flow([(535, 900), (535, 1180)], BLUE, wi(v3, "rushes"), n=6, speed=380)],
          v3, [C(0, 300, 420, 1.5), C(.35, 450, 650, 1.45), C(1, 535, 900, 1.35)], ["flapper,", "rushes"]),
    photo(T, [focus((300, 270, 470, 730), wi(v4, "float")), tag("FILL VALVE", (520, 560), (390, 520), BLUE, wi(v4, "fill")),
              flow([(388, 720), (388, 330)], BLUE, wi(v4, "refills"), n=6, speed=300)],
          v4, [C(0, 420, 560, 1.45), C(1, 395, 520, 1.7)], ["float", "fill", "valve,"]),
    photo(T, [focus((615, 250, 725, 900), wi(v5, "overflow")), tag("OVERFLOW TUBE", (200, 230), (650, 290), "green", wi(v5, "overflow")),
              flow([(670, 290), (670, 880)], AIR, wi(v5, "down"), n=7, speed=360)],
          v5, [C(0, 600, 450, 1.4), C(1, 665, 560, 1.55)], ["overflow", "floor."]),
    photo(T, [focus((455, 830, 615, 935), 0), hud("RUNNING TOILET? CHECK THE FLAPPER", "green", wi(v6, "wornout"))],
          "When a toilet keeps running, it’s usually a worn-out flapper. That’s a cheap part you can swap yourself.", [C(0, 535, 870, 1.6), C(1, 535, 880, 1.8)], ["worn-out", "cheap"], v6)],
    ("A leaky toilet can waste about 200 gallons of water every single day.", "A leaky toilet can waste about two hundred gallons of water, every single day.", ["200", "gallons"], "SOURCE: EPA WATERSENSE"),
    {"hook": "Ever wondered what actually happens when you flush?", "feel": "A running toilet sounds harmless. Your water bill disagrees.",
     "shows": "How a toilet tank works: handle, chain, flapper, fill valve, overflow tube. And the cheap part behind most running toilets.", "ask": "Got one that won’t stop running?", "tags": TAGS + " #plumbing101"},
    [focus((150, 190, 925, 955), 0)])

# ---------------- attic
A_ = "attic"; o = lambda **k: ov(A_, (190, 1375), (0, 1080), **k)
v3 = "Cool outside air comes in low, through vents under the eaves called soffit vents."
v4 = "It warms up, rises, and carries heat and moisture out through the ridge vent at the very top."
v5 = "Down on the attic floor, insulation keeps your home's heat downstairs, where you paid for it."
v6 = "Block those vents or skimp on insulation, and you get trapped moisture, mold, and ice dams."
up = lambda at: [flow([(100, 1050), (190, 900), (430, 700), (590, 430), (612, 240)], AIR, at, n=9, speed=380), flow([(1015, 1065), (950, 900), (790, 700), (640, 430), (618, 240)], AIR, at, n=9, speed=380)]
story("house-ill-attic", "How your attic breathes", "Your attic has to breathe", ["breathe"], [
    photo(A_, [o()], "From outside, it’s just a roof. But the space under it decides how long that roof lasts.", [C(0, 540, 820, 1.0), C(1, 560, 780, 1.08)], ["how", "long"]),
    photo(A_, [o(wipe_word=1, wipe_over=1.6)], "Here’s what’s happening up there.", [C(0, 560, 780, 1.08), C(1, 540, 800, 1.0)], ["up", "there."], "Here's what's happening up there."),
    photo(A_, [flow([(100, 1110), (100, 960)], AIR, wi(v3, "comes"), n=4, speed=260), focus((0, 890, 240, 1080), wi(v3, "low")),
               tag("SOFFIT VENT", (280, 1120), (110, 990), AIR, wi(v3, "soffit"))],
          v3, [C(0, 300, 980, 1.5), C(1, 220, 990, 1.7)], ["soffit", "vents."]),
    photo(A_, up(0) + [focus((450, 170, 790, 450), wi(v4, "through")), tag("RIDGE VENT", (40, 260), (560, 300), AIR, wi(v4, "ridge"))],
          v4, [C(0, 560, 820, 1.05), C(.6, 615, 360, 1.5), C(1, 615, 330, 1.65)], ["rises,", "ridge", "vent"]),
    photo(A_, up(0) + [focus((0, 1095, 1080, 1370), wi(v5, "attic")), tag("INSULATION", (60, 1420), (420, 1230), [255, 170, 190], wi(v5, "insulation")),
               glow((540, 1450), [255, 150, 60], .45, r=260, sy=.35, at_word=wi(v5, "heat"))],
          v5, [C(0, 540, 1180, 1.25), C(1, 540, 1240, 1.4)], ["insulation", "downstairs,"]),
    photo(A_, [hud("BLOCKED VENTS = MOLD + ICE DAMS", "hot", 0)], "Block those vents or skimp on insulation, and you get trapped moisture, mold, and ice dams.",
          [C(0, 540, 760, 1.1), C(1, 540, 820, 1.0)], ["moisture,", "mold,", "ice", "dams."], v6)],
    ("Sealing air leaks and insulating the attic cuts heating and cooling costs by about 15% on average.",
     "Sealing air leaks and insulating the attic cuts heating and cooling costs by about fifteen percent, on average.", ["15%"], "SOURCE: ENERGY STAR (EPA)"),
    {"hook": "Your roof’s lifespan is decided in a room you never go into.", "feel": "Bad airflow up there shows up later as mold, ice dams and higher bills.",
     "shows": "How attic ventilation works: soffit vents in, ridge vent out, insulation on the floor. Plus what happens when it’s blocked.", "ask": "Have you ever been up in yours?", "tags": TAGS + " #roofing"},
    up(0))

# ---------------- septic
SP = "septic"; o = lambda **k: ov(SP, (235, 1920), (0, 1080), **k)
v3 = "Wastewater flows from the house into a buried tank. Solids sink to the bottom as sludge, and grease floats to the top as scum."
v4 = "The clearer liquid in the middle flows out to the drain field, where the soil filters it."
v5 = "But sludge keeps piling up. Skip the pumping, and solids escape into the drain field and clog it."
story("house-ill-septic", "How a septic system works", "What’s under your yard", ["yard"], [
    photo(SP, [o()], "If your house isn’t on city sewer, everything you flush ends up right here, in your yard.", [C(0, 540, 760, 1.0), C(1, 540, 700, 1.1)], ["your", "yard."],
          "If your house isn't on city sewer, everything you flush ends up right here, in your yard."),
    photo(SP, [o(wipe_word=1, wipe_over=1.8)], "Let’s dig in.", [C(0, 540, 700, 1.1), C(1, 540, 960, 1.0)], ["dig"], "Let's dig in."),
    photo(SP, [flow([(300, 200), (300, 600)], [200, 200, 200], 0, n=5, speed=300), focus((145, 450, 950, 1140), wi(v3, "into")),
               tag("SCUM", (40, 560), (420, 645), "yel", wi(v3, "grease")), tag("SLUDGE", (40, 1160), (420, 1000), "brown", wi(v3, "sludge"))],
          v3, [C(0, 380, 360, 1.3), C(.35, 540, 820, 1.2), C(1, 520, 820, 1.3)], ["sludge,", "scum."]),
    photo(SP, [focus((560, 600, 940, 905), 0, wi(v4, "drain")), flow([(745, 640), (1060, 728)], AIR, wi(v4, "flows"), n=5, speed=260),
               focus((80, 1540, 1010, 1790), wi(v4, "drain")), tag("DRAIN FIELD", (300, 1400), (540, 1610), "green", wi(v4, "drain")),
               flow([(130, 1612), (990, 1612)], AIR, wi(v4, "soil"), n=8, speed=300), flow([(130, 1712), (990, 1712)], AIR, wi(v4, "soil"), n=8, speed=300)],
          v4, [C(0, 740, 760, 1.35), C(.45, 600, 1200, 1.1), C(1, 540, 1650, 1.3)], ["drain", "field,", "filters"]),
    photo(SP, [focus((210, 880, 895, 1085), 0), {"k": "spots", "box": B((215, 860, 890, 1075)), "n": 260, "r": 7, "c": "brown", "over": 3.0},
               hud("PUMP EVERY 3 TO 5 YEARS", "yel", wi(v5, "skip"))],
          v5, [C(0, 540, 960, 1.3), C(1, 540, 980, 1.45)], ["piling", "clog"])],
    ("Pumping runs about $250 to $500 every 3 to 5 years. Replacing a failed system: $5,000 to $15,000.",
     "Pumping runs about two hundred fifty to five hundred dollars every three to five years. Replacing a failed system costs five to fifteen thousand.", ["$5,000", "$15,000."], "SOURCE: EPA"),
    {"hook": "On a septic system? Everything you flush stays on your property.", "feel": "It’s out of sight, so it’s out of mind, right up until it backs up.",
     "shows": "How a septic tank works: sludge, scum, the drain field, and why pumping every few years beats replacing the whole system.", "ask": "Do you know when yours was last pumped?", "tags": TAGS + " #septic"},
    [focus((145, 450, 950, 1140), 0)])
