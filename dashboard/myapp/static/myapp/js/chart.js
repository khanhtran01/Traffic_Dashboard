
var xValues = [];
var yValues = [];

var humiChart = new Chart("humiChart", {
  type: "line",
  data: {
    labels: xValues,
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: yValues
    }]
  },
  options: {
    legend: { display: false },
    scales: {
      yAxes: [{ ticks: { min: 0, max: 16 } }],
    },
    title: {
      display: true,
      text: "Biểu đồ nhiệt độ tại Ngã tư Hàng Xanh"
    }
  }
});
var tempy = [];
var tempx = [];

var tempChart = new Chart("tempChart", {
  type: "line",
  data: {
    labels: tempx,
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: tempy
    }]
  },
  options: {
    legend: { display: false },
    scales: {
      yAxes: [{ ticks: { min: 0, max: 16 } }],
    },
    title: {
      display: true,
      text: "Biểu đồ độ ẩm tại Ngã tư Hàng Xanh"
    }
  }
});


var badcary= [];
var badcarx = [];
var badCarChart = new Chart("badCarChart", {
  type: "line",
  data: {
    labels: badcarx,
    datasets: [{
      fill: false,
      lineTension: 0,
      backgroundColor: "rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: badcary
    }]
  },
  options: {
    legend: { display: false },
    scales: {
      yAxes: [{ ticks: { min: 0, max: 16 } }],
    },
    title: {
      display: true,
      text: "Biểu đồ số xe vượt đèn đỏ tại Ngã tư Hàng Xanh"
    }
  }
});