function imgCarousel(a,c,b){c.forEach(function(e,h){var c=document.createElement('li');if(h==0){c.style.display='block';}else{c.style.display='none';};var g=document.createElement('img');g.src=e.path+'/'+e.image;c.appendChild(g);var f=document.createElement('h3');f.innerHTML=e.title;c.appendChild(f);a.appendChild(c);var d=document.createElement('label');d.style.backgroundColor=b.color;d.style.borderRadius='20px';d.for=h;d.innerHTML='&nbsp;';document.getElementById(a.id+'_bullets').appendChild(d);});}