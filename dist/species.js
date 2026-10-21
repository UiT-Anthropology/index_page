// Progressive enhancement: all records and links remain available without JS.
for (const group of document.querySelectorAll('[data-filter-group]')) {
  const buttons = [...group.querySelectorAll('[data-filter]')];
  const items = [...group.querySelectorAll('[data-filter-item]')];
  const count = group.querySelector('.filter-count');
  function select(value) {
    if (!buttons.some(button => button.dataset.filter === value)) value = 'all';
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === value));
    let shown = 0;
    for (const item of items) {
      item.hidden = value !== 'all' && !item.dataset.region.split(' ').includes(value);
      if (!item.hidden) shown++;
    }
    if (count) count.textContent = `${shown} ${shown === 1 ? 'entry' : 'entries'}`;
  }
  for (const button of buttons) button.addEventListener('click', () => select(button.dataset.filter));
  // A contributor deep link takes precedence over a remembered case filter.
  select(new URLSearchParams(location.search).get('region') || 'all');
}
