import json
W=json.load(open('week_2026-11-26.json'))
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
S[24]=[hook([("STOP SAYING","dark",104),("THE CITY NAME","dark",100),("EVERY SENTENCE.","w",96)]),
 {"from":1,"elements":[T(1,560,[["\"BEST PLUMBER IN MESA\"","grey"]],62),T(1,680,[["\"MESA PLUMBING\"","grey"]],62,1.0),T(1,800,[["\"PLUMBERS MESA\"","grey"]],62,1.8),T(2,1050,[["NOBODY TALKS LIKE THAT.","r"]],76)]},
 {"from":3,"elements":[T(3,640,"NOT THE VISITOR.",90),T(3,800,[["NOT THE PAGE.","r"]],90,1.0)]},
 {"from":4,"elements":[T(4,480,[["SAY THE TOWN WHERE IT'S USEFUL","y"]],60),ck(5,640,[("In the title",True,5,0),("In the first line",True,5,0.8),("In the area you cover",True,5,1.6)])]},
 {"from":6,"elements":[T(6,520,"THEN WRITE ABOUT",84),T(6,650,[["THE ACTUAL JOB.","y"]],96,0.4),chip(7,900,"What it costs",fill='w',size=56),chip(7,1040,"How long it takes",fill='w',size=56,dt=0.7),chip(7,1180,"What's included",fill='y',size=56,dt=1.4)]},
 {"from":8,"elements":[flow(8,520,[("The service","y",8,0),("Each city page","w",8,1.0),("Your WordPress","g",9,0)]),T(9,1300,[["REWRITE ANY LINE","y"]],70,0.6)]},
 real(10),cta(11)]
S[25]=[hook([("BEFORE YOU","dark",110),("BUILD, SEARCH","dark",104),("IT YOURSELF.","w",110)]),
 {"from":1,"elements":[{"type":"search","at":1,"y":480,"query":"water heater repair in Boise"},T(2,820,[["WHAT'S ON PAGE ONE?","y"]],80)]},
 {"from":3,"elements":[T(3,560,"BIG DIRECTORIES ONLY?",76),T(3,680,[["HARD FIGHT.","r"]],96,1.2),T(4,900,"THIN LOCAL SITES?",76),T(4,1020,[["THAT'S A GAP.","g"]],96,1.2)]},
 {"from":5,"elements":[T(5,520,"OPEN THE TOP 3.",90),T(5,660,[["COUNT THEIR PAGES.","y"]],84,0.8),T(6,900,[["1 PAGE FOR EVERYTHING?","w"]],70),T(6,1010,[["YOU CAN DO BETTER.","g"]],80,1.4)]},
 {"from":7,"elements":[T(7,600,"10 MINUTES",110),T(7,760,[["CAN SAVE A MONTH.","y"]],84,1.0),T(8,1000,[["ANSWER THE SEARCH BETTER","g"]],64)]},
 {"from":9,"elements":[flow(9,560,[("Every service","w",9,0),("Every nearby town","y",9,1.2)])]},
 real(10),cta(11)]
S[26]=[hook([("NO LEAD COUNT?","dark",104),("NO RENT","dark",120),("PRICE.","w",130)]),
 {"from":1,"elements":[T(1,600,"THE OWNER ASKS:",84),T(2,760,[["\"HOW MANY CALLS","y"]],84),T(2,880,[["DOES IT GET?\"","y"]],84,0.3)]},
 {"from":3,"elements":[T(3,640,[["\"UM, A FEW?\"","grey"]],100),T(3,820,[["NOT AN ANSWER.","r"]],90,1.0)]},
 {"from":4,"elements":[ck(4,520,[("Every form",True,4,0),("Every call",True,4,0.8),("The date",True,5,0),("The job they asked about",True,5,0.8)])]},
 {"from":6,"elements":[T(6,600,"A FEW MONTHS IN:",84),T(6,740,[["REAL NUMBERS.","g"]],100,1.0),T(7,960,[["YOURS. NOT A GUESS.","y"]],76)]},
 {"from":8,"elements":[flow(8,520,[("Quote request","w",8,0),("Your email","y",8,1.0),("A record of each one","g",8,2.2)]),chip(9,1280,"Track the call line too",fill='w',size=54)]},
 real(10),cta(11)]
S[27]=[hook([("STOCK PHOTOS","dark",110),("MAKE EVERY SITE","dark",96),("LOOK THE SAME.","w",104)]),
 {"from":1,"elements":[T(1,600,[["SMILING GUY","grey"]],90),T(1,720,[["WITH A WRENCH.","grey"]],90,0.3),T(2,920,[["THE SPOTLESS KITCHEN","grey"]],76),T(2,1030,[["NOBODY OWNS.","grey"]],76,0.5)]},
 {"from":3,"elements":[T(3,700,"SEEN IT",120),T(3,860,[["ON 100 SITES.","r"]],96,0.8)]},
 {"from":4,"elements":[T(4,560,[["REAL PHOTOS","g"]],110),T(4,700,"FEEL DIFFERENT.",90,0.5),T(5,940,"GOT A RENTER?",84),T(5,1060,[["ASK FOR THEIRS.","y"]],84,0.6)]},
 {"from":6,"elements":[ck(6,520,[("Their trucks",True,6,0),("Their jobs",True,6,0.6),("Their team",True,6,1.2)]),T(7,1100,[["= A REAL BUSINESS","g"]],76)]},
 {"from":8,"elements":[flow(8,560,[("The pages","w",8,0),("Your WordPress","y",8,1.0)]),T(9,1050,"SWAP A PHOTO:",80),T(9,1170,[["ONE MINUTE.","g"]],96,0.4)]},
 real(10),cta(11)]
S[28]=[hook([("PUT THE","dark",120),("DEAL IN","dark",120),("WRITING.","w",130)]),
 {"from":1,"elements":[T(1,640,"HANDSHAKE = FINE",84),T(1,780,[["UNTIL THE FIRST ARGUMENT.","r"]],62,1.2)]},
 {"from":2,"elements":[T(2,460,[["WHAT THEY RENT","y"]],76),ck(3,600,[("The site",True,3,0),("The leads",True,3,0.6),("The phone number",True,3,1.2)])]},
 {"from":4,"elements":[ck(4,520,[("Monthly price + due date",True,4,0),("How either side ends it",True,5,0),("Who keeps the site: you",True,6,0)])]},
 {"from":7,"elements":[T(7,640,"ONE PAGE.",120),T(7,800,[["CLEAR BEATS FANCY.","y"]],84,1.0)]},
 {"from":8,"elements":[flow(8,520,[("Your WordPress","w",8,0),("Site in your name","y",8,1.2),("You pick who gets leads","g",9,0)])]},
 real(10),cta(11)]
S[29]=[hook([("PICK A NICHE","dark",110),("WHERE PEOPLE","dark",104),("CALL TODAY.","w",116)]),
 {"from":1,"elements":[T(1,560,"BURST PIPE?",100),T(1,720,[["NOBODY COMPARES 10 QUOTES.","r"]],58,0.6),flow(2,900,[("Search","w",2,0),("Tap","y",2,0.5),("Call","g",2,1.0)],gap=170)]},
 {"from":3,"elements":[T(3,640,"THAT'S WHAT A",84),T(3,770,[["LEAD SITE IS GOOD AT.","y"]],76,0.4)]},
 {"from":4,"elements":[ck(4,480,[("Water heaters",True,4,0),("Garage doors",True,4,0.6),("Locksmiths",True,4,1.2),("Leaks",True,4,1.8)]),T(5,1240,[["BROKE. FIX IT NOW.","y"]],76)]},
 {"from":6,"elements":[T(6,560,[["DREAM KITCHEN?","grey"]],90),T(6,690,[["PLANNED FOR A YEAR.","grey"]],76,1.0),T(7,920,"BOTH CAN WORK.",84),T(7,1040,[["ONE CALLS FASTER.","g"]],84,0.8)]},
 {"from":8,"elements":[flow(8,520,[("Niche + city","y",8,0),("Every page","w",8,1.0),("Call button + short form","g",9,0)])]},
 real(10),cta(11)]
S[30]=[hook([("OPEN YOUR SITE","dark",100),("ON YOUR PHONE.","dark",100),("RIGHT NOW.","w",120)]),
 {"from":1,"elements":[T(1,640,"THAT'S HOW A",84),T(1,770,[["HOMEOWNER WITH A LEAK","y"]],70,0.4),T(1,880,[["SEES IT.","y"]],84,1.0)]},
 {"from":2,"elements":[ck(2,480,[("What you do, in 1 second?",False,2,0),("The town?",False,3,0),("Tap to call, no zoom?",False,4,0),("Short form for a thumb?",False,5,0)])]},
 {"from":6,"elements":[T(6,600,"ANY NO?",120),T(6,760,[["FIX THAT FIRST.","r"]],96,0.6),T(7,980,"BEFORE ANOTHER PAGE.",70),T(7,1080,"BEFORE ANOTHER BACKLINK.",64,0.8)]},
 {"from":8,"elements":[{"type":"browser","at":8,"y":420,"url":"preview.settorank.com","title":"Water Heater Repair in Boise","button":"Call now"},T(9,1380,[["EDIT IT ALL IN WORDPRESS","y"]],62)]},
 real(10),cta(11)]
for k,v in W.items():
    k=int(k)
    job={"episode":k,"series":"RANK & RENT · BUILD FASTER","hook":v['lines'][0],"accent":[64,200,255],
         "voice":f"../voices/ep{k}.mp3","atempo":1.08,"music_vol":0,"out":f"../out/ep{k}_{v['slug']}.mp4",
         "lines":v['lines'],"scenes":S[k]}
    json.dump(job,open(f'ep{k}.json','w'),indent=1)
print('ok')
