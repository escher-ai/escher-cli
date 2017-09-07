from waterbear import DefaultBear

_c = DefaultBear(None, **dict(a=10))
_c.update(b=100)
assert _c.b == 100


# @cli_parse
# class G(ParamsProto):
#     npts: int = 0
