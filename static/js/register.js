function bindEmailCaptcha()
{
    // $("#captcha-btn")//#代表id 所以表示为找到id = captcha-btn的标签，再给这个标签绑定一个点击事件click 点击时会执行click里面的函数
    $("#captcha-btn").click(function (event)//点击是个事件event，事件发生的位置，针对什么元素等等信息全部放在event事件中
    {
        var $this=$(this);
        event.preventDefault();//阻止 点击发送验证码就提交表单数据
        //var email = $('#exampleInputEmail1').val(); //通过id获取
        var email= $("input[name='email']").val();//获取到了邮箱的input的标签 然后val就可以获取input标签的值
        //alert(email)
        $.ajax({
            url:"captcha/email?email="+email,
            method:'GET',
            success:function (result){
                code = result['code']
                if (code == 200)
                {
                    var countdown = 5;

                    var timer = setInterval(function ()
                    {
                        $this.text(countdown);
                        countdown-=1;
                        if (countdown<=0){
                            clearInterval(timer);//运行了五秒，为了关闭计时就得clearInterval（timer）
                            $this.text("获取验证码");
                            bindEmailCaptcha();
                        }
                    },1000)
                }
                else{
                    alert("youxiangfasonghshibai")
                }
                //result 是后端auth.py邮箱获取邮箱验证码的返回值
            },
            fail:function (error){
                console.log(error)
            }
        });

    });
}

$(function ()//整个网页加载完成后才执行这个函数
{
    bindEmailCaptcha();
});