function skillBars(e,t,l){var i=e.querySelector("table");i.innerHTML="";var d=document.createElement("thead"),a=document.createElement("tbody");a.style["box-sizing"]="border-box",i.appendChild(d),i.appendChild(a),t.forEach(function(e,t){if(void 0!==e.tooltip&&e.tooltip,void 0!==e.url){var i=document.createElement("a");i.href=e.url}else var i=document.createElement("span");i.innerHTML=e[l.value].toFixed(l.digits)+"%",i.style.whiteSpace="nowrap";var d=document.createElement("tr");d.style.width=l.width+"px",d.title="";var r=document.createElement("td");r.style.textAlign="right",r.style.padding="0 5px";var n=document.createElement("span");n.innerHTML=e[l.label],r.appendChild(n),d.appendChild(r);var s=document.createElement("td");s.style["box-sizing"]="border-box",s.style.width="100%";var o=document.createElement("div");if(o.style.width=e[l.value].toFixed(l.digits)+"%",e[l.value].toFixed(l.digits)>l.thresholds[1]?o.style.backgroundColor=l.success:e[l.value].toFixed(l.digits)>l.thresholds[0]?o.style.backgroundColor=l.warning:o.style.backgroundColor=l.danger,o.style.fontSize="10px",o.style.lineHeight=l.height??"20px",o.style.verticalAlign="middle%",o.style.display="block",o.style.paddingLeft="5px",l&&void 0!==l.css)for(var p in l.css)o.style[p]=l.css[p];l.percentage?o.appendChild(i):(o.innerHTML="&nbsp;",o.title=e[l.value].toFixed(l.digits)+"%"),s.appendChild(o),d.appendChild(s),a.appendChild(d)})}