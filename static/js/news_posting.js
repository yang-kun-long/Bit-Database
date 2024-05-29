$(document).ready(function() {
    // 插入图片按钮的点击事件
    $('#insertImageBtn').click(function() {
        var fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);

        fileInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            var formData = new FormData();
            formData.append('image', file);

            // 通过 AJAX 发送图片到 Flask 服务器的 upload-image 端点
            $.ajax({
                url: '/upload-image', // Flask API 端点
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    if(response.success) {
                        // 上传成功，获取图片路径并插入到编辑器中
                        var imgSrc = response.filepath;
                        var range = window.getSelection().getRangeAt(0);
                        var img = document.createElement('img');
                        img.src = imgSrc;
                        img.style.maxWidth = '100%'; // 设置图片宽度
                        img.style.height = 'auto';
                        range.insertNode(img);
                        window.getSelection().removeAllRanges();
                    } else {
                        alert('图片上传失败：' + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    alert('图片上传异常：' + error);
                }
            });
        });

        fileInput.click();
    });

    // 其他代码，如插入封面按钮的点击事件和表单提交事件保持不变
    // ...

    // 表单提交事件
      $('#newsForm').submit(function(e) {
        e.preventDefault(); // 阻止表单的默认提交行为

        var formData = new FormData(this); // 创建FormData对象
        var content = $('#content').text().trim(); // 获取内容字段的文本
        var link = $('#link').val(); // 获取外部链接

        // 检查内容字段是否为空，如果为空且没有外部链接，则提示用户
        if (!content && !link) {
            alert('请提供内容或输入有效的外部链接。');
            return;
        }

        // 如果内容字段不为空，则不需要外部链接，移除链接字段
        if (content) {
            formData.delete('link');
        }

        // 附件可以为空，不需要进行额外的检查

        // 使用jQuery的ajax方法发送表单数据，包括内容或链接
        $.ajax({
            url: '/api/submit-news', // 服务器端接收提交的URL
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                console.log('新闻提交成功', response);
                // 提交成功后的逻辑，例如清空表单或提示用户
                // ...
            },
            error: function(xhr, status, error) {
                console.error('新闻提交失败', error);
                // 提交失败后的逻辑，例如显示错误信息
                // ...
            }
        });
    });
});