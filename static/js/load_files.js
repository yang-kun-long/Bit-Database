// load_files.js
document.addEventListener('DOMContentLoaded', function() {
    // 获取H1元素
    const pageTitle = document.getElementById('page-title');
    const filesContainer = document.querySelector('.contentmain main'); // 选择文件列表容器

    // 确保H1元素存在
        const urlParams = new URLSearchParams(window.location.search);
        const fileType = urlParams.get('type') || 'default'; // 获取URL中的type参数，默认为'default'


    // 构建请求URL
    const apiUrl = `/api/materials/files?type=${fileType}`;

    // 发送AJAX请求获取文件列表
    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // 渲染文件列表
        const filesHtml = data.map(file => `
            <div class="file-item">
                <h4>${file.name}</h4>
                <p>作者：${file.author}</p>
                <p>简介：${file.introduction}</p>
                <a href="${file.url}" target="_blank">下载文件</a>
            </div>
        `).join('');

        // 将文件列表HTML添加到主内容区域
        if (filesContainer) {
            filesContainer.innerHTML = filesHtml;
        }
        pageTitle.textContent = `下载专区 - ${fileType}`; // 设置页面H1标题内容
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        if (filesContainer) {
            filesContainer.innerHTML = '<p>加载文件列表失败，请稍后重试。</p>';
        }
    });
});