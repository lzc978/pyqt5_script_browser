
function handle(path) {
    // 首页
    if (path == '/zh') {
        document.getElementsByClassName('radio-inline')[1].click();
        document.getElementById('oneway_from').value='广州 (CAN)';
        document.getElementById('oneway_to').value='新加坡 (SIN)';
        document.getElementById('oneway_departuredate').value='2019年3月10日';
        document.getElementsByClassName('btn--booking')[1].click();
        return;
    }

    // 选择航班
    if (path == '/Book/Flight') {
        document.getElementsByClassName('price--sale')[0].click();
        document.getElementsByClassName('heading-4')[0].click();
        document.getElementsByClassName('btn-submit')[0].click();
        return;
    }

    // 乘客信息
    if (path == '/BookFlight/Passengers') {
        document.getElementsByClassName('fname1')[0].value = "匿名";
    }
}


let host = document.location.hostname;
if (host.endsWith('.flyscoot.com')) {
    handle(document.location.pathname);
}