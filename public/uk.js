(() => {
  'use strict';
  const search = document.getElementById('city-search');
  if (search) search.addEventListener('input', () => {
    const query = search.value.toLocaleLowerCase('en-GB').trim();
    let count = 0;
    document.querySelectorAll('[data-city]').forEach(link => {
      link.hidden = !link.dataset.city.includes(query);
      if (!link.hidden) count++;
    });
    document.querySelectorAll('.qhuk-directory-nation').forEach(section => {
      section.hidden = !section.querySelector('[data-city]:not([hidden])');
    });
    document.getElementById('city-count').textContent = count + (count === 1 ? ' location found.' : ' locations found.');
  });
  const form = document.querySelector('[data-uk-enquiry]');
  if (form) form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const fields = [['name','Name'],['location','Location'],['learner','Learner'],['level','Starting point'],['times','UK-time windows'],['message','Teacher or language preference']];
    const message = 'Assalamualaikum! Quran Hub, I would like a free trial.\n' + fields.map(([key,label]) => label + ': ' + String(data.get(key) || '').trim()).join('\n');
    window.location.assign('https://wa.me/923439486140?text=' + encodeURIComponent(message));
  });
})();
