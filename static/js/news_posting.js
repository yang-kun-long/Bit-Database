$(document).ready(function() {
    var content = $('#content');
    var insertImageBtn = $('#insertImageBtn');

    insertImageBtn.click(function() {
        var fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.style.display = 'none';
        document.body.appendChild(fileInput);

        fileInput.addEventListener('change', function(e) {
            var file = e.target.files[0];
            var reader = new FileReader();
            reader.onload = function(e) {
                // 获取当前选中的文本范围
                var range = window.getSelection().getRangeAt(0);
                // 创建一个img元素并插入到选中的文本范围
                var img = document.createElement('img');
                img.src = e.target.result;
                img.style.maxWidth = '10%';
                img.style.height = 'auto';
                range.insertNode(img);
                // 清除选中的文本范围
                window.getSelection().removeAllRanges();
            };
            reader.readAsDataURL(file);
        });

        fileInput.click();
    });
});