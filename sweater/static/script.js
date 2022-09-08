//document.getElementById("date-site").innerHTML = ;

function get_Year(text){
    return (text+ new Date().getFullYear())
}

document.getElementById('date-site').innerHTML = get_Year('© 2018-')

if (document.getElementById('price_box')){
    get_BYN_to_USD(document.getElementById('price_box').innerHTML)
    document.getElementById('price_box').innerHTML = Price_Space(document.getElementById('price_box').innerHTML, " р.")

}

function Price_Space(price, type){
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + type;
}

function get_BYN_to_USD(BYN_V) {
    $.getJSON("https://www.cbr-xml-daily.ru/daily_json.js", function convert(data) {
        usd = Math.round(BYN_V / ((data.Valute.USD.Value) / (data.Valute.BYN.Value)))
        document.getElementById('usd_box').innerHTML = Price_Space(usd, " $.");
    });
    return true;
    //usd = Price_Space(usd.toString(), " $")
}
$(document).ready(function () {
        $('img').each(function () {
            $(this).error(function () {
                $(this).attr('src', 'static/img/default.png');
            });
        });
    });

function Show_Phone(phone){
    document.getElementById('User_PhoneB').remove();
    document.getElementById('other_info').innerHTML+=`<span style="float: left; font-size: 18px">Телефон</span><span style="float: right; font-size: 18px" id="User_Phone">${phone}</span><hr><br>`;
    navigator.clipboard.writeText(phone)
    return true;
}

$( "input" ).blur(function( ) {
    if ($(this).val().trim() !== ''){
        $(this).css("background-color", "white")
    }
    else
        $(this).css("background-color", "#e7e7e7")
});


// $( "#myform" ).submit(function( form ) {
//     $(this).serializeArray().forEach(function (i, v) {
//       if (v.value == '' || v.value == null || typeof v.value == 'undefined') {
//         alert("need to fill up all those fields");
//       }
//     });
// });