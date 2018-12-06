var vm = new Vue({
    el: '#app',
    data: {
        host: 'http://127.0.0.1:8000',
        goods_list: [],         // 购物车中的商品
        origin_input: 1,        // 商品数量
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
    },

    computed: {
        select_all: function () {
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                // 重新计算小计金额, 自动刷新界面显示
                if (!goods.selected) {
                    return false;
                }
            }
            return true;
        },

        // 获取选中的商品的数量
        selected_count: function () {
            let total_count = 0;
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                // 重新计算小计金额, 自动刷新界面显示
                goods.amount = parseFloat(goods.sell_price) * parseInt(goods.count);
                if (goods.selected) {
                    total_count += parseInt(goods.count);
                }
            }
            return total_count;
        },

        // 获取选中的商品的总金额
        selected_amount: function () {
            let total_amount = 0;
            for (let i = 0; i < this.goods_list.length; i++) {
                let goods = this.goods_list[i];
                if (goods.selected) {
                    total_amount += parseFloat(goods.sell_price) * parseInt(goods.count);
                }
            }
            // 金额保存两位有效数字
            return total_amount.toFixed(2);
        },
    },

    mounted: function () {
        this.get_cart_goods();
    },

    methods: {
        // 全选和全不选
        on_select_all: function () {
            let select = !this.select_all;
            for (let i = 0; i < this.goods_list.length; i++) {
                this.goods_list[i].selected = select;
            }
        },

        // 获取购物车商品数据
        get_cart_goods: function () {
            let url = this.host + '/cart/';
            axios.get(url, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json'
            })
                .then(response => {
                    this.goods_list = response.data;
                    // 动态地新增一个变量, 记录商品的勾选状态
                    for (let i = 0; i < this.goods_list.length; i++) {
                        let goods = this.goods_list[i];
                        this.goods_list[i].amount = parseFloat(goods.sell_price * goods.count);
                    }
                })
                .catch(error => {
                    console.log('====error: ' + error)
                })
        },

        // 点击增加购买数量
        on_add: function (index) {
            let goods = this.goods_list[index];
            let count = parseInt(goods.count) + 1;

            this.update_cart_count(goods.id, count, index);
        },

        // 点击减少购买数量
        on_minus: function (index) {
            let goods = this.goods_list[index];
            let count = parseInt(goods.count);
            if (count > 1) {
                count--;
                this.update_cart_count(goods.id, count, index);
            }
        },

        // 更新购物车商品购买数量
        on_input: function (index) {
            // 输入的数量不能超过最大库存
            let goods = this.goods_list[index];
            this.update_cart_count(goods.id, goods.count, index);
        },

        // 更新购物车商品数量
        update_cart_count: function (goods_id, count, index) {
            let url = this.host + '/cart/';
            // 请求参数
            let params = {
                goods_id: goods_id,
                count: count
            };
            axios.put(url, params, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json'
            })
                .then(response => {
                    this.goods_list[index].count = count;
                    this.goods_list[index].amount = this.goods_list[index].sell_price * count;

                    // 服务器返回的购物车的总数量
                    this.total_count = response.data.total_count;
                    $('#cart_count').text('购物车(' + this.total_count + ')')
                })
                .catch(error => {
                    this.goods_list[index].count = this.origin_input;
                    if ('non_field_errors' in error.response.data) {
                        alert(error.response.data.non_field_errors[0]);
                    } else {
                        alert('修改购物车失败');
                    }
                })
        },

        // 删除购物车中的一个商品
        delete_goods: function (index) {
            let url = this.host + '/cart/';
            let params = { // 请求参数
                goods_id: this.goods_list[index].id,
            };
            axios.delete(url, {
                data: params, headers: {
                    'Authorization': 'JWT ' + this.token
                },
            })
                .then(response => {
                    $('#cart_count').text('购物车(' + this.total_count + ')');
                    location.reload()
                })
                .catch(function (error) {
                    console.log(error);
                })
        },

        // 清空购物车
        clearCart: function (index) {
            let count = 0;
            for (let i = 0; i < this.goods_list.length; i++) {
                if (this.goods_list[i].selected) {
                    count++
                }
            }
            alert(count)
        },
    }
});