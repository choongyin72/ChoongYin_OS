"""Extract the reference PDF's OWN embedded logo and use it as the report asset.

R07.001/output/logo.png is a different INPEX mark (a small square badge) from the wide
purple wordmark the reference actually uses, and JasperReports' default RetainShape scaling
then aspect-fits it into a fraction of the 128x22 box. Rather than guess which sibling
report's logo.jpg/png is the right one, take the image out of the reference itself - that is
the ground truth by definition.

Writes logo_ref.png next to the report and reports both images' dimensions for comparison.
"""
import fitz

B = r"C:\Projects\INPEX\sources\CrystalReports\R07.001"
ref = fitz.open(B + r"\crytsal report in pdf\R07.001 - Offshore Daily Operations Report.pdf")

page = ref[0]

# Render the logo REGION rather than pulling the raw XObject. The embedded image is a
# stencil whose SMask carries the letter shapes, so extracting the XObject alone produced a
# wordmark reading "INbEX" - the P malformed. Rendering the page area reproduces exactly
# what the reference displays, mask included.
bb0 = page.get_image_info()[0]["bbox"]
clip = fitz.Rect(bb0)
pm = page.get_pixmap(dpi=600, clip=clip)
region = B + r"\output\logo_ref.png"
pm.save(region)
print(f"rendered logo region -> {region}   {pm.width}x{pm.height}  "
      f"aspect={pm.width / pm.height:.3f}")

imgs = page.get_images(full=True)
print(f"embedded images on page 1: {len(imgs)}")
for i, im in enumerate(imgs):
    xref = im[0]
    pix = fitz.Pixmap(ref, xref)
    print(f"  xref {xref}: {pix.width}x{pix.height}  n={pix.n}  alpha={pix.alpha}  "
          f"aspect={pix.width / pix.height:.3f}")
    if pix.n > 3:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    out = B + r"\output\logo_xobject_only.png"
    pix.save(out)
    print(f"  written (diagnostic only, mask dropped): {out}")

existing = B + r"\output\logo.png"
try:
    p2 = fitz.Pixmap(existing)
    print(f"\nexisting logo.png: {p2.width}x{p2.height}  aspect={p2.width / p2.height:.3f}")
except Exception as e:
    print(f"\nexisting logo.png unreadable: {e}")

bb = page.get_image_info()[0]["bbox"]
print(f"\nreference draws it at {bb[2]-bb[0]:.2f} x {bb[3]-bb[1]:.2f} pt  "
      f"aspect={(bb[2]-bb[0])/(bb[3]-bb[1]):.3f}")
