function uoe(a) {
  for (var a = a.split(",").map(function (a) {
    return parseInt(a, 10)
  }), b = a.slice(1, a[0] + 1), g = (a.length - 1 - b.length) / 2, d = [], c = 0; c < g; ++c) {
    var e = b.length + 1 + 2 * c,
      f = a[e];
    d[f] = String.fromCharCode((256 + a[e + 1] - b[f % b.length]) % 256)
  }
  return d.join("")
};

$(document).ready(function () {
  $("a.oe-link").each(function () {
    if ($(this).attr("data-oe")) {
      var a = uoe($(this).attr("data-oe"));
      $(this).removeAttr("data-oe")
             .attr("href", "mailto:" + a)
             .text(a);
    }
  });

  $("span.oe-text").each(function () {
    if ($(this).attr("data-oe")) {
      var a = uoe($(this).attr("data-oe"));
      $(this).removeAttr("data-oe")
             .text(a);
    }
  });
});
