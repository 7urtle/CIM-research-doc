import re
p = r'C:\Users\weiyu\Desktop\CIM研究\tutorial\17_JSSC2025_OneShot_FP_CIM_FineTune\_src\make_videos.py'
s = open(p, encoding='utf-8').read()
# rename weight list W -> Wbits within v02 function only (lines between "def v02" and "def v03")
start = s.index('def v02')
end = s.index('def v03')
seg = s[start:end]
seg2 = seg.replace('W = [1, 0, 1, 1, 0, 1, 0, 1]', 'Wbits = [1, 0, 1, 1, 0, 1, 0, 1]')
seg2 = seg2.replace('WB = [1 - v for v in W]', 'WB = [1 - v for v in Wbits]')
seg2 = seg2.replace('G = [W[i] & XB[i] for i in range(8)]', 'G = [Wbits[i] & XB[i] for i in range(8)]')
seg2 = seg2.replace('if W[i] < X[i]:', 'if Wbits[i] < X[i]:')
seg2 = seg2.replace('elif W[i] > X[i]:', 'elif Wbits[i] > X[i]:')
seg2 = seg2.replace('str(W[c])', 'str(Wbits[c])')
seg2 = seg2.replace('d.rectangle([x, by, x + bs - 6, by + 26], fill=(44, 34, 20), outline=(240, 180, 70))', 'd.rectangle([x, by, x + bs - 6, by + 26], fill=(44, 34, 20), outline=(240, 180, 70))')
open(p, 'w', encoding='utf-8').write(s[:start] + seg2 + s[end:])
print('patched')
