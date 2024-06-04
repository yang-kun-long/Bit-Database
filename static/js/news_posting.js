var globalData = {
    cover: null, // 封面图片
    files: [] // 附件文件列表
}; // 全局变量
$(document).ready(function () {
    // 插入图片按钮的点击事件
    $('#insertImageBtn').click(function () {
        var fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);

        fileInput.addEventListener('change', function (e) {
            var file = e.target.files[0];
            var formData = new FormData();
            formData.append('image', file);

            // 通过 AJAX 发送图片到 Flask 服务器的 upload-image 端点
            $.ajax({
                url: '/api/news/upload-image', // Flask API 端点
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function (response) {
                    if (response.success) {
                        // 上传成功，获取图片路径并插入到编辑器中
                        var imgSrc = response.filepath;
                        var range = window.getSelection().getRangeAt(0);
                        var img = document.createElement('img');
                        img.src = imgSrc;
                        img.style.maxWidth = '10%'; // 设置图片宽度
                        img.style.height = 'auto';
                        range.insertNode(img);
                        window.getSelection().removeAllRanges();
                    } else {
                        alert('图片上传失败：' + response.error);
                    }
                },
                error: function (xhr, status, error) {
                    alert('图片上传异常：' + error);
                }
            });
        });

        fileInput.click();
    });
    //上传封面按钮的点击事件
    $('#insertCoverBtn').click(function () {
        var fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);

        fileInput.addEventListener('change', function (e) {
            var file = e.target.files[0];
            var formData = new FormData();
            globalData.cover = file;


        });

        fileInput.click();
    });
    $('#filePickerBtn').click(function () {
        $('#files').click(); // 触发文件输入的点击事件，打开文件选择对话框
    });

    // 文件选择输入的change事件
    $('#files').on('change', function (e) {
        var files = e.target.files; // 获取选中的文件列表
        var fileListContainer = $('#fileList'); // 获取显示文件名的容器
        // 遍历所有选中的文件，并显示它们的名称
        globalData.files = files;
        for (var i = 0; i < files.length; i++) {
            fileListContainer.append('<li>' + files[i].name + '</li>');
            // 遍历所有选中的文件，并将它们的路径添加到全局数组中
        }
    });
    // 其他代码，如插入封面按钮的点击事件和表单提交事件保持不变
    // ...

    // 表单提交事件
    $('#newsForm').submit(function (e) {
        e.preventDefault(); // 阻止表单的默认提交行为
        var formData = new FormData(this); // 创建FormData对象
        //获取标题
        var title = $('#title').val().trim();
        //获取作者
        var category = $('#categorySelect').val().trim();
        var author = $('#author').val().trim();
        // 获取内容字段的文本和图像
        var content = $('#content').html();
        var link = $('#link').val(); // 获取外部链接
        var attachmentLink = $('#attachmentLink').val(); // 获取附件链接
        if (!author || !title) {
            alert('撰稿人和标题不能为空。');
            return;
        }

        // 检查内容字段是否为空，如果为空且没有外部链接，则提示用户
        if (!content && !link) {
            alert('请提供内容或输入有效的外部链接。');
            return;
        }
        // 检查封面是否上传，如果没有上传，则提示用户
        if (!globalData.cover) {
            alert('请上传封面图片。');
            return;
        }

        formData.append('author', author);
        formData.append('title', title);
        formData.append('content', content);
        formData.append('link', link);
        formData.append('category', category);
        formData.append('attachmentLink', attachmentLink);
        for (var key in globalData) {
            formData.append(key, globalData[key]);
        }

        // 输出表单数据到控制台，用于调试
        for (var [a, b] of formData.entries()) {
            console.log(a, b);
        }
        // 使用jQuery的ajax方法发送表单数据，包括内容或链接
        $.ajax({
            url: '/api/news/submit-news', // 服务器端接收提交的URL
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                console.log('新闻提交成功', response);
                // 提交成功后的逻辑，提示用户
                alert('新闻提交成功！');
                // 刷新页面
                window.location.reload();

            },
            error: function (xhr, status, error) {
                console.error('新闻提交失败', error);
                // 提交失败后的逻辑，显示错误信息
                alert('新闻提交失败：' + error);
                // 刷新页面
                window.location.reload();
            }
        });
    });
});