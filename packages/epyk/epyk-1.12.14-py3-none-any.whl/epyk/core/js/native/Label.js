function label(c,b,a){b=getDataFromTemplate(b,a);if(typeof b!=="undefined"){if(a.showdown){var e=new showdown.Converter(a.showdown);var d=e.makeHtml(b).replace(/<\/?p[^>]*>/ig,'');}else{var d=b;};if(a._children>0){c.insertAdjacentHTML('beforeend','<div style="display:inline-block;vertical-align:middle">'+d+'</div>');}else{c.innerHTML=d;};setCss(c,a);}}