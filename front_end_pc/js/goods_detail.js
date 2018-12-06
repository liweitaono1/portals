var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',
        goods: null,
        recommend_goods: null,

        count: 1,            // 添加到购物车的商品数量
        goods_id: 0,         // 当前显示的商品id
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
    },

    mounted: function () {
        this.goods_id = get_query_string('id');
        this.get_goods_detail(this.goods_id);
        this.get_recommend_goods();
    },

    methods: {
        // 判断用户是否已经登录
        is_login: function () {
            var token = sessionStorage.token || localStorage.token;
            return token !== undefined
        },

        // 获取商品详情数据
        get_goods_detail: function (id) {
            var url = this.host + '/goods/' + id + "/";
            axios.get(url)
                .then(response => {
                    this.goods = response.data;
                })
                .catch(error => {
                    console.log(error)
                });
        },

        // 获取推荐商品
        get_recommend_goods: function () {
            let url = this.host + '/goods/recommend/';
            axios.get(url)
                .then(response => {
                    this.recommend_goods = response.data;
                })
                .catch(function (error) {
                    console.log(error.response)
                })
        },

        addToCart: function () {
            // 添加商品到购物车
            if (this.is_login()) {  // 已经登录
                let url = this.host + '/cart/';
                // 请求参数
                var params = {
                    goods_id: this.goods_id,
                    count: this.count
                };
                axios.post(url, params, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                })
                    .then(response => {
                        this.total_count = response.data.total_count;
                        $('#cart_count').text('购物车(' + this.total_count + ')')
                    })
                    .catch(function (error) {
                        console.log(error)
                        alert(error)
                    })
            } else {
                // 如果没有登录,跳转到登录界面,引导用户登录
                window.location.href = 'login.html'
            }
        },

        on_increment: function () {
            // 点击增加购买数量
            this.count++
        },

        on_decrement: function () {
            // 点击减少购买数量
            if (this.count > 1) {
                this.count--;
            }
        },
    },

    filters: {
        formatDate: function (time) {
            return dateFormat(time, "yyyy-mm-dd");
        },

        formatDate2: function (time) {
            return dateFormat(time, "yyyy-mm-dd HH:MM:ss");
        },
    },
});