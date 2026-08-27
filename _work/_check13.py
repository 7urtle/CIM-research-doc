from PIL import Image
import numpy as np
for name, idx in [("v01", 60), ("v02", 100), ("v03", 100)]:
    p = r"C:\Users\weiyu\Desktop\CIM研究\tutorial\13_JSSC2025_MultiplyLess_Approx_CIM\_work_vid13\%s\f%04d.png" % (name, idx)
    im = np.array(Image.open(p))
    uniq = len(np.unique(im.reshape(-1, 3), axis=0))
    nonbg = (np.abs(im.astype(int) - np.array([10,17,25])).sum(axis=2) > 30).sum()
    print(name, "size", im.shape, "uniq_colors", uniq, "nonbg_px", nonbg)
