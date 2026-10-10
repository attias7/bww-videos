import re,os
H=os.path.dirname(os.path.abspath(__file__)); W=os.path.join(H,'..')
s=open(os.path.join(W,'pause-decide-test.html')).read()
more="var QS2={};\n"+"\n".join(open(os.path.join(W,f'more_{p}.js')).read() for p in ['striker','winger','ten','mid','def'])
more+="\n['striker','winger','ten','mid','def'].forEach(function(k){QS[k]=QS[k].concat(QS2[k]||[])});\n"
more+="Object.assign(CATS,{press:'Pressing',counter:'Counter-attacks',setp:'Set pieces',offside:'Timing & the offside line',screen:'Screening & protecting',foul:'Tactical fouls',stepout:'Stepping out of the line',fbpos:'Full-back positioning',carry:'Carrying the ball'});\n"
s=s.replace("var Q=[];",more+"var Q=[];",1)
# intro
a=s.index('<section id="ust-intro">'); b=s.index('</section>',a)+10
s=s[:a]+'''<section id="ust-intro">
  <div class="pill"><b>PAUSE &amp; DECIDE · 100 SITUATIONS</b>&nbsp;&nbsp;Your copy</div>
  <h1>100 real match moments.<br><span>Train your eye every day.</span></h1>
  <p class="lead">20 situations for every position, drawn to scale on a real pitch. Read the picture, pick in 15 seconds, then see the pro pick and why. Play a quick 10 each day or all 20 for your position. Your best scores are saved on this device.</p>
  <div class="card" style="margin-top:26px">
    <p style="font-weight:800;color:#fff">Choose a position</p>
    <div class="pos" id="ust-pos">
      <button data-p="striker">Striker</button><button data-p="winger">Winger</button><button data-p="ten">No. 10</button><button data-p="mid">Midfielder</button><button data-p="def">Defender</button>
    </div>
    <div class="row"><button class="btn" id="ust-start" disabled>Quick 10 →</button><button class="btn ghost" id="ust-all" disabled>Play all 20</button></div>
    <p class="small" id="ust-best" style="margin-top:12px"></p>
  </div>
</section>'''+s[b:]
# results: drop offer block
a=s.index('<div class="offer">'); b=s.index('<div class="row"><button class="btn ghost" id="ust-again">')
s=s[:a]+s[b:]
s=re.sub(r'<a class="btn ghost" href="/wp-content/uploads/2026/10/Unscouted-Free-Test-[^"]+" download>Printable analysis test \(PDF\)</a>','<button class="btn ghost" id="ust-other">Try another position</button>',s)
# start logic
s=s.replace("$('start').onclick=function(){Q=QS[pos]||QS.mid;","var MODE=10;function pick(){var a=(QS[pos]||QS.mid).slice();for(var x=a.length-1;x>0;x--){var r=Math.floor(Math.random()*(x+1));var t=a[x];a[x]=a[r];a[r]=t}return a.slice(0,MODE)}\nfunction bestTxt(){try{var b=JSON.parse(localStorage.getItem('us_best')||'{}');var k=Object.keys(b);if(!k.length)return '';return 'Best scores: '+k.map(function(p){return ({striker:'Striker',winger:'Winger',ten:'No. 10',mid:'Midfielder',def:'Defender'})[p]+' '+b[p]}).join(' · ')}catch(e){return ''}}\n$('best').textContent=bestTxt();\nvar ALL=0;$('all').onclick=function(){ALL=1;$('start').onclick()};\n$('start').onclick=function(){MODE=ALL?20:10;ALL=0;Q=pick();")
s=s.replace("$('again').onclick=function(){Q=QS[pos]||QS.mid;","$('again').onclick=function(){Q=pick();")
s=s.replace("b.classList.add('on');pos=b.getAttribute('data-p');$('start').disabled=false","b.classList.add('on');pos=b.getAttribute('data-p');$('start').disabled=false;$('all').disabled=false")
# save best + other button in finish
s=s.replace("$('prog').style.width='100%';","$('prog').style.width='100%';try{var bb=JSON.parse(localStorage.getItem('us_best')||'{}');var sc=pts+'/'+Q.length;var cur=bb[pos];if(!cur||pts/Q.length>parseInt(cur)/parseInt(cur.split('/')[1]))bb[pos]=sc;localStorage.setItem('us_best',JSON.stringify(bb))}catch(e){}var ot=$('other');if(ot)ot.onclick=function(){$('res').classList.add('hide');$('intro').classList.remove('hide');$('best').textContent=bestTxt();document.getElementById('ust').scrollIntoView({behavior:'smooth'})};")
s=s.replace("var t=pts>=8?","var R=pts/Q.length;var t=R>=1?").replace(":pts>=6?['Player eyes",":R>=0.75?['Player eyes")
s=s.replace("8 moments is a quick check, not a scout's verdict.","Play again tomorrow: the situations come in a different order every time.")
s=s.replace("$('pts').innerHTML=pts+'<span>/'+Q.length+'</span>';","$('pts').innerHTML=pts+'<span>/'+Q.length+'</span>';")
s=s.replace("$('packtip')","($('packtip')||{})")
open(os.path.join(W,'pause-decide-100.html'),'w').write(s)
print('&&' in s, s.count('QS2'), len(s))
