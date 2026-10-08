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

  const root = document.body.dataset.root || '.';
  const page = document.body.dataset.page || '';

  const loadJSON = async (path) => {
    const response = await fetch(`${root}/${path}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Failed to load ${path}`);
    return response.json();
  };

  const statusClassMap = {
    todo: 'status-soft',
    doing: 'status-warning',
    done: 'status-success',
    pass: 'status-success',
    warning: 'status-warning',
    fail: 'status-danger',
    urgent: 'status-warning',
    high: 'status-warning',
    medium: 'status-info',
    low: 'status-soft',
    pinned: 'status-soft'
  };

  const statusLabel = (value) => {
    if (!value) return 'Open';
    const labels = {
      todo: 'To do',
      doing: 'In progress',
      done: 'Done',
      pass: 'Pass',
      warning: 'Warning',
      fail: 'Fail',
      urgent: 'Urgent',
      high: 'High',
      medium: 'Medium',
      low: 'Low',
      pinned: 'Pinned'
    };
    return labels[value] || String(value).replace(/-/g, ' ');
  };

  const renderHomeStats = (tasks, notes, audits, codes) => {
    const openTasks = (tasks || []).filter((task) => !(task.status === 'done' || task.status === 'completed')).length;
    const noteCount = (notes || []).length;
    const auditCount = (audits || []).length;
    const codeCount = Array.isArray(codes) ? codes.length : 523;

    const setValue = (id, value) => {
      const el = document.getElementById(id);
      if (el) el.textContent = value;
    };

    setValue('stat-tasks', String(openTasks));
    setValue('stat-notes', String(noteCount));
    setValue('stat-audits', String(auditCount).padStart(2, '0'));
    setValue('stat-code', String(codeCount));

    const kpiTasks = document.getElementById('kpi-tasks');
    if (kpiTasks) kpiTasks.textContent = String(openTasks);
    const kpiNotes = document.getElementById('kpi-notes');
    if (kpiNotes) kpiNotes.textContent = String(noteCount);
    const kpiAudits = document.getElementById('kpi-audits');
    if (kpiAudits) kpiAudits.textContent = String(auditCount).padStart(2, '0');
    const kpiCode = document.getElementById('kpi-code');
    if (kpiCode) kpiCode.textContent = String(codeCount);
  };

  const renderTaskTable = (tasks = []) => {
    const tbody = document.getElementById('task-table-body');
    if (!tbody) return;

    tbody.innerHTML = tasks.slice(0, 8).map((task) => {
      const taskId = task.id || 'TSK-0000';
      const title = task.title || task.name || 'Untitled task';
      const priority = String(task.priority || 'medium');
      const status = String(task.status || 'todo');
      const owner = task.owner || 'MJ Ahmad';
      const due = task.due || 'TBD';
      return `
        <tr>
          <td>${taskId}</td>
          <td>${title}</td>
          <td><span class="table-tag">${statusLabel(priority)}</span></td>
          <td><span class="status-pill ${statusClassMap[status] || 'status-soft'}">${statusLabel(status)}</span></td>
          <td>${owner}</td>
          <td>${due}</td>
        </tr>
      `;
    }).join('');
  };

  const renderNotesGrid = (notes = []) => {
    const grid = document.getElementById('notes-grid');
    if (!grid) return;

    grid.innerHTML = notes.slice(0, 6).map((note) => {
      const title = note.title || note.name || 'Untitled note';
      const summary = note.body || note.summary || 'Operational note';
      const status = note.pinned ? 'pinned' : (note.status || 'updated');
      return `
        <article class="info-card">
          <h3>${title}</h3>
          <p>${summary}</p>
          <span class="status-pill ${statusClassMap[status] || 'status-soft'}">${statusLabel(status)}</span>
        </article>
      `;
    }).join('');
  };

  const renderAuditGrid = (audits = []) => {
    const grid = document.getElementById('audit-grid');
    if (!grid) return;

    grid.innerHTML = audits.slice(0, 6).map((audit) => {
      const title = audit.title || audit.name || 'Audit review';
      const summary = audit.summary || audit.findings || 'Audit item pending review';
      const result = String(audit.result || 'warning');
      return `
        <article class="info-card">
          <h3>${title}</h3>
          <p>${summary}</p>
          <span class="status-pill ${statusClassMap[result] || 'status-soft'}">${statusLabel(result)}</span>
        </article>
      `;
    }).join('');
  };

  const renderCodeGrid = (codes = []) => {
    const grid = document.getElementById('code-grid');
    if (!grid) return;

    grid.innerHTML = codes.slice(0, 6).map((code) => {
      const title = code.title || code.name || 'Code item';
      const desc = code.description || code.desc || 'Repository asset';
      const lang = code.language || 'HTML';
      return `
        <article class="info-card">
          <h3>${title}</h3>
          <p>${desc}</p>
          <span class="table-tag">${lang}</span>
        </article>
      `;
    }).join('');
  };

  const renderRegistryRows = (tasks = [], notes = [], audits = [], codes = []) => {
    const tbody = document.getElementById('registry-table-body');
    if (!tbody) return;

    const rows = [
      ...tasks.map((item) => ({
        type: 'Task',
        id: item.id || 'TSK-0000',
        name: item.title || item.name || 'Untitled task',
        status: item.status || 'todo',
        updated: item.updated_at || item.due || '—'
      })),
      ...notes.map((item) => ({
        type: 'Note',
        id: item.id || 'NOT-0000',
        name: item.title || item.name || 'Untitled note',
        status: item.pinned ? 'pinned' : (item.status || 'updated'),
        updated: item.updated_at || '—'
      })),
      ...audits.map((item) => ({
        type: 'Audit',
        id: item.id || 'AUD-0000',
        name: item.title || item.name || 'Audit item',
        status: item.result || 'warning',
        updated: item.updated_at || '—'
      })),
      ...codes.map((item) => ({
        type: 'Code',
        id: item.id || 'CDE-0000',
        name: item.title || item.name || 'Code item',
        status: item.status || 'updated',
        updated: item.updated_at || '—'
      }))
    ].slice(0, 9);

    tbody.innerHTML = rows.map((row) => `
      <tr>
        <td>${row.id}</td>
        <td>${row.type}</td>
        <td>${row.name}</td>
        <td><span class="status-pill ${statusClassMap[row.status] || 'status-soft'}">${statusLabel(row.status)}</span></td>
        <td>${row.updated}</td>
      </tr>
    `).join('');
  };

  try {
    const [meta, tasks, notes, audits, codes] = await Promise.all([
      loadJSON('data/meta.json').catch(() => ({})),
      loadJSON('data/tasks.json').then((payload) => payload.tasks || payload || []).catch(() => []),
      loadJSON('data/notes.json').then((payload) => payload.notes || payload || []).catch(() => []),
      loadJSON('data/audits.json').then((payload) => payload.audits || payload || []).catch(() => []),
      loadJSON('data/codes.json').then((payload) => payload.codes || payload || []).catch(() => [])
    ]);

    renderHomeStats(tasks, notes, audits, codes);
    renderTaskTable(tasks);
    renderNotesGrid(notes);
    renderAuditGrid(audits);
    renderCodeGrid(codes);
    renderRegistryRows(tasks, notes, audits, codes);

    if (document.getElementById('stat-tasks') && meta && meta.meta && meta.meta.title) {
      document.title = `${meta.meta.title || 'MJ Ahmad'} | Registry`;
    }
  } catch (error) {
    console.warn('Data failed to load for dynamic registry UI:', error);
  }
});
