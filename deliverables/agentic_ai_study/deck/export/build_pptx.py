"""Build the PowerPoint version of the deck: one full-screen video per slide.

Each slide plays its video on arrival and rests on its last frame; slides that keep
moving then hand over to a looping video under it. A transparent shape on top takes
the clicks, so a click advances the slide instead of pausing the video, and the play
bar is switched off for the whole file. Speaker notes come from the deck's NOTES.
The slide title sits above the slide, outside the area shown, so the outline and
"go to slide" list name each slide.

Usage: python3 build_pptx.py <deck.html> <render outdir> <out.pptx>
"""
import io
import json
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

DECK, OUT, PPTX = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
W, H = Emu(12192000), Emu(6858000)          # 16:9, 13.333 × 7.5 in
HANDOFF_MS = 300                             # the first video rests on its last frame this long before the loop takes over
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"


def play(ctn, spid, ms, node, delay=0):
    return (f'<p:par><p:cTn id="{ctn}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="{node}">'
            f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>'
            f'<p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="{ctn + 1}" dur="{ms}" fill="hold"/>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par>')


def hide(ctn, spid, delay):
    return (f'<p:par><p:cTn id="{ctn}" presetID="1" presetClass="exit" presetSubtype="0" fill="hold" nodeType="afterEffect">'
            f'<p:stCondLst><p:cond delay="{delay}"/></p:stCondLst><p:childTnLst>'
            f'<p:set><p:cBhvr><p:cTn id="{ctn + 1}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>'
            f'</p:cBhvr><p:to><p:strVal val="hidden"/></p:to></p:set></p:childTnLst></p:cTn></p:par>')


def media(ctn, spid, loop):
    rep = ' repeatCount="indefinite"' if loop else ''
    return (f'<p:video><p:cMediaNode vol="80000"><p:cTn id="{ctn}"{rep} fill="hold" display="0">'
            f'<p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:video>')


def timing(v1, v1_ms, v2=None, v2_ms=None):
    """Play v1 as the slide opens ("after previous", no click); then hide it and loop v2."""
    steps = f'<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>{play(5, v1, v1_ms, "afterEffect")}</p:childTnLst></p:cTn></p:par>'
    nxt = 7
    if v2:
        steps += (f'<p:par><p:cTn id="7" fill="hold"><p:stCondLst><p:cond delay="{v1_ms}"/></p:stCondLst><p:childTnLst>'
                  f'{hide(8, v1, HANDOFF_MS)}{play(10, v2, v2_ms, "withEffect", HANDOFF_MS)}</p:childTnLst></p:cTn></p:par>')
        nxt = 12
    medias = media(nxt, v1, False) + (media(nxt + 1, v2, True) if v2 else '')
    return (f'<p:timing xmlns:p="{P}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
            f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
            f'<p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>'
            f'</p:stCondLst><p:childTnLst>{steps}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
            f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
            f'<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
            f'{medias}</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')


def poster(path):
    """The poster frame as a compact PNG (it shows until playback starts, and in the editor)."""
    buf = io.BytesIO()
    Image.open(path).convert("RGB").save(buf, "PNG", optimize=True)
    buf.seek(0)
    return buf


def add_video(slide, mp4, png, name):
    pic = slide.shapes.add_movie(str(mp4), 0, 0, W, H, poster_frame_image=poster(png), mime_type="video/mp4")
    pic.name = name
    pic._element.nvPicPr.cNvPr.set("descr", name)
    return pic


def main():
    html = DECK.read_text(encoding="utf-8")
    notes = json.loads(re.search(r"const NOTES = (\{.*?\});\n", html).group(1))
    plan = json.loads((OUT / "plan.json").read_text())
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    layout = prs.slide_layouts[5]                                   # "Title Only"
    for r in plan:
        sid, stem = r["id"], f"{r['i'] + 1:02d}_{r['id']}"
        title = notes.get(sid, {}).get("t", sid)
        s = prs.slides.add_slide(layout)
        t = s.shapes.title
        t.left, t.top, t.width, t.height = 0, -Emu(914400), W, Emu(731520)   # just above the slide
        t.text = f"{sid} · {title}"
        t.text_frame.paragraphs[0].runs[0].font.size = Pt(20)
        fps = r["fps"]
        v2 = None
        if r["loop"]:                                               # the loop goes under the first video
            v2 = add_video(s, OUT / "video" / f"{stem}_loop.mp4", OUT / "poster" / f"{sid}_end.png", f"{sid} loop")
        v1 = add_video(s, OUT / "video" / f"{stem}.mp4", OUT / "poster" / f"{sid}_a.png", f"{sid} · {title}")
        cover = s.shapes.add_shape(1, 0, 0, W, H)                   # rectangle that takes the clicks
        cover.name = "click to advance"
        cover.fill.solid()
        cover.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        etree.SubElement(cover._element.spPr.find(qn("a:solidFill"))[0], qn("a:alpha"), val="0")   # fully transparent, still clickable
        cover.line.fill.background()
        cover.shadow.inherit = False
        # replace python-pptx's click-to-play timing with autoplay (+ loop)
        sld = s._element
        old = sld.find(qn("p:timing"))
        new = etree.fromstring(timing(v1.shape_id, round(1000 * (r["nEnd"] + 1) / fps),
                                      v2.shape_id if v2 else None, round(1000 * r["nP"] / fps) if v2 else None))
        if old is not None:
            old.getparent().replace(old, new)
        else:
            sld.append(new)
        # speaker notes: the slide's name, then its paragraphs
        tf = s.notes_slide.notes_text_frame
        tf.text = f"{sid} · {title}"
        tf.paragraphs[0].runs[0].font.bold = True
        for para in notes.get(sid, {}).get("p", []):
            tf.add_paragraph().text = para
    prs.save(PPTX)
    finish(PPTX)


def finish(path):
    """Settings python-pptx has no API for: no play bar on videos, and a 16:9 size type."""
    show = (f'<p:showPr xmlns:p="{P}" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" showNarration="1">'
            f'<p:present/><p:sldAll/><p:penClr><a:prstClr val="red"/></p:penClr><p:extLst>'
            f'<p:ext uri="{{2FDB2607-1784-4EEB-B798-7EB5836EED8A}}"><p14:showMediaCtrls xmlns:p14="{P14}" val="0"/></p:ext>'
            f'</p:extLst></p:showPr>')
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "ppt/presProps.xml":
                root = etree.fromstring(data)
                for old in root.findall(f"{{{P}}}showPr"):
                    root.remove(old)
                root.insert(0, etree.fromstring(show))           # showPr precedes extLst
                data = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
            elif item.filename == "ppt/presentation.xml":
                data = re.sub(rb'(<p:sldSz [^>]*?) type="screen4x3"', rb"\1", data)
            # media is already compressed: store it as is
            ztype = zipfile.ZIP_STORED if item.filename.endswith((".mp4", ".png")) else zipfile.ZIP_DEFLATED
            zout.writestr(item, data, compress_type=ztype)
    tmp.replace(path)


if __name__ == "__main__":
    main()
