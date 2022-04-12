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
        202:"酒店信息不存在"
    }
    status = "successful" if code in [200] else "failed"
    ret = {
        "status": status,
        "msg": clock_code[code],
        "data": kwargs.get("data", "")
    }
    return ret

