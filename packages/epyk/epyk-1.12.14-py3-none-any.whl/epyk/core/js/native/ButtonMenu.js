function buttonMenu(c,s,l){var n=c.querySelector("div");s.forEach(function(c){var s=document.createElement("a");s.innerHTML=c,Object.keys(l.css_child).forEach(function(c){s.style[c]=l.css_child[c]}),null!=l.css_cls_child&&s.classList.add(...l.css_cls_child.split(" ")),n.appendChild(s)})}