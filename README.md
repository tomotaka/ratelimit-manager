# ratelimit-manager

- provides fast and memory efficient rate limit.
- support rate-limit like:
  - 300calls per 3minutes
  - 500calls per 10msec
- rate-limit "N calls per XX msec" will consume (N * 8) bytes memory
  - timestamp array is implemented with numpy array

## Installation

    $ pip install ratelimit-manager

## Basic Usage

1. create limit object with `RateLimit(MAX_CALLS_IN_DURATION, DURATION_MSEC)`
2. just call `tick()` per each call, if limit exceeded, `tick()` will raise RateLimitError


    # -*- coding: utf-8 -*-
    from rlmanager import RateLimit, RateLimitError

    limit = RateLimit(100, 1000)  # permit only 100calls per 1sec

    def _protected_api(a, b):
        return a + b

    def protected_api(a, b):
        limit.tick()
        return _protected_api(a, b)

    if __name__ == '__main__':
        for i in xrange(101):
            try:
                print protected_api(1 + i)
            except RateLimitError as e:
                print 'limited by rule: %s' % e.rule


You can also check if limit can tick or not with calling `is_tick_ok()`.


    if not limit.is_tick_ok():
        print 'too much'


## Advanced Usage: rate-limit group

You can apply multiple rate-limit rules with RateLimitManager.  
tick_all() will raise RateLimitError if call count violates any of the rule.

    # -*- coding: utf-8 -*-
    from rlmanager import RateLimitManager, RateLimitError

    limits = RateLimitManager(
        (
            (100, 1000),  # 100calls per 100
            (50, 100)     # 50calls per 100msec
        )
    )

    def _protected_api(a, b):
        return a + b

    def protected_api(a, b):
        limit.tick()
        return _protected_api(a, b)

    if __name__ == '__main__':
        for i in xrange(101):
            try:
                print protected_api(1 + i)
            except RateLimitError as e:
                print 'limited by rule: %s' % e.rule


You can also check if limit can tick or not with calling `is_all_tick_ok()`.

    if not limit.is_all_tick_ok():
        print 'too much'
