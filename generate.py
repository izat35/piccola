import json

with open('pizzeria-piccola.json', 'r', encoding='utf-8') as f:
    raw_json = f.read()

HTML = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@400;600;700;800&family=Playfair+Display:ital,wght@0,600;0,800;1,600&display=swap" rel="stylesheet">
<title>Pizzeria Piccola — Speisekarte</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#07070f;--surface:#0f0f1c;--border:#232334;
  --t1:#f0ede6;--t2:#9a9494;--t3:#52505a;
  --gold:#e8b84b;--gold-dim:#c49a35;--red:#e74c3c;
}
html,body{
  width:1920px;height:1080px;overflow:hidden;
  background:radial-gradient(circle at 10% 90%, #15151c 0%, #060608 100%);color:var(--t1);
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  -webkit-font-smoothing:antialiased;
}
#app{width:1920px;height:1080px;display:flex;flex-direction:column;overflow:hidden}

/* HEADER */
#header{
  height:72px;flex-shrink:0;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 48px;
  background:linear-gradient(90deg,#09091a 0%,#0f0f1c 100%);
  border-bottom:1px solid rgba(232,184,75,.28);
  position:relative;
}
#header::after{
  content:'';position:absolute;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold-dim),transparent);
}
.logo{display:flex;align-items:center;gap:16px}
.logo-icon{height:48px;width:auto;object-fit:contain;filter:drop-shadow(0 0 10px rgba(232,184,75,0.3))}
.logo-text{
  font-size:2.4rem;font-weight:600;color:var(--gold);
  letter-spacing:.02em;font-family:'Playfair Display',Georgia,serif;
  text-shadow:0 0 20px rgba(232,184,75,0.4);
}
.logo-tagline{font-size:.72rem;color:var(--t3);letter-spacing:.22em;text-transform:uppercase;margin-top:3px}
.hdr-right{display:flex;align-items:center;gap:28px}
#section-label{
  font-size:.88rem;color:var(--t2);letter-spacing:.1em;text-transform:uppercase;
  opacity:0;transition:opacity .5s;
}
#section-label.vis{opacity:1}
#clock{
  font-size:1.75rem;font-weight:300;color:var(--t2);
  letter-spacing:.1em;font-variant-numeric:tabular-nums;
}

/* SLIDES */
#slides-wrap{flex:1;position:relative;overflow:hidden}
.slide{
  position:absolute;inset:0;display:flex;
  opacity:0;transition:opacity .9s cubic-bezier(.4,0,.2,1);
  pointer-events:none;
}
.slide.active{opacity:1;pointer-events:auto}

/* CATEGORY BANNER */
.cat-banner{
  width:400px;flex-shrink:0;
  display:flex;flex-direction:column;justify-content:center;align-items:center;
  padding:32px 24px;text-align:center;
  position:relative;overflow:hidden;
  margin:40px 0 40px 40px;
  border-radius:40px;
  box-shadow:0 30px 60px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.1);
  border:1px solid rgba(255,255,255,0.04);
  background:linear-gradient(135deg, rgba(255,255,255,0.03), transparent);
}
.cat-banner::before{
  content:'';position:absolute;inset:0;z-index:0;
  background:var(--cat-bg);
  opacity:0.25;backdrop-filter:blur(50px);
}
.cat-banner::after{
  content:'';position:absolute;inset:0;z-index:1;
  background:linear-gradient(180deg,transparent 0%,rgba(0,0,0,.15) 35%,rgba(0,0,0,.75) 100%);
}
.cat-sep{ display:none; }
.cat-content{
  position:relative;z-index:2;
  display:flex;flex-direction:column;align-items:center;gap:10px;width:100%;
}
.cat-img{
  width:220px;height:220px;object-fit:cover;
  border-radius:50%;box-shadow:0 15px 40px rgba(0,0,0,0.8);
  border:3px solid rgba(255,255,255,0.25);
  margin-bottom:20px;
}
.cat-name{
  font-size:3.3rem;font-weight:600;color:#fff;line-height:1.1;
  text-shadow:0 4px 30px rgba(0,0,0,0.9);
  font-family:'Playfair Display',Georgia,serif;
  letter-spacing:0.03em;font-style:italic;
  margin-bottom:12px;
}
.cat-desc{
  font-size:.88rem;color:rgba(255,255,255,.85);font-weight:400;
  line-height:1.5;max-width:290px;text-shadow:0 2px 8px rgba(0,0,0,.8);
}
.cat-meta{margin-top:6px;display:flex;flex-direction:column;align-items:center;gap:6px}
.page-badge{
  background:rgba(0,0,0,.45);border:1px solid rgba(255,255,255,.18);
  border-radius:20px;padding:4px 16px;
  font-size:.73rem;color:rgba(255,255,255,.7);letter-spacing:.08em;
}
.deal-tag{
  background:var(--red);color:#fff;border-radius:4px;
  padding:3px 14px;font-size:.72rem;font-weight:700;
  letter-spacing:.12em;text-transform:uppercase;
}

/* MENU GRID */
.menu-grid{
  flex:1;padding:32px 48px;
  display:grid;gap:20px;align-content:center;
}

/* CARD */
.menu-card{
  background:rgba(20,20,30,0.2);
  backdrop-filter:blur(35px);
  -webkit-backdrop-filter:blur(35px);
  border:1px solid rgba(255,255,255,0.03);
  border-top:1px solid rgba(255,255,255,0.15);
  border-radius:20px;padding:24px 28px;
  box-shadow:0 20px 50px rgba(0,0,0,0.5);
  display:flex;flex-direction:column;justify-content:space-between;
  overflow:hidden;position:relative;
  opacity:0;animation:cardIn .7s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}
@keyframes cardIn{
  from{opacity:0;transform:translateY(20px) scale(0.96)}
  to{opacity:1;transform:translateY(0) scale(1)}
}
.menu-card::before{
  content:'';position:absolute;left:-40px;top:-40px;
  width:100px;height:100px;border-radius:50%;
  background:var(--cc,var(--gold));
  filter:blur(40px); opacity:0.4; z-index:0; pointer-events:none;
}
.menu-card.is-deal{
  border:1px solid rgba(231,76,60,.4);
  border-top:1px solid rgba(231,76,60,.6);
  background:linear-gradient(135deg,rgba(40,10,10,0.4),rgba(15,15,25,0.2));
}
.card-top, .card-bottom { position:relative; z-index:2; }
.card-num{
  position:absolute;top:12px;right:16px;z-index:2;
  font-size:.7rem;color:var(--t3);font-weight:600;letter-spacing:.04em;
}
.card-top{flex:1;padding-left:4px}
.card-name{
  font-size:1.45rem;font-weight:600;color:#fff;line-height:1.2;
  margin-bottom:12px;padding-right:24px;font-family:'Playfair Display',Georgia,serif;
  letter-spacing:0.02em;text-shadow:0 2px 10px rgba(0,0,0,0.5);
}
.card-desc{
  font-size:.85rem;color:#d0ceda;line-height:1.55;font-weight:300;
  display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;
}
.card-bottom{padding-left:4px;margin-top:12px}
.price-single{
  font-size:1.7rem;font-weight:800;letter-spacing:.03em;
  font-family:'Outfit',sans-serif;
  background:linear-gradient(135deg, #fceda1 0%, #cfa83c 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  filter:drop-shadow(0 4px 12px rgba(232,184,75,0.25));
  display:inline-block;
}
.price-single::after{content:' €';font-size:.88em;font-weight:700;}
.price-sizes{display:flex;gap:6px;flex-wrap:wrap}
.ppill{
  display:flex;align-items:center;gap:6px;
  background:linear-gradient(180deg,rgba(232,184,75,.1) 0%,rgba(232,184,75,.02) 100%);
  border:1px solid rgba(232,184,75,.25);
  border-radius:8px;padding:3px 10px;
}
.ppill-lbl{font-size:.65rem;color:var(--t2);text-transform:uppercase;letter-spacing:.06em;}
.ppill-val{font-size:1.0rem;font-weight:700;color:#ffe175;font-family:'Outfit',sans-serif;}
.ppill-val::after{content:' €';font-size:.74em;font-weight:600;opacity:0.8;}
.menu-card.is-deal .card-name{font-size:1.4rem}
.menu-card.is-deal .price-single{font-size:2.0rem}
.menu-card.is-deal .card-desc{-webkit-line-clamp:5;font-size:.85rem}

/* FOOTER */
#footer{flex-shrink:0}
#prog-track{height:3px;background:rgba(255,255,255,.05);overflow:hidden}
#prog-fill{height:100%;width:0;background:var(--gold)}
#dot-row{
  height:26px;display:flex;align-items:center;justify-content:center;
  gap:5px;background:rgba(0,0,0,.4);
}
.dot{width:5px;height:5px;border-radius:50%;background:rgba(255,255,255,.15);transition:all .3s;flex-shrink:0}
.dot.cur{background:var(--gold);width:16px;border-radius:3px}
.dot.sec{background:rgba(232,184,75,.32)}

/* BACKGROUND FX */
#header, #slides-wrap, #footer { position:relative; z-index:10; }
#bg-fx { position:absolute; inset:0; z-index:0; pointer-events:none; overflow:hidden; }
.fire {
  position:absolute; bottom:-50px; left:0; right:0; height:180px;
  background:radial-gradient(ellipse at bottom,rgba(231,76,60,.4) 0%,rgba(200,50,20,.15) 50%,transparent 70%);
  filter:blur(20px); mix-blend-mode:screen; animation:flicker 3s infinite alternate ease-in-out;
}
.fire-2 {
  position:absolute; bottom:-30px; left:15%; right:15%; height:120px;
  background:radial-gradient(ellipse at bottom,rgba(250,150,0,.35) 0%,rgba(230,80,0,.15) 50%,transparent 80%);
  filter:blur(15px); mix-blend-mode:screen; animation:flicker 4s infinite alternate-reverse ease-in-out;
}
@keyframes flicker {
  0%{transform:translateY(0) scaleY(1); opacity:.8}
  50%{transform:translateY(-15px) scaleY(1.1); opacity:1}
  100%{transform:translateY(5px) scaleY(.95); opacity:.7}
}
.steam {
  position:absolute; bottom:0; border-radius:50%; background:rgba(255,255,255,.03);
  filter:blur(25px); animation:rise 8s infinite linear;
}
.steam:nth-child(3){left:20%; width:300px; height:300px; animation-duration:11s; animation-delay:1s}
.steam:nth-child(4){left:50%; width:250px; height:250px; animation-duration:14s; animation-delay:0s}
.steam:nth-child(5){left:80%; width:350px; height:350px; animation-duration:12s; animation-delay:4s}
@keyframes rise {
  0%{transform:translateY(150px) scale(1); opacity:0}
  20%{opacity:.45} 80%{opacity:.3}
  100%{transform:translateY(-1000px) scale(2); opacity:0}
}

/* LED STRIPS */
.led-strip {
  position: absolute;
  z-index: 9999;
  border-radius: 4px;
}
.led-strip::after {
  content: '';
  position: absolute;
  background: inherit;
  filter: blur(16px);
  opacity: 0.85;
  z-index: -1;
}
.led-strip.vertical {
  top: 0;
  bottom: 0;
  width: 6px;
  background: linear-gradient(to bottom, #00c950 0%, #00c950 33.33%, #ffffff 33.33%, #ffffff 66.66%, #ff3333 66.66%, #ff3333 100%);
}
.led-strip.vertical::after {
  top: 0;
  bottom: 0;
  left: -10px;
  right: -10px;
}
.led-strip.horizontal {
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(to right, #00c950 0%, #00c950 33.33%, #ffffff 33.33%, #ffffff 66.66%, #ff3333 66.66%, #ff3333 100%);
}
.led-strip.horizontal::after {
  left: 0;
  right: 0;
  top: -10px;
  bottom: -10px;
}
.led-strip.left { left: 0; }
.led-strip.right { right: 0; }
.led-strip.top { top: 0; }
.led-strip.bottom { bottom: 0; }

/* F8 EDITOR */
#price-editor {
  position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:99999;
  display:none; flex-direction:column; align-items:center; justify-content:center;
  backdrop-filter:blur(20px); font-family:'Inter',sans-serif; color:#fff;
}
#price-editor.show { display:flex; }
.pe-box {
  background:#151520; border:1px solid #333; border-radius:12px;
  width:800px; max-height:80vh; display:flex; flex-direction:column;
  box-shadow:0 20px 60px rgba(0,0,0,0.8);
}
.pe-hdr {
  padding:20px; border-bottom:1px solid #333; display:flex; justify-content:space-between; align-items:center;
  background:linear-gradient(90deg,#111,#1a1a2e); border-radius:12px 12px 0 0;
}
.pe-hdr h2 { font-size:1.4rem; color:var(--gold); margin:0; }
.pe-close { cursor:pointer; background:none; border:none; color:#999; font-size:1.5rem; }
.pe-close:hover { color:#fff; }
.pe-body {
  padding:20px; overflow-y:auto; flex:1; display:flex; flex-direction:column; gap:16px;
}
.pe-item {
  background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:12px 16px;
  border-radius:8px; display:flex; flex-direction:column; gap:8px;
}
.pe-item-hdr { display:flex; justify-content:space-between; font-weight:600; font-size:1.1rem; }
.pe-item-sec { font-size:0.8rem; color:var(--gold); }
.pe-sizes { display:flex; gap:12px; flex-wrap:wrap; }
.pe-size { display:flex; align-items:center; gap:8px; background:rgba(0,0,0,0.4); padding:6px 10px; border-radius:6px; }
.pe-size label { font-size:0.8rem; color:#aaa; width:60px;}
.pe-size input { 
  background:#222; border:1px solid #444; color:#fff; padding:6px; border-radius:4px;
  width:80px; font-family:monospace; font-size:1rem;
}
.pe-size input:focus { outline:none; border-color:var(--gold); }
.pe-ftr {
  padding:20px; border-top:1px solid #333; display:flex; justify-content:flex-end; gap:12px;
  background:rgba(0,0,0,0.2); border-radius:0 0 12px 12px;
}
.pe-btn {
  padding:10px 24px; border:none; border-radius:6px; font-size:1rem; font-weight:600; cursor:pointer;
}
.pe-btn-cancel { background:#333; color:#fff; }
.pe-btn-cancel:hover { background:#444; }
.pe-btn-save { background:var(--gold); color:#000; }
.pe-btn-save:hover { filter:brightness(1.1); }
</style>
</head>
<body>
<div id="app">
  <div class="led-strip vertical left"></div>
  <div class="led-strip vertical right"></div>
  <div class="led-strip horizontal top"></div>
  <div class="led-strip horizontal bottom"></div>
  <div id="bg-fx">
    <div class="fire"></div><div class="fire-2"></div>
    <div class="steam"></div><div class="steam"></div><div class="steam"></div>
  </div>
  <header id="header">
    <div class="logo">
      <img src="logo.png" class="logo-icon" alt="Logo">
      <div>
        <div class="logo-text">Pizzeria Piccola</div>
        <div class="logo-tagline">Ristorante · Pizzeria · Lieferservice</div>
      </div>
    </div>
    <div class="hdr-right">
      <div id="section-label"></div>
      <div id="clock">00:00</div>
    </div>
  </header>
  <main id="slides-wrap"></main>
  <footer id="footer">
    <div id="prog-track"><div id="prog-fill"></div></div>
    <div id="dot-row"></div>
  </footer>

  <div id="price-editor">
    <div class="pe-box">
      <div class="pe-hdr">
        <h2>Preis-Editor</h2>
        <button class="pe-close" onclick="closeEditor()">&times;</button>
      </div>
      <div class="pe-body" id="pe-list"></div>
      <div class="pe-ftr">
        <button class="pe-btn pe-btn-cancel" onclick="closeEditor()">Abbrechen</button>
        <button class="pe-btn pe-btn-save" onclick="saveEditor()">Speichern & Download</button>
      </div>
    </div>
  </div>
</div>
<script>
const DATA=JSONPLACEHOLDER;

const CAT={
  'Pizza':           {e:'img/pizza.png',c:'#e74c3c',g:'linear-gradient(155deg,#5c0a00,#a31515,#c0392b)'},
  'Burger':          {e:'img/burger.png',c:'#e67e22',g:'linear-gradient(155deg,#3d1500,#8a3a00,#c0550a)'},
  'Salat':           {e:'img/salat.png',c:'#27ae60',g:'linear-gradient(155deg,#021f0a,#0d5c26,#1e8449)'},
  'Spaghetti':       {e:'img/spaghetti.png',c:'#f1c40f',g:'linear-gradient(155deg,#2a1f00,#7a5a00,#b08000)'},
  'Taschennudeln':   {e:'img/taschennudeln.png',c:'#e2b714',g:'linear-gradient(155deg,#241900,#6b4d00,#9c6e00)'},
  'Bandnudeln':      {e:'img/bandnudeln.png',c:'#d4ac0d',g:'linear-gradient(155deg,#1e1500,#5c4200,#8a6200)'},
  'Rohrnudeln':      {e:'img/rohrnudeln.png',c:'#c9a227',g:'linear-gradient(155deg,#1a1200,#543e00,#7d5c00)'},
  'Kartoffelnudel':  {e:'img/kartoffelnudel.png',c:'#ca8a04',g:'linear-gradient(155deg,#1c1000,#5c3600,#8b5200)'},
  'Pasta al Forno':  {e:'img/pasta_al_forno.png',c:'#e05c2a',g:'linear-gradient(155deg,#1a0500,#6b1c00,#9c2800)'},
  'Verdura al forno':{e:'img/verdura_al_forno.png',c:'#2ecc71',g:'linear-gradient(155deg,#011a08,#055c22,#0a8c35)'},
  'Putenschnitzel':  {e:'img/putenschnitzel.png',c:'#c0392b',g:'linear-gradient(155deg,#200305,#6b0c0c,#a01010)'},
  'Beilagen':        {e:'img/beilagen.png',c:'#f39c12',g:'linear-gradient(155deg,#1a0f00,#6b4200,#a06000)'},
  'Omelette':        {e:'img/omelette.png',c:'#f1c40f',g:'linear-gradient(155deg,#1a1500,#6b5500,#9c7a00)'},
  'Pizzabrötchen':{e:'img/pizzabrotchen.png',c:'#e67e22',g:'linear-gradient(155deg,#1a0d00,#6b3200,#a04a00)'},
  'Baguettes':       {e:'img/baguettes.png',c:'#d4830a',g:'linear-gradient(155deg,#1a0e00,#6b3800,#a05200)'},
  'Getränke':   {e:'img/getranke.png',c:'#3498db',g:'linear-gradient(155deg,#001426,#053d7a,#0a5aaf)'},
  'Angebote':        {e:'img/angebote.png',c:'#e74c3c',g:'linear-gradient(155deg,#1a0000,#7a0000,#b00000)'},
};
const DCAT={e:'img/pizza.png',c:'#e8b84b',g:'linear-gradient(155deg,#0a0806,#2a2010,#3a2e10)'};

const SZ={'24cm':'24cm','30cm':'30cm','40cm':'40cm','stand':'','dose':'Dose','1,0 l':'1,0 l','6 Stücke':'6 St.','12 Stücke':'12 St.'};

function getLayout(sec,n){
  if(sec==='Angebote') {
    if(n<=2) return {cols:2,rows:1,pp:2};
    if(n<=4) return {cols:2,rows:2,pp:4};
    return {cols:3,rows:2,pp:6};
  }
  if(n===1)            return{cols:1,rows:1,pp:1};
  if(n<=4)             return{cols:2,rows:2,pp:4};
  if(n<=6)             return{cols:3,rows:2,pp:6};
  if(n<=9)             return{cols:3,rows:3,pp:9};
  if(n<=12)            return{cols:4,rows:3,pp:12};
                       return{cols:4,rows:4,pp:16};
}

function priceHtml(price){
  const ents=Object.entries(price||{}).filter(([,v])=>v&&v!=='0,00');
  if(!ents.length) return '';
  if(ents.length===1) return '<span class="price-single">'+ents[0][1]+'<\\/span>';
  return '<div class="price-sizes">'+ents.map(([k,v])=>{
    const lbl=SZ[k]!==undefined?SZ[k]:k;
    return '<span class="ppill">'+(lbl?'<span class="ppill-lbl">'+lbl+'<\\/span>':'')+'<span class="ppill-val">'+v+'<\\/span><\\/span>';
  }).join('')+'<\\/div>';
}

function buildSlides(){
  const mdesc=DATA.sections.mdesc;
  const prods=DATA.product;
  const grp={};
  Object.entries(prods).forEach(([id,item])=>{
    const s=item.section;if(!grp[s])grp[s]=[];
    grp[s].push({id:+id,...item});
  });
  Object.values(grp).forEach(a=>a.sort((a,b)=>a.id-b.id));
  const slides=[];
  Object.keys(mdesc).forEach(sec=>{
    const items=grp[sec];if(!items||!items.length)return;
    const info=mdesc[sec];const st=CAT[sec]||DCAT;
    const{cols,rows,pp}=getLayout(sec,items.length);
    const tp=Math.ceil(items.length/pp);
    for(let p=0;p<tp;p++){
      slides.push({sec,info,st,items:items.slice(p*pp,(p+1)*pp),page:p+1,tp,cols,rows,deal:sec==='Angebote'});
    }
  });
  return slides;
}

let slides=[],cur=0,slideTimer;
function getDur(idx) {
  const itemCnt = slides[idx]?.items?.length || 1;
  return 5000 + (itemCnt * 1000); // 5 seconds base + 1 second per item
}

function render(){
  const wrap=document.getElementById('slides-wrap');
  const dotRow=document.getElementById('dot-row');
  slides.forEach((sl)=>{
    const el=document.createElement('div');
    el.className='slide';
    // banner
    const ban=document.createElement('div');
    ban.className='cat-banner';
    ban.style.setProperty('--cat-bg', sl.st.g);
    ban.innerHTML='<div class="cat-sep"></div><div class="cat-content"><img src="'+sl.st.e+'" class="cat-img" alt="'+sl.sec+'"><div class="cat-name">'+sl.sec+'</div>'+(sl.info.des?'<div class="cat-desc">'+sl.info.des+'</div>':'')+'<div class="cat-meta">'+(sl.tp>1?'<div class="page-badge">'+sl.page+' / '+sl.tp+'</div>':'')+(sl.deal?'<div class="deal-tag">🔥 Angebot</div>':'')+'</div></div>';
    // grid
    const grid=document.createElement('div');
    grid.className='menu-grid';
    grid.style.gridTemplateColumns='repeat('+sl.cols+',1fr)';
    grid.style.gridTemplateRows='repeat('+sl.rows+',1fr)';
    sl.items.forEach((item,i)=>{
      const card=document.createElement('div');
      card.className='menu-card'+(sl.deal?' is-deal':'');
      card.style.setProperty('--cc',sl.st.c);
      card.style.animationDelay=(i*45)+'ms';
      card.innerHTML='<div class="card-num">'+item.id+'<\\/div><div class="card-top"><div class="card-name">'+item.name+'<\\/div>'+(item.desO?'<div class="card-desc">'+item.desO+'<\\/div>':'')+'<\\/div><div class="card-bottom">'+priceHtml(item.price)+'<\\/div>';
      grid.appendChild(card);
    });
    el.appendChild(ban);el.appendChild(grid);wrap.appendChild(el);
    // dot
    const dot=document.createElement('div');dot.className='dot';dotRow.appendChild(dot);
  });
}

function goTo(idx){
  clearTimeout(slideTimer);
  const els=document.querySelectorAll('.slide');
  const dots=document.querySelectorAll('.dot');
  els[cur]?.classList.remove('active');dots[cur]?.classList.remove('cur');
  cur=(idx+els.length)%els.length;
  els[cur]?.classList.add('active');
  const cs=slides[cur]?.sec;
  dots.forEach((d,i)=>{
    d.classList.remove('cur','sec');
    if(i===cur)d.classList.add('cur');
    else if(slides[i]?.sec===cs)d.classList.add('sec');
  });
  const lbl=document.getElementById('section-label');
  lbl.textContent=cs||'';lbl.classList.add('vis');
  const fill=document.getElementById('prog-fill');
  fill.style.transition='none';fill.style.width='0%';
  const currentDur = getDur(cur);
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    fill.style.transition='width '+currentDur+'ms linear';
    fill.style.width='100%';
  }));
  slideTimer = setTimeout(()=>goTo(cur+1), currentDur);
}

function startClock(){
  function upd(){
    const n=new Date();
    document.getElementById('clock').textContent=String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0');
  }
  upd();setInterval(upd,10000);
}

slides=buildSlides();render();goTo(0);
startClock();

// --- F8 EDITOR LOGIC ---
const editorModal = document.getElementById('price-editor');
const editorList = document.getElementById('pe-list');

document.addEventListener('keydown', (e) => {
  if (e.key === 'F8') {
    e.preventDefault();
    if (editorModal.classList.contains('show')) closeEditor();
    else openEditor();
  } else if (e.key === 'ArrowRight') {
    goTo(cur+1);
  } else if (e.key === 'ArrowLeft') {
    goTo(cur-1);
  }
});

function openEditor() {
  editorModal.classList.add('show');
  editorList.innerHTML = '';
  const prods = DATA.product;
  
  const grp = {};
  Object.keys(prods).forEach(id => {
    const item = prods[id];
    if(!grp[item.section]) grp[item.section] = [];
    grp[item.section].push({id: id, ...item});
  });
  
  Object.keys(grp).sort().forEach(sec => {
    grp[sec].forEach(item => {
      if(!item.price) return;
      const ents = Object.entries(item.price);
      if(!ents.length) return;
      
      const el = document.createElement('div');
      el.className = 'pe-item';
      
      let sizesHtml = '';
      ents.forEach(([size, price]) => {
         sizesHtml += '<div class="pe-size">' +
           '<label>' + size + '</label>' +
           '<input type="text" data-id="' + item.id + '" data-size="' + size + '" value="' + price + '">' +
         '</div>';
      });
      
      el.innerHTML = '<div class="pe-item-hdr">' +
          '<span>' + item.name + ' <span style="font-weight:400;color:#aaa;font-size:0.9rem">#' + item.id + '</span></span>' +
          '<span class="pe-item-sec">' + item.section + '</span>' +
        '</div>' +
        '<div class="pe-sizes">' + sizesHtml + '</div>';
      
      editorList.appendChild(el);
    });
  });
}

function closeEditor() {
  editorModal.classList.remove('show');
}

function saveEditor() {
  const inputs = editorModal.querySelectorAll('input');
  inputs.forEach(inp => {
    const id = inp.getAttribute('data-id');
    const size = inp.getAttribute('data-size');
    const val = inp.value;
    
    if(DATA.product[id] && DATA.product[id].price) {
       DATA.product[id].price[size] = val;
    }
    if(DATA.product[id] && DATA.product[id].priceV2 && DATA.product[id].priceV2[size]) {
       const len = DATA.product[id].priceV2[size].length;
       DATA.product[id].priceV2[size] = Array(len).fill(val);
    }
  });
  
  const jsonStr = JSON.stringify(DATA);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'pizzeria-piccola.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  
  alert('Datei "pizzeria-piccola.json" wurde heruntergeladen! Bitte ersetze die alte Datei im Projektordner und fuehre "python generate.py" aus.');
  closeEditor();
}
</script>
</body>
</html>"""

final = HTML.replace('JSONPLACEHOLDER', raw_json)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final)

print(f"Done! {len(final)//1024} KB")
