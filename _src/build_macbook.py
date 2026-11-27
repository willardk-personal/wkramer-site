#!/usr/bin/env python3
"""Builds macbook-pro.html and macbook/*.html. Run: python3 _src/build_macbook.py
(importing build also rebuilds the Mac mini pages)."""
from build import page, table, spec, bars, path, stats, sec, notes

READ = "November 27, 2026"
CUR = "macbook-pro.html"
MB = ("node", "MacBook Pro", "Mac17,9 · M5 Pro", "../macbook-pro.html")
DOCK = ("node", "Ivanky dock", "13-in-1 USB-C", "ivanky-dock.html")
UP = ("wire", "10 Gb/s USB-C", "usb")

D = []

# ---------------------------------------------------------------- Ivanky dock
D.append(dict(
    slug="ivanky-dock", name="Ivanky", em="13‑in‑1 USB‑C dock", group="Dock", bus="usb", spd="10 Gb/s uplink",
    card="Ivanky 13-in-1 USB-C dock, the Mac mini's old one. One monitor, both backup drives and the camera share a single 10 Gb/s link to the MacBook.",
    lede="One USB-C cable to the MacBook. The Ivanky 13-in-1 dock that used to sit under the Mac mini now carries one monitor, both Time Machine drives, a card reader and the camera. It replaced an Anker Thunderbolt 5 dock in late November.",
    path=[MB, UP, ("node", "Ivanky dock", "VIA VL822 hub · 10 Gb/s", "me")],
    stats=[("10", "Gb/s", "link to the MacBook, shared"), ("13", "ports", "on the box"), ("1440p", "144 Hz", "monitor on its HDMI"), ("140", "W", "Mokin charger, shared with the MacBook")],
    body=[
        sec("What it is", spec([
            ("Model", "Ivanky 13-in-1 Mac mini dock and stand (Fusion Dock 3)"),
            ("Type", "A 10 Gb/s USB-C dock, not Thunderbolt. macOS's Thunderbolt report lists no device, which is expected."),
            ("Link to the MacBook", 'The MacBook\'s Thunderbolt port on the HDMI edge, used as a plain USB-C port. macOS sees a VIA hub <span class="mono">(2109:0822)</span> at 10 Gb/s on a USB 3.1 bus.'),
            ("Video", "HDMI out, up to 4K at 144 Hz. The picture travels over DisplayPort Alt Mode on its own wires in the cable, so it takes nothing from the 10 Gb/s the USB devices share."),
            ("Power", "It came with a 20 W adapter, which isn't used. It runs from the same Mokin 140 W smart charger as the MacBook, which shows the power draw."),
            ("USB 3 inside", 'VIA <span class="mono">2109:0822</span> at 10 Gb/s, feeding a VIA <span class="mono">2109:0817</span> at 5 Gb/s'),
            ("USB 2 inside", 'VIA <span class="mono">2822</span> → VIA <span class="mono">2817</span>, plus two Genesys <span class="mono">05e3:0608</span> hubs, at 480 Mb/s'),
            ("History", 'The same unit sat under the <a href="mac-mini.html">Mac mini</a> until early November, with the Scratch Disk in its M.2 slot.'),
        ]),
            '<p class="note-t">Port list from the Ivanky product listing. Everything else is what macOS reported on November 27.</p>'),
        sec("Its ports, and what is in them", table(["Port", "Rated", "In use"], [
            ("USB-C upstream", "10 Gb/s", "The MacBook"),
            ("HDMI", "4K at 144 Hz", 'One <a href="displays.html">KTC H24T7</a>, 2560×1440 at 144 Hz'),
            ("USB-A and USB-C", "10 Gb/s each", '<a href="sandisk-backup.html">SanDisk SSD</a>, 10 Gb/s'),
            ("USB-A and USB-C", "5 Gb/s each", '<a href="seagate-backup.html">Seagate hard drive</a>, 5 Gb/s'),
            ("USB-A ×3", "USB 2", "Lenovo Performance RGB Camera, 480 Mb/s"),
            ("SD and TF", "—", 'macOS lists a USB 3 card reader <span class="mono">(05e3:0749)</span> at 5 Gb/s, no card'),
            ("M.2 NVMe / SATA slot", "10 Gb/s", 'Empty. Its Realtek RTL9210B-CG bridge shows at 480 Mb/s with no drive in it. On the Mac mini it held the Scratch Disk at about 780 MB/s.'),
            ("Audio ×2", "—", "Not checked"),
            ("Power in", "20 W adapter in the box", "Mokin 140 W charger"),
        ]),
            '<p class="note-t">macOS doesn\'t say which socket each device uses.</p>'),
        sec("One 10 Gb/s link for everything", '<p>The SanDisk, the Seagate, the card reader, the camera and the M.2 slot all share one 10 Gb/s link to the MacBook. The SanDisk alone can use most of it, so a backup to it and a backup to the Seagate at the same time would share it. Video doesn\'t count against it.</p>'),
        sec("The docks before this one", '<p>From November 6 to 26 this desk used an Anker Prime 14-in-1 Thunderbolt 5 dock (A83B5). It linked at 80 Gb/s, or 120 Gb/s with both monitors on, carried both monitors over USB-C to HDMI cables and the wired network, and had its power supply built in. It is being returned. Before that, a Wavlink WL-UTD58 Thunderbolt 5 dock was here; it now serves the <a href="../devices/wavlink-dock.html">Mac mini</a>.</p>'),
    ]))

# ---------------------------------------------------------------- SanDisk
D.append(dict(
    slug="sandisk-backup", name="SanDisk SSD", em="1 TB backup", group="Storage", bus="usb", spd="10 Gb/s USB",
    card="SanDisk SSD 1 TB on the Ivanky dock at 10 Gb/s. The portable Time Machine disk: 780 MB/s read on November 27.",
    lede="The backup that travels. A SanDisk 1 TB portable SSD used by Time Machine, on the Ivanky dock's 10 Gb/s hub.",
    path=[MB, UP, DOCK, ("wire", "USB 3 hub · 10 Gb/s", "usb"), ("node", "SanDisk SSD 1 TB", "SANDISK TIMEMACHINE", "me")],
    stats=[("780", "MB/s", "read, Nov 27"), ("505", "GiB", "used of 931"), ("10", "Gb/s", "USB link")],
    body=[
        sec("The drive", spec([
            ("Drive", 'SanDisk SSD 1 TB, portable <span class="mono">(0781:5504)</span>'),
            ("Link", "USB 10 Gb/s, the most the drive offers"),
            ("Where", "The Ivanky dock's first USB 3 hub (VIA VL822), one hop from the MacBook, sharing the dock's 10 Gb/s link"),
            ("Volume", "SANDISK TIMEMACHINE. 505 GiB used of 931 GiB (November 27)."),
            ("Job", "Time Machine destination, chosen because it is small and tough enough to travel."),
        ])),
        sec("Read speed on the Ivanky", table(["Date", "Read"], [
            ("Nov 27, 2026", "780 MB/s"),
            ("Nov 26, 2026", "766 MB/s"),
        ], num=(1,)),
            '<p class="note-t">4 GiB of a Windows 11 ISO inside the latest backup, read once with the page cache bypassed, after Time Machine had finished. Not comparable one-to-one with the 8 GiB runs below.</p>'),
        sec("Earlier: Anker dock against the MacBook's own port", bars([
            ("On the Anker dock", "Nov 7", 794, 702, "usb"),
            ("Own MacBook port", "Nov 7, late evening", 845, 813, "usb"),
        ], 1250),
            '<p class="note-t">8 GiB sequential, three runs each, write includes sync, read after a cache purge, no backup running. The own-port figures are the middle of 842 to 847 write and 812 to 814 read. The bar scale ends at 1,250 MB/s, the ceiling of a 10 Gb/s USB link.</p>'),
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
    card="Seagate Expansion 2 TB portable hard drive on the Ivanky dock. The second Time Machine disk.",
    lede="The second backup. A Seagate Expansion 2 TB portable hard drive on the Ivanky dock's 5 Gb/s hub, used only by Time Machine.",
    path=[MB, UP, DOCK, ("wire", "USB 3 hubs · 5 Gb/s", "usb5"), ("node", "Seagate Expansion 2 TB", "MacBook Backup", "me")],
    stats=[("99", "MB/s", "read, Nov 27"), ("789", "GiB", "used of 1.8 TiB"), ("5", "Gb/s", "USB link"), ("5,400", "rpm", "drive inside")],
    body=[
        sec("The drive", spec([
            ("Drive", 'Seagate Expansion 2 TB portable hard drive <span class="mono">(0bc2:2030)</span>'),
            ("Disk inside", 'Seagate <span class="mono">ST2000LM007</span>: 2.5-inch, 7 mm, 5,400 rpm, two 1 TB shingled (SMR) platters, 128 MB cache'),
            ("Rated speed", "Up to 140 MB/s"),
            ("Link", "USB 5 Gb/s, two hubs from the MacBook (VIA VL822 → VL817) inside the Ivanky dock"),
            ("Volume", "MacBook Backup. 789 GiB used of 1.8 TiB (November 27)."),
            ("Job", "Time Machine destination that stays at the desk."),
        ]),
            '<p class="note-t">Disk details are Seagate\'s published figures for the ST2000LM007.</p>'),
        sec("Read speed", table(["Date", "Read"], [
            ("Nov 27, 2026", "99 MB/s"),
            ("Nov 26, 2026", "128 MB/s"),
        ], num=(1,)),
            '<p class="note-t">4 GiB of a Windows 11 ISO inside the latest backup, read once with the page cache bypassed. Why November 27 read lower wasn\'t determined from one run; where a file sits on a hard drive\'s platter changes its speed.</p>'),
        sec("Things to know", notes([
            "Shingled drives write quickly in bursts and slow down on long rewrites. Time Machine's hourly backups suit that well.",
            'It shares the dock\'s 10 Gb/s link with the <a href="sandisk-backup.html">SanDisk SSD</a>. At hard drive speeds that barely matters.',
        ])),
    ]))

# ---------------------------------------------------------------- Displays
D.append(dict(
    slug="displays", name="Displays", em="two KTCs", group="Displays", bus="hdmi", spd="144 Hz + 144 Hz",
    card="The same two KTC H24T7 monitors as the Mac mini, both at 1440p and 144 Hz: one from the MacBook's own HDMI port, one from the Ivanky dock.",
    lede="Two KTC H24T7 monitors on their HDMI inputs: one straight from the MacBook's HDMI port, the other from the Ivanky dock. Both are shared with the Mac mini, which uses their DisplayPort inputs.",
    path=[MB, ("wire", "HDMI · and dock HDMI", "hdmi"), ("node", "KTC H24T7 ×2", "1440p · 144 Hz each", "me")],
    stats=[("1440p", "144 Hz", "KTC H24T7, main"), ("1440p", "144 Hz", "KTC H24T7, second")],
    body=[
        sec("What the MacBook sees", table(["Display", "Role", "Running at", "Against its maximum"], [
            ('<a href="../devices/ktc-h24t7.html">KTC H24T7</a>', "Main", "2560×1440 at 144 Hz", "The monitor's HDMI maximum. The panel's 180 Hz and VRR need DisplayPort, which the Mac mini uses"),
            ('<a href="../devices/ktc-h24t7-hdmi.html">KTC H24T7</a>', "Second", "2560×1440 at 144 Hz", "Same: the HDMI maximum"),
        ]),
            '<p class="note-t">Read November 27, 2026. At home the MacBook runs with its lid closed: one KTC is the main display and the other extends the desktop.</p>',
            '<p class="note-t">Panel details for each monitor are on its Mac mini page.</p>'),
        sec("How they are connected", table(["From", "Cable", "Notes"], [
            ("The MacBook's own HDMI port", "HDMI, straight into the monitor", "The MacBook's port is HDMI 2.1; the monitor's input is HDMI 2.0, which tops out at 144 Hz here"),
            ('<a href="ivanky-dock.html">Ivanky dock</a> HDMI', "HDMI from the dock", "Carried from the MacBook over DisplayPort Alt Mode on the dock cable's own wires, so it doesn't use the dock's 10 Gb/s"),
        ]),
            '<p class="note-t">macOS reports no connection type for either monitor, so it doesn\'t say which one is on which cable, or which is the main display.</p>'),
        sec("Sharing with the Mac mini", '<p>Both computers stay connected to both monitors all the time: the Mac mini on each monitor\'s DisplayPort input at 180 Hz with VRR, the MacBook on its HDMI input at 144 Hz. There is no KVM switch. Switching a monitor\'s input moves it from one computer to the other, and nothing has to be unplugged.</p><p>144 Hz is the KTC\'s HDMI limit. The MacBook is for work, not games, so it loses nothing that matters.</p>'),
        sec("Before November 27", '<p>On the Anker Thunderbolt 5 dock both monitors ran from the dock over USB-C to HDMI cables, also at 1440p and 144 Hz.</p>'),
    ]))

# ---------------------------------------------------------------- Network
D.append(dict(
    slug="network", name="Network", em="Wi-Fi 7", group="Network", bus="net", spd="Wi-Fi 7 · 6 GHz",
    card="Wi-Fi 7 on 6 GHz: 1.50 Gb/s down and 1.25 Gb/s up on November 27. The Ivanky dock has no Ethernet port.",
    lede="How the MacBook reaches the network. Wi-Fi 7 on 6 GHz is the default route since the move to the Ivanky dock, which has no Ethernet port.",
    path=[MB, ("wire", "Wi-Fi 7 · 6 GHz", "net"), ("node", "Home Wi-Fi", "Verizon CHR30A router", "me")],
    stats=[("1.50", "Gb/s", "down"), ("1.25", "Gb/s", "up"), ("13.8", "ms", "idle ping")],
    body=[
        sec("The link", spec([
            ("Interface", "en0, Wi-Fi 7 (802.11be), default route"),
            ("Channel", "37, 6 GHz, 160 MHz wide"),
            ("Signal", "−46 dBm, noise −94 dBm, link rate 1921 Mb/s"),
            ("Router", "Verizon CHR30A, on a Verizon fiber terminal"),
        ])),
        sec("Speed tests", table(["Date", "Link", "Down", "Up", "Idle ping"], [
            ("Nov 27, 2026", "Wi-Fi 7, 6 GHz, 160 MHz", "1.50 Gb/s", "1.25 Gb/s", "13.8 ms"),
            ("Nov 26, 2026, test 1", "Wi-Fi 7, 6 GHz, 160 MHz", "1.34 Gb/s", "1.06 Gb/s", "57 ms"),
            ("Nov 26, 2026, test 2", "Wi-Fi 7, 6 GHz, 160 MHz", "580 Mb/s", "842 Mb/s", "16 ms"),
        ], num=(2, 3, 4)),
            '<p class="note-t">macOS networkQuality. On November 27 responsiveness was Medium on upload and High on download.</p>'),
        sec("Earlier tests", table(["Date", "Link", "Down", "Up", "Idle ping"], [
            ("Nov 8, 2026", "Wired, 2.5 GbE through the Anker dock", "1.47 Gb/s", "1.98 Gb/s", "10.9 ms"),
            ("Nov 8, 2026", "Wi-Fi 7, 5 GHz, 80 MHz", "161.8 Mb/s", "214.6 Mb/s", "14.3 ms"),
            ("Oct 19, 2026", "Wired, through the Wavlink dock", "1.74 Gb/s", "2.11 Gb/s", "12 ms"),
            ("Oct 19, 2026, earlier", "Wired, through the Wavlink dock", "1.60 Gb/s", "2.00 Gb/s", "—"),
        ], num=(2, 3, 4)),
            '<p class="note-t">The wired tests used each Thunderbolt dock\'s built-in Realtek RTL8156 2.5 GbE adapter. Wi-Fi on 6 GHz now gets close to what wired did through those docks.</p>'),
        sec("Link to the Mac mini", '<p>The two Macs normally talk over the home network. In a test on November 25 a direct Thunderbolt link, with the MacBook on the Mac mini\'s Wavlink dock, ran at 37.7 Gb/s each way, about 16 times the home network\'s 2.5 Gb/s.</p>'),
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
PWR = 'style="stroke:#d9577a;stroke-width:3"'
svg = ['<svg viewBox="0 0 1160 730" role="img" aria-labelledby="mbT"><title id="mbT">Port map: one USB-C cable at 10 Gb/s links the MacBook Pro to the Ivanky dock, which carries one monitor, both backup drives, a card reader, an empty M.2 slot and the camera. The second monitor is on the MacBook\'s own HDMI port. A Mokin 140 W charger powers the MacBook over MagSafe, and the network is Wi-Fi 7.</title>']
svg += [line(280, 240, 430, 240, "l-u10", "10 Gb/s", "c-u10"), '<text x="355" y="262" class="lbl2" text-anchor="middle">USB-C, not TB</text>',
        line(280, 330, 332, 330, "l-free"), '<text x="338" y="334" class="lbl2">2 free</text>',
        line(638, 129, R, 129, "l-hdmi", "HDMI", "c-hdmi"),
        line(638, 199, R, 199, "l-u10", "10 Gb/s", "c-u10"),
        line(638, 279, R, 279, "l-u5", "5 Gb/s", "c-u5"), line(638, 349, R, 349, "l-u5", "5 Gb/s", "c-u5"),
        line(638, 429, R, 429, "l-u2", "480 Mb/s", "c-u2"), line(638, 499, R, 499, "l-u2", "480 Mb/s", "c-u2"),
        '<polyline points="280,420 340,420 340,609 760,609" class="ln l-hdmi"/>', '<text x="550" y="600" class="lbl c-hdmi" text-anchor="middle">HDMI 2.1 → monitor\'s HDMI 2.0</text>',
        f'<line x1="90" y1="470" x2="90" y2="570" class="ln" {PWR}/>', '<text x="100" y="525" class="lbl" style="fill:#d9577a">MagSafe</text>',
        line(245, 470, 245, 650, "l-air"), '<text x="255" y="560" class="lbl c-mut">Wi-Fi 7</text>']
svg += ['<rect x="30" y="150" width="250" height="320" rx="14" class="node mini"/>',
        '<text x="48" y="192" class="t-big">MacBook Pro</text><text x="48" y="214" class="t2">M5 Pro · Mac17,9 · 48 GB</text>',
        '<text x="48" y="256" class="t2">Internal 1 TB SSD</text><text x="48" y="274" class="t2">Battery 100%, 13 cycles</text>',
        '<text x="270" y="236" class="tag" text-anchor="end">TB port · HDMI edge</text><text x="270" y="326" class="tag" text-anchor="end">TB ports</text><text x="270" y="410" class="tag" text-anchor="end">HDMI</text>',
        '<text x="90" y="460" class="tag" text-anchor="middle">MagSafe</text><text x="245" y="460" class="tag" text-anchor="middle">en0</text>',
        box(30, 570, 180, 64, "Mokin 140 W charger", "smart, shows power draw"),
        box(30, 650, 330, 64, "Home Wi-Fi · Verizon CHR30A", "6 GHz · ch 37 · 160 MHz · default route"),
        '<rect x="430" y="20" width="230" height="525" rx="14" class="node dock"/>',
        '<text x="448" y="52" class="t-big" style="font-size:18px">Ivanky dock</text><text x="448" y="74" class="t2">13-in-1 · USB-C, not Thunderbolt</text>',
        '<rect x="446" y="100" width="192" height="58" rx="8" class="sub"/><text x="460" y="124" class="t1">HDMI out</text><text x="460" y="144" class="t2">4K@144 max · own wires</text>',
        '<rect x="446" y="170" width="192" height="58" rx="8" class="sub"/><text x="460" y="194" class="t1">USB 3 hub · 10 Gb/s</text><text x="460" y="214" class="tm">VIA 2109:0822</text>',
        '<rect x="446" y="250" width="192" height="128" rx="8" class="sub"/><text x="460" y="274" class="t1">↳ USB 3 hub · 5 Gb/s</text><text x="460" y="294" class="tm">VIA 2109:0817</text>',
        '<rect x="446" y="400" width="192" height="128" rx="8" class="sub"/><text x="460" y="424" class="t1">USB 2 hubs</text><text x="460" y="444" class="tm">VIA 2822 → 2817</text><text x="460" y="460" class="tm">Genesys 05e3:0608 ×2</text>',
        box(R, 100, 385, 58, "KTC H24T7 · via the dock", "1440p at 144 Hz · dock HDMI"),
        box(R, 170, 385, 58, "SanDisk SSD 1 TB · SANDISK TIMEMACHINE", "Time Machine · 780 MB/s read"),
        box(R, 250, 385, 58, "Seagate Expansion 2 TB · MacBook Backup", "Time Machine · hard drive"),
        box(R, 320, 385, 58, "Card reader", "SD and TF · 05e3:0749 · no card"),
        box(R, 400, 385, 58, "M.2 slot · empty", "Realtek RTL9210B-CG · built into the dock"),
        box(R, 470, 385, 58, "Lenovo camera", "Performance RGB Camera · USB 2"),
        box(R, 580, 385, 58, "KTC H24T7 · MacBook HDMI", "1440p at 144 Hz · HDMI 2.0 input")]
HITS = [("ivanky-dock", "usb", 430, 20, 230, 64), ("displays", "hdmi", R, 100, 385, 58), ("sandisk-backup", "usb", R, 170, 385, 58),
        ("seagate-backup", "usb5", R, 250, 385, 58), ("displays", "hdmi", R, 580, 385, 58), ("network", "net", 30, 650, 330, 64)]
svg += [f'<a href="macbook/{s}.html" class="b-{b}" aria-label="{names[s]}"><rect class="hit" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></a>' for s, b, x, y, w, h in HITS]
svg.append("</svg>")
KEYS = [("usb", "USB 10 Gb/s"), ("hdmi", "HDMI"), ("usb5", "USB 5 Gb/s"), ("usb2", "USB 2")]
fig = ('<figure class="wiring"><div class="dscroll">' + "".join(svg) + '</div><figcaption>'
       + "".join(f'<span class="key b-{b}"><i></i>{t}</span>' for b, t in KEYS)
       + '<span>macOS does not report which USB socket each device uses, or which monitor is on which cable. Select a device to open its page.</span></figcaption></figure>')

cards = ""
for g in ["Dock", "Storage", "Displays", "Network"]:
    cards += f'<div class="grp">{g}</div><div class="grid">' + "".join(
        f'<a class="card b-{d["bus"]}" href="macbook/{d["slug"]}.html"><span class="spd">{d["spd"]}</span><b>{d["name"]} {d["em"]}</b><span>{d["card"]}</span><span class="go">Details &rarr;</span></a>'
        for d in D if d["group"] == g) + "</div>\n"

L = lambda s, t: f'<a href="macbook/{s}.html">{t}</a>'
OK = '<span class="okk">✓ max</span>'
PDFS = ('<div class="grid"><a class="card" href="downloads/mac-mini-desk-layout-2026-11-23.pdf"><span class="spd">PDF · Nov 23, 2026</span><b>Mac mini desk layout</b><span>Both monitors on the mini\'s own ports over DisplayPort, the Wavlink dock with Media, DATA and the Scratch Disk, and the November 23 drive tests.</span><span class="go">Open PDF &rarr;</span></a>'
        '<a class="card" href="downloads/macbook-pro-desk-layout-2026-11-27.pdf"><span class="spd">PDF · Nov 27, 2026</span><b>MacBook Pro desk layout</b><span>The work-from-home MacBook on the Ivanky 13-in-1 USB-C dock, one monitor on its own HDMI, the backups, the internal SSD and Wi-Fi.</span><span class="go">Open PDF &rarr;</span></a>'
        '<a class="card" href="downloads/macbook-pro-desk-layout-2026-11-20.pdf"><span class="spd">PDF · Nov 20, 2026</span><b>MacBook Pro, earlier</b><span>The same desk on the Anker Thunderbolt 5 dock, before November 27.</span><span class="go">Open PDF &rarr;</span></a></div>')
hub = "\n".join([
    f'<section><h2>What is plugged into what</h2>{fig}</section>',
    f'<section><h2>The devices</h2><p class="note-t">Each one has its own page: what it is, the path its signal takes from the MacBook, and what it measured.</p>{cards}</section>',
    sec("The machine", spec([
        ("Model", "MacBook Pro 14-inch (Mac17,9), silver, part Z1MH0004ELL/A"),
        ("Chip", "Apple M5 Pro: 18-core CPU (6 Super, 12 Performance), 20-core GPU"),
        ("Memory and storage", "48 GB, 1 TB internal SSD (AP1024Z), 392 of 926 GiB used"),
        ("Thunderbolt", "3 Thunderbolt 5 ports, up to 120 Gb/s. The one on the HDMI edge holds the Ivanky dock as plain USB-C; the other two are free."),
        ("Power", "Mokin 140 W smart charger over a USB-C to MagSafe cable. The same charger powers the dock. A second Mokin lives in the travel kit; one charges the MacBook, an iPad mini and an iPhone at once."),
        ("Battery", "100% maximum capacity, 13 cycles, condition Normal after about three months (November 27). Held at 80% charge on the desk."),
        ("Wireless", "Wi-Fi 7, the default route"),
    ])),
    sec("Every link, against its maximum", '<p class="note-t">The most each port allows, next to what macOS reported as negotiated on November 27.</p>',
        table(["Connection", "Chip", "Port maximum", "Negotiated", ""], [
            ("MacBook → " + L("ivanky-dock", "Ivanky dock") + '<br><span class="sub">Thunderbolt port on the HDMI edge, as USB-C</span>', "VIA 2109:0822", "10 Gb/s (the dock\'s USB-C uplink)", "10 Gb/s on a USB 3.1 bus. No Thunderbolt device, as expected", OK),
            ("MacBook HDMI → " + L("displays", "KTC H24T7") + '<br><span class="sub">MacBook HDMI 2.1, monitor HDMI 2.0</span>', "—", "1440p at 144 Hz (monitor\'s HDMI max)", "1440p at 144 Hz", OK),
            ("Ivanky HDMI → " + L("displays", "KTC H24T7") + '<br><span class="sub">DisplayPort Alt Mode, own wires</span>', "—", "1440p at 144 Hz (monitor\'s HDMI max)", "1440p at 144 Hz", OK),
            ("↳ " + L("sandisk-backup", "SanDisk SSD 1 TB"), "SanDisk 0781:5504", "10 Gb/s", "10 Gb/s", OK),
            ('↳ USB 3 hub<br><span class="sub">Inside the dock</span>', "VIA 2109:0817", "5 Gb/s", "5 Gb/s", OK),
            ("&nbsp;&nbsp;↳ " + L("seagate-backup", "Seagate Expansion 2 TB"), "Seagate 0bc2:2030", "5 Gb/s", "5 Gb/s", OK),
            ("&nbsp;&nbsp;↳ Card reader, no card", "Generic 05e3:0749", "5 Gb/s", "5 Gb/s", OK),
            ('↳ USB 2 hubs<br><span class="sub">Inside the dock</span>', "VIA 2822 → 2817, Genesys 05e3:0608 ×2", "480 Mb/s", "480 Mb/s", OK),
            ("&nbsp;&nbsp;↳ M.2 slot, empty", "Realtek 0bda:9210", "10 Gb/s with a drive", '480 Mb/s <span class="sub">(no drive)</span>', '<span class="sub">empty</span>'),
            ("&nbsp;&nbsp;↳ Lenovo camera", "Lenovo 17ef:4839", "USB 2", "480 Mb/s", OK),
            ('MacBook → Wi-Fi<br><span class="sub">en0, default route</span>', "Wi-Fi 7", "—", "6 GHz ch 37, 160 MHz, 1921 Mb/s, −46 dBm", '<span class="sub">6 GHz</span>'),
        ])),
    sec("Drive speeds", '<p class="note-t">4 GiB read of the same file, page cache bypassed, one run each, November 27, 2026. Internal SSD write: 4 GiB with a full flush to flash.</p>',
        bars([
            ("Internal SSD", "Apple AP1024Z", 11561, 9990, "tb"),
            ("SanDisk SSD", "on the Ivanky, 10 Gb/s", None, 780, "usb"),
            ("Seagate HDD", "on the Ivanky, 5 Gb/s", None, 99, "usb5"),
        ]),
        '<p class="note-t">Write speeds weren\'t tested on the backup drives; macOS blocks writes to Time Machine disks. The SanDisk read 766 MB/s and the Seagate 128 MB/s the day before. The Samsung 990 PRO that ran 2,877 / 2,928 MB/s on a MacBook port on November 7 now lives on the Mac mini as <a href="devices/data.html">DATA</a>.</p>'),
    sec("Storage", table(["Volume", "Drive", "Used", "Size"], [
        ("Macintosh HD", "Apple 1 TB internal (AP1024Z), FileVault on", "392 GiB", "926 GiB"),
        (L("sandisk-backup", "SANDISK TIMEMACHINE"), "SanDisk SSD 1 TB, on the Ivanky, Time Machine", "505 GiB", "931 GiB"),
        (L("seagate-backup", "MacBook Backup"), "Seagate Expansion 2 TB hard drive, on the Ivanky, Time Machine", "789 GiB", "1.8 TiB"),
    ], num=(2, 3)), '<p class="note-t">Used space read November 27, 2026.</p>'),
    sec("Network", table(["Interface", "Link", "Down", "Up", "Idle ping"], [
        ("en0 · Wi-Fi 7", "6 GHz, channel 37, 160 MHz, default route", "1.50 Gb/s", "1.25 Gb/s", "13.8 ms"),
    ], num=(2, 3, 4)), f'<p class="note-t">Measured {READ}. The Ivanky has no Ethernet port, so there is no wired link now. Earlier wired tests are on the ' + L("network", "network page") + '.</p>'),
    '<section><h2>Worth remembering</h2><div class="callouts">'
    '<div class="callout"><h3>One 10 Gb/s link, and that\'s enough</h3><p>The Ivanky is a USB-C dock, not Thunderbolt. Both backup drives, the card reader and the camera share its single 10 Gb/s link. The SanDisk still reads at 780 MB/s, close to what it managed on its own port.</p></div>'
    '<div class="callout"><h3>Video rides its own wires</h3><p>The dock\'s monitor runs over DisplayPort Alt Mode, separate from the USB data, so it doesn\'t slow the drives. The second monitor sits on the MacBook\'s own HDMI port.</p></div>'
    '<div class="callout"><h3>Two computers, no KVM</h3><p>Each monitor has both Macs plugged in at once: the Mac mini on DisplayPort, this MacBook on HDMI. The monitor\'s input button picks the computer.</p></div>'
    '<div class="callout"><h3>One charger for everything</h3><p>A Mokin 140 W smart charger runs the MacBook over MagSafe and the dock, and shows the power draw. With several devices on it, the 140 W is split, so the MacBook gets less than it would alone.</p></div>'
    '<div class="callout attn"><h3>A $50 dock replaced a $350 one</h3><p>The Anker Thunderbolt 5 dock is going back. The Ivanky, the Mac mini\'s old dock, gives the same everyday setup. What it gives up: Thunderbolt speed for fast drives, and wired Ethernet.</p></div>'
    '</div></section>',
    sec("Desk layout PDFs", '<p class="note-t">Printable layouts of both desks, read from macOS: a port diagram, every negotiated link, storage, measured speeds and notes.</p>', PDFS),
    sec("Next to the Mac mini", table(["", "Mac Work Book Pro", "Home Mac mini"], [
        ("Chip", "Apple M5 Pro", "Apple M6"),
        ("CPU", "18 cores: 6 Super, 12 Performance", "12 cores: 2 Super, 4 Performance, 6 Efficiency"),
        ("GPU", "20 cores", "12 cores"),
        ("Memory", "48 GB", "16 GB"),
        ("Internal SSD", "1 TB", "512 GB"),
        ("Thunderbolt", "Thunderbolt 5, up to 120 Gb/s (the dock uses one port as USB-C)", "Thunderbolt 4, 40 Gb/s"),
        ("Dock", "Ivanky 13-in-1, USB-C at 10 Gb/s", "Wavlink WL-UTD58, Thunderbolt 5 at 40 Gb/s"),
    ]), '<p class="note-t">"Performance" is the lower of two tiers on the M5 Pro but the middle of three on the M6.</p>'),
])
hero = (f'<div class="eyebrow">Read {READ} · Mac17,9</div>\n'
        '<h1>Mac Work Book <em>Pro*</em></h1>\n'
        '<p class="lede">An Apple M5 Pro MacBook Pro with 48 GB of memory at the home desk. One USB-C cable to the Ivanky dock carries a monitor, both backup drives and the camera; the second monitor is on the MacBook\'s own HDMI port, and a Mokin 140 W charger powers it all.</p>\n'
        '<p class="lede" style="font-size:14px">* I wish I owned this. Alas, it\'s on loan from work.</p>\n'
        + stats([("10", "Gb/s", "dock link"), ("48", "GB", "memory"), ("2", "backups", "Time Machine disks"), ("144 + 144", "Hz", "two displays"), ("100", "%", "battery capacity")]))
page("macbook-pro.html", "Mac Work Book Pro",
     "An Apple M5 Pro MacBook Pro on an Ivanky 13-in-1 USB-C dock: what is plugged into what, a page for each device, and measured speeds.",
     "usb", hero, hub, one=False, cur=CUR)
