// 谣言检测助手：弹出框逻辑
const RUMOR_URL = 'https://youngthomas37-beep.github.io/rumor.html';

document.getElementById('go').addEventListener('click', () => {
  const text = document.getElementById('text').value.trim();
  if (!text) return;
  chrome.tabs.create({ url: RUMOR_URL + '?text=' + encodeURIComponent(text) });
});
