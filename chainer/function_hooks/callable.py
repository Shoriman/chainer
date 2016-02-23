from chainer import function


class CallableHook(function.FunctionHook):

    def __init__(self, f):
        self.f = f

    def __call__(self, function, in_data, out_grad=None):
        return self.f(function, in_data, out_grad)