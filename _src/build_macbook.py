#!/usr/bin/env python3
"""Builds macbook-pro.html and macbook/*.html. Run: python3 _src/build_macbook.py
(importing build also rebuilds the Mac mini pages)."""
from build import page, table, spec, bars, path, stats, sec, notes

READ = "November 8, 2026"
CUR = "macbook-pro.html"
MB = ("node", "MacBook Pro", "Mac17,9 · M5 Pro", "../macbook-pro.html")
DOCK = ("node", "Anker Prime dock", "Thunderbolt 5", "anker-dock.html")
UP = ("wire", "80 Gb/s", "tb")
HUB3 = ("node", "Dock USB 3 hub", "one 10 Gb/s uplink", None)

D = []

# ---------------------------------------------------------------- Anker dock
D.append(dict(
    slug="anker-dock", name="Anker Prime", em="Thunderbolt 5 dock", group="Dock", bus="tb", spd="80 Gb/s uplink",
    card="Anker Prime 14-in-1 Thunderbolt 5 docking station. One cable carries power, both monitors, wired network, a backup drive and the camera.",
    lede="One cable to the MacBook. An Anker Prime 14-in-1 Thunderbolt 5 docking station with its power supply built in, linked at the full 80 Gb/s.",
    path=[MB, UP, ("node", "Anker Prime dock", "USB4 v2 mode · fw 64.1", "me")],
    stats=[("80", "Gb/s", "link to the MacBook"), ("14", "ports", "on the box"), ("140", "W", "charging, rated"), ("10", "Gb/s", "shared by all its USB")],
    body=[
        sec("What it is", spec([
            ("Model", "Anker Prime TB5 Docking Station, 14-in-1 (A83B5)"),
            ("Firmware", "64.1"),
            ("Link to the MacBook", "80 Gb/s in USB4 v2 mode, on the MacBook's Thunderbolt bus 0, receptacle 1"),
            ("Power", "Built-in power supply, no brick. Rated to charge the laptop at up to 140 W."),
            ("Size", "116 × 116 × 75 mm, about 1.1 kg"),
            ("USB 3 inside", 'Intel hub <span class="mono">8087:5787</span> feeding two VIA VL822 hubs'),
            ("USB 2 inside", 'Fresco Logic hub <span class="mono">1d5c:5801</span> feeding two VIA 2822 hubs'),
        ]),
            '<p class="note-t">Rated figures come from Anker\'s published specifications. Everything else is what macOS reported.</p>'),
        sec("Its ports, and what is in them", table(["Port", "Where", "Rated", "In use"], [
            ("Thunderbolt 5 upstream", "back", "80 Gb/s, 120 Gb/s boost, 140 W", "The MacBook, at 80 Gb/s"),
            ("Thunderbolt 5 downstream ×2", "back", "Up to 120 Gb/s", 'One carries the <a href="displays.html">KTC H24T7</a> display. The other is free. macOS lists displays under the graphics chip, so it shows both ports as empty.'),
            ("HDMI 2.1 / DisplayPort 2.1", "back", "One at a time", 'The <a href="displays.html">Dell S2425HS</a>, over HDMI'),
            ("Ethernet", "back", "2.5 Gb/s", '<a href="network.html">Realtek RTL8156</a>, en8, 2500Base-T full duplex'),
            ("USB-A ×2", "back", "10 Gb/s each", '<a href="seagate-backup.html">Seagate hard drive</a> (5 Gb/s) and the Lenovo camera (480 Mb/s). macOS does not report which socket each uses.'),
            ("USB-C ×2, USB-A ×1", "front", "10 Gb/s each, 45 W across the two USB-C", "See the row above"),
            ("SD and TF", "side", "—", 'Card reader <span class="mono">(Genesys Logic 05e3:0764)</span>, 5 Gb/s, no card'),
            ("Audio", "front", "—", "Not checked"),
            ("AC in", "back", "—", "Mains power"),
        ])),
        sec("One hub behind every USB port", '<p>Inside the dock, every USB port, the 2.5 Gb Ethernet and the card reader share one 10 Gb/s USB 3 uplink. That is a small slice of the 80 Gb/s cable, and it is the real limit for anything plugged into the dock\'s USB sockets.</p>',
            '<p>It is why the <a href="sandisk-backup.html">SanDisk backup SSD</a> moved off the dock to its own MacBook port: its backups no longer share that uplink with the wired network, and it runs faster in both directions.</p>'),
        sec("The dock before this one", '<p>Until early November this desk used a Wavlink WL-UTD58 Thunderbolt 5 dock. That dock now serves the <a href="../devices/wavlink-dock.html">Mac mini</a>, where its own power supply lets two NVMe enclosures run at once.</p>'),
    ]))

# ---------------------------------------------------------------- SanDisk
D.append(dict(
    slug="sandisk-backup", name="SanDisk SSD", em="1 TB backup", group="Storage", bus="usb", spd="10 Gb/s USB",
    card="SanDisk SSD 1 TB on the MacBook's own port. The portable Time Machine disk, faster since it left the dock.",
    lede="The backup that travels. A SanDisk 1 TB portable SSD used by Time Machine, plugged straight into the MacBook instead of the dock.",
    path=[MB, ("wire", "own port · 10 Gb/s", "usb"), ("node", "SanDisk SSD 1 TB", "SANDISK TIMEMACHINE", "me")],
    stats=[("845", "MB/s", "write"), ("813", "MB/s", "read"), ("366", "GiB", "used of 931"), ("10", "Gb/s", "USB link")],
    body=[
        sec("The drive", spec([
            ("Drive", 'SanDisk SSD 1 TB, portable <span class="mono">(0781:5504)</span>'),
            ("Link", "USB 10 Gb/s, the most the drive offers"),
            ("Where", "One of the MacBook's own ports (receptacle 2 or 3; macOS does not say which)"),
            ("Volume", "SANDISK TIMEMACHINE. 366 GiB used of 931 GiB."),
            ("Job", "Time Machine destination, chosen because it is small and tough enough to travel. Latest backup November 8, 2026 at 4:43 PM."),
        ])),
        sec("Dock against the MacBook's own port", bars([
            ("On the dock", "Nov 7", 794, 702, "usb"),
            ("Own MacBook port", "Nov 7, late evening", 845, 813, "usb"),
        ], 1250),
            '<p class="note-t">8 GiB sequential, three runs each, write includes sync, read after a cache purge, no backup running. The own-port figures are the middle of 842 to 847 write and 812 to 814 read. The bar scale ends at 1,250 MB/s, the ceiling of a 10 Gb/s USB link.</p>',
            '<p>The drive is faster on its own port in both directions, and its backups no longer compete with the wired network for the dock\'s single USB uplink.</p>'),
        sec("Earlier: cables and sockets", '<p class="note-t">8 GB write and read back on October 17 and 19, on the Wavlink dock that was here then.</p>',
            table(["Connection", "Write", "Read"], [
                ("MacBook's own Thunderbolt port, new cable", "~783 MB/s", "~769 MB/s"),
                ("Dock USB-A, retest, no backup copying", "~779 MB/s", "~702 MB/s"),
                ("Dock rear USB-A, non-SanDisk cable and adapter", "~712-725 MB/s", "~661-668 MB/s"),
                ("Dock front USB-A, same cable", "~730 MB/s", "~584 MB/s"),
                ("Dock USB-A, SanDisk's own cable and adapter", "~446 MB/s", "~682 MB/s"),
            ], num=(1, 2)),
            '<p>The cable made the difference. On the dock\'s USB-A ports a different cable raised the write speed from about 450 to about 720 MB/s.</p>'),
    ]))

# ---------------------------------------------------------------- Seagate
D.append(dict(
    slug="seagate-backup", name="Seagate Expansion", em="2 TB backup", group="Storage", bus="usb5", spd="5 Gb/s USB",
    card="Seagate Expansion 2 TB portable hard drive on the dock. The second Time Machine disk.",
    lede="The second backup. A Seagate Expansion 2 TB portable hard drive on the dock's USB hub, used only by Time Machine.",
    path=[MB, UP, DOCK, ("wire", "USB hub · 5 Gb/s", "usb5"), ("node", "Seagate Expansion 2 TB", "MacBook Backup", "me")],
    stats=[("701", "GiB", "used of 1.8 TiB"), ("5", "Gb/s", "USB link"), ("5,400", "rpm", "drive inside")],
    body=[
        sec("The drive", spec([
            ("Drive", "Seagate Expansion 2 TB portable hard drive"),
            ("Disk inside", 'Seagate <span class="mono">ST2000LM007</span>: 2.5-inch, 7 mm, 5,400 rpm, two 1 TB shingled (SMR) platters, 128 MB cache'),
            ("Rated speed", "Up to 140 MB/s"),
            ("Link", "USB 5 Gb/s, on one of the dock's USB sockets"),
            ("Volume", "MacBook Backup. 701 GiB used of 1.8 TiB."),
            ("Job", "Time Machine destination that stays at the desk."),
        ]),
            '<p class="note-t">Disk details are Seagate\'s published figures for the ST2000LM007. Its speed has not been measured here.</p>'),
        sec("Things to know", notes([
            "Shingled drives write quickly in bursts and slow down on long rewrites. Time Machine's hourly backups suit that well.",
            'It shares the dock\'s USB uplink with the wired network. At hard drive speeds that does not matter, which is why this one stayed on the dock and the <a href="sandisk-backup.html">SanDisk SSD</a> moved off.',
        ])),
    ]))

# ---------------------------------------------------------------- Displays
D.append(dict(
    slug="displays", name="Displays", em="KTC and Dell", group="Displays", bus="hdmi", spd="144 Hz + 100 Hz",
    card="The same two monitors as the Mac mini: KTC H24T7 at 1440p and 144 Hz, Dell S2425HS at 1080p and 100 Hz.",
    lede="Two monitors on the dock: the KTC on one of its Thunderbolt 5 ports and the Dell on its HDMI port. Both are shared with the Mac mini.",
    path=[MB, UP, DOCK, ("wire", "TB5 port · HDMI", "hdmi"), ("node", "KTC H24T7 · Dell S2425HS", "KTC on Thunderbolt 5, Dell on HDMI", "me")],
    stats=[("1440p", "144 Hz", "KTC H24T7, main"), ("1080p", "100 Hz", "Dell S2425HS")],
    body=[
        sec("What the MacBook sees", table(["Display", "Role", "Running at", "Against its maximum"], [
            ('<a href="../devices/ktc-h24t7.html">KTC H24T7</a>', "Main", "2560×1440 at 144 Hz", "Below the panel's 180 Hz, which the Mac mini reaches over DisplayPort"),
            ('<a href="../devices/dell-s2425hs.html">Dell S2425HS</a>', "Second", "1920×1080 at 100 Hz", "The panel's maximum"),
        ]),
            '<p class="note-t">Panel details for each monitor are on its Mac mini page.</p>'),
        sec("How they are connected", table(["Display", "Dock port", "Notes"], [
            ("KTC H24T7", "Thunderbolt 5 downstream", "Leaves the dock\'s second Thunderbolt 5 port free"),
            ("Dell S2425HS", "HDMI 2.1", "The dock\'s DisplayPort output stays unused, since the box says HDMI and DisplayPort cannot run together"),
        ]),
            '<p class="note-t">macOS lists displays under the graphics chip, not under Thunderbolt, so it shows the dock\'s Thunderbolt 5 ports as empty even with the KTC on one.</p>'),
        sec("Sharing with the Mac mini", '<p>The Mac mini drives the same two monitors on their other inputs: the KTC over DisplayPort at 180 Hz and the Dell over HDMI at 100 Hz. Switching a monitor\'s input moves it from one computer to the other.</p>'),
    ]))

# ---------------------------------------------------------------- Network
D.append(dict(
    slug="network", name="Network", em="wired through the dock", group="Network", bus="net", spd="2.5 Gb/s Ethernet",
    card="2.5 Gb Ethernet through the dock's Realtek adapter. 1.47 Gb/s down and 1.98 Gb/s up in the last test, with Wi-Fi 7 as the fallback.",
    lede="How the MacBook reaches the network. The dock's 2.5 Gb Ethernet port is the default route, with Wi-Fi 7 behind it.",
    path=[MB, UP, DOCK, ("wire", "USB hub · 5 Gb/s", "usb5"), ("node", "Realtek RTL8156", "en8 · 2500Base-T", "me"), ("wire", "Ethernet", "net"), ("node", "Home network", "", None)],
    stats=[("1.47", "Gb/s", "down"), ("1.98", "Gb/s", "up"), ("10.9", "ms", "idle ping")],
    body=[
        sec("The wired link", spec([
            ("Adapter", "Realtek RTL8156, built into the dock, on its USB 3 hub at 5 Gb/s"),
            ("Interface", "en8"),
            ("Negotiated", "2500Base-T, full duplex. That is the port's top speed."),
            ("Role", "Default route"),
        ])),
        sec("Last speed test", table(["Interface", "Link", "Down", "Up", "Idle ping"], [
            ("en8 · wired", "2.5GbE through the dock", "1.47 Gb/s", "1.98 Gb/s", "10.9 ms"),
            ("en0 · Wi-Fi 7", "5 GHz, channel 36, 80 MHz, 1080 Mb/s link, −34 dBm", "161.8 Mb/s", "214.6 Mb/s", "14.3 ms"),
        ], num=(2, 3, 4)),
            f'<p class="note-t">Measured {READ}. On Wi-Fi, responsiveness under load was low (511 ms). The Mac mini, on its own Ethernet port, measured about 2.1 Gb/s each way the same day.</p>',
            '<p>Wired through the dock is about nine times faster than Wi-Fi here. Download runs below upload, and below the Mac mini\'s 2.1 Gb/s. Drives were slower on the dock too. There are two candidates, not yet tested apart. One is video: both monitors run through the dock, and display traffic is reserved ahead of data on the Thunderbolt link. The other is that the dock\'s Ethernet is a USB adapter sharing one 10 Gb/s uplink with the dock\'s other USB devices. Moving the KTC to one of the MacBook\'s own ports and retesting would tell them apart.</p>'),
        sec("Earlier tests", table(["Date", "Down", "Up", "Idle latency"], [
            ("Nov 8, 2026", "1.47 Gb/s", "1.98 Gb/s", "10.9 ms"),
            ("Oct 19, 2026", "1.74 Gb/s", "2.11 Gb/s", "12 ms"),
            ("Oct 19, 2026, earlier", "1.60 Gb/s", "2.00 Gb/s", "—"),
        ], num=(1, 2, 3)),
            '<p class="note-t">All wired. The October tests ran through the Wavlink dock that was here then, which uses the same Realtek adapter chip.</p>'),
        sec("Link to the Mac mini", '<p>The two Macs normally talk over the home network. A direct Thunderbolt cable between them linked at 40 Gb/s in a test on November 7. It is unplugged now.</p>'),
    ]))

names = {d["slug"]: d["name"] for d in D}
for i, d in enumerate(D):
    prev, nxt = D[i - 1], D[(i + 1) % len(D)]
    hero = (f'<div class="eyebrow"><a href="../macbook-pro.html">Mac Work Book Pro</a> / {d["group"]} / <b>{d["spd"]}</b></div>\n'
            f'<h1>{d["name"]} <em>{d["em"]}</em></h1>\n<p class="lede">{d["lede"]}</p>\n{path(d["path"])}\n{stats(d["stats"])}')
    pager = (f'<div class="pager"><a href="{prev["slug"]}.html">&larr; {prev["name"]}</a>'
             f'<a href="../macbook-pro.html">All devices</a><a href="{nxt["slug"]}.html">{nxt["name"]} &rarr;</a></div>')
    foot = f'<p class="note-t">Read from macOS on the MacBook Pro, {READ}.</p>'
    page(f'macbook/{d["slug"]}.html', f'{d["name"]} · Mac Work Book Pro', d["card"], d["bus"], hero,
         "\n".join(d["body"]) + "\n" + foot + "\n" + pager, cur=CUR)

# ================================================================= hub diagram
def box(x, y, w, h, t1, t2, tm="", cls="node"):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" class="{cls}"/><text x="{x+14}" y="{y+25}" class="t1">{t1}</text><text x="{x+14}" y="{y+44}" class="t2">{t2}</text>'
    return o + (f'<text x="{x+14}" y="{y+62}" class="tm">{tm}</text>' if tm else "")

def line(x1, y1, x2, y2, cls, label="", lc="", lx=None, ly=None):
    o = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="ln {cls}"/>'
    if label:
        o += f'<text x="{lx if lx is not None else (x1+x2)/2}" y="{ly if ly is not None else y1-9}" class="lbl {lc}" text-anchor="middle">{label}</text>'
    return o

R = 760
svg = ['<svg viewBox="0 0 1160 640" role="img" aria-labelledby="mbT"><title id="mbT">Port map: one Thunderbolt 5 cable links the MacBook Pro to the Anker dock, which carries the displays, a backup hard drive, wired Ethernet, the card reader and the camera. The SanDisk backup SSD is on the MacBook\'s own port.</title>']
svg += [line(280, 250, 430, 250, "l-tb", "80 Gb/s", "c-tb"), '<text x="355" y="272" class="lbl2" text-anchor="middle">USB4 v2 mode</text>',
        line(155, 430, 155, 520, "l-u10", "10 Gb/s", "c-u10", 195, 482),
        line(280, 340, 332, 340, "l-free"), '<text x="338" y="344" class="lbl2">free</text>',
        line(660, 79, R, 79, "l-dp", "TB5 port", "c-dp"), line(660, 149, R, 149, "l-hdmi", "HDMI", "c-hdmi"),
        line(660, 257, R, 257, "l-u5", "5 Gb/s", "c-u5"), line(660, 327, R, 327, "l-u5", "5 Gb/s", "c-u5"),
        line(660, 397, R, 397, "l-u5", "5 Gb/s", "c-u5"), line(660, 527, R, 527, "l-u2", "480 Mb/s", "c-u2")]
svg += ['<rect x="30" y="170" width="250" height="260" rx="14" class="node mini"/>',
        '<text x="48" y="212" class="t-big">MacBook Pro</text><text x="48" y="234" class="t2">M5 Pro · Mac17,9 · 48 GB</text>',
        '<text x="48" y="286" class="t2">Internal 1 TB SSD</text><text x="48" y="304" class="t2">Wi-Fi 7 as fallback</text>',
        '<text x="270" y="254" class="tag" text-anchor="end">TB rec. 1</text><text x="270" y="344" class="tag" text-anchor="end">TB port</text><text x="155" y="420" class="tag" text-anchor="middle">own port</text>',
        box(30, 520, 330, 76, "SanDisk SSD 1 TB · SANDISK TIMEMACHINE", "Time Machine · on the MacBook's own port", "moved off the dock"),
        '<rect x="430" y="30" width="230" height="580" rx="14" class="node dock"/>',
        '<text x="448" y="62" class="t-big" style="font-size:18px">Anker Prime dock</text><text x="448" y="84" class="t2">Thunderbolt 5 · 14-in-1</text>',
        '<rect x="446" y="100" width="192" height="64" rx="8" class="sub"/><text x="460" y="126" class="t1">HDMI 2.1 | DP 2.1</text><text x="460" y="146" class="t2">one at a time</text>',
        '<rect x="446" y="200" width="192" height="240" rx="8" class="sub"/><text x="460" y="226" class="t1">USB 3 hub · 10 Gb/s</text><text x="460" y="290" class="tm">Intel 8087:5787</text><text x="460" y="306" class="tm">→ VIA VL822 ×2</text><text x="460" y="356" class="t2">One uplink for every</text><text x="460" y="374" class="t2">USB port, Ethernet</text><text x="460" y="392" class="t2">and the card reader</text>',
        '<rect x="446" y="480" width="192" height="94" rx="8" class="sub"/><text x="460" y="506" class="t1">USB 2 side</text><text x="460" y="540" class="tm">Fresco 1d5c:5801</text><text x="460" y="556" class="tm">→ VIA 2822 ×2</text>',
        '<text x="448" y="600" class="tm">1 TB5 downstream port free</text>',
        box(R, 50, 385, 58, "KTC H24T7 · main display", "1440p at 144 Hz · on a dock Thunderbolt 5 port"),
        box(R, 120, 385, 58, "Dell S2425HS", "1080p at 100 Hz · on the dock's HDMI port"),
        box(R, 228, 385, 58, "Seagate Expansion 2 TB · MacBook Backup", "Time Machine · hard drive"),
        box(R, 298, 385, 58, "Realtek 2.5G LAN → home network", "RTL8156 · en8 · 2500Base-T · default route"),
        box(R, 368, 385, 58, "Card reader", "SD and TF · Genesys Logic · no card"),
        box(R, 498, 385, 58, "Lenovo camera", "USB 2")]
HITS = [("anker-dock", "tb", 430, 30, 230, 64), ("sandisk-backup", "usb", 30, 520, 330, 76), ("displays", "hdmi", R, 50, 385, 58), ("displays", "hdmi", R, 120, 385, 58),
        ("seagate-backup", "usb5", R, 228, 385, 58), ("network", "net", R, 298, 385, 58)]
svg += [f'<a href="macbook/{s}.html" class="b-{b}" aria-label="{names[s]}"><rect class="hit" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></a>' for s, b, x, y, w, h in HITS]
svg.append("</svg>")
KEYS = [("tb", "Thunderbolt 5, 80 Gb/s"), ("dp", "Display over Thunderbolt 5"), ("hdmi", "HDMI"), ("usb", "USB 10 Gb/s"), ("usb5", "USB 5 Gb/s"), ("usb2", "USB 2")]
fig = ('<figure class="wiring"><div class="dscroll">' + "".join(svg) + '</div><figcaption>'
       + "".join(f'<span class="key b-{b}"><i></i>{t}</span>' for b, t in KEYS)
       + '<span>macOS does not report which USB socket each device uses. Select a device to open its page.</span></figcaption></figure>')

cards = ""
for g in ["Dock", "Storage", "Displays", "Network"]:
    cards += f'<div class="grp">{g}</div><div class="grid">' + "".join(
        f'<a class="card b-{d["bus"]}" href="macbook/{d["slug"]}.html"><span class="spd">{d["spd"]}</span><b>{d["name"]} {d["em"]}</b><span>{d["card"]}</span><span class="go">Details &rarr;</span></a>'
        for d in D if d["group"] == g) + "</div>\n"

L = lambda s, t: f'<a href="macbook/{s}.html">{t}</a>'
OK = '<span class="okk">✓ max</span>'
hub = "\n".join([
    f'<section><h2>What is plugged into what</h2>{fig}</section>',
    f'<section><h2>The devices</h2><p class="note-t">Each one has its own page: what it is, the path its signal takes from the MacBook, and what it measured.</p>{cards}</section>',
    sec("The machine", spec([
        ("Model", "MacBook Pro (Mac17,9)"),
        ("Chip", "Apple M5 Pro: 18-core CPU (6 Super, 12 Performance), 20-core GPU"),
        ("Memory and storage", "48 GB, 1 TB internal SSD (AP1024Z), 336 of 926 GiB used"),
        ("Thunderbolt", "3 Thunderbolt 5 ports, up to 120 Gb/s. One holds the dock, one the SanDisk SSD, one is free."),
        ("Power", "Charged through the dock's cable"),
        ("Wireless", "Wi-Fi 7"),
    ])),
    sec("Every link, against its maximum", '<p class="note-t">The most each port allows, next to what macOS reports as negotiated.</p>',
        table(["Connection", "Chip", "Port maximum", "Negotiated", ""], [
            ("MacBook → " + L("anker-dock", "Anker dock") + '<br><span class="sub">TB bus 0, receptacle 1</span>', "Anker TB5 dock, fw 64.1", "80 Gb/s (TB5, 120 Gb/s boost)", "80 Gb/s, USB4 v2 mode", OK),
            (L("displays", "KTC H24T7") + ' · main display<br><span class="sub">Dock Thunderbolt 5 port</span>', "—", "—", "1440p at 144 Hz", '<span class="okk">✓</span>'),
            (L("displays", "Dell S2425HS") + '<br><span class="sub">Dock HDMI port</span>', "—", "1080p at 100 Hz (panel max)", "1080p at 100 Hz", OK),
            ('Anker → USB 3 hub<br><span class="sub">Inside the dock</span>', "Intel 8087:5787 → VIA VL822 ×2", "10 Gb/s", "10 Gb/s", OK),
            ("↳ " + L("seagate-backup", "Seagate Expansion 2 TB"), "Seagate ST2000LM007", "5 Gb/s", "5 Gb/s", OK),
            ("↳ " + L("network", "2.5G LAN adapter"), "Realtek RTL8156", "5 Gb/s", "5 Gb/s", OK),
            ("↳ Card reader, no card", "Genesys Logic 05e3:0764", "5 Gb/s", "5 Gb/s", OK),
            ('Anker → Lenovo camera<br><span class="sub">USB 2 hub chain</span>', "Fresco 1d5c:5801 → VIA 2822 ×2", "USB 2", "480 Mb/s", OK),
            ("MacBook → " + L("sandisk-backup", "SanDisk SSD 1 TB") + '<br><span class="sub">Own MacBook port</span>', "SanDisk 0781:5504", "10 Gb/s", "10 Gb/s", OK),
            ("MacBook → " + L("network", "home network") + '<br><span class="sub">en8, through the dock</span>', "Realtek 2.5GbE", "2.5 Gb/s", "2500Base-T full duplex", OK),
            ('MacBook → Wi-Fi<br><span class="sub">en0</span>', "Wi-Fi 7", "—", "5 GHz ch 36, 80 MHz, 1080 Mb/s, −34 dBm", '<span class="sub">5 GHz</span>'),
            ("Anker → second TB5 downstream", "—", "120 Gb/s", "No device", '<span class="sub">free</span>'),
        ])),
    sec("Drive speeds", '<p class="note-t">8 GiB sequential, three runs each, write includes sync, read after a cache purge, no backup running. November 7, 2026.</p>',
        bars([
            ("Samsung 990 PRO", "MacBook's own TB port", 2877, 2928, "tb"),
            ("SanDisk SSD", "own MacBook port", 845, 813, "usb"),
            ("SanDisk SSD", "on the dock", 794, 702, "usb"),
        ]),
        '<p class="note-t">The SanDisk is faster on its own port in both directions. The 990 PRO and its ACASIS enclosure have since moved to the Mac mini, where the drive is called <a href="devices/data.html">DATA</a>.</p>'),
    sec("Storage", table(["Volume", "Drive", "Used", "Size"], [
        ("Macintosh HD", "Apple 1 TB internal (AP1024Z)", "336 GiB", "926 GiB"),
        (L("sandisk-backup", "SANDISK TIMEMACHINE"), "SanDisk SSD 1 TB, own MacBook port, Time Machine", "366 GiB", "931 GiB"),
        (L("seagate-backup", "MacBook Backup"), "Seagate Expansion 2 TB hard drive, on the dock, Time Machine", "701 GiB", "1.8 TiB"),
    ], num=(2, 3)), '<p class="note-t">Latest Time Machine backup: November 8, 2026 at 4:43 PM.</p>'),
    sec("Network", table(["Interface", "Link", "Down", "Up", "Idle ping"], [
        ("en8 · wired", "2.5GbE through the dock, default route", "1.47 Gb/s", "1.98 Gb/s", "10.9 ms"),
        ("en0 · Wi-Fi 7", "5 GHz, 80 MHz", "161.8 Mb/s", "214.6 Mb/s", "14.3 ms"),
    ], num=(2, 3, 4)), f'<p class="note-t">Measured {READ}. Details and earlier tests are on the ' + L("network", "network page") + '.</p>'),
    '<section><h2>Worth remembering</h2><div class="callouts">'
    '<div class="callout"><h3>The dock\'s USB is one 10 Gb/s lane</h3><p>Every USB socket, the Ethernet port and the card reader share it. Fast drives belong on the MacBook\'s own ports or the dock\'s Thunderbolt ports.</p></div>'
    '<div class="callout"><h3>HDMI or DisplayPort, not both</h3><p>The dock\'s two video outputs cannot be used at the same time, so the Dell takes HDMI and the KTC runs from a Thunderbolt 5 port.</p></div>'
    '<div class="callout attn"><h3>Video is king: a dock does video or fast drives</h3><p>On any dock, display traffic is reserved first and data gets what is left. This dock carries both monitors, so the fast drive sits on the MacBook\'s own port, where it measured quicker. The <a href="mac-mini.html">Mac mini</a> makes the opposite choice: its dock carries the SSDs and the monitors plug into the mini.</p></div>'
    '<div class="callout"><h3>One free Thunderbolt 5 port</h3><p>The KTC uses one of the dock\'s two downstream ports. The other is empty, rated up to 120 Gb/s.</p></div>'
    '<div class="callout"><h3>What moved to the Mac mini</h3><p>The Wavlink dock and the ACASIS enclosure with the Samsung 990 PRO both live on the <a href="mac-mini.html">Mac mini</a> now.</p></div>'
    '</div></section>',
    sec("Next to the Mac mini", table(["", "Mac Work Book Pro", "Home Mac mini"], [
        ("Chip", "Apple M5 Pro", "Apple M6"),
        ("CPU", "18 cores: 6 Super, 12 Performance", "12 cores: 2 Super, 4 Performance, 6 Efficiency"),
        ("GPU", "20 cores", "12 cores"),
        ("Memory", "48 GB", "16 GB"),
        ("Internal SSD", "1 TB", "512 GB"),
        ("Thunderbolt", "Thunderbolt 5, 80 Gb/s in use", "Thunderbolt 4, 40 Gb/s"),
        ("Dock", "Anker Prime, Thunderbolt 5", "Wavlink WL-UTD58, Thunderbolt 5 at 40 Gb/s"),
    ]), '<p class="note-t">"Performance" is the lower of two tiers on the M5 Pro but the middle of three on the M6.</p>'),
])
hero = (f'<div class="eyebrow">Read {READ} · Mac17,9</div>\n'
        '<h1>Mac Work Book <em>Pro*</em></h1>\n'
        '<p class="lede">An Apple M5 Pro MacBook Pro with 48 GB of memory at the home desk. One Thunderbolt 5 cable to an Anker dock carries power, the wired network, a backup drive and the camera.</p>\n'
        '<p class="lede" style="font-size:14px">* I wish I owned this. Alas, it\'s on loan from work.</p>\n'
        + stats([("80", "Gb/s", "dock link"), ("48", "GB", "memory"), ("2", "backups", "Time Machine disks"), ("144 + 100", "Hz", "two displays"), ("1.98", "Gb/s", "wired upload")]))
page("macbook-pro.html", "Mac Work Book Pro",
     "An Apple M5 Pro MacBook Pro on an Anker Thunderbolt 5 dock: what is plugged into what, a page for each device, and measured speeds.",
     "usb", hero, hub, one=False, cur=CUR)
