async function fettch(method, url, body: any = undefined) {
    let token = localStorage.getItem('xtoken');

    url = '/api' + url;

    let rq = await fetch(url, {
        method: method,
        headers: {
            'Content-type': 'application/json',
            'X-Token': token || '',
        },
        body: body && JSON.stringify(body) || undefined,
    });

    return await rq.json().then(data => {
        if (typeof data === 'object' && data && ('errors' in data || 'detail' in data)) {
            console.error('API SAID NO:', data.errors || data.detail);
            return undefined;
        } else {
            return data;
        }
    });
}

export function event(url, callback) {
    let token = localStorage.getItem('xtoken');
    let source = new EventSource('/api' + url + '?token=' + token);

    source.onopen = () => {
        console.log('EventSource connected');
    }

    source.addEventListener('message', function (event) {
        console.log('incoming', event.data);
        callback(JSON.parse(event.data));
    });

    source.onerror = (error) => {
        console.error('EventSource failed', error)
        source.close()
    }

    return () => source.close();
}

export let get = fettch.bind(undefined, 'GET');
export let post = fettch.bind(undefined, 'POST');

window['gg'] = get;
window['pp'] = post;