$(document).ready(function () {
    $("#settimesubmit").click(function (e) {
        e.preventDefault();
        var form = $(".Traffic_time_form");
        var actionUrl = form.attr('action');
        $.ajax({
            type: 'post',
            url: actionUrl,
            data: form.serialize()+'&action=1',
            success: function (result) {
                //   document.getElementById("input_id").value = '';
                if (result['status'] == false){
                    alert("Thời gian không hợp lệ !! Xin bạn nhập lại")
                }
                console.log(result);

                
            }
        });
    });
    $("#comfirm_time").click(function (e) {
        e.preventDefault();
        var form = $(".Traffic_time_form");
        var actionUrl = form.attr('action');
        $.ajax({
            type: 'post',
            url: actionUrl,
            data: form.serialize()+'&action=0',
            success: function (result) {
                //   document.getElementById("input_id").value = '';
                if (result['status'] == false){
                    alert("Thời gian không hợp lệ !! Xin bạn nhập lại")
                }
                if (result['status'] == true){
                    liveCar(result['time'])
                    console.log(result['time']);
                }
            }
        });
    });
});

// setTraffic_time_form

$(document).ready(function () {
    $(".setTraffic_time_form").submit(function (e) {
        e.preventDefault();
        var form = $(this);
        var actionUrl = form.attr('action');
        $.ajax({
            type: 'post',
            url: actionUrl,
            data: form.serialize(),
            success: function () {
                //   document.getElementById("input_id").value = '';
                console.log(actionUrl);
            }
        });
    });
});

function pushData(humi, temp) {
    $.ajax({
        type: 'get',
        url: '/myapp/pushData/',
        data: {
            'humi': humi,
            'temp': temp
        },
        success: function (result) {
            console.log(result);
            $("#div1").html(result.data);
        }
    });
}

function pushCar(car) {
    $.ajax({
        type: 'get',
        url: '/myapp/pushData/',
        data: {
            'car': car
        },
        success: function (result) {
            console.log(result);
            $("#div1").html(result.data);
        }
    });
}