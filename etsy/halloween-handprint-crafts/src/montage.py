# Combine preview PNGs side by side: python3 src/montage.py id1 id2 ... -> build/preview/_m.png
import sys
from PIL import Image
ims=[]
for i in sys.argv[1:]:
    row=[Image.open(f'build/preview/{i}-{t}.png').convert('RGB') for t in ('sample','color','bw')]
    w=sum(r.width for r in row)+20; h=max(r.height for r in row)
    canvas=Image.new('RGB',(w,h),(120,120,120)); x=0
    for r in row: canvas.paste(r,(x,0)); x+=r.width+10
    ims.append(canvas)
W=max(i.width for i in ims); H=sum(i.height for i in ims)+10*len(ims)
out=Image.new('RGB',(W,H),(80,80,80)); y=0
for i in ims: out.paste(i,(0,y)); y+=i.height+10
s=float(sys.argv[0] and 0.55)
out=out.resize((int(W*s),int(H*s)))
out.save('build/preview/_m.png')
