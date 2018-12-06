var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        token: sessionStorage.token || localStorage.token,

        provinces: [],
        cities: [],
        districts: [],

        addresses: [],
        limit: '',
        default_address_id: '',
        form_address: {
            receiver: '',
            province_id: '',
            city_id: '',
            district_id: '',
            place: '',
            mobile: '',
            tel: '',
            email: '',
        },

        error_receiver: false,
        error_place: false,
        error_mobile: false,
        error_email: false,
    },

    mounted: function () {
        // 获取所有的省份
        axios.get(this.host + '/areas/')
            .then(response => {
                this.provinces = response.data;
            })
            .catch(error => {
                alert(error.response.data);
            });
    },

    watch: {
        // 监听省份的改变, 查询对应的城市并刷新界面显示
        'form_address.province_id': function () {
            if (this.form_address.province_id) {
                axios.get(this.host + '/areas/' + this.form_address.province_id + '/')
                    .then(response => {
                        this.cities = response.data.subs;
                    })
                    .catch(error => {
                        console.log(error.response.data);
                        this.cities = [];
                    });
            }
        },

        // 监听城市的改变, 查询对应的区县并刷新界面显示
        'form_address.city_id': function () {
            if (this.form_address.city_id) {
                axios.get(this.host + '/areas/' + this.form_address.city_id + '/')
                    .then(response => {
                        this.districts = response.data.subs;
                    })
                    .catch(error => {
                        console.log(error.response.data);
                        this.districts = [];
                    });
            }
        }
    },

    methods: {
        // 展示新增地址界面
        show_add: function () {
            this.form_address.receiver = '';
            this.form_address.province_id = '';
            this.form_address.city_id = '';
            this.form_address.district_id = '';
            this.form_address.place = '';
            this.form_address.mobile = '';
            this.form_address.tel = '';
            this.form_address.email = '';
        },

        check_receiver: function () {
            if (!this.form_address.receiver) {
                this.error_receiver = true;
            } else {
                this.error_receiver = false;
            }
        },

        check_place: function () {
            if (!this.form_address.place) {
                this.error_place = true;
            } else {
                this.error_place = false;
            }
        },

        check_mobile: function () {
            var re = /^1[345789]\d{9}$/;
            if (re.test(this.form_address.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile = true;
            }
        },

        check_email: function () {
            if (this.form_address.email) {
                var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
                if (re.test(this.form_address.email)) {
                    this.error_email = false;
                } else {
                    this.error_email = true;
                }
            }
        },

        // 保存地址
        save_address: function () {
            if (this.error_receiver || this.error_place
                || this.error_mobile || this.error_email
                || !this.form_address.province_id
                || !this.form_address.city_id
                || !this.form_address.district_id) {
                alert('信息填写有误！');
            } else {
                this.form_address.title = this.form_address.receiver;
                // 新增地址
                axios.post(this.host + '/addresses/', this.form_address, {
                        headers: {
                                'Authorization': 'JWT ' + this.token
                            },
                        })
                    .then(response => {
                        // 跳转回地址列表界面
                        location.href = '/user_center_address.html'
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
    }
});