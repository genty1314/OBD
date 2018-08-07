 function getCookie(name){
    var x = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return x ? x[1]:undefined;
}

$(document).ready(function(){
    $("#login").click(function(){
        var email = $("#user_email").val();
        var pwd = $("#password").val();
        var rem = $("#remember_me").is(':checked');
        var pd = {"user_email":email, "password":pwd,"remember_me":rem, "_xsrf":getCookie("_xsrf")};
        $.ajax({
            type:"post",
            url:"/login",
            data:pd,
            cache:false,
            success:function(data){
                window.location.href = "/user?user="+data;
            },
            error:function(){
                alert("error!");
            },
        });
    });
});