import json
W=json.load(open('week_2026-11-19.json'))
def T(at,y,segs,size=90,dt=0):
    if isinstance(segs,str): segs=[[segs,'w']]
    return {"type":"text","at":at,"y":y,"segs":segs,"size":size,"dt":dt}
def chip(at,y,text,fill='y',color='dark',size=56,dt=0): return {"type":"chip","at":at,"y":y,"text":text,"fill":fill,"color":color,"size":size,"dt":dt}
def ck(at,y,items): return {"type":"checklist","at":at,"y":y,"items":[{"text":t,"ok":ok,"at":a,"dt":d} for t,ok,a,d in items]}
def flow(at,y,nodes,gap=200): return {"type":"flow","at":at,"y":y,"gap":gap,"nodes":[{"label":l,"color":c,"at":a,"dt":d} for l,c,a,d in nodes]}
def hook(segs): # list of (text,color,size)
    ys=[560,720,890]; return {"from":0,"bg":"yellow","elements":[T(0,ys[i],[[t,c]],s,[-0.3,0,0.4][i]) for i,(t,c,s) in enumerate(segs)]}
def real(i): return {"from":i,"elements":[T(i,500,[["REAL TALK","y"]],80),T(i,700,"IT BUILDS THE SITE.",84,0.4),T(i,900,[["IT DOESN'T","grey"]],72,1.6),T(i,1020,[["GUARANTEE RANKINGS.","grey"]],72,1.8)]}
def cta(i): return {"from":i,"elements":[T(i,700,"BUILD ONE",110),T(i,850,[["FREE.","y"]],130,0.2),chip(i,1150,"Link in bio · settorank.com",size=50,dt=0.6)]}
S={}
S[17]=[hook([("YOUR CITY PAGES","dark",100),("HAVE NO","dark",104),("WAY IN.","w",130)]),
 {"from":1,"elements":[ck(1,480,[("Mesa",True,1,0),("Gilbert",True,1,0.3),("Chandler",True,1,0.6),("Tempe",True,1,0.9)]),T(2,1250,[["LINKS TO THEM: ","w"],["0","r"]],90)]},
 {"from":3,"elements":[T(3,600,"GOOGLE FOLLOWS LINKS.",80),T(3,760,[["SO DO VISITORS.","y"]],80,1.2),T(4,1000,[["NO LINK = NOT FOUND","r"]],72)]},
 {"from":5,"elements":[flow(5,520,[("Service page","w",5,0),("Town pages","y",5,0.8),("Back to services","g",6,0)]),chip(7,1300,"Main pages in the menu",fill='w',size=52)]},
 {"from":8,"elements":[flow(8,560,[("Every service","w",8,0),("Every nearby city","y",8,0.8),("Your WordPress","g",9,0)]),T(9,1300,[["CHANGE ANY LINK","y"]],70,0.6)]},
 real(10),cta(11)]
S[18]=[hook([("ONE SITE.","dark",120),("ONE","dark",120),("NICHE.","w",140)]),
 {"from":1,"elements":[ck(1,480,[("Plumbing",False,1,0),("Roofing",False,1,0.4),("Pest control",False,1,0.8)]),T(2,1100,[["= THREE HALF-SITES","r"]],76)]},
 {"from":3,"elements":[T(3,600,"WHAT IS THIS",90),T(3,740,[["SITE ABOUT?","y"]],100,0.4),T(4,980,"NO PLUMBER RENTS",70),T(4,1080,[["A ROOFING SITE.","r"]],70,0.5)]},
 {"from":5,"elements":[flow(5,520,[("One service","y",5,0),("A page per job","w",6,0),("A page per town","g",7,0)])]},
 {"from":8,"elements":[T(8,560,"ONE NICHE.",90),T(8,700,"ONE CITY.",90,0.6),T(8,840,[["THE TOWNS AROUND IT.","y"]],70,1.2),chip(9,1150,"2nd niche = 2nd site",fill='w',size=56)]},
 real(10),cta(11)]
S[19]=[hook([("YOUR RENTER","dark",110),("QUIT.","dark",130),("NOW WHAT?","w",110)]),
 {"from":1,"elements":[T(1,600,"RENTERS COME AND GO.",80),T(2,800,[["THE SITE STAYS YOURS.","y"]],80)]},
 {"from":3,"elements":[T(3,560,"SWAP IN MINUTES,",84),T(3,690,[["NOT A REBUILD.","y"]],84,0.6),ck(4,880,[("Lead email you can change",True,4,0),("Call number you control",True,5,0),("Business name easy to edit",True,6,0)])]},
 {"from":7,"elements":[T(7,700,"NEXT RENTER =",90),T(7,850,[["ONE UPDATE.","g"]],110,0.4)]},
 {"from":8,"elements":[flow(8,520,[("Your WordPress","w",8,0),("Leads by email","y",8,0.8),("Whoever you choose","g",9,0)])]},
 real(10),cta(11)]
S[20]=[hook([("NOBODY READS","dark",100),("YOUR PAGE.","dark",104),("THEY SCAN IT.","w",110)]),
 {"from":1,"elements":[T(1,560,"WATER HEATER",90),T(1,690,[["JUST DIED.","r"]],100,0.3),T(2,900,[["3 ANSWERS. FAST.","y"]],80)]},
 {"from":3,"elements":[ck(3,520,[("Do you do this?",False,3,0),("Do you come to my town?",False,3,0.9),("Roughly what does it cost?",False,3,1.9)])]},
 {"from":4,"elements":[T(4,640,[["\"OUR PASSION IS...\"","grey"]],76),T(4,820,[["THEY'RE GONE.","r"]],100,1.0)]},
 {"from":5,"elements":[flow(5,480,[("Service + town","y",5,0),("What's included + price","w",6,0),("Call + short form","g",7,0)])]},
 {"from":8,"elements":[ck(8,520,[("Town pages",True,8,0.3),("Cost calculator",True,8,1.0),("Quote form",True,8,1.7)]),T(9,1150,[["REWRITE ANY LINE","y"]],70)]},
 real(10),cta(11)]
S[21]=[hook([("YOUR HOMEPAGE","dark",100),("ISN'T WHERE","dark",100),("LEADS COME FROM.","w",88)]),
 {"from":1,"elements":[T(1,600,"DAYS ON THE HOMEPAGE.",76),T(2,800,[["NOBODY SEARCHES FOR IT.","r"]],70)]},
 {"from":3,"elements":[{"type":"search","at":3,"y":480,"query":"roof leak repair in Tulsa"},T(4,800,"LANDS ON A",80),T(4,920,[["SERVICE OR CITY PAGE","y"]],76,0.3),T(5,1150,[["NO PAGE = NOT IN THE RACE","r"]],60)]},
 {"from":6,"elements":[T(6,560,"WORK WHERE",90),T(6,690,[["THE SEARCHES GO.","y"]],90,0.4),chip(7,950,"1 page per service",fill='w',size=56),chip(7,1100,"1 page per town",fill='y',size=56,dt=0.6)]},
 {"from":8,"elements":[flow(8,560,[("Niche + city","y",8,0),("Every page","w",8,0.8),("Homepage too","grey",9,0)])]},
 real(10),cta(11)]
S[22]=[hook([("DON'T PITCH","dark",110),("WITH NOTHING","dark",104),("TO SHOW.","w",120)]),
 {"from":1,"elements":[T(1,640,[["\"I CAN GET YOU LEADS\"","grey"]],72),T(1,800,[["= IGNORED","r"]],90,1.2)]},
 {"from":2,"elements":[{"type":"browser","at":2,"y":420,"url":"preview.settorank.com","title":"Roof Leak Repair in Tulsa","button":"Get a quote"},T(3,1380,[["THEY CAN CLICK IT.","y"]],70)]},
 {"from":4,"elements":[T(4,600,"REAL CALLS =",90),T(4,740,[["REAL PROOF.","g"]],100,0.6),T(5,980,"BUILD FIRST.",84),T(5,1100,[["RENT LATER.","y"]],84,0.6)]},
 {"from":6,"elements":[T(6,600,"BY HAND:",90),T(6,740,[["WEEKS.","r"]],130,0.4),flow(7,960,[("Niche + city","y",7,0),("Whole site","g",7,0.8)])]},
 {"from":8,"elements":[T(8,560,"BUILD + PREVIEW",90),T(8,700,[["FREE","g"]],130,0.4),T(8,880,[["PLANS FROM $47/MO","y"]],70,2.0),T(9,1050,"NO FAKE REVIEWS.",66),T(9,1150,"NO MADE-UP NUMBERS.",66,0.7)]},
 real(10),cta(11)]
S[23]=[hook([("STOP RESEARCHING.","dark",96),("PICK","dark",120),("ONE.","w",140)]),
 {"from":1,"elements":[T(1,600,"3 WEEKS COMPARING.",84),T(1,740,[["0 SITES LIVE.","r"]],100,0.8),T(2,980,[["NOT LIVE = CAN'T RANK","y"]],70)]},
 {"from":3,"elements":[flow(3,480,[("A service people need","y",3,0),("A city + its towns","w",4,0),("Build. Publish. Watch.","g",5,0)])]},
 {"from":6,"elements":[T(6,620,"SLOW? YOU LEARNED.",80),T(7,820,[["SITE #2 > SITE #1","y"]],86)]},
 {"from":8,"elements":[flow(8,560,[("Niche + city","y",8,0),("Whole site","w",8,0.8)]),T(8,1050,[["NOT WEEKS","g"]],90,2.2),T(9,1250,[["BUILD + PREVIEW: FREE","y"]],64)]},
 real(10),cta(11)]
for k,v in W.items():
    k=int(k)
    job={"episode":k,"series":"RANK & RENT · BUILD FASTER","hook":v['lines'][0],"accent":[64,200,255],
         "voice":f"../voices/ep{k}.mp3","atempo":1.08,"music_vol":0,"out":f"../out/ep{k}_{v['slug']}.mp4",
         "lines":v['lines'],"scenes":S[k]}
    json.dump(job,open(f'ep{k}.json','w'),indent=1)
print('ok')
