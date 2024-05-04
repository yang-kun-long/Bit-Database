document.addEventListener('DOMContentLoaded', function() {
    // 添加事件监听器到上传按钮
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();
        // 获取上传的文件
        var file = document.querySelector('input[type="file"]').files[0];
        var type = document.querySelector('select[name="type"]').value;
        if (file) {
            // 准备发送文件到服务器
            var formData = new FormData(event.target);
            formData.append('type', type); // 添加类型到表单数据中
            // 发送文件到服务器
            fetch('/import_users', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('成功导入用户：', data);
                // 处理成功导入用户后的逻辑
            })
            .catch(error => {
                console.error('导入用户失败：', error);
                // 处理导入用户失败后的逻辑
            });
        }
    });
});
