function chat(e,t,n){let r=document.createElement("p");setCss(e,n,!0),r.style.margin="0 0 5px 0",r.innerHTML=getHtmlData(t,n),e.querySelector("div").prepend(r);var l=new Date,i=moment(l).format("YYYY-MM-DD HH:mm:ss"),a=document.createElement("p");a.style.margin=0,a.style.fontWeight="bold",a.innerHTML=i,e.querySelector("div").prepend(a)}