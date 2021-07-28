from Controller.basic import check
from Object.service import service

def service_list(cn, nextc):
    err = service().list()
    return cn.call_next(nextc, err)

def service_exist(cn, nextc):
    err = check.contain(cn.rt, ["service"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = service().exist(cn.rt["service"])
    return cn.call_next(nextc, err)

def service_infos(cn, nextc):
    err = check.contain(cn.rt, ["service"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = service().infos(cn.rt["service"])
    return cn.call_next(nextc, err)

def service_setup_infos(cn, nextc):
    err = check.contain(cn.rt, ["setup"])
    if not err[0]:
        return cn.toret.add_error(err[1], err[2])
    err = service().setup_by_id(cn.rt["setup"])
    return cn.call_next(nextc, err)

def service_new(cn, nextc):
    err = service().gen_commands(cn.rt["service"], cn.pr)
    return cn.call_next(nextc, err)
