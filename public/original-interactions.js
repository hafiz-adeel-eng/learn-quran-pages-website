(function () {
 'use strict';
 function initQuranlyHubMotion() {
  var root = document.querySelector('body.page-id-280 .elementor-280');
  if (!root || root.hasAttribute('data-qh-motion-bound') || document.body.classList.contains('elementor-editor-active')) return;
  root.setAttribute('data-qh-motion-bound', 'true');
  var preference = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  if ((preference && preference.matches) || !('IntersectionObserver' in window)) return;
  var nodes = Array.prototype.slice.call(root.querySelectorAll(
   '.qh-sky-benefit,.qh-sky-step,.qh-course-card,.qh-price-card,.qh-about-perks .elementor-icon-list-item,.elementor-element-3ab1e33,.elementor-element-c51fc7b'
  ));
  root.querySelectorAll('.elementor-widget-heading').forEach(function (node) {
   if (node.querySelector('h2') && !node.closest('.qh-hero-copy-compact,.qh-course-card,.qh-price-card,.qh-sky-step,.qh-sky-benefit')) nodes.push(node);
  });
  var groups = new WeakMap();
  var observer;
  function show(node) {
   node.classList.remove('qh-motion-pending');
   node.classList.add('qh-motion-enter');
   node.addEventListener('animationend', function cleanup(event) {
    if (event.target !== node || event.animationName !== 'qhScrollWelcome') return;
    node.classList.remove('qh-motion-enter');
    node.style.removeProperty('--qh-motion-delay');
    node.removeEventListener('animationend', cleanup);
   });
  }
  function showAll() {
   if (observer) observer.disconnect();
   nodes.forEach(function (node) {
    node.classList.remove('qh-motion-pending', 'qh-motion-enter');
    node.style.removeProperty('--qh-motion-delay');
   });
  }
  try {
   observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
     if (!entry.isIntersecting) return;
     show(entry.target);
     observer.unobserve(entry.target);
    });
   }, { threshold: 0.10, rootMargin: '0px 0px -24px 0px' });
   nodes.forEach(function (node) {
    var rect = node.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    var group = node.parentElement;
    var index = groups.get(group) || 0;
    groups.set(group, index + 1);
    node.style.setProperty('--qh-motion-delay', (Math.min(index, 3) * 75) + 'ms');
    if (rect.top < window.innerHeight) {
     show(node);
    } else {
     node.classList.add('qh-motion-pending');
     observer.observe(node);
    }
   });
   if (preference) {
    var onPreferenceChange = function (event) { if (event.matches) showAll(); };
    if (preference.addEventListener) preference.addEventListener('change', onPreferenceChange);
    else if (preference.addListener) preference.addListener(onPreferenceChange);
   }
   window.addEventListener('pageshow', function (event) { if (event.persisted) showAll(); });
  } catch (error) {
   showAll();
  }
 }
 if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initQuranlyHubMotion, { once: true });
 else initQuranlyHubMotion();
})();

(function(){var drawer=document.getElementById('qh-drawer');if(!drawer){return}
var opener=document.querySelector('[data-qh-open]');function setOpen(open){drawer.setAttribute('data-open',open?'true':'false');if(opener){opener.setAttribute('aria-expanded',open?'true':'false')}
document.body.style.overflow=open?'hidden':'';if(open){var first=drawer.querySelector('a,button');if(first){first.focus()}}else{drawer.querySelectorAll('[data-qh-toggle]').forEach(function(btn){btn.setAttribute('aria-expanded','false');var panel=document.getElementById(btn.getAttribute('aria-controls'));if(panel){panel.setAttribute('data-open','false')}})}}
if(opener){opener.addEventListener('click',function(){setOpen(!0)})}
drawer.querySelectorAll('[data-qh-close]').forEach(function(el){el.addEventListener('click',function(){setOpen(!1)})});drawer.querySelectorAll('a.qh-dlink').forEach(function(a){a.addEventListener('click',function(){setOpen(!1)})});drawer.querySelectorAll('[data-qh-toggle]').forEach(function(btn){btn.addEventListener('click',function(){var panel=document.getElementById(btn.getAttribute('aria-controls'));if(!panel){return}
var willOpen=panel.getAttribute('data-open')!=='true';panel.setAttribute('data-open',willOpen?'true':'false');btn.setAttribute('aria-expanded',willOpen?'true':'false')})});document.addEventListener('keydown',function(e){if(e.key==='Escape'){setOpen(!1)}});document.querySelectorAll('.qh-nav-item > .qh-nav-toggle, .qh-nav-drop .qh-nav-toggle').forEach(function(btn){var container=btn.parentElement;btn.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();var willOpen=!container.classList.contains('qh-nav-open');var siblingParent=container.parentElement;if(siblingParent){siblingParent.querySelectorAll(':scope > .qh-nav-item.qh-nav-open, :scope > li.qh-nav-open').forEach(function(sib){if(sib!==container){sib.classList.remove('qh-nav-open');var sibBtn=sib.querySelector(':scope > .qh-nav-toggle');if(sibBtn){sibBtn.setAttribute('aria-expanded','false')}}})}
container.classList.toggle('qh-nav-open',willOpen);btn.setAttribute('aria-expanded',willOpen?'true':'false')})});function qhCloseAllNavOpen(){document.querySelectorAll('.qh-nav-item.qh-nav-open, .qh-nav-drop li.qh-nav-open').forEach(function(el){el.classList.remove('qh-nav-open');var btn=el.querySelector(':scope > .qh-nav-toggle');if(btn){btn.setAttribute('aria-expanded','false')}})}
document.addEventListener('click',function(e){if(!e.target.closest('.qh-nav')){qhCloseAllNavOpen()}});document.addEventListener('keydown',function(e){if(e.key==='Escape'){qhCloseAllNavOpen()}});function qhNavHoverIntent(el,delay){var closeTimer=null;el.addEventListener('mouseenter',function(){if(closeTimer){clearTimeout(closeTimer);closeTimer=null}
el.classList.add('qh-nav-open')});el.addEventListener('mouseleave',function(){closeTimer=setTimeout(function(){el.classList.remove('qh-nav-open')},delay)})}
document.querySelectorAll('.qh-nav-item').forEach(function(item){qhNavHoverIntent(item,300)});var waBubble=document.getElementById('qh-wa-bubble');var reduceMotion=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;if(waBubble&&!reduceMotion){function qhWaCycle(){waBubble.classList.add('qh-wa-show');setTimeout(function(){waBubble.classList.remove('qh-wa-show')},4000)}
setTimeout(qhWaCycle,1500);setInterval(qhWaCycle,10000)}
document.querySelectorAll('[data-qh-lead-form]').forEach(function(form){form.addEventListener('submit',function(e){e.preventDefault();var name=(form.querySelector('[name="name"]')||{}).value||'';var course=(form.querySelector('[name="course"]')||{}).value||'';var wa=(form.querySelector('[name="whatsapp"]')||{}).value||'';var country=form.getAttribute('data-country')||'';var lines=['Assalamualaikum! Quran Hub, I\'d like to book a free trial class.'];if(name){lines.push('Name: '+name)}
if(country){lines.push('Country: '+country)}
if(course){lines.push('Course: '+course)}
if(wa){lines.push('My WhatsApp: '+wa)}
window.open('https://wa.me/923439486140?text='+encodeURIComponent(lines.join(' | ')),'_blank','noopener')})})})();

document.documentElement.classList.remove('no-js');(function(){var reduceMotion=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;var reveals=document.querySelectorAll('.qh-reveal');var hasIO='IntersectionObserver' in window;if(reveals.length){if(!hasIO||reduceMotion){reveals.forEach(function(el){el.classList.add('qh-in')})}else{var groupIndex={};var revealIO=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting){entry.target.classList.add('qh-in');revealIO.unobserve(entry.target)}})},{threshold:0.12,rootMargin:'0px 0px -40px 0px'});reveals.forEach(function(el){var parent=el.parentElement;var key=parent?(parent.dataset.qhGroupId||(parent.dataset.qhGroupId='g'+Object.keys(groupIndex).length)):'root';groupIndex[key]=(groupIndex[key]||0);el.style.transitionDelay=(Math.min(groupIndex[key],5)*70)+'ms';groupIndex[key]++;revealIO.observe(el)})}}
var counters=document.querySelectorAll('.qh-counter');if(counters.length){var runCounter=function(wrapperEl){var el=wrapperEl.querySelector('.elementor-heading-title')||wrapperEl;var text=(el.textContent||'').trim();var match=text.match(/^(\d+)(.*)$/);if(!match){return}
var target=parseInt(match[1],10);var suffix=match[2];if(reduceMotion){el.textContent=target+suffix;return}
var duration=1100;var start=null;function tick(ts){if(start===null){start=ts}
var progress=Math.min((ts-start)/duration,1);var eased=1-Math.pow(1-progress,3);el.textContent=Math.floor(eased*target)+suffix;if(progress<1){window.requestAnimationFrame(tick)}else{el.textContent=target+suffix}}
window.requestAnimationFrame(tick)};if(!hasIO){counters.forEach(runCounter)}else{var counterIO=new IntersectionObserver(function(entries){entries.forEach(function(entry){if(entry.isIntersecting){runCounter(entry.target);counterIO.unobserve(entry.target)}})},{threshold:0.5});counters.forEach(function(el){counterIO.observe(el)})}}})();