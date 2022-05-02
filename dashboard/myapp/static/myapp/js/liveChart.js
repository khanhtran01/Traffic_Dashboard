var xValues = [];
var yValues = [];

var yTemp = [];
var xTemp = [];

var yCar = [];
var xCar = [];
// get init value from database
function initHumi(){
	const xhttp = new XMLHttpRequest();
	xhttp.onload = function () {
		yValues = JSON.parse(this.responseText).humidata;
		xValues = JSON.parse(this.responseText).humitime;
		yTemp = JSON.parse(this.responseText).tempdata;
		xTemp = JSON.parse(this.responseText).temptime;
		yCar = JSON.parse(this.responseText).cardata;
		xCar = JSON.parse(this.responseText).cartime;
		// console.log(JSON.parse(this.responseText))
		updateChartInit(humiChart, xValues, yValues);
		updateChartInit(tempChart, xTemp, yTemp);
		updateChartInit(badCarChart, xCar, yCar);
	}
	xhttp.open("GET", "/myapp/initHumi");
	xhttp.send();
}

function initDataForWeek(){
	const xhttp = new XMLHttpRequest();
	xhttp.onload = function () {
		console.log(JSON.parse(this.responseText));
		updateChartInitWeek(humiChart_week, JSON.parse(this.responseText).humiweek, JSON.parse(this.responseText).humi)
		updateChartInitWeek(tempChart_week, JSON.parse(this.responseText).tempweek, JSON.parse(this.responseText).temp)
		updateChartInitWeek(humiChart_month, JSON.parse(this.responseText).humimonth, JSON.parse(this.responseText).humimonthdata)
		updateChartInitWeek(tempChart_month, JSON.parse(this.responseText).tempmonth, JSON.parse(this.responseText).tempmonthdata)
		updateChartInitWeek(badCarChart_week, JSON.parse(this.responseText).badcarweek, JSON.parse(this.responseText).badcarweekdata)
		updateChartInitWeek(badCarChart_month, JSON.parse(this.responseText).badcarmonth, JSON.parse(this.responseText).badcarmonthdata)
		console.log(this.responseText)
	}
	xhttp.open("GET", "/myapp/initWeek");
	xhttp.send();
}
function updateChartInitWeek(chartName, xarrayInput, yarrayInput) {
	yarray = chartName.data.datasets[0].data;
	xarray = chartName.data.labels;
	for (var i = 0; i < yarrayInput.length; i++) {
		yarray.push(yarrayInput[i])
		xarray.push(xarrayInput[i]);
	}
	chartName.options.scales.yAxes[0].ticks.max = Math.max.apply(Math, yarrayInput) + 15;
	chartName.update();
}
initDataForWeek()
// function initTemp(){
// 	const xhttp = new XMLHttpRequest();
// 	xhttp.onload = function () {
// 		yValues = JSON.parse(this.responseText).humidata;
// 		xValues = JSON.parse(this.responseText).humitime;
// 		console.log(JSON.parse(this.responseText))
// 		updateChartInit();
// 	}
// 	xhttp.open("GET", "/myapp/initHumi");
// 	xhttp.send();
// }



initHumi();
setTimeout(live, 100);
function live() {
	$(document).ready(function () {
		function fetchData() {
			$.ajax({
				url: 'https://io.adafruit.com/api/v2/khanhtran01/feeds/humi-and-temp',
				success: function (result) {
					let time =  new Date().toLocaleTimeString();
					// console.log(time.slice(0,8));
					liveChartUpdate(humiChart,JSON.parse(result['last_value'])['humi'], time.slice(0,8));
					liveChartUpdate(tempChart,JSON.parse(result['last_value'])['temp'], time.slice(0,8));
				}
			});
		}
		fetchData()
		setInterval(fetchData, 5000);
	});
}

// setTimeout(getAPI, 100);
// function getAPI() {
// 	$(document).ready(function () {
// 		function getData() {
// 			$.ajax({
// 				url: 'https://io.adafruit.com/api/v2/khanhtran01/feeds/humi-and-temp',
// 				success: function (result) {
// 					console.log(JSON.parse(result['last_value']))
// 				}
// 			});
// 		}
// 		setInterval(getData, 1000);
// 	});
// }

var count = 0;

function updateChartInit(chartName, xarrayInput, yarrayInput) {
	yarray = chartName.data.datasets[0].data;
	xarray = chartName.data.labels;
	for (var i = 0; i < yarrayInput.length; i++) {
		yarray.push(yarrayInput[i])
		if (count % 4 == 0) {
			xarray.push(xarrayInput[i].slice(11, 18));
		}
		else {
			xarray.push('');
		}
		count++;
		if (count > 4) {
			count = 1;
		}
	}
	chartName.options.scales.yAxes[0].ticks.max = Math.max.apply(Math, yarrayInput) + 5;
	// console.log(yarray);
	chartName.update();
}



function liveChartUpdate(chartName,y, x) {
	newy = y
	// newX = humiChart.data.labels[19] + 10;
	newX = count % 4 == 0 ? x : '';
	count++;
	// console.log(y);
	yarray = chartName.data.datasets[0].data;
	if (newy > Math.max.apply(Math, yarray)) {
		chartName.options.scales.yAxes[0].ticks.max = newy + 5;
	}
	chartName.data.labels.push(newX);
	chartName.data.datasets[0].data.push(newy);
	if (yarray.length > 20) {
		chartName.data.datasets[0].data.shift();
	}
	chartName.data.labels.shift()
	chartName.update();
}

function pushDatatoServer(data){
	$.ajax({
		url: '/myapp/pushData',
		method: "POST",
		headers: {
			"X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
		  },
		data: {
			humi: data['humi'],
			temp: data['temp']
		},
		success: function(data){console.log("complete");},
		error: function(errMsg) {
			alert(JSON.stringify(errMsg));
		}
	});
}