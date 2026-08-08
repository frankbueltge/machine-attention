'use strict';
function pad(n) { return String(n).padStart(2, '0'); }
function fmt(ms) {
  var s = Math.max(0, Math.floor(ms / 1000));
  var d = Math.floor(s / 86400);
  return (d > 0 ? d + 'd ' : '') + pad(Math.floor(s % 86400 / 3600)) + ':' +
    pad(Math.floor(s % 3600 / 60)) + ':' + pad(s % 60);
}
function parseUTC(iso) {
  if (!iso) return NaN;
  return Date.parse(/Z|[+-]\d\d:\d\d$/.test(iso) ? iso : iso + 'Z');
}
function nextReading(now) {
  var next = new Date(now);
  next.setUTCHours(5, 45, 0, 0);
  if (next.getTime() <= now) next.setUTCDate(next.getUTCDate() + 1);
  return next.getTime();
}
function tick() {
  var now = Date.now();
  var countdown = document.getElementById('countdown');
  if (countdown) countdown.textContent = fmt(nextReading(now) - now);
  document.querySelectorAll('.clock').forEach(function (c) {
    var to = parseUTC(c.getAttribute('data-to'));
    var from = parseUTC(c.getAttribute('data-from'));
    if (!isNaN(to)) {
      c.textContent = to > now
        ? fmt(to - now) + ' left in the announced danger window'
        : 'danger window passed ' + fmt(now - to) + ' ago — warning still active';
    } else if (!isNaN(from)) {
      c.textContent = 'ongoing for ' + fmt(now - from);
    }
  });
}
tick(); setInterval(tick, 1000);

var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var traces = Array.prototype.slice.call(document.querySelectorAll('.trace[data-cycle]'));
if (!reduced && traces.length > 3) {
  traces.forEach(function (t, i) { if (i >= 3) t.classList.add('is-hidden'); });
  var ti = 0;
  setInterval(function () {
    traces[ti % traces.length].classList.add('is-hidden');
    traces[(ti + 3) % traces.length].classList.remove('is-hidden');
    ti += 1;
  }, 6000);
}
