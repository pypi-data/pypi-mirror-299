function checkButton(e,t,i){if(e.innerHTML="",!0===t||"Y"==t){var a=document.createElement("i");a.classList.add(...i.icon_check.split(" ")),a.style.color=i.green,a.style.marginBottom="2px",a.style.marginLeft="2px",e.appendChild(a),e.parentNode.setAttribute("data-isChecked",!0)}else{var a=document.createElement("i");a.classList.add(...i.icon_not_check.split(" ")),a.style.color=i.red,a.style.marginBottom="2px",a.style.marginLeft="2px",e.appendChild(a),e.parentNode.setAttribute("data-isChecked",!1)}}