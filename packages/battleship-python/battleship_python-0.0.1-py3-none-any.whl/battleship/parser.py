"""
Pure functional JSON-RPC

Should not handle codec nor IO
"""

DEFAULT_VERSION = "2.0"


def RequestMessage(id, method, params=None, jsonrpc=DEFAULT_VERSION):
    result = {"id": id, "method": method, "jsonrpc": jsonrpc}
    if params is not None:
        result["params"] = params
    return result


def NotificationMessage(method, params=None, jsonrpc=DEFAULT_VERSION):
    result = {"method": method, "jsonrpc": jsonrpc}
    if params is not None:
        result["params"] = params
    return result


def ResultMessage(id, result, jsonrpc=DEFAULT_VERSION):
    return {"id": id, "result": result, "jsonrpc": jsonrpc}


def ErrorMessage(id, code, message, data=None, jsonrpc=DEFAULT_VERSION):
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"id": id, "error": error, "jsonrpc": jsonrpc}


def ParseError(data=None, jsonrpc=DEFAULT_VERSION):
    return ErrorMessage(None, -32700, "Parse error", data=data, jsonrpc=jsonrpc)


def InvalidRequest(id=None, data=None, jsonrpc=DEFAULT_VERSION):
    return ErrorMessage(id, -32600, "Invalid request", data=data, jsonrpc=jsonrpc)


def MethodNotFound(id, data=None, jsonrpc=DEFAULT_VERSION):
    return ErrorMessage(id, -32601, "Method not found", data=data, jsonrpc=jsonrpc)


def InvalidParams(id, data=None, jsonrpc=DEFAULT_VERSION):
    return ErrorMessage(id, -32602, "Invalid params", data=data, jsonrpc=jsonrpc)


def InternalError(id, data=None, jsonrpc=DEFAULT_VERSION):
    return ErrorMessage(id, -32603, "Internal error", data=data, jsonrpc=jsonrpc)


def ServerError(id, code, message, data=None, jsonrpc=DEFAULT_VERSION):
    assert -32100 < code <= -3200
    return ErrorMessage(id, code, message, data=data, jsonrpc=jsonrpc)
