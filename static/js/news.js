$(document).ready(function() {
    // 调用 API 获取新闻列表
    $.ajax({
        url: '/api/news/news-list',
        type: 'GET',
        dataType: 'json',
        success: function(newsData) {
            var newsListContainer = $('#news-list-container');
            newsListContainer.empty(); // 清空新闻列表容器

            newsData.forEach(function(newsItem) {
                // 创建新闻项的HTML结构
                var newsHtml = `
                    <div class="news-item">
                        <h3>${newsItem.title}</h3>
                        <p>作者：${newsItem.author}</p>
                        <p>创建时间：${newsItem.create_time}</p>
                        <!-- 使用jQuery的html()方法来插入HTML内容 -->
                        <div class="news-content"">${newsItem.content}</div>
                        <div class="news-attachments">
                            附件：
                            ${newsItem.attachments.map(function(attachment) {
                                var link = attachment.trim();
                                return `<a href="${link}" target="_blank">链接</a>`;
                            }).join(' | ')}
                        </div>
                    </div>
                `;
                // 将创建的HTML添加到新闻列表容器中
                $(newsHtml).appendTo(newsListContainer);
            });
        },
        error: function(xhr, status, error) {
            console.error('获取新闻列表失败:', error);
            var errorMessage = '无法加载新闻列表，请稍后再试。';
            $('#news-list-container').html('<p>' + errorMessage + '</p>');
        }
    });
});