from PIL import Image, ImageDraw, ImageFilter
import math, random

W = H = 768
img = Image.new('RGB', (W, H), (5, 8, 24))
p = img.load()
# Deep ocean-to-cosmos gradient with a warm horizon.
for y in range(H):
    t = y / H
    for x in range(W):
        wave = 10 * math.sin(x * .018 + y * .011)
        r = int(5 + 13*t + max(0, 1-t)*wave*.18)
        g = int(8 + 15*t + max(0, 1-t)*wave*.25)
        b = int(24 + 35*t + max(0, 1-t)*wave*.65)
        if y < 270:
            glow = max(0, 1 - math.hypot(x-390, y-210)/330)
            r += int(42*glow); g += int(15*glow); b += int(5*glow)
        p[x,y] = (min(r,90), min(g,80), min(b,120))
# Draw geometry at double resolution, then downsample for clean paper edges.
img = img.resize((W*2, H*2), Image.Resampling.BICUBIC)
class SmoothDraw:
    def __init__(self, image):
        self.draw = ImageDraw.Draw(image, 'RGBA')
    def __getattr__(self, name):
        def scaled(coords, *args, **kwargs):
            if coords and isinstance(coords[0], (tuple,list)):
                coords = [(x*2,y*2) for x,y in coords]
            else:
                coords = tuple(v*2 for v in coords)
            if 'width' in kwargs:
                kwargs['width'] *= 2
            return getattr(self.draw, name)(coords, *args, **kwargs)
        return scaled
d = SmoothDraw(img)

# Nebula and stars: sparse so the dragon remains the focal point.
for i in range(125):
    x = (i*137 + 41) % W
    y = (i*71 + 19) % 330
    a = 80 + (i*31)%130
    rr = 1 if i%5 else 2
    d.ellipse((x-rr,y-rr,x+rr,y+rr), fill=(120,220,244,a))
for i in range(20):
    x = 70 + (i*89)%630; y = 55 + (i*47)%240
    d.line((x-5,y,x+5,y), fill=(255,205,100,100), width=1)
    d.line((x,y-5,x,y+5), fill=(255,205,100,100), width=1)

# Spiral galaxy behind the rising dragon.
cx, cy = 401, 249
for k in range(90, 2, -3):
    a = k * .075
    x = cx + math.cos(a*2.4) * k * 1.35
    y = cy + math.sin(a*2.4) * k * .46
    col = (255, 116 + int(k*.7), 67, max(10, int(95-k*.45)))
    d.ellipse((x-3,y-3,x+3,y+3), fill=col)

# Ocean folds and a sweeping cyan wave.
for row in range(18):
    yy = 525 + row*11
    pts=[]
    for x in range(-30,W+35,18):
        pts.append((x, yy + 9*math.sin(x*.025+row*.8)))
    d.line(pts, fill=(35,142+row*3,177+row*2,130), width=3)
for k in range(9):
    pts=[]
    for x in range(-20, 805, 12):
        y = 630 + k*13 + 20*math.sin(x*.013+k*.9) + 8*math.sin(x*.035)
        pts.append((x,y))
    d.line(pts, fill=(7,49,81,170), width=8)

# Dragon: one huge angular silhouette, tail curling into the galaxy.
# Tail spiral is constructed from a thick polyline plus highlighted facet edges.
tail=[]
for i in range(180):
    t=i/179
    ang = 5.0 - t*math.pi*2.5
    rad = 265*(1-t) + 18
    tail.append((cx + math.cos(ang)*rad*1.05, cy + math.sin(ang)*rad*.55))
d.line(tail, fill=(224,77,49,255), width=48, joint='curve')
d.line(tail, fill=(255,173,67,255), width=29, joint='curve')
d.line(tail, fill=(255,221,125,255), width=7, joint='curve')
# dark facet cuts on tail
for i in range(12,165,18):
    x,y=tail[i]; d.line((x-15,y-20,x+18,y+17), fill=(111,40,56,230), width=5)

# Wings: sharp paper planes.
left_wing=[(343,260),(155,125),(215,307),(92,356),(306,342)]
right_wing=[(447,269),(610,114),(571,300),(694,350),(477,350)]
d.polygon(left_wing, fill=(244,117,54,255), outline=(255,220,126,255), width=5)
d.polygon(right_wing, fill=(230,72,52,255), outline=(255,220,126,255), width=5)
d.line((343,260,215,307,306,342), fill=(103,32,55,255), width=4)
d.line((447,269,571,300,477,350), fill=(103,32,55,255), width=4)
d.line((343,260,155,125), fill=(255,217,126,220), width=3)
d.line((447,269,610,114), fill=(255,217,126,220), width=3)

# A luminous orbital lens makes the dragon's neck double as a surreal observatory.
d.arc((206,92,612,494), 205, 338, fill=(76,232,239,115), width=12)
d.arc((228,114,590,472), 205, 338, fill=(137,255,239,210), width=3)
d.polygon([(398,101),(425,82),(450,103),(424,115)], fill=(117,249,235,220))
for q in range(6):
    xx = 190 + q*78
    d.line((xx, 485+q*7, xx+42, 510+q*5), fill=(93,236,233,130), width=4)

# Main neck/head rising toward upper center.
neck=[(302,480),(287,377),(319,275),(366,192),(402,149),(450,184),(463,270),(438,372),(414,490)]
d.polygon(neck, fill=(246,101,48,255), outline=(255,219,125,255), width=6)
# folded planes
d.polygon([(319,275),(366,192),(386,312),(351,384)], fill=(255,177,65,220))
d.polygon([(386,312),(402,149),(438,372),(414,490)], fill=(167,44,54,220))
d.line((319,275,386,312,438,372), fill=(100,30,51,255), width=5)
d.line((351,384,414,490), fill=(255,223,140,200), width=3)
# dragon crown and snout.
d.polygon([(366,192),(360,125),(391,154),(414,84),(431,153),(477,117),(451,189),(492,220),(426,234)], fill=(255,157,61,255), outline=(255,226,143,255), width=5)
d.polygon([(426,234),(492,220),(464,260),(403,253)], fill=(201,55,52,255))
# luminous eye
d.ellipse((409,185,439,215), fill=(12,32,48,255), outline=(255,242,164,255), width=5)
d.ellipse((420,193,431,204), fill=(255,245,166,255))
# jaw sparks
d.line((441,243,478,252), fill=(255,231,151,255), width=4)
d.line((442,250,472,267), fill=(255,231,151,220), width=3)

# Boat at the base, crisp and tiny for scale.
boat=[(270,574),(494,574),(431,640),(320,640)]
d.polygon(boat, fill=(247,182,82,255), outline=(255,235,157,255), width=5)
d.polygon([(270,574),(385,598),(494,574),(430,615),(319,615)], fill=(255,222,134,255), outline=(105,45,46,255), width=4)
d.line((385,598,385,640), fill=(115,46,47,255), width=4)
# tiny observer
x,y=386,565
d.ellipse((x-7,y-25,x+7,y-11), fill=(8,15,29,255))
d.polygon([(x-10,y-10),(x+10,y-10),(x+15,y+21),(x-14,y+21)], fill=(8,15,29,255))
d.line((x-7,y+19,x-16,y+35), fill=(8,15,29,255), width=5)
d.line((x+7,y+19,x+16,y+35), fill=(8,15,29,255), width=5)

# Foreground foam arcs add depth and motion.
for k in range(8):
    box=(25+k*75, 570+k*7, 270+k*62, 740+k*3)
    d.arc(box, 198, 342, fill=(92,225,229,150), width=4)
# small warm reflections under the boat
d.line((292,663,478,663), fill=(255,173,74,100), width=4)
d.line((325,680,449,680), fill=(255,126,63,80), width=3)

# Downsample-free final polish: a narrow dark border keeps thumbnail silhouette clean.
d.rectangle((10,10,W-11,H-11), outline=(255,213,120,150), width=3)
img.resize((W, H), Image.Resampling.LANCZOS).save('entry.png', format='PNG', optimize=True, compress_level=9)
