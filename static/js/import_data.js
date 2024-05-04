// import_users.js
document.getElementById('file').addEventListener('change', function(event) {
    var file = event.target.files[0];
    if (file) {
        var fileType = file.type;
        var validTypes = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv'];
        if (validTypes.indexOf(fileType) === -1) {
            alert('请选择有效的 Excel 或 CSV 文件。');
            event.target.value = ''; // 清空文件输入
        }
    }
});

document.querySelector('form').addEventListener('submit', function(event) {
    // 这里进行表单提交前的额外验证
    var fileInput = document.getElementById('file');
    if (!fileInput.value) { // 检查文件输入字段是否为空
        event.preventDefault(); // 阻止表单提交
        alert('请选择要上传的文件。');
    }
    // 可以在这里添加更多验证逻辑
});