document.addEventListener('DOMContentLoaded', function () {
    // 获取H1元素和分页容器
    const pageTitle = document.getElementById('page-title');
    const filesContainer = document.getElementById('files-list');
    const paginationContainer = document.getElementById('pagination');

    let currentPage = 1; // 初始化当前页码
    const filesPerPage = 5; // 每页显示的文件数量

    // 确保H1元素存在
    const urlParams = new URLSearchParams(window.location.search);
    const fileType = urlParams.get('type') || '默认类型'; // 获取URL中的type参数，默认为'默认类型'
    pageTitle.textContent = `下载专区 - ${fileType}`;

    // 函数：渲染文件列表
    function renderFilesList(page) {
        currentPage = page;
        const apiUrl = `/api/materials/files?type=${fileType}&page=${page}&limit=${filesPerPage}`;
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // 清空现有文件列表
                filesContainer.innerHTML = '';
                // 渲染文件列表
                data.files.forEach(file => {
                    const fileItem = `
                        <div class="file-item">
                            <div class="file-info">
                                <h4>${file.name}</h4>
                                <p>作者：${file.author}</p>
                            </div>
                            <div class="file-intro">
                                <p>简介：${file.introduction}</p>
                            </div>
                            <div class="download-button-container">
                                <a href="${file.url}" target="_blank" class="download-button">下载文件</a>
                            </div>
                        </div>
                    `;
                    filesContainer.innerHTML += fileItem;
                });
                // 渲染分页
                renderPagination(data.pages, data.page);
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
                filesContainer.innerHTML = '<p>加载文件列表失败，请稍后重试。</p>';
            });
    }

    // 函数：渲染分页按钮
    function renderPagination(pages, currentPage) {
        // 清空现有分页按钮
        paginationContainer.innerHTML = '';
        if (pages > 1) {
            for (let i = 1; i <= pages; i++) {
                const button = document.createElement('button');
                button.textContent = i;
                button.disabled = i === currentPage;
                // 这里不需要使用立即调用的箭头函数，因为 renderFilesList 已经接收 page 作为参数
                button.addEventListener('click', function () {
                    renderFilesList(i); // 点击分页按钮时，传递正确的页码
                });
                paginationContainer.appendChild(button);
            }
        }
    }

    // 初始加载第一页文件列表
    renderFilesList();
});