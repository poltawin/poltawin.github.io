from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1200,630
BG=(0x13,0x14,0x15); CY=(0x1E,0xBE,0xD6); WH=(255,255,255); SEC=(0xad,0xb0,0xb1)
B="RP.ttf"; R="RP-400.ttf"; L="RP-300.ttf"; S="RP-600.ttf"
PFP="/Users/tawinchoksitthikasam/Desktop/Pol cv/assets/pfp.jpg"
NAME1,NAME2="Pol Tawin","Choksitthikasam"
ROLE="MSc Financial Technology  ·  Imperial College London"
SUB="Data-driven finance, blockchain and machine learning"
DOM="poltawin.com"

def F(p,s): return ImageFont.truetype(p,s)
def draw_t(d,xy,t,f,fill):
    d.text(xy,t,font=f,fill=fill); b=d.textbbox(xy,t,font=f); return b

def monogram(size):
    """cyan tile with the P knocked out"""
    ss=4; tile=Image.new("RGBA",(size*ss,size*ss),(0,0,0,0))
    dd=ImageDraw.Draw(tile)
    dd.rounded_rectangle((0,0,size*ss-1,size*ss-1),radius=int(size*ss*0.22),fill=CY)
    target=size*ss*0.54; lo,hi=1,size*ss*3
    for _ in range(30):
        mid=(lo+hi)/2; f=F(B,int(mid) or 1)
        bb=dd.textbbox((0,0),"P",font=f)
        if bb[3]-bb[1]<target: lo=mid
        else: hi=mid
    f=F(B,int(lo) or 1); bb=dd.textbbox((0,0),"P",font=f)
    w=bb[2]-bb[0]; h=bb[3]-bb[1]
    dd.text((size*ss/2-w/2-bb[0], size*ss/2-h/2-bb[1]),"P",font=f,fill=BG)
    return tile.resize((size,size),Image.LANCZOS)

def crop_person(box_w,box_h):
    im=Image.open(PFP).convert("RGB")
    # he sits in the right ~55% of the frame, face near y=0.29H
    ar=box_w/box_h
    src_w=int(im.width*0.64); src_h=int(src_w/ar)
    x0=im.width-src_w; y0=max(0,int(im.height*0.29-src_h*0.42))
    if y0+src_h>im.height:
        y0=im.height-src_h
    return im.crop((x0,y0,x0+src_w,y0+src_h)).resize((box_w,box_h),Image.LANCZOS)

def text_block(d,x,y,name_px,role_px,gap=1.02,with_sub=True):
    fB=F(B,name_px)
    b=draw_t(d,(x,y),NAME1,fB,WH); y=b[3]+int(name_px*(gap-1))+2
    b=draw_t(d,(x,y),NAME2,fB,WH); y=b[3]+int(name_px*0.46)
    b=draw_t(d,(x,y),ROLE,F(R,role_px),SEC); y=b[3]+int(role_px*0.55)
    if with_sub:
        b=draw_t(d,(x,y),SUB,F(L,int(role_px*0.86)),SEC)
    return y

# ---------- A: typographic ----------
def variant_a():
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    M=92
    im.paste(monogram(78),(M,M-6),monogram(78))
    text_block(d,M,M+112,84,30)
    d.rectangle((M,H-M-2,M+64,H-M+2),fill=CY)
    d.text((M+86,H-M-19),DOM,font=F(S,29),fill=CY)
    return im

# ---------- B: split, photo panel right ----------
def variant_b():
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    pw=452
    ph=crop_person(pw,H); im.paste(ph,(W-pw,0))
    # feather the photo's left edge into the background
    grad=Image.new("L",(160,1))
    for i in range(160): grad.putpixel((i,0),int(255*(i/159)**0.85))
    mask=grad.resize((160,H))
    im.paste(Image.new("RGB",(160,H),BG),(W-pw,0),Image.eval(mask,lambda v:255-v))
    M=88
    im.paste(monogram(70),(M,M-4),monogram(70))
    text_block(d,M,M+100,72,26)
    d.rectangle((M,H-M-2,M+56,H-M+2),fill=CY)
    d.text((M+76,H-M-17),DOM,font=F(S,26),fill=CY)
    return im

# ---------- C: photo background + scrim ----------
def variant_c():
    im=Image.open(PFP).convert("RGB")
    sc=max(W/im.width,H/im.height)
    nw,nh=int(im.width*sc),int(im.height*sc)
    im=im.resize((nw,nh),Image.LANCZOS)
    fy=int(im.height*0.29)
    y0=min(max(0,fy-int(H*0.46)),nh-H)
    im=im.crop((max(0,nw-W),y0,max(0,nw-W)+W,y0+H))
    # dark scrim, heavy on the left where the text sits
    scrim=Image.new("L",(W,1))
    for x in range(W):
        t=x/(W-1)
        scrim.putpixel((x,0),int(248*(1-t)**0.62+42))
    im=Image.composite(Image.new("RGB",(W,H),BG),im,scrim.resize((W,H)))
    d=ImageDraw.Draw(im)
    M=88
    im.paste(monogram(70),(M,M-4),monogram(70))
    text_block(d,M,M+100,72,26,with_sub=False)
    d.rectangle((M,H-M-2,M+56,H-M+2),fill=CY)
    d.text((M+76,H-M-17),DOM,font=F(S,26),fill=CY)
    return im

for n,fn in [("a",variant_a),("b",variant_b),("c",variant_c)]:
    img=fn(); img.save(f"og-{n}.png"); print("og-%s.png"%n, img.size)
