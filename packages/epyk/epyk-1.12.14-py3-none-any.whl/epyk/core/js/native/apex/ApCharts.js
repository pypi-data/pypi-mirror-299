function apCharts(o,r){if(o.python)result={series:[],labels:o.labels},o.datasets.forEach(function(s,a){void 0===s.backgroundColor&&(s.backgroundColor=r.background_colors[a]),void 0===s.borderColor&&(s.borderColor=r.colors[a]),void 0===s.hoverBackgroundColor&&(s.hoverBackgroundColor=r.background_colors[a]),void 0!==r.commons&&Object.assign(s,r.commons),s.name=o.series[a],void 0!==r?._ek?.alterSeries&&r._ek.alterSeries(s,a),result.series.push(s)});else{var s,a,e={},i=[],n={};s="function"==typeof r.y_columns?r.y_columns(o,r):r.y_columns,a="function"==typeof r.x_axis?r.x_axis(o,r):r.x_axis,s.forEach(function(o){e[o]={}}),o.forEach(function(o){s.forEach(function(r){void 0!==o[r]&&(o[a]in n||(i.push(o[a]),n[o[a]]=!0),e[r][o[a]]=o[r])})}),result={series:[],labels:i,xaxis:{}},s.forEach(function(o,s){if(dataSet={label:o,data:[]},void 0!==r.attrs&&void 0!==r.attrs[o])for(var a in r.attrs[o])dataSet[a]=r.attrs[o][a];else if(void 0!==r.commons)for(var a in r.commons)dataSet[a]=r.commons[a];i.forEach(function(r){void 0===e[o][r]?dataSet.data.push(null):dataSet.data.push({x:r,y:e[o][r]})}),void 0!==r?._ek?.alterSeries&&r._ek.alterSeries(dataSet,s),result.series.push(dataSet)})}return result}