function media(t,e,a){setCss(t,a,!0);let i=document.createElement("source");for(let l in t.innerHTML="",i.setAttribute("src",e.path+"/"+e.video),a)"autoplay"===l?t.autoplay=a.autoplay:i.setAttribute(l,a[l]);t.appendChild(i)}