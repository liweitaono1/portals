import json

from django.shortcuts import render

# Create your views here.


# 请求方式 ： POST /cart/
from django_redis import get_redis_connection

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import Goods

from .serializers import CartSerializer


class Cart(APIView):
    def post(self, request):
        data = request.data
        goods_id = data['goods_id']
        count = data['count']
        selected = data.get('selected', False)
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            pipeline = conn.pipeline()
            pipeline.hincrby(cart_id, goods_id, count)
            if selected:
                pipeline.sadd(cart_selected_id, goods_id)
            else:
                # 移除选中状态
                pipeline.srem(cart_selected_id, goods_id)
            pipeline.execute()
            total_count = 0
            try:
                user = request.user
            except Exception:
                user = None
            if user is not None and user.is_authenticated:
                conn = get_redis_connection('cart')
                cart_id = 'cart_%d' % user.id
                cart_selected_id = 'cart_selected_%d' % user.id
                goods_ids = conn.hgetall(cart_id)
                cart_selected_ids = conn.smembers(cart_selected_id)
                for goods_id in goods_ids:
                    count = int(goods_ids[goods_id])
                    total_count += count
                data['total_count'] = total_count
            else:
                cart_cookie = request.COOKIES.get('cart', None)
                if cart_cookie:
                    cart = json.loads(cart_cookie)
                else:
                    cart = {}

                for goods_id in cart:
                    count = cart[goods_id]['count']
                    total_count += count

                data['total_count'] = total_count
            return Response(data, status=201)
        else:
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}
            if goods_id in cart:
                cart[goods_id]['count'] += count
            else:
                cart[goods_id] = {
                    'count': count
                }
            if selected:
                cart[goods_id]['selected'] = True
            else:
                cart[goods_id]['selected'] = False
        total_count = 0
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            goods_ids = conn.hgetall(cart_id)
            cart_selected_ids = conn.smembers(cart_selected_id)
            for goods_id in goods_ids:
                count = int(goods_ids[goods_id])
                total_count += count
            data['total_count'] = total_count
        else:
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}

            for goods_id in cart:
                count = cart[goods_id]['count']
                total_count += count

            data['total_count'] = total_count
            response = Response(data, status=201)
            response.set_cookie('cart', json.dumps(cart), max_age=60 * 60 * 24 * 365)
            return response

    def get(self, request):
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            goods_ids = conn.hgetall(cart_id)
            cart_selected_ids = conn.smembers(cart_selected_id)
            goods = []
            for goods_id in goods_ids:
                good = Goods.objects.get(id=int(goods_id))
                good.count = int(goods_ids[goods_id])
                if goods_id in cart_selected_ids:
                    good.selected = True
                else:
                    good.selected = False

                goods.append(good)
            serializers = CartSerializer(goods, many=True)
            return Response(serializers.data)
        else:
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}
        goods = []

        for goods_id in cart:
            good = Goods.objects.get(id=goods_id)
            good.count = cart[goods_id]['count']
            good.selected = cart[goods_id]['selected']
            goods.append(good)

        serializers = CartSerializer(goods, many=True)
        return Response(serializers.data)

    def put(self, request):
        data = request.data
        goods_id = data['goods_id']
        count = data['count']
        selected = data.get('selected', False)
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            pipeline = conn.pipeline()
            pipeline.hmset(cart_id, {goods_id: count})
            if selected:
                pipeline.sadd(cart_selected_id, goods_id)
            else:
                pipeline.srem(cart_selected_id, goods_id)
            pipeline.execute()
            total_count = 0
            try:
                user = request.user
            except Exception:
                user = None
            if user is not None and user.is_authenticated:
                conn = get_redis_connection('cart')
                cart_id = 'cart_%d' % user.id
                cart_selected_id = 'cart_selected_%d' % user.id
                goods_ids = conn.hgetall(cart_id)
                cart_selected_ids = conn.smembers(cart_selected_id)
                for goods_id in goods_ids:
                    count = int(goods_ids[goods_id])
                    total_count += count
                data['total_count'] = total_count
            else:
                cart_cookie = request.COOKIES.get('cart', None)
                if cart_cookie:
                    cart = json.loads(cart_cookie)
                else:
                    cart = {}

                for goods_id in cart:
                    count = cart[goods_id]['count']
                    total_count += count

                data['total_count'] = total_count
            return Response(data, status=201)
        else:
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}

            if selected:
                cart[str(goods_id)] = {
                    'count': count,
                    'selected': True
                }
            else:
                cart[str(goods_id)] = {
                    'count': count,
                    'selected': False
                }
        total_count = 0
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            goods_ids = conn.hgetall(cart_id)
            cart_selected_ids = conn.smembers(cart_selected_id)
            for goods_id in goods_ids:
                count = int(goods_ids[goods_id])
                total_count += count
            data['total_count'] = total_count
        else:
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}

            for goods_id in cart:
                count = cart[goods_id]['count']
                total_count += count

            data['total_count'] = total_count
            response = Response(data, status=201)
            response.set_cookie('cart', json.dumps(cart), max_age=60 * 60 * 24 * 365)

            return response

    def delete(self, request):
        data = request.data
        goods_id = data['goods_id']
        try:
            user = request.user
        except Exception:
            # 异常说民用户未登录
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            pipeline = conn.pipeline()
            # 删除商品
            pipeline.hdel(cart_id, goods_id)
            # 移出选中状态
            pipeline.srem(cart_selected_id, goods_id)
            pipeline.execute()
            return Response(status=204)
        else:
            # 操作cookie
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}
            if str(goods_id) in cart:
                del cart[str(goods_id)]

            response = Response(status=204)
            response.set_cookie('cart', json.dumps(cart), max_age=60 * 60 * 24 * 365)
            return response


class CartSelectView(APIView):
    permission_classes = (IsAuthenticated,)

    def perform_authentication(self, request):
        pass

    def put(self, request):
        # 获取数据
        data = request.data
        selected = data.get('selected', False)

        # 判断用户是否登录
        try:
            user = request.user
        except Exception:
            # 异常说民用户未登录
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            sku_ids = conn.hkeys(cart_id)  # 返回的是sku_id数组
            if selected:
                conn.sadd(cart_selected_id, *sku_ids)
            else:
                conn.srem(cart_selected_id, *sku_ids)
            return Response({'message': 'OK'}, status=201)

        else:
            # 操作cookie
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}

            for goods_id in cart:
                if selected:
                    cart[goods_id]['selected'] = True
                else:
                    cart[goods_id]['selected'] = False

            response = Response({'message': 'OK'}, status=201)
            response.set_cookie('cart', json.dumps(cart), max_age=60 * 60 * 24 * 365)
            return response


class CARTCOUNT(APIView):
    permission_classes = (IsAuthenticated,)

    def perform_authentication(self, request):
        pass

    def get(self, request):
        total_count = 0
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            conn = get_redis_connection('cart')
            cart_id = 'cart_%d' % user.id
            cart_selected_id = 'cart_selected_%d' % user.id
            goods_ids = conn.hgetall(cart_id)
            cart_selected_ids = conn.smembers(cart_selected_id)
            for goods_id in goods_ids:
                count = int(goods_ids[goods_id])
                total_count += count
        else:
            cart_cookie = request.COOKIES.get('cart', None)
            if cart_cookie:
                cart = json.loads(cart_cookie)
            else:
                cart = {}

            for goods_id in cart:
                count = cart[goods_id]['count']
                total_count += count


        return Response({"total_count": total_count})
