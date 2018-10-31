#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "chenwei"
# Date: 2018/10/12

import redis


class UserRedis(object):
    def __init__(self, ip="127.0.0.1", port=6379):
        self._rs = redis.StrictRedis(ip, port)

    def set_user(self, user, value, timeout=120):
        return self._rs.setex(user, timeout, value)

    def incr_user(self, user):
        return self._rs.incr(user)

    def get_user(self, user):
        return self._rs.get(user)


class User(object):
    def __init__(self):
        self._login_dict = {
            'alex': 123,
            'hah': 123
        }

    def __getattr__(self, item):
        return self._login_dict[item]


def AccessLimit(username=None, seconds=None, maxCount=None, needLogin=True):
    def outer(func):
        def inner(*args, **kwargs):
            user, userredis = User(), UserRedis()
            userCount, has_user = userredis.get_user(user[username]), user[username]
            if needLogin and not has_user:
                return "登陆后，在尝试"
            if not userCount:
                userredis.set_user(username, 1, timeout=seconds)
            else:
                userredis.incr_user(username)
            if userCount and int(userCount) > maxCount:
                return "访问太频繁啦~"
            return func(*args, **kwargs)
        return inner
    return outer


@AccessLimit(username='alex', seconds=10, maxCount=5)
def index():
    return 'index'


res = index()
print(res)