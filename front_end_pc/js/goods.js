var vm = new Vue({
    el: '#app',
    data: {
        recommend_goods: [],
        categories: [],
    },

    mounted: function () {
        this.get_recommend_goods();
        this.get_category_goods();
    },

    methods: {
        get_recommend_goods: function () {
            axios.get('http://127.0.0.1:8000/goods/recommend/')
                .then(response => {
                    this.recommend_goods = response.data;
                })
                .catch(function (error) {
                    console.log(error.response)
                })
        },

        get_category_goods: function () {
            axios.get('http://127.0.0.1:8000/goods/category/')
                .then(response => {
                    this.categories = response.data;
                })
                .catch(function (error) {
                    console.log(error.response)
                })
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
