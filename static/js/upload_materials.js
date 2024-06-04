// upload_materials.js
$(document).ready(function() {
    $('#uploadForm').submit(function(e) {
        e.preventDefault(); // 阻止表单的默认提交行为
        console.log('上传资料');
        var formData = new FormData(this); // 创建FormData对象
        // 打印FormData对象内容
        for (var pair of formData.entries()) {
            console.log(pair[0] + ', '+ pair[1]);
        }

        // 上传文件
        $.ajax({
            url: '/api/materials/upload', // API地址
            type: 'POST',
            data: formData,
            processData: false, // 告诉jQuery不要处理数据
            contentType: false, // 告诉jQuery不要设置内容类型
            success: function(data) {
                // 处理成功响应
                console.log('资料上传成功:', data);
                alert('资料上传成功');
                location.reload(); // 刷新页面
            },
            error: function(xhr, status, error) {
                // 处理错误响应
                console.error('资料上传失败:', error);
                alert('资料上传失败，请稍后重试');
                location.reload(); // 刷新页面
            }
        });
    });
});