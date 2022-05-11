# -------------------------------------------------------------------------------
# Description:  公共
# Reference:
# Author: 
# Date:   2022/4/10
# -------------------------------------------------------------------------------


def ret_code(code,**kwargs):
    clock_code = {
        200:"操作成功",
        201:"请输入正确的参数",
        202:"酒店信息不存在",
        203:"用户已注册",
        204:"登录已失效,请重新登录",
        205:"下单成功",
        206:"下单失败",
        207:"登录失败"
    }
    status = "successful" if code in [200] else "failed"
    ret = {
        "status": status,
        "msg": clock_code[code],
        "data": kwargs.get("data", "")
    }
    return ret

