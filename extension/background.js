// 谣言检测助手：后台服务，负责右键菜单
const RUMOR_URL = 'https://youngthomas37-beep.github.io/rumor.html';

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'detect-rumor',
    title: '检测是否谣言',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === 'detect-rumor' && info.selectionText) {
    chrome.tabs.create({
      url: RUMOR_URL + '?text=' + encodeURIComponent(info.selectionText)
    });
  }
});
