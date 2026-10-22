/* Track outbound accommodation-provider referrals in GA4. */
(function () {
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    var destination;
    try { destination = new URL(link.href, window.location.href); } catch (_) { return; }
    if (!/^https?:$/.test(destination.protocol) || destination.origin === window.location.origin) return;
    var isProvider = link.classList.contains('outbound') ||
      destination.searchParams.get('utm_source') === 'studentaccommodationbristol';
    if (!isProvider || typeof window.gtag !== 'function') return;
    var host = destination.hostname.replace(/^www\./, '');
    var provider = host.indexOf('thisisfresh.com') !== -1 ? 'Fresh' :
      host.indexOf('studentroost.co.uk') !== -1 ? 'Student Roost' :
      host.indexOf('iqstudentaccommodation.com') !== -1 ? 'iQ' :
      host.indexOf('unitestudents.com') !== -1 ? 'Unite Students' :
      host.indexOf('yugo.com') !== -1 ? 'Yugo' : host;
    window.gtag('event', 'provider_click', {
      provider_name: provider,
      destination_url: destination.href,
      source_page: window.location.pathname,
      transport_type: 'beacon'
    });
  }, true);
})();
