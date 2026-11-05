# SetToRank TikTok week 2026-11-06..11-12 (ep10-16). Generates epNN.json + captions_ep10-16.json
import json
RT="Real talk. It builds the site. It doesn't guarantee rankings."
CTA="Build one free. Link in bio."
TAGS="#rankandrent #localseo #wordpress #seo #leadgeneration"
def T(at,y,text,c="w",size=84,dt=0): return {"type":"text","at":at,"y":y,"segs":[[text,c]],"size":size,"dt":dt}
def chip(at,y,text,fill="grey",color="dark",size=60,dt=0): return {"type":"chip","at":at,"y":y,"text":text,"fill":fill,"color":color,"size":size,"dt":dt}
def check(at,y,items): return {"type":"checklist","at":at,"y":y,"items":[{"text":t,"ok":ok,"at":a,"dt":d} for t,ok,a,d in items]}
def hook(words):  # words: list of (text,color,size)
    ys=[580,730,900]; return {"from":0,"bg":"yellow","elements":[T(0,ys[i],w,c,s,[-0.3,0,0.4][i]) for i,(w,c,s) in enumerate(words)]}
def realtalk(i): return {"from":i,"elements":[T(i,500,"REAL TALK","y",80),T(i,700,"IT BUILDS THE SITE.","w",84,0.4),T(i,900,"IT DOESN'T","grey",72,1.6),T(i,1020,"GUARANTEE RANKINGS.","grey",72,1.8)]}
def cta(i): return {"from":i,"elements":[T(i,700,"BUILD ONE","w",110),T(i,850,"FREE.","y",130,0.2),chip(i,1150,"Link in bio · settorank.com","y","dark",50,0.6)]}
E={}
E[10]=dict(slug="page_titles",date="2026-11-06",angle="page titles",
 lines=["Your page titles are costing you clicks.","Most rank and rent pages just say Home or Services.","That's the line people see in Google before they click.","A good title says the service and the city.","Water heater repair in Mesa. Not Services.","Every service page needs its own. Every city page too.","By hand, across forty pages, that takes hours.","SetToRank writes a title for every page it builds.","Service pages, city pages, the home page, all of them.","You can still edit any of them in WordPress.",RT,CTA],
 scenes=[hook([("YOUR PAGE TITLES","dark",96),("ARE COSTING YOU","dark",96),("CLICKS.","w",130)]),
  {"from":1,"elements":[chip(1,600,"Home"),chip(1,740,"Services",dt=0.4),T(2,960,"THAT'S WHAT GOOGLE","w",72),T(2,1060,"SHOWS BEFORE THE CLICK","r",64,0.4)]},
  {"from":3,"elements":[T(3,480,"SERVICE + CITY","y",96),{"type":"versus","at":4,"y":660,"heads":["Weak","Strong"],"rows":[["Services","Water Heater Repair in Mesa"],["Home","Mesa Plumbing Repair"]],"step":0.6},T(5,1200,"ONE PER PAGE","g",80)]},
  {"from":6,"elements":[T(6,640,"BY HAND:","w",100),T(6,800,"40 PAGES","r",110,0.4),T(6,950,"OF TITLES","r",76,0.8)]},
  {"from":7,"elements":[T(7,420,"SETTORANK WRITES THEM","y",70),check(7,560,[("Service pages",True,8,0),("City pages",True,8,0.5),("Home page",True,8,1.0)]),T(9,1180,"YOUR WORDPRESS.","w",70),T(9,1280,"EDIT ANYTHING.","g",70,0.3)]},
  realtalk(10),cta(11)],
 caption="Your page titles are costing you clicks.\n\"Services\" tells nobody anything. \"Water heater repair in Mesa\" does. Every service page and every city page needs its own title.\nBuild one free. Link in bio.")
E[11]=dict(slug="niche_first",date="2026-11-07",angle="niche before city",
 lines=["Rank and renters: pick the niche before the city.","Most people pick a city first, then look for something to rank.","Flip it.","Pick a service people search when something breaks.","Burst pipe. Dead water heater. Tree on the roof.","Those searches usually end in a phone call.","Then pick a city, and the towns around it.","Now you know exactly which pages the site needs.","SetToRank builds the whole site from that niche and city.","A page for each service and each nearby town.",RT,CTA],
 scenes=[hook([("PICK THE NICHE","dark",104),("BEFORE","dark",104),("THE CITY.","w",130)]),
  {"from":1,"elements":[chip(1,620,"1. City"),chip(1,760,"2. Niche?",dt=0.5),T(2,1000,"FLIP IT.","y",130)]},
  {"from":3,"elements":[T(3,420,"SOMETHING BROKE","r",90),check(4,580,[("Burst pipe",True,4,0),("Dead water heater",True,4,0.6),("Tree on the roof",True,4,1.2)]),T(5,1180,"= A PHONE CALL","g",90)]},
  {"from":6,"elements":[{"type":"flow","at":6,"y":560,"gap":200,"nodes":[{"label":"Niche","color":"y","at":6,"dt":0},{"label":"Main city","color":"w","at":6,"dt":0.5},{"label":"Nearby towns","color":"g","at":6,"dt":1.0}]},T(7,1200,"= YOUR PAGE LIST","w",80)]},
  {"from":8,"elements":[T(8,420,"SETTORANK BUILDS","y",80),chip(8,600,"Plumbing · Mesa","y","dark",60,0.5),check(9,760,[("A page per service",True,9,0),("A page per nearby town",True,9,0.6)])]},
  realtalk(10),cta(11)],
 caption="Rank and renters: pick the niche before the city.\nStart with a service people search when something breaks. Then the city and the towns around it. That's your page list.\nBuild one free. Link in bio.")
E[12]=dict(slug="click_to_call",date="2026-11-08",angle="click-to-call on mobile",
 lines=["Your visitor is on a phone. Can they call?","Their water heater just died. They search on their phone.","They land on your site and want to talk now.","If the number is buried in the footer, they hit back.","If it's plain text, they have to copy it.","One tap to call. That's the whole job.","Put the call button at the top.","SetToRank adds a click-to-call button to every site it builds.","And the calls ring the number on the site.","Plus a quote form for people who'd rather type.",RT,CTA],
 scenes=[hook([("YOUR VISITOR","dark",104),("IS ON A PHONE.","dark",104),("CAN THEY CALL?","w",120)]),
  {"from":1,"elements":[{"type":"google_phone","at":1,"y":420,"query":"water heater repair near me"},T(2,1500,"THEY WANT TO TALK. NOW.","y",64)]},
  {"from":3,"elements":[chip(3,560,"Number in the footer"),T(3,720,"BACK BUTTON","r",90,0.6),chip(4,920,"Plain text number",dt=0),T(4,1080,"COPY. PASTE. GONE.","r",76,0.6)]},
  {"from":5,"elements":[T(5,600,"ONE TAP","g",130),T(5,760,"TO CALL.","w",110,0.3),chip(6,1000,"☎  Call now","g","dark",70,0),T(6,1160,"AT THE TOP","y",80,0.4)]},
  {"from":7,"elements":[T(7,420,"SETTORANK BUILDS IT IN","y",70),check(7,560,[("Click-to-call button",True,7,0.6),("Rings the site number",True,8,0),("Quote form",True,9,0)])]},
  realtalk(10),cta(11)],
 caption="Your visitor is on a phone. Can they call you in one tap?\nA number buried in the footer, or plain text they have to copy, sends them back to Google. Put a call button at the top.\nBuild one free. Link in bio.")
E[13]=dict(slug="thin_pages",date="2026-11-09",angle="thin service pages",
 lines=["A page with three sentences isn't a service page.","Lots of rank and rent sites look like this.","A heading, a stock photo, call now.","Google has nothing to go on. Neither does the visitor.","A real service page answers the questions people have.","What's included. Rough cost. How fast you come.","Which towns you cover. How to get a quote.","Writing that for every service is the slow part.","SetToRank writes a full page for every service and every city.","Unique pages, not copies, with FAQs and a quote form.",RT,CTA],
 scenes=[hook([("THREE SENTENCES","dark",100),("ISN'T A","dark",104),("SERVICE PAGE.","w",120)]),
  {"from":1,"elements":[chip(2,560,"Heading"),chip(2,700,"Stock photo",dt=0.4),chip(2,840,"Call now",dt=0.8),T(3,1060,"NOTHING TO GO ON","r",80)]},
  {"from":4,"elements":[T(4,420,"A REAL PAGE ANSWERS","y",76),check(5,560,[("What's included",True,5,0),("Rough cost",True,5,0.7),("How fast",True,5,1.4),("Towns covered",True,6,0),("How to get a quote",True,6,0.8)])]},
  {"from":7,"elements":[T(7,640,"FOR EVERY SERVICE?","w",84),T(7,800,"THE SLOW PART","r",100,0.6)]},
  {"from":8,"elements":[T(8,420,"SETTORANK WRITES","y",80),check(8,560,[("Every service page",True,8,0.5),("Every city page",True,8,1.2),("Unique, not copies",True,9,0),("FAQs + quote form",True,9,0.8)])]},
  realtalk(10),cta(11)],
 caption="A page with three sentences isn't a service page.\nA real one says what's included, roughly what it costs, how fast you come, which towns you cover and how to get a quote.\nBuild one free. Link in bio.")
E[14]=dict(slug="short_quote_form",date="2026-11-10",angle="short quote form",
 lines=["Your quote form is too long.","Name, email, phone, address, budget, start date, how did you hear about us.","Someone with a leaking roof isn't filling that out.","Keep it short.","Name. Phone. What they need. Which town.","That's enough to call them back.","Then the lead has to land somewhere you'll see it.","SetToRank puts a quote form on every site it builds.","Requests go out by email, to you or straight to the renter.","And a call button, for people who'd rather talk.",RT,CTA],
 scenes=[hook([("YOUR QUOTE FORM","dark",100),("IS","dark",104),("TOO LONG.","w",130)]),
  {"from":1,"elements":[check(1,420,[("Name",False,1,0),("Email",False,1,0.3),("Phone",False,1,0.6),("Address",False,1,0.9),("Budget",False,1,1.2),("Start date",False,1,1.5)]),T(2,1500,"NOBODY FILLS THAT OUT","r",64)]},
  {"from":3,"elements":[T(3,420,"KEEP IT SHORT","g",96),{"type":"form","at":4,"y":560,"title":"Get a quote","fields":[["Name","Dana"],["Phone","(480) 555-0142"],["Need","Roof leak"],["Town","Mesa"]],"button":"Send"}]},
  {"from":6,"elements":[T(6,560,"THEN THE LEAD","w",90),T(6,700,"HAS TO LAND","y",90,0.4),T(6,840,"SOMEWHERE","y",90,0.7)]},
  {"from":7,"elements":[T(7,420,"SETTORANK BUILDS IT IN","y",70),{"type":"flow","at":8,"y":620,"gap":200,"nodes":[{"label":"Quote form","color":"w","at":8,"dt":0},{"label":"Email","color":"y","at":8,"dt":0.5},{"label":"You or the renter","color":"g","at":8,"dt":1.0}]},chip(9,1300,"☎  Call button","g","dark",60,0)]},
  realtalk(10),cta(11)],
 caption="Your quote form is too long.\nSomeone with a leaking roof won't fill out seven fields. Name, phone, what they need, which town. Then make sure the lead lands where you'll see it.\nBuild one free. Link in bio.")
E[15]=dict(slug="slow_ranking_fast_build",date="2026-11-11",angle="ranking is slow, building shouldn't be",
 lines=["Rank and rent is slow. Building shouldn't be.","Ranking a new site takes months. Nobody can skip that.","What you can skip is the weeks of building.","Writing every service page. Every city page.","Titles, FAQs, schema, the form, the call button.","Every week spent building is a week the site isn't live.","And Google can't rank a site that doesn't exist yet.","SetToRank builds the whole site from a niche and a city.","Then publishes it to your own WordPress.","So the slow part, ranking, starts sooner.",RT,CTA],
 scenes=[hook([("RANK AND RENT","dark",104),("IS SLOW.","dark",104),("BUILDING SHOULDN'T BE.","w",90)]),
  {"from":1,"elements":[{"type":"calendar","at":1,"y":620,"labels":["M1","M2","M3"]},T(1,1000,"RANKING TAKES MONTHS","w",72,0.6),T(2,1150,"BUILDING DOESN'T HAVE TO","g",62)]},
  {"from":3,"elements":[T(3,420,"THE WEEKS OF BUILDING","r",70),check(3,560,[("Service pages",False,3,0.4),("City pages",False,3,1.0),("Titles + FAQs",False,4,0),("Schema",False,4,0.6),("Form + call button",False,4,1.2)])]},
  {"from":5,"elements":[T(5,600,"NOT LIVE YET?","w",100),T(6,780,"NOTHING","r",120),T(6,940,"TO RANK.","r",100,0.3)]},
  {"from":7,"elements":[T(7,420,"SETTORANK","y",90),{"type":"flow","at":7,"y":600,"gap":200,"nodes":[{"label":"Niche + city","color":"y","at":7,"dt":0.4},{"label":"Whole site","color":"w","at":7,"dt":1.0},{"label":"Your WordPress","color":"g","at":8,"dt":0}]},T(9,1300,"RANKING STARTS SOONER","g",64)]},
  realtalk(10),cta(11)],
 caption="Rank and rent is slow. Building shouldn't be.\nRanking a new site takes months and nobody can skip that. The weeks of building, you can. A site that isn't live can't start ranking.\nBuild one free. Link in bio.")
E[16]=dict(slug="preview_before_paying",date="2026-11-12",angle="free build + preview",
 lines=["Rank and renters: see the whole site before you pay.","You shouldn't have to pay to find out if a site is any good.","SetToRank works the other way.","Type a niche and a city.","It builds the site. Service pages, city pages, the calculator, the form.","You click through every page.","Read the copy. Check the towns. See if it fits.","Building and previewing is free.","If you like it, plans start at forty seven a month.","If it's not right, you've lost nothing.",RT,CTA],
 scenes=[hook([("SEE THE WHOLE SITE","dark",96),("BEFORE","dark",104),("YOU PAY.","w",130)]),
  {"from":1,"elements":[T(1,620,"PAY FIRST,","w",100),T(1,770,"FIND OUT LATER?","r",90,0.5),T(2,1000,"OTHER WAY AROUND.","y",80)]},
  {"from":3,"elements":[{"type":"search","at":3,"y":420,"query":"Plumbing · Mesa, AZ"},check(4,620,[("Service pages",True,4,0.3),("City pages",True,4,0.9),("Cost calculator",True,4,1.5),("Quote form",True,4,2.1)])]},
  {"from":5,"elements":[{"type":"browser","at":5,"y":420,"url":"preview.settorank.com","title":"Water Heater Repair in Mesa","button":"Get a quote"},T(6,1380,"READ IT. CHECK IT.","y",70)]},
  {"from":7,"elements":[T(7,560,"BUILD + PREVIEW","w",90),T(7,700,"FREE","g",140,0.4),T(8,900,"PLANS FROM $47/MO","y",72),T(9,1050,"NOT RIGHT? NOTHING LOST.","w",60)]},
  realtalk(10),cta(11)],
 caption="Rank and renters: see the whole site before you pay.\nType a niche and a city, then click through every page it builds. Building and previewing is free. Plans start at $47 a month if you keep it.\nBuild one free. Link in bio.")
caps={}
for n,e in E.items():
    assert len(e["lines"])==12
    job={"episode":n,"series":"RANK & RENT · BUILD FASTER","hook":e["lines"][0],"accent":[64,200,255],"voice":f"../voices/ep{n:02d}.mp3","atempo":1.08,"music_vol":0,"out":f"../out/ep{n:02d}_{e['slug']}.mp4","lines":e["lines"],"scenes":e["scenes"]}
    json.dump(job,open(f"ep{n:02d}.json","w"),indent=1)
    caps[str(n)]=e["caption"]+"\n"+TAGS
    print(n,e["date"],len(" ".join(e["lines"]).split()),"words")
json.dump(caps,open("captions_ep10-16.json","w"),indent=1)
json.dump({str(n):{k:e[k] for k in ("slug","date","angle")} for n,e in E.items()},open("meta_ep10-16.json","w"),indent=1)
