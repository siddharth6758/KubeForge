const state = { user: null, editingId: null, modalTimer: null, pollTimer: null, notifications: [] };
const $ = (id) => document.getElementById(id);
const showStatus = (id, message, error = true) => { const node = $(id); node.textContent = message; node.style.color = error ? 'var(--coral)' : 'var(--mint-dark)'; };
const notificationStorageKey = () => `pulseboard-notifications-${state.user.user_id}`;

async function request(path, options = {}) {
  const response = await fetch(path, { headers: { 'Content-Type': 'application/json' }, ...options });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || body.message || `Request failed (${response.status})`);
  return body;
}

async function enterWorkspace(user) {
  state.user = user;
  localStorage.setItem('pulseboard-user', JSON.stringify(user));
  $('loginView').classList.add('hidden');
  $('appView').classList.remove('hidden');
  $('userChip').textContent = `USER #${state.user.user_id} / ${state.user.username}`;
  try { state.notifications = JSON.parse(localStorage.getItem(notificationStorageKey()) || '[]'); } catch (error) { state.notifications = []; }
  renderNotifications();
  await loadNotifications();
  clearInterval(state.pollTimer);
  state.pollTimer = setInterval(loadNotifications, 2000);
}

$('loginForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  showStatus('loginStatus', 'Connecting...', false);
  try {
    await enterWorkspace(await request('/user-create/', { method: 'POST', body: JSON.stringify($('username').value.trim()) }));
  } catch (error) { showStatus('loginStatus', error.message); }
});

async function loadNotifications() {
  try {
    const result = await request(`/pending-notification/${state.user.user_id}`);
    const pending = Array.isArray(result) ? result : (result.notifications || result.items || []);
    const pendingIds = new Set(pending.map((notification) => notification.notification_id));
    const notified = state.notifications.filter((notification) => !pendingIds.has(notification.notification_id) && notification.is_notified !== true);
    const due = pending.find((notification) => notification.is_notified === true || new Date(notification.scheduled_at).getTime() <= Date.now() && !state.notifications.some((saved) => saved.notification_id === notification.notification_id && saved.is_notified === true));
    if (notified.length || due) showNotificationModal(notified[0] || due);
    const pendingWithStatus = pending.map((notification) => {
      const saved = state.notifications.find((item) => item.notification_id === notification.notification_id);
      const hasReachedTime = notification.scheduled_at && new Date(notification.scheduled_at).getTime() <= Date.now();
      return { ...notification, is_notified: notification.is_notified === true || saved?.is_notified === true || hasReachedTime };
    });
    state.notifications = [...pendingWithStatus, ...state.notifications.filter((notification) => !pendingIds.has(notification.notification_id)).map((notification) => ({ ...notification, is_notified: true }))];
    saveNotifications();
    renderNotifications();
  } catch (error) { showStatus('formStatus', error.message); }
}

function renderNotifications() {
  const list = $('notificationList');
  $('notificationCount').textContent = `${state.notifications.length} ${state.notifications.length === 1 ? 'item' : 'items'}`;
  list.innerHTML = state.notifications.length ? state.notifications.map(renderNotification).join('') : '<div class="empty">Nothing scheduled yet.</div>';
}

function saveNotifications() {
  localStorage.setItem(notificationStorageKey(), JSON.stringify(state.notifications));
}

function renderNotification(notification) {
  const date = notification.scheduled_at ? new Date(notification.scheduled_at).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' }) : 'No date';
  const badge = notification.is_notified === true ? '<span class="notified-badge">Notified</span>' : '';
  return `<article class="notification-card"><div class="card-meta"><span class="card-meta-left"><span>${escapeHtml(date)}</span>${badge}</span><span>#${notification.notification_id}</span></div><h3>${escapeHtml(notification.title)}</h3><p>${escapeHtml(notification.description || 'No description')}</p><div class="card-actions"><button type="button" onclick="editNotification(${notification.notification_id})">Edit</button><button type="button" class="danger" onclick="deleteNotification(${notification.notification_id})">Delete</button></div></article>`;
}

function showNotificationModal(notification) {
  clearTimeout(state.modalTimer);
  $('modalTitle').textContent = notification.title || 'Notification';
  $('modalDescription').textContent = notification.description || 'No description';
  $('notificationModal').classList.remove('hidden');
  state.modalTimer = setTimeout(() => $('notificationModal').classList.add('hidden'), 10000);
}

$('notificationForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const payload = { title: $('title').value.trim(), description: $('description').value.trim(), scheduled_at: new Date($('scheduledAt').value).toISOString() };
  const wasEditing = state.editingId;
  try {
    const path = wasEditing ? `/notification-update/${wasEditing}` : '/notification/';
    const savedNotification = await request(path, { method: wasEditing ? 'PATCH' : 'POST', body: JSON.stringify(wasEditing ? payload : { user_id: state.user.user_id, ...payload }) });
    state.notifications = [...state.notifications.filter((notification) => notification.notification_id !== savedNotification.notification_id), savedNotification];
    saveNotifications();
    resetForm(); showStatus('formStatus', wasEditing ? 'Notification updated.' : 'Notification created.', false); await loadNotifications();
  } catch (error) { showStatus('formStatus', error.message); }
});

window.editNotification = async (id) => {
  try {
    const item = await request(`/notification/${id}`);
    state.editingId = id; $('formEyebrow').textContent = '02 / revise'; $('formTitle').textContent = 'Edit notification'; $('saveButton').textContent = 'Save changes'; $('cancelButton').classList.remove('hidden');
    $('title').value = item.title || ''; $('description').value = item.description || ''; $('scheduledAt').value = item.scheduled_at ? new Date(item.scheduled_at).toISOString().slice(0, 16) : ''; $('title').focus();
  } catch (error) { showStatus('formStatus', error.message); }
};

window.deleteNotification = async (id) => {
  if (!window.confirm('Delete this notification?')) return;
  try { await request(`/notification/${id}`, { method: 'DELETE' }); state.notifications = state.notifications.filter((notification) => notification.notification_id !== id); saveNotifications(); renderNotifications(); await loadNotifications(); } catch (error) { showStatus('formStatus', error.message); }
};

$('cancelButton').addEventListener('click', resetForm);
function resetForm() { state.editingId = null; $('notificationForm').reset(); $('formEyebrow').textContent = '02 / compose'; $('formTitle').textContent = 'Create a notification'; $('saveButton').textContent = 'Create notification'; $('cancelButton').classList.add('hidden'); }
function escapeHtml(value) { return String(value).replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character])); }

window.addEventListener('DOMContentLoaded', async () => {
  try {
    const savedUser = JSON.parse(localStorage.getItem('pulseboard-user'));
    if (!savedUser || !savedUser.user_id) return;
    await enterWorkspace(await request(`/user/${savedUser.user_id}`));
  } catch (error) {
    localStorage.removeItem('pulseboard-user');
  }
});
