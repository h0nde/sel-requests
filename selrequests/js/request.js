var resp = await fetch(
    arguments[1],
    {
        method: arguments[0],
        body: arguments[2],
        headers: arguments[3],
        mode: arguments[4],
        credentials: arguments[5]
    }
)
var body = await resp.text()
var headers = {}

resp.headers.forEach((v,k)=>{
    headers[k] = v
})

return {
    url: resp.url,
    ok: resp.ok,
    status_code: resp.status,
    reason: resp.statusText,
    text: body,
    headers: headers
}