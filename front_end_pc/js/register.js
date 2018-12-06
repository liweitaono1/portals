var vm = new Vue({
    el: '#app',
    data: {
        // 双向绑定变量
        username: '',
        password: '',
        password2: '',
        mobile: '',
        sms_code: '',
        allow: false,

        // 控制元素是否显示
        error_name: false,
        error_password: false,
        error_check_password: false,
        error_phone: false,
        error_sms_code: false,
        error_allow: false,

        // 出错提示
        error_name_message: '请输入5-20个字符的用户名',
        error_password_message: '请输入8-20位的登录密码',
        error_phone_message: '请输入正确的手机号',
        error_sms_code_message: '请输入短信验证码',

        // 图片验证码
        image_code_id: '',
        image_code_url: '',
    },

    // 当vue实例挂载到界面后执行, 可以在此方法中执行界面初始化操作
    mounted: function () {
    },

    methods: {
        check_username: function () {
            var len = this.username.length;
            if (len < 5 || len > 20) {
                this.error_name = true;
            } else {
                this.error_name = false;
            }
        },

        check_pwd: function () {
            var len = this.password.length;
            if (len < 8 || len > 20) {
                this.error_password = true;
            } else {
                this.error_password = false;
            }
        },

        check_cpwd: function () {
            if (this.password !== this.password2) {
                this.error_check_password = true;
            } else {
                this.error_check_password = false;
            }
        },

        check_phone: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone = true;
            }
        },

        check_sms_code: function () {
            var len = this.sms_code.length;
            if (len === 0) {
                this.error_sms_code = true;
            } else {
                this.error_sms_code = false;
            }
        },

        check_allow: function () {
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },

        // 获取短信
        get_sms_code: function() {
            this.check_phone();

            if (!this.error_phone) {
                // axios.get('http://127.0.0.1:8000/sms_code/' + this.mobile);
                // 向后端接口发送请求，让后端发送短信验证码
                axios.get('http://127.0.0.1:8000/sms_code/' + this.mobile + '/', {
                    responseType: 'json'
                });
            }

        },
        // 点击注册按钮
        on_submit: function () {

            this.check_username();
            this.check_pwd();
            this.check_cpwd();
            this.check_phone();
            this.check_allow();

            if (this.error_name === false
                && this.error_password === false
                && this.error_check_password === false
                && this.error_phone === false
                && this.error_allow === false) {

                // 定义请求参数
                var url = 'http://127.0.0.1:8000/users/';
                var params = {	// post请求参数
                    username: this.username,
                    password: this.password,
                    password2: this.password2,
                    mobile: this.mobile,
                    sms_code: this.sms_code,
                    allow: this.allow.toString()  //
                };

                // 发起post请求
                axios.post(url, params)
                    .then(response => {
                        // 注册成功进入登录界面
                        location.href = '/login.html';
                    }).catch(error => {
                        console.log(error.response.data);
                        // 请求参数校验有误
                        if (error.response.status === 400) {
                            this.error_sms_code = true;
                            this.error_sms_code_message = '验证码不正确'
                        } else {
                            console.log(error.response.data);
                        }
                    })
            } else {
                alert('填写有误')
            }
        },
    }
});

