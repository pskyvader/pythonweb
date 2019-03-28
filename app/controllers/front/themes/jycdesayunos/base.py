
class base:
    def init(self, var: list):
        from inspect import signature
        import inspect

        if len(var) == 0:
            var = ['index']

        if hasattr(self, var[0]) and callable(getattr(self, var[0])):
            fun = var[0]
            del var[0]
            method = getattr(self, fun)
            sig = signature(method)
            params = sig.parameters
            if 'self' in params:
                if 'var' in params:
                    ret = method(self, var=var)
                else:
                    ret = method(self)
            else:
                if 'var' in params:
                    ret = method(var=var)
                else:
                    ret = method()
        else:
            ret = {
                'error': 404
            }
        return ret