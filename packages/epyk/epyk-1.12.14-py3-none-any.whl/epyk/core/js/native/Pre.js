function pre(c,b,a){setCss(c,a,true);if(a.templateMode=='loading'){b=a.templateLoading(b);}else if(a.templateMode=='error'){b=a.templateError(b);}else if(typeof a.template!=='undefined'&&b){b=a.template(b);}if(a.showdown){var d=new showdown.Converter(a.showdown);c.innerHTML=d.makeHtml(b);}else{c.innerHTML=b;}}