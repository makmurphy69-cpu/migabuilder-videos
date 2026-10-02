// Static assets ignore Range requests, but Safari only plays videos that
// support them (and every browser needs them to skip ahead). Only *.mp4
// requests run this script (see run_worker_first in wrangler.jsonc); posters
// are served as plain static files.
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const res = await env.ASSETS.fetch(new Request(url, { method: request.method === 'HEAD' ? 'HEAD' : 'GET' }));
    if (res.status !== 200) return res;
    const headers = new Headers(res.headers);
    headers.set('Accept-Ranges', 'bytes');
    headers.set('Access-Control-Allow-Origin', '*');
    headers.set('Cache-Control', 'public, max-age=86400');
    const range = /^bytes=(\d*)-(\d*)$/.exec((request.headers.get('Range') || '').trim());
    if (!range || request.method === 'HEAD' || (range[1] === '' && range[2] === '')) return new Response(res.body, { status: 200, headers });
    const body = await res.arrayBuffer();
    const size = body.byteLength;
    let start, end;
    if (range[1] === '') { start = Math.max(0, size - Number(range[2])); end = size - 1; }
    else { start = Number(range[1]); end = range[2] === '' ? size - 1 : Math.min(Number(range[2]), size - 1); }
    if (start >= size || start > end) return new Response(null, { status: 416, headers: { 'Content-Range': 'bytes */' + size } });
    headers.set('Content-Range', 'bytes ' + start + '-' + end + '/' + size);
    headers.set('Content-Length', String(end - start + 1));
    return new Response(body.slice(start, end + 1), { status: 206, headers });
  }
};
