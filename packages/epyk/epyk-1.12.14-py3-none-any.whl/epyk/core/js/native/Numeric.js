function numeric(c,b,a){b=getDataFromTemplate(b,a);setCss(c,a,true);if(a.type_number=='money'){if((a.templateMode=='loading')||(a.templateMode=='error')){c.querySelector('font').innerHTML=b;}else{c.querySelector('font').innerHTML=accounting.formatMoney(b,a.symbol,a.digits,a.thousand_sep,a.decimal_sep,a.format);}}else{if((a.templateMode=='loading')||(a.templateMode=='error')){c.querySelector('font').innerHTML=b;}else{c.querySelector('font').innerHTML=accounting.formatNumber(b,a.digits,a.thousand_sep,a.decimal_sep);}}}