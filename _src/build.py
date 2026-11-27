#!/usr/bin/env python3
"""Builds mac-mini.html and devices/*.html. Run from anywhere: python3 _src/build.py"""
import pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKED = "November 23, 2026"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')


def page(path, title, desc, bus, hero, main, one=True, cur="mac-mini.html"):
    p = "../" if "/" in path else ""
    links = [("index.html", "About"), ("mac-mini.html", "Mac mini setup"), ("macbook-pro.html", "Mac Work Book Pro"), ("dev-env.html", "Dev environment"), ("articles.html", "Articles")]
    nav = (f'<nav><a class="brand" href="{p}index.html">Willard Kramer</a>'
           + "".join(f'<a href="{p}{h}"{' aria-current="page"' if h == cur else ""}>{t}</a>' for h, t in links) + "</nav>")
    out = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{html.escape(desc, quote=True)}">
{FONTS}
<link rel="stylesheet" href="{p}site.css">
</head><body class="b-{bus}">
<div class="mast{' one' if one else ''}"><div class="wrap">
{nav}
<div class="hero">
{hero}
</div></div></div>
<div class="wrap"><main>
{main}
</main>
<footer>Willard Kramer &middot; New York, NY &middot; <a href="mailto:willardk@gmail.com">willardk@gmail.com</a></footer>
</div></body></html>
'''
    f = ROOT / path
    f.parent.mkdir(exist_ok=True)
    f.write_text(out)
    print("wrote", path, len(out))


def table(head, rows, cls="", num=()):
    th = "".join(f'<th{" class=n" if i in num else ""}>{h}</th>' for i, h in enumerate(head or []))
    tr = "".join("<tr>" + "".join(f'<td{" class=n" if i in num else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>\n" for r in rows)
    thead = f"<thead><tr>{th}</tr></thead>" if head else ""
    return f'<div class="scroll"><table class="{cls}">{thead}<tbody>\n{tr}</tbody></table></div>'


def spec(rows):
    return table(None, rows, "spec")


def bars(rows, top=None):
    """rows: (label, small, write, read, bus). None skips a bar."""
    top = top or max(v for r in rows for v in r[2:4] if v)
    o = []
    for lab, small, w, r, bus in rows:
        t = ""
        for v, k, c in ((w, "write", "w"), (r, "read", "r")):
            if v:
                t += f'<div class="t {c}"><i style="width:{max(v / top * 82, .6):.1f}%"></i><span>{v:,} <em>MB/s {k}</em></span></div>'
            elif v is None:
                t += f'<div class="t {c}"><span><em>{k} not tested</em></span></div>'
        o.append(f'<div class="bar b-{bus}"><div class="lab">{lab}<small>{small}</small></div>{t}</div>')
    return '<div class="bars">' + "\n".join(o) + "</div>"


def path(hops):
    """hops: alternating ('node', title, sub, href|None|'me') and ('wire', label, bus)."""
    o = []
    for h in hops:
        if h[0] == "wire":
            o.append(f'<div class="wire b-{h[2]}"><span>{h[1]}</span><i></i></div>')
        else:
            _, t, s, href = h
            if href == "me":
                o.append(f'<div class="hop me"><b>{t}</b><span>{s}</span></div>')
            elif href:
                o.append(f'<a class="hop" href="{href}"><b>{t}</b><span>{s}</span></a>')
            else:
                o.append(f'<div class="hop"><b>{t}</b><span>{s}</span></div>')
    return '<div class="path" aria-label="Signal path from the Mac mini">' + "".join(o) + "</div>"


def stats(items):
    return '<div class="stats">' + "".join(f'<div class="stat"><b>{v}<small>{u}</small></b><span>{l}</span></div>' for v, u, l in items) + "</div>"


def sec(title, *body):
    return f"<section><h2>{title}</h2>\n" + "\n".join(body) + "\n</section>"


def notes(items):
    return '<ul class="notes">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


MINI = ("node", "Mac mini M6", "Mac18,5", "../mac-mini.html")
DOCK = ("node", "Wavlink dock", "WL-UTD58", "wavlink-dock.html")
UPLINK = ("wire", "40 Gb/s · R2", "tb")

D = []  # device pages, in pager order

# ---------------------------------------------------------------- Wavlink
D.append(dict(
    slug="wavlink-dock", name="Wavlink WL-UTD58", em="Thunderbolt 5 dock", group="Dock", bus="tb", spd="40 Gb/s uplink",
    card="Self-powered Thunderbolt 5 dock. Carries three SSDs, the Time Machine disk, a LAN adapter and the Blu-ray burner on one cable.",
    lede="The one cable that carries almost everything. A self-powered Thunderbolt 5 dock on the mini's port R2, with both drive enclosures on two of its Thunderbolt ports and the front 30 W one charging and syncing an iPad mini or iPhone.",
    path=[MINI, UPLINK, ("node", "Wavlink WL-UTD58", "USB4 v2 mode · fw 64.64", "me")],
    stats=[("40", "Gb/s", "link to the mini"), ("~4.0", "GB/s", "combined drive ceiling"), ("3.8", "GB/s", "each NVMe drive, alone"), ("7", "", "devices it serves")],
    body=[
        sec("What it is", spec([
            ("Model", "Wavlink WL-UTD58 Rev.b Thunderbolt 5 Dock"),
            ("Reported vendor", 'Winstars Technology Limited <span class="mono">(vendor 0x2629, device 0xD59, rev 3)</span>'),
            ("Firmware", "64.64, port controllers 1.11.0"),
            ("Link to the mini", "40 Gb/s in USB4 v2 mode, on Thunderbolt port R2 (R4 until November 16)"),
            ("Power", "Its own power supply. It does not draw from the mini."),
            ("Downstream Thunderbolt", "3 ports, 40 Gb/s each. One of them is the front 30 W USB-C port."),
            ("USB 3 side", 'Intel hub <span class="mono">8087:5787</span> at 10 Gb/s, feeding Parade hubs <span class="mono">1da0:5512</span>'),
            ("USB 2 side", 'Fresco Logic hub <span class="mono">1d5c:5801</span>, feeding Parade hubs <span class="mono">1da0:551d</span>'),
            ("Dock controller", 'Infineon management device <span class="mono">2629:0d59</span>'),
        ]),
            '<p class="note-t">It is a Thunderbolt 5 dock, but the mini\'s ports are Thunderbolt 4, so the link runs at 40 Gb/s. That is the top speed the mini offers.</p>'),
        sec("What is plugged into it", table(["Dock port", "Device", "Link", "Carried by"], [
            ("Thunderbolt", '<a href="media.html">Media</a> · Crucial P310 in a Mokin enclosure', "40 Gb/s USB4", "Thunderbolt"),
            ("Thunderbolt", '<a href="data.html">DATA</a> · Samsung 990 PRO in a second Mokin enclosure', "40 Gb/s USB4", "Thunderbolt"),
            ("Thunderbolt (front, 30 W)", "iPad mini or iPhone · charging at the full 30 W (15 V / 2 A USB-C PD)", "10 Gb/s USB 3, over USB4", "USB 3 hub, tunneled"),
            ("USB-A (orange)", '<a href="scratch-disk.html">Scratch Disk</a> · Ugreen USB enclosure', "10 Gb/s USB", "USB 3 hub, two hubs down"),
            ("USB 3 hub", '<a href="backup-hdd.html">Backup</a> · WD Elements 4 TB', "5 Gb/s", "USB 3 hub"),
            ("USB 3 hub", '<a href="lan-adapter.html">Realtek 2.5G LAN</a>', "5 Gb/s", "USB 3 hub"),
            ("USB 2 side", '<a href="blu-ray.html">Blu-ray burner</a>', "480 Mb/s", "USB 2 hub"),
        ]),
            '<p class="note-t">The dock\'s four USB-A ports are rated 10 Gb/s each, but everything USB shares one 10 Gb/s link inside the dock: the Scratch Disk, the Backup drive, the LAN adapter and the card reader. The front 30 W port is the only 30 W port, so it is the charging spot for the iPad mini or iPhone. With an 80 Gb/s cable the iPad links at 10 Gb/s, its top speed, and its data joins that same shared USB link. The iPad reports a USB-C PD charger offering 5 V / 3 A, 9 V / 3 A and 15 V / 2 A, and it picks 15 V / 2 A, the full 30 W.</p>'),
        sec("One shared uplink", '<p>Everything behind the dock shares the single 40 Gb/s link to the mini. Run alone, each NVMe drive reads about 3.8 GB/s. Run together, they split a ceiling of about 4 GB/s.</p>',
            bars([
                ("DATA alone", "990 PRO", 3669, 3835, "tb"),
                ("Media alone", "P310", 2972, 3816, "tb"),
                ("DATA, both at once", "990 PRO", 2232, 2011, "tb"),
                ("Media, both at once", "P310", 1788, 2008, "tb"),
                ("Dock total", "two drives together", 4021, 4019, "tb"),
            ]),
            '<p class="note-t">fio, 8 GB direct I/O, median of three, November 23, 2026. No errors. With no display on it, the dock has topped out near 4 GB/s in every run: 4006 MB/s write and 4020 read on November 22, 4055 and 4059 on November 20 with the Scratch Disk added, and 3770 and 3870 on November 7.</p>'),
        sec("Why the dock is here", '<p>The mini runs one bus-powered NVMe enclosure reliably, not two. On October 19 I tried every arrangement of the two enclosures on the mini\'s own ports:</p>',
            table(["Setup", "Result"], [
                ("Mokin first, ACASIS second", "ACASIS fell back to USB 10 Gb/s and its drive ran at about 950 MB/s. A new cable and a reboot did not help."),
                ("ACASIS first, Mokin second", "ACASIS came up at 40 Gb/s. The Mokin's drive failed to attach, mounted unwritable, then dropped."),
                ("Mokin alone", "Stable at 40 Gb/s."),
            ]),
            '<p>Whichever enclosure connected second lost. Each port supplies about 15 W of bus power, and that is the likely cause, though the logs cannot prove it: no PCIe or NVMe errors, and the overcurrent counters stayed at 0. A dock with its own power supply fixes it. Both enclosures run behind the Wavlink at 40 Gb/s with no drops. Only during a one-day trial, November 22 to 23, did DATA run from the mini\'s own port.</p>'),
        sec("Keep monitors off it", '<p>DisplayPort video reserves outbound Thunderbolt bandwidth, the same direction drive writes use. With the main KTC (1440p at 180 Hz) on the dock, Media\'s writes capped near 1.5 GB/s; with no display on it they reach about 3 GB/s. Reads were barely affected. From November 22 to 23 the main monitor ran through the dock to free a port for DATA. That trial was undone after the screen stayed dark following a restart, cause not found. Both monitors plug into the mini directly.</p>'),
    ]))

# ---------------------------------------------------------------- Media
D.append(dict(
    slug="media", name="Media", em="Crucial P310 2 TB", group="Storage", bus="tb", spd="40 Gb/s · Gen4 x4",
    card="Crucial P310 2 TB in a fanless Mokin USB4 enclosure. The Plex and Apple TV streaming source.",
    lede="The streaming library. A Crucial P310 2 TB NVMe drive in a fanless Mokin USB4 enclosure, behind the Wavlink dock.",
    path=[MINI, UPLINK, DOCK, ("wire", "40 Gb/s USB4", "tb"), ("node", "Mokin enclosure", "ASMedia 246x", None), ("wire", "PCIe Gen4 x4", "tb"), ("node", "Crucial P310 2 TB", "volume Media", "me")],
    stats=[("3,816", "MB/s", "read, alone"), ("2,972", "MB/s", "write, alone"), ("934", "GB", "used of 2 TB"), ("51", "°C", "idle")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", 'Crucial P310 2 TB <span class="mono">(CT2000P310SSD8)</span>, QLC flash, firmware VACR011'),
            ("Drive link", "PCIe Gen4, 4 lanes, 16 GT/s"),
            ("Enclosure", "Mokin USB4 enclosure, fanless"),
            ("Enclosure chip", 'ASMedia 246x <span class="mono">(device 0x2463)</span>, firmware 4b.29'),
            ("Enclosure link", "40 Gb/s USB4, on a Wavlink Thunderbolt port"),
            ("Volume", "Media (APFS), formerly EXTERNAL-2TB. 934 GB used, 1.07 TB free."),
            ("Job", "Source for Plex and Apple TV streaming. A 4K remux needs about 12 MB/s."),
        ])),
        sec("Measured speed", bars([
            ("Direct on the mini", "Nov 6, 4 GB", 3210, 3845, "tb"),
            ("Behind the dock", "Nov 23, 8 GB, alone", 2972, 3816, "tb"),
            ("Behind the dock", "Nov 23, DATA busy too", 1788, 2008, "tb"),
            ("With the main display on the dock", "Nov 22 trial, alone", 1481, 3608, "tb"),
            ("Sustained write", "after the cache fills", 900, 0, "tb"),
        ]),
            '<p class="note-t">fio with direct I/O. Random 4k at queue depth 32 (70% read): 55k read and 23k write operations per second with the drive cool (November 22).</p>',
            '<p>Short writes land in a fast cache at about 3 GB/s. Once the cache fills, writes settle near 0.9 GB/s, which is the limit of QLC flash. Reads are not affected. During the November 22 trial, with the main display on the dock, writes arrived at no more than about 1.5 GB/s.</p>'),
        sec("Heat", '<p>The enclosure has no fan. The drive sits at 43 to 55 °C in normal use. It reached 70 °C after about 400 GB of nonstop writes, and 77 °C in a stress test that pushed about 560 GB of I/O in 8 minutes. It never throttled. In the November 23 load test it went from 55 to 61 °C. A longer retest on November 22 peaked at 77 °C, with no errors or drops. The critical limit is 85 °C. A heatsink or some airflow would help on very long runs.</p>'),
        sec("Health", spec([
            ("Wear", "0% used, 100% spare"),
            ("Written / read", "7.26 TB / 11.9 TB"),
            ("Power-on time", "1,151 hours, 116 power cycles"),
            ("Unsafe shutdowns", "56"),
            ("Media errors", "0"),
        ]),
            '<p class="note-t">From smartctl, November 23, 2026 (SMART status passed). It was pulled while mounted during the November 22 swap, and verified clean afterwards. Most of the unsafe shutdowns come from unplugging without ejecting during the October troubleshooting. Eject first.</p>'),
    ]))

# ---------------------------------------------------------------- DATA
D.append(dict(
    slug="data", name="DATA", em="Samsung 990 PRO 1 TB", group="Storage", bus="tb", spd="40 Gb/s · Gen4 x4",
    card="Samsung 990 PRO 1 TB in a fanless Mokin USB4 enclosure. The fastest drive here for small random work.",
    lede="The working drive. A Samsung 990 PRO 1 TB in a fanless Mokin USB4 enclosure, on a dock port next to Media's Mokin. It moved there from an ACASIS Thunderbolt 3 enclosure on November 13, and spent November 22 to 23 on the mini's own port R4.",
    path=[MINI, UPLINK, DOCK, ("wire", "40 Gb/s USB4", "tb"), ("node", "Mokin enclosure", "ASMedia 246x", None), ("wire", "PCIe Gen4 x4", "tb"), ("node", "990 PRO 1 TB", "volume DATA", "me")],
    stats=[("3,835", "MB/s", "read, alone"), ("3,669", "MB/s", "write, alone"), ("112k", "IOPS", "random 4k read"), ("39", "°C", "idle")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", "Samsung SSD 990 PRO 1 TB, firmware 3B2QJXD7"),
            ("Drive link", "PCIe Gen4, 4 lanes, 16 GT/s, the drive's full link"),
            ("Enclosure", "Mokin USB4 enclosure, fanless. Until November 13 an ACASIS TBU405Pro (Thunderbolt 3), now a spare."),
            ("Enclosure chip", 'ASMedia 246x <span class="mono">(device 0x2463)</span>, firmware 53.26'),
            ("Enclosure link", "40 Gb/s USB4, on a Wavlink Thunderbolt port next to Media, on the dock's power. On the mini's port R4 from November 22 to 23."),
            ("Volume", "DATA (APFS, not encrypted), formerly SAMSUNG SSD. 103 GB used, 897 GB free."),
            ("History", "Came over from the MacBook Pro."),
        ])),
        sec("Measured speed", bars([
            ("Mokin, behind the dock", "Nov 23, 8 GB, alone", 3669, 3835, "tb"),
            ("Mokin, behind the dock", "Nov 23, Media busy too", 2232, 2011, "tb"),
            ("Mokin, on the mini's R4", "Nov 22 trial, alone", 3677, 3861, "tb"),
            ("Mokin, on the mini's R4", "Nov 22 trial, Media busy too", 3658, 3861, "tb"),
            ("Sustained write", "Nov 13, 3 minutes nonstop", 3674, 0, "tb"),
            ("ACASIS, behind the dock", "Nov 11, 8 GB, alone", 2930, 3170, "tb"),
        ], 3861),
            '<p class="note-t">fio with direct I/O. Random 4k at queue depth 32 (70% read): 112k read and 48k write operations per second on November 20, the same as in the ACASIS. That is more than twice the internal SSD (43k and 18k) in the same test. On November 13, the first day in the Mokin, it measured 3,660 MB/s write and 3,831 read. A retest that evening, after the move to the 15 W port, gave 3,490 MB/s write and 3,624 read. Media, which did not move, dropped by the same 5%, so that is run-to-run spread, not the port.</p>'),
        sec("Heat", '<p>The Mokin has no fan. Its thermal pad presses the drive against the aluminum case, which works as the heatsink, so the case feels warm in use. The 3-minute sustained write rewrote a 64 GB file, 661 GB in all, at a steady 3,674 MB/s. The drive went from 31 to 42 °C, far below where it would slow down.</p>'),
        sec("Thunderbolt 3 against USB4", table(["Standard", "Speed", "In this setup"], [
            ("Thunderbolt 3 (2015)", "40 Gb/s", "The ACASIS enclosure DATA used until November 13"),
            ("USB4 (2019)", "20 or 40 Gb/s", 'The Mokin enclosures holding DATA and <a href="media.html">Media</a>'),
            ("Thunderbolt 4 (2020)", "40 Gb/s", "The mini's three back ports"),
            ("Thunderbolt 5 (2024)", "80 or 120 Gb/s", 'The <a href="wavlink-dock.html">Wavlink dock</a>, held to 40 Gb/s by the mini'),
        ]),
            '<p>Both enclosures hold a 40 Gb/s link. The difference is inside. The ACASIS Thunderbolt 3 chip reached the 990 PRO at PCIe Gen3, about 3.2 GB/s. The Mokin\'s USB4 chip runs it at Gen4, so reads rose from 3,170 to 3,831 MB/s and writes from 2,930 to 3,660 MB/s. About 3.8 GB/s is the most any enclosure gets on the mini\'s 40 Gb/s ports. Neither enclosure would get faster on a Thunderbolt 5 port.</p>'),
        sec("Health", spec([
            ("Wear", "0% used, 100% spare"),
            ("Written / read", "3.71 TB / 1.92 TB"),
            ("Power-on time", "942 hours, 140 power cycles"),
            ("Unsafe shutdowns", "70"),
            ("Media errors", "0"),
        ]),
            '<p class="note-t">From smartctl, November 23, 2026 (SMART status passed). The count went from 58 to 61 when the drive was moved on November 10, to 63 with the enclosure swap on November 13, and to 68 by November 15, which included a forced restart. It read 70 after the November 22 swap and was unchanged on November 23. Eject before unplugging.</p>'),
    ]))

# ---------------------------------------------------------------- Scratch
D.append(dict(
    slug="scratch-disk", checked="November 23, 2026", name="Scratch Disk", em="512 GB SSD", group="Storage", bus="usb", spd="10 Gb/s USB",
    card="512 GB SSD in a Ugreen USB enclosure. Temp files and working space, kept off the internal drive.",
    lede="Working space. A 512 GB SSD in a Ugreen USB enclosure, plugged into one of the dock's USB-A ports.",
    path=[MINI, UPLINK, DOCK, ("wire", "USB hub · 10 Gb/s", "usb"), ("node", "Ugreen enclosure", "Realtek RTL9210", None), ("wire", "NVMe", "usb"), ("node", "512 GB SSD", "volume Scratch Disk", "me")],
    stats=[("768", "MB/s", "write"), ("692", "MB/s", "read"), ("69", "GB", "used of 512 GB"), ("10", "Gb/s", "USB link")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", "512 GB NVMe SSD"),
            ("Enclosure", 'Ugreen USB enclosure, Realtek RTL9210 bridge <span class="mono">(0bda:9210)</span>'),
            ("Link", "USB 10 Gb/s, drawing up to 4.5 W from the dock"),
            ("Where", "An orange USB-A port on the Wavlink, using a USB-A to C cable rated 10 Gb/s. It sits two Parade hubs below the dock's main USB hub. Until November 13 it was on a Thunderbolt port."),
            ("Volume", "Scratch Disk (APFS). 69 GB used, 443 GB free."),
            ("Job", "Temporary files, test output and working copies, so the internal SSD stays clear."),
        ])),
        sec("Measured speed", bars([
            ("USB-A port, alone", "Nov 23, 8 GB, median of 3", 768, 692, "usb"),
            ("USB-A port, alone", "Nov 20, 8 GB", 737, 674, "usb"),
            ("USB-A port, all at once", "Nov 20", 756, 697, "usb"),
            ("USB-A port, alone", "Nov 13, 8 GB", 766, 684, "usb"),
            ("Thunderbolt port, alone", "Nov 13, 8 GB", 787, 752, "usb"),
            ("Thunderbolt port, all at once", "Nov 13", 787, 754, "usb"),
        ], 1250),
            '<p class="note-t">fio with direct I/O. The bar scale ends at 1,250 MB/s, the ceiling of a 10 Gb/s USB link. Random 4k at queue depth 32: 11k to 12k read and 5k write operations per second on either port (11k and 5k on November 20). The USB-A port costs about 3% on writes and 9% on reads, from the two extra hub hops.</p>',
            '<p>The drive is limited by its USB bridge, not by the dock. It keeps full speed while the two NVMe drives are busy, because 0.8 GB/s is a small share of the dock\'s 4 GB/s.</p>'),
        sec("History", '<p>This SSD used to sit in the M.2 slot of an Ivanky USB dock, where it measured the same ~780 MB/s. When the Wavlink replaced that dock, the drive moved into its own enclosure. Since November 27 that Ivanky dock serves the <a href="macbook/ivanky-dock.html">MacBook Pro</a>.</p>'),
    ]))

# ---------------------------------------------------------------- SSD BACKUP
D.append(dict(
    slug="ssd-backup", checked="November 22, 2026; speeds are from November 20", name="SSD BACKUP", em="WD Green SN350 2 TB", group="Storage", bus="usb", spd="10 Gb/s USB",
    card="WD Green SN350 2 TB in a UGREEN USB enclosure on the mini's front port. Time Machine copy of Media.",
    lede="The fast backup. A WD Green SN350 2 TB in a UGREEN USB enclosure on the mini's own front USB-C port, outside the dock.",
    path=[MINI, ("wire", "front USB-C · 10 Gb/s", "usb"), ("node", "UGREEN enclosure", "Realtek RTL9210", None), ("wire", "NVMe", "usb"), ("node", "WD Green SN350 2 TB", "volume SSD BACKUP", "me")],
    stats=[("866", "MB/s", "read"), ("1.32", "TB", "used of 2 TB"), ("10", "Gb/s", "USB link"), ("0", "", "shared with the dock")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", "WD Green SN350 2 TB, PCIe Gen3, QLC flash, no DRAM cache"),
            ("Enclosure", 'UGREEN USB enclosure, Realtek RTL9210 bridge <span class="mono">(0bda:9210)</span>'),
            ("Link", "USB 10 Gb/s, the most the front port and the enclosure both offer"),
            ("Where", "One of the mini's two front USB-C ports. The other is free."),
            ("Volume", "SSD BACKUP (case-sensitive APFS). 1.32 TB used, 679 GB free."),
            ("Job", 'Time Machine destination. It holds a backup of <a href="media.html">Media</a>.'),
        ])),
        sec("Measured speed", bars([
            ("Alone", "Nov 20, 8 GB read", None, 866, "usb"),
            ("Alone", "Nov 11, 8 GB read", None, 860, "usb"),
            ("While the dock is busy", "Nov 11", None, 870, "usb"),
        ], 1250),
            '<p class="note-t">Time Machine blocks ordinary writes to its destination, so this drive was tested read-only on an existing file. The bar scale ends at 1,250 MB/s, the ceiling of a 10 Gb/s USB link. On November 20 the first read after a backup gave only 562 MB/s, then 829, 868 and 864; the bar is the average of the last two. Random 4k reads at queue depth 32: 40k per second.</p>',
            '<p>Because it is on the mini\'s own port, it does not share the dock\'s link. On November 11 it held 870 MB/s while the three drives then on the dock ran flat out.</p>'),
        sec("Things to know", notes([
            "QLC flash with no DRAM: a large first backup slows once the drive's cache fills. Later backups are small and quick.",
            "Keep 15 to 20% free so the drive has room to work.",
            "USB enclosures do not pass the drive's temperature or SMART data through, so there is no health readout for it.",
        ])),
    ]))

# ---------------------------------------------------------------- Backup HDD
D.append(dict(
    slug="backup-hdd", checked="November 20, 2026", name="Backup", em="WD Elements 4 TB", group="Storage", bus="usb5", spd="5 Gb/s USB",
    card="WD Elements 4 TB hard drive. The main Time Machine disk.",
    lede="The big, slow, safe one. A WD Elements 4 TB hard drive on the dock's USB hub, used only by Time Machine.",
    path=[MINI, UPLINK, DOCK, ("wire", "USB hub · 5 Gb/s", "usb5"), ("node", "WD Elements 4 TB", "volume Backup", "me")],
    stats=[("~95", "MB/s", "read"), ("2.7", "TB", "used of 4 TB"), ("5", "Gb/s", "USB link")],
    body=[
        sec("The drive", spec([
            ("Drive", 'WD Elements 4 TB portable hard drive <span class="mono">(1058:2621)</span>'),
            ("Link", "USB 5 Gb/s, drawing up to 4.5 W from the dock"),
            ("Where", "The Wavlink's USB 3 hub, behind one of its Parade hubs"),
            ("Volume", "Backup (APFS). 2.7 TB used, 1.3 TB free (November 20)."),
            ("Job", "Time Machine destination for the mini."),
        ])),
        sec("Measured speed", '<p>Reads measured 89 to 98 MB/s on November 6. That is normal for a portable hard drive, and far below what its 5 Gb/s link could carry. Time Machine blocks ordinary writes, so writes were not tested.</p>'),
        sec("Things to know", notes([
            "A hard drive is the slowest device here by a wide margin, which does not matter for hourly backups that run in the background.",
            'The <a href="ssd-backup.html">SSD BACKUP</a> drive is a second, faster Time Machine destination.',
        ])),
    ]))

# ---------------------------------------------------------------- KTC
D.append(dict(
    slug="ktc-h24t7", name="KTC H24T7", em="main display", group="Displays", bus="dp", spd="DisplayPort · 180 Hz",
    card="24-inch 1440p Fast IPS at 180 Hz with VRR, on DisplayPort straight from the mini.",
    lede="The main display. A 24-inch 1440p Fast IPS panel at 180 Hz, on the right of the desk, on DisplayPort end to end from the mini's port R4.",
    path=[MINI, ("wire", "R4 · USB-C to DP", "dp"), ("node", "USB-C to DP cable", "4 lanes · HBR3", None), ("wire", "DisplayPort", "dp"), ("node", "KTC H24T7", "1440p · 180 Hz · VRR", "me")],
    stats=[("180", "Hz", "refresh, with VRR"), ("2560×1440", "", "panel"), ("400", "nits", "HDR400"), ("~95", "%", "DCI-P3")],
    body=[
        sec("The panel", spec([
            ("Panel", "24-inch Fast IPS, 2560×1440"),
            ("Refresh", "180 Hz, 185 Hz overclocked, variable refresh"),
            ("Brightness", "400 nits, HDR400"),
            ("Colour", '8-bit plus FRC (sold as "10-bit"), about 95% DCI-P3 wide gamut'),
            ("Contrast", "1000:1"),
        ])),
        sec("How it is connected", spec([
            ("Port", "Mac mini Thunderbolt port R4. Through the Wavlink dock from November 22 to 23."),
            ("Cable", "USB-C to DisplayPort"),
            ("Signal", "DisplayPort alt mode, 4 lanes at HBR3, no compression (no DSC)"),
            ("Running at", "Looks like 2560×1440 in HiDPI (5120×2880 backing) at 180 Hz, VRR 50 to 180 Hz"),
            ("Colour", "RGB Full, 10-bit, with its own H24T7 colour profile"),
            ("Role", "Main display"),
        ])),
        sec("Things to know", notes([
            'Keep it off the <a href="wavlink-dock.html">Wavlink dock</a>. From November 22 to 23 it ran through the dock to free a port for DATA. Writes behind the dock capped near 1.5 GB/s, and after a restart on the morning of November 23 this screen stayed dark, cause not found. It went back to R4 that day.',
            "Until November 16 it ran on the mini's HDMI port, which held it to 144 Hz with no VRR (the monitor's HDMI maximum). There macOS picked YCbCr Limited with a generic profile and it needed a manual fix in BetterDisplay. On DisplayPort it came up RGB Full with its own profile.",
            'A <a href="ktc-h24t7-hdmi.html">second H24T7</a> sits to its left, on DisplayPort from port R1. Both report the same identity to macOS, so tell them apart by port.',
            'Its HDMI input carries the <a href="../macbook-pro.html">MacBook</a>, over a USB-C to HDMI cable from that machine\'s dock, at 144 Hz. Both computers stay plugged in; the monitor\'s input button switches between them, no KVM.',
        ])),
    ]))

# ---------------------------------------------------------------- KTC #2 (HDMI)
D.append(dict(
    slug="ktc-h24t7-hdmi", name="KTC H24T7 #2", em="second display", group="Displays", bus="dp", spd="DisplayPort · 180 Hz",
    card="A second 24-inch 1440p KTC, at 180 Hz with VRR on DisplayPort from the mini's port R1.",
    lede="The second display, the same model as the main one. A 24-inch 1440p Fast IPS panel at 180 Hz with VRR, on the left of the desk. It runs DisplayPort end to end from the mini's port R1.",
    path=[MINI, ("wire", "R1 · USB-C to DP", "dp"), ("node", "USB-C to DP cable", "4 lanes · HBR3", None), ("wire", "DisplayPort", "dp"), ("node", "KTC H24T7", "1440p · 180 Hz · VRR", "me")],
    stats=[("180", "Hz", "refresh, with VRR"), ("2560×1440", "", "panel"), ("400", "nits", "HDR400"), ("~95", "%", "DCI-P3")],
    body=[
        sec("The panel", '<p>The same panel as the <a href="ktc-h24t7.html">main display</a>: 24-inch Fast IPS, 2560×1440, 400 nits, about 95% DCI-P3.</p>'),
        sec("How it is connected", spec([
            ("Port", "Mac mini Thunderbolt port R1"),
            ("Cable", "USB-C to DisplayPort"),
            ("Signal", "DisplayPort alt mode, 4 lanes at HBR3, no compression (no DSC)"),
            ("Running at", "Looks like 2560×1440 in HiDPI (5120×2880 backing) at 180 Hz, VRR 50 to 180 Hz"),
            ("Colour", "RGB Full, 10-bit, with its own H24T7 colour profile"),
            ("Role", "Second display"),
        ])),
        sec("Things to know", notes([
            "Keep it on DisplayPort. Through an HDMI 1.4-class USB-C to HDMI cable it dropped to 75 Hz.",
            'Its HDMI input carries the <a href="../macbook-pro.html">MacBook</a>, over a USB-C to HDMI cable from that machine\'s dock, at 144 Hz. That is plenty for work. Both computers stay plugged in; the monitor\'s input button switches between them, no KVM.',
            "All three of the mini's back Thunderbolt ports are in use: this display on R1, the main display on R4 and the dock on R2.",
        ])),
    ]))

# ---------------------------------------------------------------- Dell (spare)
D.append(dict(
    slug="dell-s2425hs", name="Dell S2425HS", em="spare display", group="Displays", bus="hdmi", spd="Not connected",
    card="24-inch 1080p IPS at 100 Hz. Unplugged from the mini on November 15, 2026, replaced by a second KTC.",
    lede="The former second display, now a spare. A 24-inch 1080p IPS panel, 100 Hz at most. A second KTC H24T7 took its place on the mini's HDMI port on November 15, 2026.",
    checked="November 15, 2026",
    path=[MINI, ("wire", "HDMI · until Nov 15", "hdmi"), ("node", "Dell S2425HS", "1080p · 100 Hz · spare", "me")],
    stats=[("100", "Hz", "refresh, panel max"), ("1920×1080", "", "panel"), ("250", "nits", ""), ("99", "%", "sRGB")],
    body=[
        sec("The panel", spec([
            ("Panel", "24-inch IPS, 1920×1080"),
            ("Refresh", "100 Hz, the panel's maximum"),
            ("Brightness", "250 nits"),
            ("Colour", "8-bit, 99% sRGB"),
            ("Contrast", "1500:1"),
        ])),
        sec("Status", spec([
            ("Now", "Not connected to the Mac mini"),
            ("Until Nov 15", "Mac mini HDMI, looks like 1920×1080 in HiDPI (3840×2160 backing) at 100 Hz"),
            ("Replaced by", '<a href="ktc-h24t7.html">KTC H24T7</a>, now the main display'),
        ])),
        sec("Things to know", notes([
            'Next to a <a href="ktc-h24t7.html">KTC</a> its white never quite matched: this is an sRGB 250-nit panel and the KTC is a wide-gamut 400-nit one. Two identical KTCs solve that.',
        ])),
    ]))

# ---------------------------------------------------------------- LAN
D.append(dict(
    slug="lan-adapter", checked="November 20, 2026", name="Realtek 2.5G LAN", em="USB adapter", group="Other", bus="net", spd="5 Gb/s USB · idle",
    card="Realtek RTL8156 2.5 Gb Ethernet on the dock's USB hub. Present but not in use.",
    lede="A spare network port. A Realtek RTL8156 2.5 Gb Ethernet adapter on the dock's USB hub. Nothing is plugged into it.",
    path=[MINI, UPLINK, DOCK, ("wire", "USB hub · 5 Gb/s", "usb5"), ("node", "Realtek RTL8156", "en12 · not in use", "me")],
    stats=[("2.5", "Gb/s", "Ethernet, rated"), ("5", "Gb/s", "USB link"), ("en12", "", "interface")],
    body=[
        sec("The adapter", spec([
            ("Chip", 'Realtek RTL8156 <span class="mono">(0bda:8156)</span>'),
            ("macOS name", "USB 10/100/1G/2.5G LAN, interface en12"),
            ("Link", "USB 5 Gb/s, about 1.3 W"),
            ("Where", "The Wavlink's USB 3 hub, behind one of its Parade hubs"),
            ("Status", "No cable, no address. Not in use."),
        ])),
        sec("Why it is idle", '<p>The mini has its own 2.5 Gb Ethernet port (en0), and that carries all the traffic through the <a href="home-network.html">home network</a>: about 2.13 Gb/s down and 2.12 Gb/s up. A second 2.5 Gb port through a shared USB hub would add nothing, so this one stays empty.</p>'),
    ]))

# ---------------------------------------------------------------- Blu-ray
D.append(dict(
    slug="blu-ray", checked="November 20, 2026", name="Blu-ray burner", em="Matshita UJ260", group="Other", bus="usb2", spd="480 Mb/s USB 2",
    card="Matshita BD-MLT UJ260 slim Blu-ray and DVD burner on the dock's USB 2 side.",
    lede="For discs. A Matshita BD-MLT UJ260 slim Blu-ray and DVD burner in a USB 2 case, on the dock's USB 2 side.",
    path=[MINI, UPLINK, DOCK, ("wire", "USB 2 · 480 Mb/s", "usb2"), ("node", "Initio bridge", "13fd:0840", None), ("wire", "SATA", "usb2"), ("node", "Matshita UJ260", "BD / DVD burner", "me")],
    stats=[("480", "Mb/s", "USB 2 link"), ("BD · DVD · CD", "", "reads and burns")],
    body=[
        sec("The drive", spec([
            ("Drive", "Matshita BD-MLT UJ260, slim Blu-ray / DVD burner"),
            ("USB bridge", 'Initio slim-drive bridge <span class="mono">(13fd:0840)</span>. macOS lists it as "External" from "Generic".'),
            ("Link", "USB 2, 480 Mb/s"),
            ("Where", "The Wavlink's USB 2 side, behind a Parade hub"),
            ("Software", "macOS's built-in disc burning support"),
        ])),
        sec("Is USB 2 enough?", '<p>Yes. USB 2 carries up to about 60 MB/s on paper. Blu-ray at 6x speed is about 27 MB/s, so the disc is the limit, not the cable.</p>'),
    ]))

# ---------------------------------------------------------------- Home network
D.append(dict(
    slug="home-network", checked="November 20, 2026", name="Home network", em="wired 2.5 Gb", group="Network", bus="net", spd="2.5 Gb/s Ethernet",
    card="The mini's built-in 2.5 Gb Ethernet into an ACASIS 2.5 Gb switch. 2.30 Gb/s down and 2.31 Gb/s up in the last test.",
    lede="How the mini reaches the internet. Its built-in 2.5 Gb Ethernet port runs to an ACASIS 2.5 Gb Ethernet switch, and from there to the router.",
    path=[MINI, ("wire", "en0 · 2500Base-T", "net"), ("node", "ACASIS 2.5GbE switch", "Ethernet hub for the desk", "me"), ("wire", "Ethernet", "net"), ("node", "Router", "internet", None)],
    stats=[("2.30", "Gb/s", "down"), ("2.31", "Gb/s", "up"), ("11.0", "ms", "idle latency"), ("0.68", "ms", "ping to the router")],
    body=[
        sec("The link", spec([
            ("Mac port", "Built-in 2.5 Gb Ethernet, interface en0"),
            ("Plugged into", "ACASIS 2.5 Gb Ethernet switch"),
            ("Negotiated", "2500Base-T, full duplex, flow control on. That is the port's top speed."),
            ("MTU", "1500"),
            ("Role", "Default route. All of the mini's traffic goes over this cable."),
            ("Router ping", "0.62 / 0.76 / 0.86 ms (min / average / max), 10 of 10 packets returned"),
        ]),
            '<p class="note-t">Read from ifconfig and ping on November 11, 2026.</p>'),
        sec("A detailed speed test", '<p class="note-t">Apple\'s <span class="mono">networkQuality</span> on en0, November 11, 2026 at 6:42 PM. The test ran for 21.6 seconds.</p>',
            table(["Measure", "Result", "Detail"], [
                ("Download", "2.128 Gb/s", "5.56 GB moved over 8 flows"),
                ("Upload", "2.124 Gb/s", "4.47 GB moved over 16 flows"),
                ("Idle latency", "10.8 ms", "5,566 round trips per minute"),
                ("Responsiveness under load", "High", "1,411 round trips per minute, 42.5 ms"),
                ("Protocol", "HTTP/2", "100% of flows"),
                ("Accuracy", "High", "For capacity, latency and responsiveness"),
            ]),
            '<p>Both directions land at about 85% of the 2.5 Gb/s link, so the cable, the switch and the internet line all keep up with each other. Latency stays low while the line is full, which is what the High responsiveness rating means.</p>'),
        sec("All tests", table(["Date", "Interface", "Down", "Up", "Idle latency"], [
            ("Nov 20, 2026", "en0 · wired", "2.30 Gb/s", "2.31 Gb/s", "11.0 ms"),
            ("Nov 16, 2026", "en0 · wired", "2.15 Gb/s", "2.10 Gb/s", "9.4 ms"),
            ("Nov 15, 2026", "en0 · wired", "2.15 Gb/s", "2.09 Gb/s", "9.9 ms"),
            ("Nov 11, 2026", "en0 · wired", "2.13 Gb/s", "2.12 Gb/s", "10.8 ms"),
            ("Nov 7, 2026", "en0 · wired", "2.15 Gb/s", "2.12 Gb/s", "15 ms"),
            ("Oct 17, 2026", "en0 · wired", "2.29 Gb/s", "2.18 Gb/s", "—"),
            ("Nov 20, 2026", "en1 · Wi-Fi 7, 6 GHz", "743 Mb/s", "937 Mb/s", "13.3 ms"),
            ("Nov 16, 2026", "en1 · Wi-Fi 7, 5 GHz", "254 Mb/s", "266 Mb/s", "14.7 ms"),
            ("Nov 15, 2026", "en1 · Wi-Fi 7, 5 GHz", "179 Mb/s", "270 Mb/s", "15.5 ms"),
            ("Nov 7, 2026", "en1 · Wi-Fi 7, 5 GHz", "226 Mb/s", "238 Mb/s", "17 ms"),
        ], num=(2, 3, 4)),
            '<p class="note-t">Wired has held at 2.1 to 2.3 Gb/s across six tests. On 5 GHz Wi-Fi managed about a tenth of that: three runs on November 16 gave 220 to 258 Mb/s down and 252 to 289 Mb/s up. On 6 GHz (channel 37, 160 MHz) on November 20 it reached 743 down and 937 up, about a third of wired. Router ping on November 16: 0.68 ms average, no loss.</p>'),
        sec("Things to know", notes([
            "The mini also has Wi-Fi 7 (en1) connected, but the wired port is the default route.",
            'A second 2.5 Gb port sits unused on the dock: the <a href="lan-adapter.html">Realtek LAN adapter</a>.',
        ])),
    ]))

SLUGS = [d["slug"] for d in D]
for i, d in enumerate(D):
    prev, nxt = D[i - 1], D[(i + 1) % len(D)]
    hero = (f'<div class="eyebrow"><a href="../mac-mini.html">Mac mini setup</a> / {d["group"]} / <b>{d["spd"]}</b></div>\n'
            f'<h1>{d["name"]} <em>{d["em"]}</em></h1>\n<p class="lede">{d["lede"]}</p>\n{path(d["path"])}\n{stats(d["stats"])}')
    pager = (f'<div class="pager"><a href="{prev["slug"]}.html">&larr; {prev["name"]}</a>'
             f'<a href="../mac-mini.html">All devices</a><a href="{nxt["slug"]}.html">{nxt["name"]} &rarr;</a></div>')
    foot = f'<p class="note-t">Read from system_profiler, smartctl and fio on the Mac mini. Checked {d.get("checked", CHECKED)}.</p>'
    page(f'devices/{d["slug"]}.html', f'{d["name"]} · Mac mini setup', d["card"], d["bus"], hero, "\n".join(d["body"]) + "\n" + foot + "\n" + pager)

# ================================================================= hub
svg = (ROOT / "_src/diagram.svg").read_text().replace('<text x="28" y="650" class="tm">192.168.1.2</text>', "")
HITS = [("ktc-h24t7", "dp", 190, 30, 165, 118), ("ktc-h24t7-hdmi", "dp", 15, 30, 165, 118), ("ssd-backup", "usb", 15, 700, 340, 106),
        ("wavlink-dock", "tb", 430, 40, 230, 100), ("media", "tb", 760, 150, 385, 62), ("data", "tb", 760, 226, 385, 62),
        ("scratch-disk", "usb", 760, 706, 385, 62), ("backup-hdd", "usb5", 760, 478, 385, 62), ("lan-adapter", "net", 760, 554, 385, 62),
        ("blu-ray", "usb2", 760, 630, 385, 62), ("home-network", "net", 15, 560, 165, 110)]
names = {d["slug"]: d["name"] for d in D}
hits = "".join(f'<a href="devices/{s}.html" class="b-{b}" aria-label="{names[s]}"><rect class="hit" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></a>' for s, b, x, y, w, h in HITS)
svg = svg.replace("</svg>", hits + "</svg>")
KEYS = [("tb", "Thunderbolt / USB4 40 Gb/s"), ("dp", "DisplayPort"), ("usb", "USB 10 Gb/s"), ("usb5", "USB 5 Gb/s"), ("usb2", "USB 2"), ("net", "Ethernet")]
fig = ('<figure class="wiring"><div class="dscroll">' + svg + '</div><figcaption>'
       + "".join(f'<span class="key b-{b}"><i></i>{t}</span>' for b, t in KEYS)
       + '<span>R1, R2 and R4 are the numbers macOS gives the mini\'s Thunderbolt ports. Select a device to open its page.</span></figcaption></figure>')

cards = ""
for g in ["Dock", "Storage", "Displays", "Network", "Other"]:
    cards += f'<div class="grp">{g}</div><div class="grid">' + "".join(
        f'<a class="card b-{d["bus"]}" href="devices/{d["slug"]}.html"><span class="spd">{d["spd"]}</span><b>{d["name"]}</b><span>{d["card"]}</span><span class="go">Details &rarr;</span></a>'
        for d in D if d["group"] == g) + "</div>\n"

L = lambda s, t: f'<a href="devices/{s}.html">{t}</a>'
OK = '<span class="okk">✓ max</span>'
hub = "\n".join([
    f'<section><h2>What is plugged into what</h2>{fig}</section>',
    f'<section><h2>The devices</h2><p class="note-t">Each one has its own page: what it is, the chip inside, the path its signal takes from the mini, and what it measured.</p>{cards}</section>',
    sec("The machine", spec([
        ("Model", "Mac mini (Mac18,5), 2026"),
        ("Chip", "Apple M6: 12-core CPU (2 Super, 4 Performance, 6 Efficiency), 12-core GPU"),
        ("Memory and storage", "16 GB, 512 GB internal SSD (283 GB used)"),
        ("Software", "macOS 27.2.1"),
        ("Back ports", "3 Thunderbolt 4 (R1 second monitor, R4 main monitor, R2 dock), HDMI (free), 2.5 Gb Ethernet"),
        ("Front ports", "2 USB-C at 10 Gb/s (one drive, one free), headphone jack"),
        ("Wireless", "Wi-Fi 7, Bluetooth 6. MX Keys S keyboard and MX Anywhere 3S mouse over Bluetooth."),
    ])),
    sec("Every link, against its maximum", '<p class="note-t">The most each port allows, next to what macOS reports as negotiated on November 23 (the iPad, last seen November 14). Every link negotiates its maximum.</p>',
        table(["Connection", "Chip", "Port maximum", "Negotiated", ""], [
            ("Mac mini → " + L("wavlink-dock", "Wavlink dock") + '<br><span class="sub">Thunderbolt port R2</span>', "Wavlink TB5 controller", "40 Gb/s (TB4 host)", "40 Gb/s, USB4 v2 mode", OK),
            ("Mac mini → " + L("ktc-h24t7-hdmi", "KTC H24T7 #2") + '<br><span class="sub">Left. Port R1, USB-C to DP cable</span>', "DP alt mode", "DP 4 lanes, HBR3", "4 lanes, top rate, no compression · 180 Hz, VRR", OK),
            ("Mac mini → " + L("ktc-h24t7", "KTC H24T7") + '<br><span class="sub">Main, right. Port R4, USB-C to DP cable</span>', "DP alt mode", "DP 4 lanes, HBR3", "4 lanes, top rate, no compression · 180 Hz, VRR", OK),
            ("Mac mini → " + L("ssd-backup", "SSD BACKUP") + '<br><span class="sub">Front USB-C</span>', "Realtek RTL9210", "10 Gb/s", "10 Gb/s", OK),
            ("Wavlink → Media's Mokin enclosure", "ASMedia 246x", "40 Gb/s", "40 Gb/s USB4", OK),
            ("↳ " + L("media", "Media") + " · Crucial P310", "Crucial P310 (QLC)", "PCIe Gen4 x4", "Gen4 x4, 16 GT/s", OK),
            ("Wavlink → DATA\'s Mokin enclosure", "ASMedia 246x", "40 Gb/s", "40 Gb/s USB4", OK),
            ("↳ " + L("data", "DATA") + " · Samsung 990 PRO", "Samsung 990 PRO", "PCIe Gen4 x4", "Gen4 x4, 16 GT/s", OK),
            ("Wavlink → iPad mini" + '<br><span class="sub">Front 30 W port, 80 Gb/s cable, also used for the iPhone</span>', "Apple iPad mini", "10 Gb/s (iPad USB 3)", "10 Gb/s, over USB4", OK),
            ("↳ iPad mini charging", "USB-C PD", "30 W", "15 V / 2 A = 30 W", OK),
            ("Wavlink → " + L("scratch-disk", "Scratch Disk"), "Realtek RTL9210", "10 Gb/s (USB enclosure)", "10 Gb/s", OK),
            ("Wavlink → " + L("backup-hdd", "Backup") + " · WD Elements", "WD USB bridge", "5 Gb/s", "5 Gb/s", OK),
            ("Wavlink → " + L("lan-adapter", "2.5G LAN adapter"), "Realtek RTL8156", "5 Gb/s", "5 Gb/s", OK),
            ("Wavlink → " + L("blu-ray", "Blu-ray burner"), "Initio bridge", "USB 2", "480 Mb/s", OK),
            ("Mac mini → " + L("home-network", "home network") + '<br><span class="sub">en0, into the ACASIS 2.5GbE switch</span>', "Built-in 2.5GbE", "2.5 Gb/s", "2500Base-T full duplex", OK),
        ])),
    sec("Drive speeds", '<p class="note-t">fio, 8 GB direct I/O. DATA, Media and the Scratch Disk are the median of three runs on November 23. The internal SSD and SSD BACKUP were last tested November 20, on the same layout.</p>',
        bars([
            ("Internal SSD", "alone, Nov 20", 5781, 6473, "usb2"),
            ("DATA · 990 PRO", "alone", 3669, 3835, "tb"),
            ("Media · P310", "alone", 2972, 3816, "tb"),
            ("SSD BACKUP · SN350", "alone, read-only, Nov 20", None, 866, "usb"),
            ("Scratch Disk", "alone", 768, 692, "usb"),
        ], 7456),
        bars([
            ("DATA · 990 PRO", "both at once", 2232, 2011, "tb"),
            ("Media · P310", "both at once", 1788, 2008, "tb"),
            ("DATA + Media", "total, both on the dock", 4021, 4019, "tb"),
            ("DATA + Media", "total, Nov 22 trial with DATA on R4", 5144, 7456, "tb"),
        ], 7456),
        '<p class="note-t">Both charts share one scale. Together the two NVMe drives split the dock\'s 40 Gb/s link, about 4 GB/s each way, within 1% of the November 22 run before the trial. No errors; DATA 41 °C and Media 61 °C afterwards. The last bar is the one-day trial with DATA on its own port and the main display on the dock: faster together, but it halved Media\'s writes and was undone on November 23 after the main screen stayed dark following a restart.</p>'),
    sec("Storage", table(["Volume", "Drive", "Used", "Size", "Temp"], [
        ("Macintosh HD", "Apple 512 GB internal", "283 GB", "494 GB", "35 °C"),
        (L("media", "Media"), "Crucial P310 2 TB, Mokin enclosure", "934 GB", "2.0 TB", "51 °C"),
        (L("data", "DATA"), "Samsung 990 PRO 1 TB, Mokin enclosure", "103 GB", "1.0 TB", "39 °C"),
        (L("ssd-backup", "SSD BACKUP"), "WD Green SN350 2 TB, UGREEN enclosure", "1.32 TB", "2.0 TB", "—"),
        (L("scratch-disk", "Scratch Disk"), "512 GB SSD, Ugreen enclosure", "69 GB", "512 GB", "—"),
        (L("backup-hdd", "Backup"), "WD Elements 4 TB hard drive", "2.7 TB", "4.0 TB", "—"),
    ], num=(2, 3, 4)), '<p class="note-t">Used space November 22; idle temperatures November 23 for DATA and Media, November 22 for the internal SSD. USB enclosures do not pass the drive\'s temperature through. DATA and Media passed a file system check on November 22, the others on November 16.</p>'),
    sec("Network", table(["Interface", "Link", "Down", "Up", "Idle ping"], [
        ("en0 · wired", "2.5GbE via the ACASIS switch, carries the traffic", "2.30 Gb/s", "2.31 Gb/s", "11.0 ms"),
        ("en1 · Wi-Fi 7", "6 GHz, 160 MHz, 2161 Mb/s link", "743 Mb/s", "937 Mb/s", "13.3 ms"),
    ], num=(2, 3, 4)), '<p class="note-t">Both measured November 20, 2026. Full details are on the ' + L("home-network", "home network page") + '. The internet line is fine at about 2.3 Gb/s each way. Wi-Fi moved from 5 GHz to 6 GHz and roughly tripled, but it is still about a third of wired speed, so the mini stays on the cable.</p>'),
    '<section><h2>Worth remembering</h2><div class="callouts">'
    '<div class="callout attn"><h3>Eject before unplugging</h3><p>Unsafe shutdowns on record: P310 56, 990 PRO 70, internal 11. All drives report no data errors.</p></div>'
    '<div class="callout attn"><h3>Video is king: a dock does video or fast drives</h3><p>Display traffic is reserved first on the Thunderbolt link. With a monitor on this dock, drive writes fell from about 3 GB/s to 1.5 GB/s. So the dock carries the SSDs and both monitors plug into the mini. A one-day trial on November 22 put the main monitor on the dock; it was undone the next day. The <a href="macbook-pro.html">MacBook</a> makes the opposite choice.</p></div>'
    '<div class="callout"><h3>Two enclosures need the dock</h3><p>The mini runs only one bus-powered NVMe enclosure reliably. The Wavlink\'s own power supply lets both run at 40 Gb/s.</p></div>'
    '<div class="callout"><h3>No spare lane</h3><p>DATA and Media rarely transfer at the same time, so sharing the dock is fine. All three back Thunderbolt ports are taken (two monitors and the dock), so neither drive can get a port of its own.</p></div>'
    '</div></section>',
    sec("Next to the MacBook Pro", table(["", "This Mac mini", "Mac Work Book Pro"], [
        ("Chip", "Apple M6", "Apple M5 Pro"),
        ("CPU", "12 cores: 2 Super, 4 Performance, 6 Efficiency", "18 cores: 6 Super, 12 Performance"),
        ("GPU", "12 cores", "20 cores"),
        ("Memory", "16 GB", "48 GB"),
        ("Internal SSD", "512 GB", "1 TB"),
        ("Thunderbolt", "Thunderbolt 4, 40 Gb/s", "Thunderbolt 5, up to 120 Gb/s"),
    ]), '<p class="note-t">The MacBook Pro is no longer cabled to the mini. It runs from its own dock. See the <a href="macbook-pro.html">MacBook Pro page</a>.</p>'),
    sec("Desk layout PDFs", '<p class="note-t">Printable layouts of both desks, read from macOS (the mini on November 23, 2026 with MacBook rows updated November 27, the MacBook on November 27): a port diagram, every negotiated link, storage, measured speeds and notes.</p>', '<div class="grid"><a class="card" href="downloads/mac-mini-desk-layout-2026-11-27.pdf"><span class="spd">PDF · Nov 27, 2026</span><b>Mac mini desk layout</b><span>Both monitors on the mini\'s own ports over DisplayPort, the Wavlink dock with Media, DATA and the Scratch Disk, the November 23 drive tests, and the MacBook rows updated November 27.</span><span class="go">Open PDF &rarr;</span></a><a class="card" href="downloads/macbook-pro-desk-layout-2026-11-27.pdf"><span class="spd">PDF · Nov 27, 2026</span><b>MacBook Pro desk layout</b><span>The work-from-home MacBook on the Ivanky 13-in-1 USB-C dock, one monitor on its own HDMI, the backups and Wi-Fi.</span><span class="go">Open PDF &rarr;</span></a></div>'),
    '<section><h2>Earlier snapshots</h2><p class="note-t">How the desk looked on October 19, 2026, before the Wavlink dock and the KTC monitor: the <a href="mac-mini-m6-scan.html">full scan</a> and the <a href="mac-mini-map.html">chip and dock map</a>.</p></section>',
])
hero = (f'<div class="eyebrow">Checked {CHECKED} · Mac18,5</div>\n'
        '<h1>Mac mini <em>desk setup</em></h1>\n'
        '<p class="lede">My play toy: an Apple M6 Mac mini, what is plugged into it, the chip inside each device, and the speed every link actually runs at.</p>\n'
        + stats([("40", "Gb/s", "dock uplink"), ("~4.0", "GB/s", "drives behind the dock, combined"), ("6", "drives", "10 TB in all"), ("180 + 180", "Hz", "two displays"), ("0", "errors", "in the Nov 23 drive tests")]))
page("mac-mini.html", "Mac mini setup",
     "An Apple M6 Mac mini with a Thunderbolt 5 dock, six drives and two monitors: what is plugged into what, a page for each device, and measured speeds.",
     "tb", hero, hub, one=False)
