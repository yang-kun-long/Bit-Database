window.addEventListener('beforeunload', function (e) {
    // 这里可以放一些自定义的逻辑，比如确认对话框等
    // 如果使用了确认对话框，需要返回一个字符串，否则某些浏览器会忽略这个事件

    // 发送登出请求
    fetch('/logout', { method: 'POST' })
      .then(response => {
        if (!response.ok) {
          throw new Error('登出失败');
        }
        return response.json();
      })
      .then(data => {
        console.log('登出成功', data);
      })
      .catch(error => {
        console.error('登出时发生错误:', error);
      });

    // 返回空字符串，避免某些浏览器忽略事件
    return '';
});