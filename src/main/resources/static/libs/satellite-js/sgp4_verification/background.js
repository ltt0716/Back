chrome.app.runtime.onLaunched.addListener(function(launchData) {
  chrome.app.window.create('index1.html', {width: 1400, height: 850}, function(win) {
    win.contentWindow.launchData = launchData;
  });
});
