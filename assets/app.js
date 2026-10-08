document.addEventListener('DOMContentLoaded', () => {
  const yearNode = document.getElementById('year');
  if (yearNode) {
    yearNode.textContent = new Date().getFullYear();
  }

  const panel = document.getElementById('commandPanel');
  const toggles = document.querySelectorAll('.command-toggle');
  const closeButton = document.querySelector('.close-panel');

  const openPanel = () => {
    if (!panel) return;
    panel.classList.add('visible');
    panel.setAttribute('aria-hidden', 'false');
  };

  const closePanel = () => {
    if (!panel) return;
    panel.classList.remove('visible');
    panel.setAttribute('aria-hidden', 'true');
  };

  toggles.forEach((button) => {
    button.addEventListener('click', openPanel);
  });

  if (closeButton) {
    closeButton.addEventListener('click', closePanel);
  }

  if (panel) {
    panel.addEventListener('click', (event) => {
      if (event.target === panel) closePanel();
    });
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && panel && panel.classList.contains('visible')) {
      closePanel();
    }
  });

  document.querySelectorAll('.command-row button').forEach((button) => {
    button.addEventListener('click', async () => {
      const code = button.closest('.command-row')?.querySelector('code')?.textContent;
      if (!code) return;

      try {
        await navigator.clipboard.writeText(code);
        const original = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => {
          button.textContent = original;
        }, 1200);
      } catch (error) {
        button.textContent = 'Copy failed';
      }
    });
  });
});
