import asyncio
import time

try:
    from pysnmp.hlapi.v3arch.asyncio import (
        SnmpEngine, CommunityData, UdpTransportTarget, ContextData,
        ObjectType, ObjectIdentity, get_cmd,
    )
except ImportError:
    SnmpEngine = CommunityData = UdpTransportTarget = ContextData = None
    ObjectType = ObjectIdentity = get_cmd = None


async def _check_snmp_async(host, port, community, timeout):
    result = await get_cmd(
        SnmpEngine(),
        CommunityData(community, mpModel=1),
        await UdpTransportTarget.create((host, port), timeout=timeout, retries=0),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysName", 0)),
    )
    return result


def check_snmp(host, port=161, community="public", timeout=3):
    if get_cmd is None:
        return {"status": "failed", "host": host, "port": port, "reachable": False,
                "error": "pysnmp is not installed"}
    start_time = time.perf_counter()
    try:
        error_indication, error_status, error_index, var_binds = asyncio.run(
            _check_snmp_async(host, port, community, timeout)
        )
        response_time = (time.perf_counter() - start_time) * 1000
        if error_indication:
            return {"status": "failed", "host": host, "port": port, "reachable": False,
                    "response_time_ms": round(response_time, 2), "error": str(error_indication)}
        if error_status:
            return {"status": "failed", "host": host, "port": port, "reachable": False,
                    "response_time_ms": round(response_time, 2), "error": str(error_status)}
        data = [f"{name} = {value}" for name, value in var_binds]
        return {"status": "success", "host": host, "port": port, "reachable": True,
                "response_time_ms": round(response_time, 2), "data": data}
    except Exception as error:
        return {"status": "failed", "host": host, "port": port, "reachable": False,
                "error": str(error)}
