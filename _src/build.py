#!/usr/bin/env python3
"""Builds mac-mini.html and devices/*.html. Run from anywhere: python3 _src/build.py"""
import pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKED = "November 11, 2026"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')


def page(path, title, desc, bus, hero, main, one=True):
    p = "../" if "/" in path else ""
    nav = (f'<nav><a class="brand" href="{p}index.html">Willard Kramer</a><a href="{p}index.html">About</a>'
           f'<a href="{p}mac-mini.html" aria-current="page">Mac mini setup</a><a href="{p}macbook-pro.html">Mac Work Book Pro</a>'
           f'<a href="{p}dev-env.html">Dev environment</a></nav>')
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
DOCK = ("node", "Wavlink dock", "WL-UTD59", "wavlink-dock.html")
UPLINK = ("wire", "40 Gb/s · R4", "tb")

D = []  # device pages, in pager order

# ---------------------------------------------------------------- Wavlink
D.append(dict(
    slug="wavlink-dock", name="Wavlink WL-UTD59", em="Thunderbolt 5 dock", group="Dock", bus="tb", spd="40 Gb/s uplink",
    card="Self-powered Thunderbolt 5 dock. Carries three SSDs, the Time Machine disk, a LAN adapter and the Blu-ray burner on one cable.",
    lede="The one cable that carries almost everything. A self-powered Thunderbolt 5 dock on the mini's port R4, with all three downstream Thunderbolt ports in use.",
    path=[MINI, UPLINK, ("node", "Wavlink WL-UTD59", "USB4 v2 mode · fw 64.64", "me")],
    stats=[("40", "Gb/s", "link to the mini"), ("3 / 3", "", "Thunderbolt ports in use"), ("~4.0", "GB/s", "combined drive ceiling"), ("6", "", "devices behind it")],
    body=[
        sec("What it is", spec([
            ("Model", "Wavlink WL-UTD59 Thunderbolt 5 Dock"),
            ("Reported vendor", 'Winstars Technology Limited <span class="mono">(vendor 0x2629, device 0xD59, rev 3)</span>'),
            ("Firmware", "64.64, port controllers 1.11.0"),
            ("Link to the mini", "40 Gb/s in USB4 v2 mode, on Thunderbolt port R4"),
            ("Power", "Its own power supply. It does not draw from the mini."),
            ("Downstream Thunderbolt", "3 ports, 40 Gb/s each. One of them is the front 30 W USB-C port."),
            ("USB 3 side", 'Intel hub <span class="mono">8087:5787</span> at 10 Gb/s, feeding Parade hubs <span class="mono">1da0:5512</span>'),
            ("USB 2 side", 'Fresco Logic hub <span class="mono">1d5c:5801</span>, feeding Parade hubs <span class="mono">1da0:551d</span>'),
            ("Dock controller", 'Infineon management device <span class="mono">2629:0d59</span>'),
        ]),
            '<p class="note-t">It is a Thunderbolt 5 dock, but the mini\'s ports are Thunderbolt 4, so the link runs at 40 Gb/s. That is the top speed the mini offers.</p>'),
        sec("What is plugged into it", table(["Dock port", "Device", "Link", "Carried by"], [
            ("Thunderbolt 1", '<a href="media.html">Media</a> · Crucial P310 in a Mokin enclosure', "40 Gb/s USB4", "Thunderbolt"),
            ("Thunderbolt 2 (front, 30 W)", '<a href="data.html">DATA</a> · Samsung 990 PRO in an ACASIS enclosure', "40 Gb/s Thunderbolt 3", "Thunderbolt"),
            ("Thunderbolt 3", '<a href="scratch-disk.html">Scratch Disk</a> · Ugreen USB enclosure', "10 Gb/s USB", "USB 3 hub"),
            ("USB 3 hub", '<a href="backup-hdd.html">Backup</a> · WD Elements 4 TB', "5 Gb/s", "USB 3 hub"),
            ("USB 3 hub", '<a href="lan-adapter.html">Realtek 2.5G LAN</a>', "5 Gb/s", "USB 3 hub"),
            ("USB 2 side", '<a href="blu-ray.html">Blu-ray burner</a>', "480 Mb/s", "USB 2 hub"),
        ]),
            '<p class="note-t">The Scratch Disk sits on a Thunderbolt port, but its enclosure is USB. macOS shows that Thunderbolt port as empty and lists the drive under the dock\'s USB hub, which it shares with the other USB devices.</p>'),
        sec("One shared uplink", '<p>Everything behind the dock shares the single 40 Gb/s link to the mini. Run alone, each NVMe drive gets about 3 GB/s. Run together, they split a ceiling of about 4 GB/s.</p>',
            bars([
                ("DATA alone", "990 PRO", 2930, 3170, "tb"),
                ("Media alone", "P310", 2850, 3610, "tb"),
                ("DATA, all at once", "990 PRO", 1780, 1670, "tb"),
                ("Media, all at once", "P310", 1410, 1640, "tb"),
                ("Scratch, all at once", "USB 10 Gb/s", 790, 755, "usb"),
                ("Dock total", "three drives together", 3990, 4070, "tb"),
            ]),
            '<p class="note-t">fio, 8 GB direct I/O, November 11, 2026. No errors, peak drive temperature 53 °C. A two-drive run on November 7 gave the same ceiling: 3770 MB/s write and 3870 read combined, within 0.3% over three passes.</p>'),
        sec("Why the dock is here", '<p>The mini runs one bus-powered NVMe enclosure reliably, not two. On October 19 I tried every arrangement of the two enclosures on the mini\'s own ports:</p>',
            table(["Setup", "Result"], [
                ("Mokin first, ACASIS second", "ACASIS fell back to USB 10 Gb/s and its drive ran at about 950 MB/s. A new cable and a reboot did not help."),
                ("ACASIS first, Mokin second", "ACASIS came up at 40 Gb/s. The Mokin's drive failed to attach, mounted unwritable, then dropped."),
                ("Mokin alone", "Stable at 40 Gb/s."),
            ]),
            '<p>Whichever enclosure connected second lost. Each port supplies about 15 W of bus power, and that is the likely cause, though the logs cannot prove it: no PCIe or NVMe errors, and the overcurrent counters stayed at 0. A dock with its own power supply fixes it. Both enclosures now run behind the Wavlink at 40 Gb/s with no drops.</p>'),
        sec("Keep monitors off it", '<p>DisplayPort video reserves outbound Thunderbolt bandwidth, the same direction drive writes use. With the KTC monitor (1440p at 180 Hz) on the dock, writes to the NVMe drives capped near 1.5 GB/s. With the monitor on the mini\'s own port, they reach about 3 GB/s. Reads were barely affected. Both monitors now plug into the mini directly.</p>'),
    ]))

# ---------------------------------------------------------------- Media
D.append(dict(
    slug="media", name="Media", em="Crucial P310 2 TB", group="Storage", bus="tb", spd="40 Gb/s · Gen4 x4",
    card="Crucial P310 2 TB in a fanless Mokin USB4 enclosure. The Plex and Apple TV streaming source.",
    lede="The streaming library. A Crucial P310 2 TB NVMe drive in a fanless Mokin USB4 enclosure, behind the Wavlink dock.",
    path=[MINI, UPLINK, DOCK, ("wire", "40 Gb/s USB4", "tb"), ("node", "Mokin enclosure", "ASMedia 246x", None), ("wire", "PCIe Gen4 x4", "tb"), ("node", "Crucial P310 2 TB", "volume Media", "me")],
    stats=[("3,610", "MB/s", "read, alone"), ("2,850", "MB/s", "write, alone"), ("912", "GB", "used of 2 TB"), ("48", "°C", "idle")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", 'Crucial P310 2 TB <span class="mono">(CT2000P310SSD8)</span>, QLC flash, firmware VACR011'),
            ("Drive link", "PCIe Gen4, 4 lanes, 16 GT/s"),
            ("Enclosure", "Mokin USB4 enclosure, fanless"),
            ("Enclosure chip", 'ASMedia 246x <span class="mono">(device 0x2463)</span>, firmware 4b.29'),
            ("Enclosure link", "40 Gb/s USB4, on a Wavlink Thunderbolt port"),
            ("Volume", "Media (APFS), formerly EXTERNAL-2TB. 912 GB used, 1.09 TB free."),
            ("Job", "Source for Plex and Apple TV streaming. A 4K remux needs about 12 MB/s."),
        ])),
        sec("Measured speed", bars([
            ("Direct on the mini", "Nov 6, 4 GB", 3210, 3845, "tb"),
            ("Behind the dock", "Nov 11, 8 GB, alone", 2850, 3610, "tb"),
            ("Behind the dock", "Nov 11, all drives at once", 1410, 1640, "tb"),
            ("Sustained write", "after the cache fills", 900, 0, "tb"),
        ]),
            '<p class="note-t">fio with direct I/O. Random 4k at queue depth 32 (70% read): 56k read and 24k write operations per second.</p>',
            '<p>Short writes land in a fast cache at about 3 GB/s. Once the cache fills, writes settle near 0.9 GB/s, which is the limit of QLC flash. Reads are not affected.</p>'),
        sec("Heat", '<p>The enclosure has no fan. The drive sits at 43 to 55 °C in normal use. It reached 70 °C after about 400 GB of nonstop writes, and 77 °C in a stress test that pushed about 560 GB of I/O in 8 minutes. It never throttled. The critical limit is 85 °C. A heatsink or some airflow would help on very long runs.</p>'),
        sec("Health", spec([
            ("Wear", "0% used, 100% spare"),
            ("Written / read", "6.52 TB / 10.3 TB"),
            ("Power-on time", "863 hours, 98 power cycles"),
            ("Unsafe shutdowns", "47"),
            ("Media errors", "0"),
        ]),
            '<p class="note-t">From smartctl, November 11, 2026. Most of the unsafe shutdowns come from unplugging without ejecting during the October troubleshooting. Eject first.</p>'),
    ]))

# ---------------------------------------------------------------- DATA
D.append(dict(
    slug="data", name="DATA", em="Samsung 990 PRO 1 TB", group="Storage", bus="tb", spd="40 Gb/s · Gen3 x4",
    card="Samsung 990 PRO 1 TB in a fan-cooled ACASIS Thunderbolt 3 enclosure. The fastest drive here for small random work.",
    lede="The working drive. A Samsung 990 PRO 1 TB in a fan-cooled ACASIS Thunderbolt 3 enclosure, on the dock's front port.",
    path=[MINI, UPLINK, DOCK, ("wire", "40 Gb/s TB3", "tb"), ("node", "ACASIS TBU405Pro", "Intel Titan Ridge", None), ("wire", "PCIe Gen3 x4", "tb"), ("node", "990 PRO 1 TB", "volume DATA", "me")],
    stats=[("3,170", "MB/s", "read, alone"), ("2,930", "MB/s", "write, alone"), ("111k", "IOPS", "random 4k read"), ("41", "°C", "idle")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", "Samsung SSD 990 PRO 1 TB, firmware 3B2QJXD7"),
            ("Drive link", "PCIe Gen3, 4 lanes, 8 GT/s. The enclosure sets this limit; the drive itself is Gen4."),
            ("Enclosure", "ACASIS TBU405Pro, fan-cooled"),
            ("Enclosure chip", "Intel Titan Ridge (Thunderbolt 3), firmware 69.1, link controller 1.45.0"),
            ("Enclosure link", "40 Gb/s Thunderbolt 3, on the Wavlink's front 30 W port"),
            ("Volume", "DATA (APFS, not encrypted), formerly SAMSUNG SSD. 146 GB used, 854 GB free."),
            ("History", "Came over from the MacBook Pro."),
        ])),
        sec("Measured speed", bars([
            ("Behind the dock", "Nov 11, 8 GB, alone", 2930, 3170, "tb"),
            ("Behind the dock", "Nov 11, all drives at once", 1780, 1670, "tb"),
        ], 3845),
            '<p class="note-t">fio with direct I/O. Random 4k at queue depth 32 (70% read): 111k read and 48k write operations per second. That is more than twice the internal SSD (46k and 20k) in the same test.</p>'),
        sec("Thunderbolt 3 against USB4", table(["Standard", "Speed", "In this setup"], [
            ("Thunderbolt 3 (2015)", "40 Gb/s", "This ACASIS enclosure"),
            ("USB4 (2019)", "20 or 40 Gb/s", 'The Mokin enclosure holding <a href="media.html">Media</a>'),
            ("Thunderbolt 4 (2020)", "40 Gb/s", "The mini's three back ports"),
            ("Thunderbolt 5 (2024)", "80 or 120 Gb/s", 'The <a href="wavlink-dock.html">Wavlink dock</a>, held to 40 Gb/s by the mini'),
        ]),
            '<p>Both enclosures hold a 40 Gb/s link. Inside, the Mokin\'s USB4 chip reaches its drive at PCIe Gen4, about 3.6 GB/s here. The ACASIS Thunderbolt 3 chip runs Gen3, about 3.2 GB/s, even though the 990 PRO is the faster drive. Neither would get faster on a Thunderbolt 5 port.</p>'),
        sec("Health", spec([
            ("Wear", "0% used, 100% spare"),
            ("Written / read", "2.36 TB / 1.15 TB"),
            ("Power-on time", "655 hours, 119 power cycles"),
            ("Unsafe shutdowns", "62"),
            ("Media errors", "0"),
        ]),
            '<p class="note-t">From smartctl, November 11, 2026. The count went from 58 to 61 when the drive was moved on November 10. Eject before unplugging.</p>'),
    ]))

# ---------------------------------------------------------------- Scratch
D.append(dict(
    slug="scratch-disk", name="Scratch Disk", em="512 GB SSD", group="Storage", bus="usb", spd="10 Gb/s USB",
    card="512 GB SSD in a Ugreen USB enclosure. Temp files and working space, kept off the internal drive.",
    lede="Working space. A 512 GB SSD in a Ugreen USB enclosure, plugged into a Thunderbolt port on the dock but running as plain USB.",
    path=[MINI, UPLINK, DOCK, ("wire", "USB hub · 10 Gb/s", "usb"), ("node", "Ugreen enclosure", "Realtek RTL9210", None), ("wire", "NVMe", "usb"), ("node", "512 GB SSD", "volume Scratch Disk", "me")],
    stats=[("780", "MB/s", "write"), ("740", "MB/s", "read"), ("58", "GB", "used of 512 GB"), ("10", "Gb/s", "USB link")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", "512 GB NVMe SSD"),
            ("Enclosure", 'Ugreen USB enclosure, Realtek RTL9210 bridge <span class="mono">(0bda:9210)</span>'),
            ("Link", "USB 10 Gb/s, drawing up to 4.5 W from the dock"),
            ("Where", "A Thunderbolt port on the Wavlink. Because the enclosure is USB, macOS lists it under the dock's USB hub and shows the Thunderbolt port as empty."),
            ("Volume", "Scratch Disk (APFS). 58 GB used, 454 GB free."),
            ("Job", "Temporary files, test output and working copies, so the internal SSD stays clear."),
        ])),
        sec("Measured speed", bars([
            ("Alone", "Nov 11, 8 GB", 780, 740, "usb"),
            ("All drives at once", "Nov 11", 790, 755, "usb"),
        ], 1250),
            '<p class="note-t">fio with direct I/O. The bar scale ends at 1,250 MB/s, the ceiling of a 10 Gb/s USB link. Random 4k at queue depth 32: 13k read and 5k write operations per second.</p>',
            '<p>The drive is limited by its USB bridge, not by the dock. It keeps full speed while the two NVMe drives are busy, because 0.8 GB/s is a small share of the dock\'s 4 GB/s.</p>'),
        sec("History", '<p>This SSD used to sit in the M.2 slot of an Ivanky USB dock, where it measured the same ~780 MB/s. When the Wavlink replaced that dock, the drive moved into its own enclosure.</p>'),
    ]))

# ---------------------------------------------------------------- SSD BACKUP
D.append(dict(
    slug="ssd-backup", name="SSD BACKUP", em="WD Green SN350 2 TB", group="Storage", bus="usb", spd="10 Gb/s USB",
    card="WD Green SN350 2 TB in a UGREEN USB enclosure on the mini's front port. Time Machine copy of Media.",
    lede="The fast backup. A WD Green SN350 2 TB in a UGREEN USB enclosure on the mini's own front USB-C port, outside the dock.",
    path=[MINI, ("wire", "front USB-C · 10 Gb/s", "usb"), ("node", "UGREEN enclosure", "Realtek RTL9210", None), ("wire", "NVMe", "usb"), ("node", "WD Green SN350 2 TB", "volume SSD BACKUP", "me")],
    stats=[("870", "MB/s", "read"), ("1.10", "TB", "used of 2 TB"), ("10", "Gb/s", "USB link"), ("0", "", "shared with the dock")],
    body=[
        sec("The drive and its enclosure", spec([
            ("Drive", "WD Green SN350 2 TB, PCIe Gen3, QLC flash, no DRAM cache"),
            ("Enclosure", 'UGREEN USB enclosure, Realtek RTL9210 bridge <span class="mono">(0bda:9210)</span>'),
            ("Link", "USB 10 Gb/s, the most the front port and the enclosure both offer"),
            ("Where", "One of the mini's two front USB-C ports. The other is free."),
            ("Volume", "SSD BACKUP (case-sensitive APFS). 1.10 TB used, 896 GB free."),
            ("Job", 'Time Machine destination. It holds a backup of <a href="media.html">Media</a>.'),
        ])),
        sec("Measured speed", bars([
            ("Alone", "Nov 11, 8 GB read", None, 860, "usb"),
            ("While the dock is busy", "Nov 11", None, 870, "usb"),
        ], 1250),
            '<p class="note-t">Time Machine blocks ordinary writes to its destination, so this drive was tested read-only on an existing file. The bar scale ends at 1,250 MB/s, the ceiling of a 10 Gb/s USB link.</p>',
            '<p>Because it is on the mini\'s own port, it does not share the dock\'s link. It held 870 MB/s while all three dock drives ran flat out.</p>'),
        sec("Things to know", notes([
            "QLC flash with no DRAM: a large first backup slows once the drive's cache fills. Later backups are small and quick.",
            "Keep 15 to 20% free so the drive has room to work.",
            "USB enclosures do not pass the drive's temperature or SMART data through, so there is no health readout for it.",
        ])),
    ]))

# ---------------------------------------------------------------- Backup HDD
D.append(dict(
    slug="backup-hdd", name="Backup", em="WD Elements 4 TB", group="Storage", bus="usb5", spd="5 Gb/s USB",
    card="WD Elements 4 TB hard drive. The main Time Machine disk.",
    lede="The big, slow, safe one. A WD Elements 4 TB hard drive on the dock's USB hub, used only by Time Machine.",
    path=[MINI, UPLINK, DOCK, ("wire", "USB hub · 5 Gb/s", "usb5"), ("node", "WD Elements 4 TB", "volume Backup", "me")],
    stats=[("~95", "MB/s", "read"), ("2.6", "TB", "used of 4 TB"), ("5", "Gb/s", "USB link")],
    body=[
        sec("The drive", spec([
            ("Drive", 'WD Elements 4 TB portable hard drive <span class="mono">(1058:2621)</span>'),
            ("Link", "USB 5 Gb/s, drawing up to 4.5 W from the dock"),
            ("Where", "The Wavlink's USB 3 hub, behind one of its Parade hubs"),
            ("Volume", "Backup (APFS). 2.6 TB used, 1.4 TB free."),
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
    lede="The main display. A 24-inch 1440p Fast IPS panel at 180 Hz, on DisplayPort end to end from the mini's port R1.",
    path=[MINI, ("wire", "R1 · USB-C to DP", "dp"), ("node", "Cable Matters cable", "4 lanes · HBR3", None), ("wire", "DisplayPort", "dp"), ("node", "KTC H24T7", "1440p · 180 Hz · VRR", "me")],
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
            ("Port", "Mac mini Thunderbolt port R1"),
            ("Cable", "Cable Matters USB-C to DisplayPort"),
            ("Signal", "DisplayPort alt mode, 4 lanes at HBR3, no compression (no DSC)"),
            ("Running at", "Looks like 2048×1152 in HiDPI (4096×2304 backing) at 180 Hz"),
            ("Role", "Main display"),
        ])),
        sec("Things to know", notes([
            "Keep it on DisplayPort. Through an HDMI 1.4-class USB-C to HDMI cable it dropped to 75 Hz.",
            'Keep it off the <a href="wavlink-dock.html">Wavlink dock</a>. With this monitor on the dock, writes to the NVMe drives behind it capped near 1.5 GB/s. On the mini\'s own port they reach about 3 GB/s.',
            'Its white does not match the <a href="dell-s2425hs.html">Dell</a> out of the box: this is a wide-gamut 400-nit panel and the Dell is an sRGB 250-nit one. Match brightness first, then use the sRGB mode, then adjust RGB gain.',
        ])),
    ]))

# ---------------------------------------------------------------- Dell
D.append(dict(
    slug="dell-s2425hs", name="Dell S2425HS", em="second display", group="Displays", bus="hdmi", spd="HDMI · 100 Hz",
    card="24-inch 1080p IPS at 100 Hz on the mini's HDMI port.",
    lede="The second display. A 24-inch 1080p IPS panel at its full 100 Hz, on the mini's HDMI port.",
    path=[MINI, ("wire", "HDMI", "hdmi"), ("node", "Dell S2425HS", "1080p · 100 Hz", "me")],
    stats=[("100", "Hz", "refresh, panel max"), ("1920×1080", "", "panel"), ("250", "nits", ""), ("99", "%", "sRGB")],
    body=[
        sec("The panel", spec([
            ("Panel", "24-inch IPS, 1920×1080"),
            ("Refresh", "100 Hz, the panel's maximum"),
            ("Brightness", "250 nits"),
            ("Colour", "8-bit, 99% sRGB"),
            ("Contrast", "1500:1"),
        ])),
        sec("How it is connected", spec([
            ("Port", "Mac mini HDMI"),
            ("Running at", "Looks like 1920×1080 in HiDPI (3840×2160 backing) at 100 Hz"),
            ("Role", "Second display"),
        ])),
        sec("Things to know", notes([
            'It is dimmer and narrower in colour than the <a href="ktc-h24t7.html">KTC</a>, so the two whites differ. Set the KTC down to match this one.',
            "HDMI keeps it off the Thunderbolt ports, which leaves port R2 free for a drive.",
        ])),
    ]))

# ---------------------------------------------------------------- LAN
D.append(dict(
    slug="lan-adapter", name="Realtek 2.5G LAN", em="USB adapter", group="Other", bus="net", spd="5 Gb/s USB · idle",
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
        sec("Why it is idle", '<p>The mini has its own 2.5 Gb Ethernet port (en0), and that carries all the traffic: about 2.15 Gb/s down and 2.12 Gb/s up with a 15 ms idle ping. A second 2.5 Gb port through a shared USB hub would add nothing, so this one stays empty.</p>'),
    ]))

# ---------------------------------------------------------------- Blu-ray
D.append(dict(
    slug="blu-ray", name="Blu-ray burner", em="Matshita UJ260", group="Other", bus="usb2", spd="480 Mb/s USB 2",
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

SLUGS = [d["slug"] for d in D]
for i, d in enumerate(D):
    prev, nxt = D[i - 1], D[(i + 1) % len(D)]
    hero = (f'<div class="eyebrow"><a href="../mac-mini.html">Mac mini setup</a> / {d["group"]} / <b>{d["spd"]}</b></div>\n'
            f'<h1>{d["name"]} <em>{d["em"]}</em></h1>\n<p class="lede">{d["lede"]}</p>\n{path(d["path"])}\n{stats(d["stats"])}')
    pager = (f'<div class="pager"><a href="{prev["slug"]}.html">&larr; {prev["name"]}</a>'
             f'<a href="../mac-mini.html">All devices</a><a href="{nxt["slug"]}.html">{nxt["name"]} &rarr;</a></div>')
    foot = f'<p class="note-t">Read from system_profiler, smartctl and fio on the Mac mini. Checked {CHECKED}.</p>'
    page(f'devices/{d["slug"]}.html', f'{d["name"]} · Mac mini setup', d["card"], d["bus"], hero, "\n".join(d["body"]) + "\n" + foot + "\n" + pager)

# ================================================================= hub
svg = (ROOT / "_src/diagram.svg").read_text().replace("1920×1080 @ 180Hz", "2048×1152 @ 180Hz").replace("HiDPI, 4K backing, VRR", "HiDPI, VRR").replace('<text x="28" y="650" class="tm">192.168.1.2</text>', "")
HITS = [("ktc-h24t7", "dp", 15, 30, 165, 118), ("dell-s2425hs", "hdmi", 190, 30, 165, 118), ("ssd-backup", "usb", 15, 700, 340, 106),
        ("wavlink-dock", "tb", 430, 40, 230, 100), ("media", "tb", 760, 150, 385, 62), ("data", "tb", 760, 226, 385, 62),
        ("scratch-disk", "usb", 760, 302, 385, 62), ("backup-hdd", "usb5", 760, 478, 385, 62), ("lan-adapter", "net", 760, 554, 385, 62),
        ("blu-ray", "usb2", 760, 630, 385, 62)]
names = {d["slug"]: d["name"] for d in D}
hits = "".join(f'<a href="devices/{s}.html" class="b-{b}" aria-label="{names[s]}"><rect class="hit" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></a>' for s, b, x, y, w, h in HITS)
svg = svg.replace("</svg>", hits + "</svg>")
KEYS = [("tb", "Thunderbolt / USB4 40 Gb/s"), ("dp", "DisplayPort"), ("hdmi", "HDMI"), ("usb", "USB 10 Gb/s"), ("usb5", "USB 5 Gb/s"), ("usb2", "USB 2"), ("net", "Ethernet")]
fig = ('<figure class="wiring"><div class="dscroll">' + svg + '</div><figcaption>'
       + "".join(f'<span class="key b-{b}"><i></i>{t}</span>' for b, t in KEYS)
       + '<span>R1, R2 and R4 are the numbers macOS gives the mini\'s Thunderbolt ports. Select a device to open its page.</span></figcaption></figure>')

cards = ""
for g in ["Dock", "Storage", "Displays", "Other"]:
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
        ("Memory and storage", "16 GB, 512 GB internal SSD (251 GB used)"),
        ("Software", "macOS 27.2.1"),
        ("Back ports", "3 Thunderbolt 4 (R1 monitor, R2 free, R4 dock), HDMI, 2.5 Gb Ethernet"),
        ("Front ports", "2 USB-C at 10 Gb/s (one drive, one free), headphone jack"),
        ("Wireless", "Wi-Fi 7, Bluetooth 6. MX Keys S keyboard and MX Anywhere 3S mouse over Bluetooth."),
    ])),
    sec("Every link, against its maximum", '<p class="note-t">The most each port allows, next to what macOS reports as negotiated. Every connection runs at its top speed.</p>',
        table(["Connection", "Chip", "Port maximum", "Negotiated", ""], [
            ("Mac mini → " + L("wavlink-dock", "Wavlink dock") + '<br><span class="sub">Thunderbolt port R4</span>', "Wavlink TB5 controller", "40 Gb/s (TB4 host)", "40 Gb/s, USB4 v2 mode", OK),
            ("Mac mini → " + L("ktc-h24t7", "KTC H24T7") + '<br><span class="sub">Port R1, USB-C to DP cable</span>', "Cable Matters adapter", "DP 4 lanes, HBR3", "4 lanes, top rate, no compression", OK),
            ("Mac mini → " + L("dell-s2425hs", "Dell S2425HS") + '<br><span class="sub">HDMI</span>', "—", "1080p at 100 Hz (panel max)", "1080p at 100 Hz", OK),
            ("Mac mini → " + L("ssd-backup", "SSD BACKUP") + '<br><span class="sub">Front USB-C</span>', "Realtek RTL9210", "10 Gb/s", "10 Gb/s", OK),
            ("Wavlink → Mokin enclosure", "ASMedia 246x", "40 Gb/s", "40 Gb/s USB4", OK),
            ("↳ " + L("media", "Media") + " · Crucial P310", "Crucial P310 (QLC)", "PCIe Gen4 x4", "Gen4 x4, 16 GT/s", OK),
            ("Wavlink → ACASIS enclosure", "Intel Titan Ridge (TB3)", "40 Gb/s", "40 Gb/s Thunderbolt 3", OK),
            ("↳ " + L("data", "DATA") + " · Samsung 990 PRO", "Samsung 990 PRO", "PCIe Gen3 x4 (enclosure limit)", "Gen3 x4, 8 GT/s", OK),
            ("Wavlink → " + L("scratch-disk", "Scratch Disk"), "Realtek RTL9210", "10 Gb/s (USB enclosure)", "10 Gb/s", OK),
            ("Wavlink → " + L("backup-hdd", "Backup") + " · WD Elements", "WD USB bridge", "5 Gb/s", "5 Gb/s", OK),
            ("Wavlink → " + L("lan-adapter", "2.5G LAN adapter"), "Realtek RTL8156", "5 Gb/s", "5 Gb/s", OK),
            ("Wavlink → " + L("blu-ray", "Blu-ray burner"), "Initio bridge", "USB 2", "480 Mb/s", OK),
            ('Mac mini → home network<br><span class="sub">en0</span>', "Built-in 2.5GbE", "2.5 Gb/s", "2500Base-T full duplex", OK),
        ])),
    sec("Drive speeds", '<p class="note-t">fio, 8 GB direct I/O, November 11, 2026. First each drive alone, then all of them at once.</p>',
        bars([
            ("Internal SSD", "alone", 6150, 6640, "usb2"),
            ("DATA · 990 PRO", "alone", 2930, 3170, "tb"),
            ("Media · P310", "alone", 2850, 3610, "tb"),
            ("SSD BACKUP · SN350", "alone, read-only", None, 860, "usb"),
            ("Scratch Disk", "alone", 780, 740, "usb"),
        ]),
        bars([
            ("DATA · 990 PRO", "all at once", 1780, 1670, "tb"),
            ("Media · P310", "all at once", 1410, 1640, "tb"),
            ("Scratch Disk", "all at once", 790, 755, "usb"),
            ("SSD BACKUP · SN350", "all at once, read-only", None, 870, "usb"),
            ("Dock drives combined", "DATA + Media + Scratch", 3990, 4070, "tb"),
        ], 6640),
        '<p class="note-t">Both charts share one scale. The three drives behind the dock hit its 40 Gb/s ceiling together, at about 4 GB/s. SSD BACKUP kept full speed because it is on the mini\'s own port. No errors, peak 53 °C.</p>'),
    sec("Storage", table(["Volume", "Drive", "Used", "Size", "Temp"], [
        ("Macintosh HD", "Apple 512 GB internal", "251 GB", "494 GB", "37 °C"),
        (L("media", "Media"), "Crucial P310 2 TB, Mokin enclosure", "912 GB", "2.0 TB", "48 °C"),
        (L("data", "DATA"), "Samsung 990 PRO 1 TB, ACASIS enclosure", "146 GB", "1.0 TB", "41 °C"),
        (L("ssd-backup", "SSD BACKUP"), "WD Green SN350 2 TB, UGREEN enclosure", "1.10 TB", "2.0 TB", "—"),
        (L("scratch-disk", "Scratch Disk"), "512 GB SSD, Ugreen enclosure", "58 GB", "512 GB", "—"),
        (L("backup-hdd", "Backup"), "WD Elements 4 TB hard drive", "2.6 TB", "4.0 TB", "—"),
    ], num=(2, 3, 4)), '<p class="note-t">Idle temperatures. USB enclosures do not pass the drive\'s temperature through.</p>'),
    sec("Network", table(["Interface", "Link", "Down", "Up", "Idle ping"], [
        ("en0 · wired", "2.5GbE, carries the traffic", "2.15 Gb/s", "2.12 Gb/s", "15 ms"),
        ("en1 · Wi-Fi 7", "5 GHz, 80 MHz, 864 Mb/s link", "226 Mb/s", "238 Mb/s", "17 ms"),
    ], num=(2, 3, 4)), '<p class="note-t">Measured November 7, 2026. The internet line is fine at about 2.1 Gb/s each way. Wi-Fi is the bottleneck at roughly a tenth of wired speed, so the mini stays on the cable.</p>'),
    '<section><h2>Worth remembering</h2><div class="callouts">'
    '<div class="callout attn"><h3>Eject before unplugging</h3><p>Unsafe shutdowns on record: P310 47, 990 PRO 62, internal 10. All drives report no data errors.</p></div>'
    '<div class="callout"><h3>Monitors stay off the dock</h3><p>A display on the dock takes outbound Thunderbolt bandwidth, the direction drive writes use. Writes fell from about 3 GB/s to 1.5 GB/s.</p></div>'
    '<div class="callout"><h3>Two enclosures need the dock</h3><p>The mini runs only one bus-powered NVMe enclosure reliably. The Wavlink\'s own power supply lets both run at 40 Gb/s.</p></div>'
    '<div class="callout"><h3>R2 is the spare lane</h3><p>DATA and Media rarely transfer at the same time. If both ever need full speed at once, move one to the free R2 port.</p></div>'
    '</div></section>',
    sec("Next to the MacBook Pro", table(["", "This Mac mini", "Mac Work Book Pro"], [
        ("Chip", "Apple M6", "Apple M5 Pro"),
        ("CPU", "12 cores: 2 Super, 4 Performance, 6 Efficiency", "18 cores: 6 Super, 12 Performance"),
        ("GPU", "12 cores", "20 cores"),
        ("Memory", "16 GB", "48 GB"),
        ("Internal SSD", "512 GB", "1 TB"),
        ("Thunderbolt", "Thunderbolt 4, 40 Gb/s", "Thunderbolt 5, up to 80 Gb/s"),
    ]), '<p class="note-t">The MacBook Pro is no longer cabled to the mini. It runs from its own dock. See the <a href="macbook-pro.html">MacBook Pro page</a>.</p>'),
    '<section><h2>Earlier snapshots</h2><p class="note-t">How the desk looked on October 19, 2026, before the Wavlink dock and the KTC monitor: the <a href="mac-mini-m6-scan.html">full scan</a> and the <a href="mac-mini-map.html">chip and dock map</a>.</p></section>',
])
hero = (f'<div class="eyebrow">Checked {CHECKED} · Mac18,5</div>\n'
        '<h1>Mac mini <em>desk setup</em></h1>\n'
        '<p class="lede">My play toy: an Apple M6 Mac mini, what is plugged into it, the chip inside each device, and the speed every link actually runs at.</p>\n'
        + stats([("40", "Gb/s", "dock uplink"), ("~4.0", "GB/s", "drives behind the dock, combined"), ("6", "drives", "10 TB in all"), ("180 + 100", "Hz", "two displays"), ("0", "errors", "in the Nov 11 load tests")]))
page("mac-mini.html", "Mac mini setup",
     "An Apple M6 Mac mini with a Thunderbolt 5 dock, six drives and two monitors: what is plugged into what, a page for each device, and measured speeds.",
     "tb", hero, hub, one=False)
