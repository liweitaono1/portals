var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        token: sessionStorage.token || localStorage.token,

        addresses: [],      // 当前登录用户的地址列表
        user_id: 0,         // 当前登录用户的id
        default_address_id: '',     // 当前登录用户的默认地址的id
    },

    mounted: function(){
        // 请求当前登录用户的所有的地址
        // 参数1: url地址
        // 参数2: 请求参数
        axios.get(this.host + '/addresses/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
            })
            .then(response => {
                // 接收服务器返回的数据
                this.user_id = response.data.user_id;
                this.default_address_id = response.data.default_address_id;
                this.addresses = response.data.addresses;
            })
            .catch(error => {
                if (error.response.status ===  401) {
                    alert('您尚未登录,请您先登录')
                }
            });
    },

    methods: {
        // 设置默认地址
        set_default: function(){
            if (!this.default_address_id) {
                alert('请先选择默认地址');
                return
            }

            let url = this.host + '/addresses/' + this.default_address_id + '/status/';
            axios.put(url, null, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
            })
            .then(response => {
                // 接收服务器返回的数据
                alert('默认地址设置成功');
            })
            .catch(error => {
                if (error.response.status === 401) {
                    alert('您尚未登录,请您先登录')
                }
            });
        },

        // 删除默认地址
        delete_address: function (address_id) {
            // 删除不变
            axios.delete(this.host + '/addresses/' + address_id + "/", {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
            }).then(response => {
                location.href = '/user_center_address.html'
            }).catch(error => {
                alert('删除失败')
            })
        }
    }
});