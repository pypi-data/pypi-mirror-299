function itemLink(g,a,h){var c=document.createElement("div");var b=document.createElement("a");if(typeof a!=="object"){a={text:a};};c.classList.add("html-item-link");b.setAttribute('name','value');b.setAttribute('data-valid',false);b.innerHTML=a.text;if(typeof a.url!=='undefined'){b.href=a.url;}else{b.href='#';};if(typeof a.target!=="undefined"){b.target=a.target;}if(typeof a.icon!=='undefined'){var e=document.createElement("i");e.setAttribute("class",a.icon);e.classList.add("html-item-link-icon");c.appendChild(e);};c.appendChild(b);if(typeof a.dsc!=="undefined"){var d=document.createElement("div");d.classList.add("html-item-link-dsc");d.innerHTML=a.dsc;c.appendChild(d);};if(typeof a.image!=="undefined"){var f=document.createElement("img");d.classList.add("html-item-link-image");f.setAttribute('src',a.image);b.prepend(f);};g.appendChild(c);}