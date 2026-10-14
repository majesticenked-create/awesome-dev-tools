"""Render two silent Etsy listing videos (14-14.6 s, 1920x1440, 30 fps).

  videos/01-flip-through.mp4   title card -> 7 key pages slide past -> end card
  videos/02-type-tick-label.mp4  fillable demo on a tablet: typing, ticking, labeling

Usage:  python3 make_videos.py      (run build_planner.py first)
"""
import os
import subprocess
from PIL import Image, ImageDraw, ImageFilter
from pypdf import PdfReader

import make_mockups as mm

VW, VH, FPS = 1920, 1440, 30
OUT = os.path.join(mm.HERE, "videos")
ROOMS = [("K", "#E9B49E"), ("L", "#A9C5B2"), ("D", "#EBD394"), ("B1", "#A9C0D8"),
         ("B2", "#CBB8D8"), ("BA", "#9ED2CD"), ("O", "#D9C4A7"), ("G", "#C2C3BA")]


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def background():
    saved = (mm.W, mm.H)
    mm.W, mm.H = VW, VH
    try:
        return mm.soft_background((250, 246, 240), (245, 236, 226), [
            (1600, 200, 520, (214, 230, 220, 255)),
            (1350, 1400, 500, (247, 221, 207, 255)),
            (200, 1350, 380, (246, 234, 206, 200)),
        ])
    finally:
        mm.W, mm.H = saved


def sprite(page, w, shadow=True):
    """Page resized to width w with a soft shadow baked in (RGBA, padded by 60px)."""
    p = page.resize((w, int(page.height * w / page.width)), Image.LANCZOS)
    pad = 60
    s = Image.new("RGBA", (p.width + 2 * pad, p.height + 2 * pad), (0, 0, 0, 0))
    if shadow:
        m = Image.new("L", s.size, 0)
        ImageDraw.Draw(m).rectangle([pad, pad + 14, pad + p.width, pad + p.height + 14], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v * 0.30))
        s.paste((40, 40, 30), (0, 0), m)
    s.paste(p, (pad, pad))
    return s


def with_alpha(img, a):
    if a >= 1:
        return img
    r = img.copy()
    r.putalpha(r.getchannel("A").point(lambda v: int(v * a)))
    return r


def text_layer(draw_fn):
    layer = Image.new("RGBA", (VW, VH), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    return layer


def encoder(path):
    os.makedirs(OUT, exist_ok=True)
    return subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{VW}x{VH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path],
        stdin=subprocess.PIPE)


def swatches(d, cx, y, n_visible, size=96, gap=14):
    total = 8 * size + 7 * gap
    x0 = cx - total / 2
    for i, (code, col) in enumerate(ROOMS[:n_visible]):
        sx = x0 + i * (size + gap)
        d.rounded_rectangle([sx, y, sx + size, y + size], radius=20, fill=col)
        f = mm.SERIF_B(46 if len(code) == 1 else 38)
        tw = d.textlength(code, font=f)
        bb = d.textbbox((0, 0), code, font=f)
        d.text((sx + (size - tw) / 2, y + (size - (bb[3] - bb[1])) / 2 - bb[1]), code, font=f, fill=mm.INK)


# =================================================================== video 1
def video_flip(pk):
    bg = background()
    pages = [("8 weeks before", "Week-by-week checklists"), ("Moving day", "Moving day schedule"),
             ("Moving budget", "Budget & quote trackers"), ("Room key (codes & colors)", "Color-coded room key"),
             ("Box labels: Kitchen", "72 color box labels"), ("Room door signs 1", "Room door signs"),
             ("Move-out cleaning", "Cleaning checklists")]
    pw = 860
    sprites = [sprite(mm.page_img(pk[t], dpi=200), pw) for t, _ in pages]
    total, t_title, t_end = 14.0, 2.0, 12.0
    seg = (t_end - t_title) / len(pages)
    trans = 0.42

    def title(d, a, dy):
        col = lambda c: c + (int(255 * a),)
        mm.caps(d, VW / 2, 470 + dy, "The Calm Move", mm.SANS_SB(40), col(mm.SAGE), 9, center=True)
        mm.text_c(d, VW / 2, 540 + dy, "Moving Planner", mm.SERIF(190), col(mm.INK))
        mm.text_c(d, VW / 2, 800 + dy, "51 pages  ·  fillable + printable  ·  US Letter + A4",
                  mm.SANS_M(48), col(mm.MUTED))

    enc = encoder(os.path.join(OUT, "01-flip-through.mp4"))
    for f in range(int(total * FPS)):
        t = f / FPS
        frame = bg.copy()
        if t < t_title + 0.3:  # title card
            a = ease(t / 0.6) * (1 - ease((t - (t_title - 0.3)) / 0.5))
            dy = int(30 * (1 - ease(t / 0.6)))
            lay = text_layer(lambda d: title(d, a, dy))
            frame.paste(lay, (0, 0), lay)
        if t_title - 0.2 <= t < t_end + 0.3:  # carousel
            u = t - (t_title - 0.2)
            i = min(int(u // seg), len(pages) - 1)
            local = u - i * seg
            p = ease(local / trans)
            cx_cur = VW / 2 + (1 - p) * (VW / 2 + pw)
            cx_prev = VW / 2 - p * (VW / 2 + pw)
            fade_out = 1 - ease((t - t_end) / 0.25) if t > t_end else 1
            items = [(i, cx_cur)]
            if i > 0 and p < 1:
                items.append((i - 1, cx_prev))
            for j, cx in items:
                sp = with_alpha(sprites[j], fade_out)
                frame.paste(sp, (int(cx - sp.width / 2), 40), sp)
                cap = pages[j][1]

                def draw_cap(d, cap=cap, cx=cx):
                    f_ = mm.SANS_SB(46)
                    w = d.textlength(cap, font=f_) + 90
                    d.rounded_rectangle([cx - w / 2, 1282, cx + w / 2, 1376], radius=47,
                                        fill=(255, 255, 255, int(255 * fade_out)))
                    d.text((cx - w / 2 + 45, 1304), cap, font=f_, fill=mm.INK + (int(255 * fade_out),))
                lay = text_layer(draw_cap)
                frame.paste(lay, (0, 0), lay)
        if t >= t_end + 0.25:  # end card
            e = t - t_end - 0.25
            a = ease(e / 0.5)

            def end(d):
                col = lambda c: c + (int(255 * a),)
                mm.text_c(d, VW / 2, 330, "51 pages.", mm.SERIF(170), col(mm.INK))
                mm.text_c(d, VW / 2, 530, "One calm move.", mm.SERIF_I(150), col(mm.CLAY))
                swatches(d, VW / 2, 800, min(8, int(max(0, e - 0.3) / 0.07) + (1 if e > 0.3 else 0)))
                mm.text_c(d, VW / 2, 990, "Instant download  ·  US Letter + A4", mm.SANS_M(48), col(mm.MUTED))
                mm.caps(d, VW / 2, 1240, "CropUp Creative", mm.SANS_SB(38), col(mm.MUTED), 10, center=True)
            lay = text_layer(end)
            frame.paste(lay, (0, 0), lay)
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    print(os.path.join(OUT, "01-flip-through.mp4"))


# =================================================================== video 2
TABLET_X, TABLET_Y = 800, 150
SCR_W, SCR_H = 1040, VH - 150  # screen bleeds off the bottom of the frame


def page_fields(n):
    """Text and checkbox rects (in PDF points, top-left origin) for page n, in creation order."""
    r = PdfReader(mm.PDF)
    pg = r.pages[n - 1]
    h = float(pg.mediabox[3])
    tx, cb = [], []
    for a in pg.get("/Annots") or []:
        a = a.get_object()
        x1, y1, x2, y2 = [float(v) for v in a["/Rect"]]
        rect = (x1, h - y2, x2, h - y1)
        if a.get("/FT") == "/Tx":
            tx.append(rect)
        elif a.get("/FT") == "/Btn":
            cb.append(rect)
    return tx, cb, float(pg.mediabox[2])


class TabletPage:
    """A high-res page that can be drawn on, then framed by a zooming camera."""

    def __init__(self, n, target):
        self.img = mm.page_img(n, dpi=300)
        self.tx, self.cb, wpt = page_fields(n)
        self.s = self.img.width / wpt
        self.target = target  # (zoom, cx, cy) as fractions of page width / height

    def draw(self, typed, ticks, caret=None):
        im = self.img.copy()
        d = ImageDraw.Draw(im)
        f = mm.SANS(int(9.5 * self.s))
        for idx, txt in typed:
            x1, y1, x2, y2 = [v * self.s for v in self.tx[idx]]
            d.text((x1 + 3 * self.s, y2 - 2.5 * self.s), txt, font=f, fill=mm.INK, anchor="ls")
            if caret == idx:
                cx = x1 + 4 * self.s + d.textlength(txt, font=f)
                d.line([cx, y1 + self.s, cx, y2 - self.s], fill=mm.CLAY, width=int(self.s * 0.9))
        for idx, k in ticks:
            x1, y1, x2, y2 = [v * self.s for v in self.cb[idx]]
            w = (x2 - x1) * (0.7 + 0.5 * k)
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            pts = [(cx - w * 0.38, cy), (cx - w * 0.08, cy + w * 0.32), (cx + w * 0.48, cy - w * 0.42)]
            d.line(pts, fill=mm.SAGE, width=int(self.s * 1.5), joint="curve")
        return im

    def frame(self, im, k):
        """Camera at progress k (0 = whole page width, 1 = target zoom)."""
        z0, cx0, cy0 = 1.0, 0.5, 0.48
        z1, cx1, cy1 = self.target
        z, cx, cy = z0 + (z1 - z0) * k, cx0 + (cx1 - cx0) * k, cy0 + (cy1 - cy0) * k
        W_, H_ = im.size
        cw = W_ / z
        ch = cw * SCR_H / SCR_W
        left = min(max(cx * W_ - cw / 2, 0), W_ - cw)
        top = min(max(cy * H_ - ch / 2, 0), max(H_ - ch, 0))
        return im.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((SCR_W, SCR_H), Image.LANCZOS)


def video_demo(pk):
    bg = background()
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([TABLET_X - 46, TABLET_Y - 46, TABLET_X + SCR_W + 46, VH + 200], radius=70, fill=(38, 42, 44))
    d.rounded_rectangle([TABLET_X - 3, TABLET_Y - 3, TABLET_X + SCR_W + 3, VH + 200], radius=6, fill=(20, 20, 20))

    glance = TabletPage(pk["Move at a glance"], (1.75, 0.29, 0.30))
    weeks = TabletPage(pk["8 weeks before"], (1.6, 0.33, 0.29))
    labels = TabletPage(pk["Box labels: Kitchen"], (2.0, 0.28, 0.24))

    glance_seq = [(0, "12 Oak Street"), (1, "Apartment 4B"), (2, "Portland, OR 97201"), (3, "June 28, 10 am"),
                  (8, "Sat, June 29"), (10, "8:00 am"), (16, "Blue Bird Movers")]
    label_seq = [(0, "07"), (1, "24"), (2, "Pots & pans"), (3, "Baking trays, mixing bowls"), (4, "Spice rack")]

    def typing(seq, u, cps):
        n = int(u * cps)
        out, caret = [], None
        for idx, txt in seq:
            if n <= 0:
                break
            out.append((idx, txt[:n]))
            caret = idx if n < len(txt) else caret
            n -= len(txt)
        if caret is None and out:
            caret = out[-1][0]
        return out, caret

    scenes = [  # (start, end, caption, subcopy)
        (0.0, 4.8, "Type it.", "Click any line and type.\nWorks in Acrobat Reader,\nPreview and GoodNotes."),
        (4.8, 8.0, "Tick it.", "Check off every task,\nweek by week."),
        (8.0, 11.6, "Label it.", "Number every box and\nlog what's inside."),
    ]
    T_END, total = 11.6, 14.6
    end_bg = background()

    def zoom_in(u):
        return ease((u - 0.15) / 0.8)

    def screen_at(t):
        blink = int(t * 2.5) % 2 == 0
        if t < 4.8:
            typed, caret = typing(glance_seq, max(0, t - 1.1), 30)
            return glance.frame(glance.draw(typed, [], caret if blink else None), zoom_in(t))
        if t < 8.0:
            u = t - 4.8
            ticks = [(i, ease((u - 0.9 - i * 0.24) / 0.15)) for i in range(10) if u - 0.9 - i * 0.24 > 0]
            return weeks.frame(weeks.draw([], ticks), zoom_in(u))
        u = t - 8.0
        typed, caret = typing(label_seq, max(0, u - 0.9), 26)
        ticks = [(0, ease((u - 3.0) / 0.15))] if u > 3.0 else []
        return labels.frame(labels.draw(typed, ticks, caret if blink else None), zoom_in(u))

    def caption(d, i, a):
        _, _, cap, sub = scenes[i]
        col = lambda c: c + (int(255 * a),)
        mm.caps(d, 110, 380, f"Step {i + 1} of 3", mm.SANS_SB(36), col(mm.SAGE), 8)
        d.text((100, 430), cap, font=mm.SERIF(150), fill=col(mm.INK))
        for j, line in enumerate(sub.split("\n")):
            d.text((110, 640 + j * 66), line, font=mm.SANS(46), fill=col(mm.MUTED))

    def end_text(dd, e):
        mm.text_c(dd, VW / 2, 280, "Type it. Tick it.", mm.SERIF(150), mm.INK)
        mm.text_c(dd, VW / 2, 460, "Or print it.", mm.SERIF_I(150), mm.CLAY)
        pills = ["51 pages", "Fillable PDF", "US Letter + A4"]
        fnt = mm.SANS_SB(46)
        widths = [dd.textlength(p_, font=fnt) + 90 for p_ in pills]
        x = VW / 2 - (sum(widths) + 30 * (len(pills) - 1)) / 2
        for p_, w in zip(pills, widths):
            dd.rounded_rectangle([x, 760, x + w, 856], radius=48, fill=mm.WHITE)
            dd.text((x + 45, 781), p_, font=fnt, fill=mm.INK)
            x += w + 30
        swatches(dd, VW / 2, 950, min(8, int(max(0, e - 0.4) / 0.07) + (1 if e > 0.4 else 0)))
        mm.caps(dd, VW / 2, 1240, "CropUp Creative", mm.SANS_SB(38), mm.MUTED, 10, center=True)

    enc = encoder(os.path.join(OUT, "02-type-tick-label.mp4"))
    last = None
    for f in range(int(total * FPS)):
        t = f / FPS
        if t < T_END:
            frame = bg.copy()
            scr = screen_at(t)
            for s0 in (4.8, 8.0):  # crossfade the screen at scene changes
                if s0 <= t < s0 + 0.3:
                    scr = Image.blend(screen_at(s0 - 0.001), scr, ease((t - s0) / 0.3))
            frame.paste(scr, (TABLET_X, TABLET_Y))
            i = 0 if t < 4.8 else 1 if t < 8.0 else 2
            s0, s1 = scenes[i][0], scenes[i][1]
            a = ease((t - s0) / 0.35) * (1 - ease((t - (s1 - 0.25)) / 0.25))
            lay = text_layer(lambda dd: caption(dd, i, a))
            frame.paste(lay, (0, 0), lay)
            last = frame
        else:
            e = t - T_END
            end = end_bg.copy()
            lay = text_layer(lambda dd: end_text(dd, e))
            end.paste(lay, (0, 0), lay)
            frame = Image.blend(last, end, ease(e / 0.5))
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    enc.wait()
    print(os.path.join(OUT, "02-type-tick-label.mp4"))


if __name__ == "__main__":
    pk = mm.page_key()
    video_flip(pk)
    video_demo(pk)
