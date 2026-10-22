var C = "pp-v1";
var CORE = ["./", "index.html", "fonts.css", "manifest.webmanifest", "icon-192.png", "icon-512.png"];
self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(C).then(function (c) {
      return Promise.all(CORE.map(function (u) { return c.add(u).catch(function () {}); }));
    }).then(function () { return self.skipWaiting(); })
  );
});
self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (k) {
      return Promise.all(k.filter(function (x) { return x !== C; }).map(function (x) { return caches.delete(x); }));
    }).then(function () { return self.clients.claim(); })
  );
});
self.addEventListener("fetch", function (e) {
  var r = e.request;
  if (r.method !== "GET" || new URL(r.url).origin !== location.origin) return;
  e.respondWith(
    caches.open(C).then(function (c) {
      return c.match(r, { ignoreSearch: true }).then(function (hit) {
        var net = fetch(r).then(function (res) {
          if (res && res.ok) c.put(r, res.clone());
          return res;
        }).catch(function () {
          return hit || (r.mode === "navigate" ? c.match("index.html") : null) || Response.error();
        });
        return hit || net;
      });
    })
  );
});
