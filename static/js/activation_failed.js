document.addEventListener('DOMContentLoaded', function() {
    // 自动将焦点放在第一个按钮上
    var buttons = document.querySelectorAll('.btn');
    if (buttons.length > 0) {
        buttons[0].focus();
    }

    // 你可以在这里添加更多的JavaScript逻辑
    // 例如，实现页面加载后自动关闭提示信息的功能
    setTimeout(function() {
        var flashes = document.querySelectorAll('.flashes li');
        if (flashes.length > 0) {
            flashes[0].style.opacity = 0;
            setTimeout(function() {
                flashes[0].style.display = 'none';
            }, 300);
        }
    }, 3000); // 3000 毫秒（3秒）后执行
});