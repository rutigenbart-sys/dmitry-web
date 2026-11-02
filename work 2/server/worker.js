// Cloudflare Worker: приём заявок -> Telegram (бесплатно, подходит для GitHub Pages).
// Секреты: wrangler secret put BOT_TOKEN ; wrangler secret put CHAT_ID
const ALLOWED = ["https://dmitry-web.ru", "https://www.dmitry-web.ru"];
export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    const h = {
      "Access-Control-Allow-Origin": ALLOWED.includes(origin) ? origin : ALLOWED[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Content-Type": "application/json; charset=utf-8", "Vary": "Origin",
    };
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: h });
    if (req.method !== "POST" || !ALLOWED.includes(origin)) return new Response('{"ok":false}', { status: 403, headers: h });
    let d; try { d = JSON.parse((await req.text()).slice(0, 20000)); } catch { return new Response('{"ok":false}', { status: 400, headers: h }); }
    if (d.website || (typeof d.t === "number" && d.t < 1200)) return new Response('{"ok":true}', { headers: h });
    let text = String(d.text || "").trim();
    if (!text || text.length > 3500) return new Response('{"ok":false}', { status: 400, headers: h });
    text += "\nСтраница: " + String(d.page || "").slice(0, 200);
    const r = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/sendMessage`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: env.CHAT_ID, text, disable_web_page_preview: true }),
    });
    return new Response(r.ok ? '{"ok":true}' : '{"ok":false}', { status: r.ok ? 200 : 502, headers: h });
  },
};
