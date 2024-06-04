$(document).ready(function() {
    // 调用 API 获取新闻列表
    $.ajax({
        url: '/api/news/news-list',
        type: 'GET',
        dataType: 'json',
        success: function(newsData) {
            var containers = {
                'news': $('#news-photo-wall'),
                'notice': $('#notice-photo-wall'),
                'academic': $('#activity-photo-wall')
            };

            // 清空所有容器
            Object.values(containers).forEach(function(container) {
                container.empty();
            });

            newsData.forEach(function(newsItem) {
                // 创建照片墙的HTML结构模板
                var template = `
                    <div class="photo-item">
                        <a href="{{link}}" target="_blank">
                            <img src="{{cover}}" alt="封面图" class="photo-thumbnail" />
                        </a>
                    </div>
                `;
                console.log(newsItem.cover);
                // 替换模板中的变量
                var photoHtml = template.replace('{{link}}', newsItem.link || '/news_model?id=' + newsItem.id)
                                         .replace('{{cover}}', newsItem.cover);

                // 将字符串模板转换为jQuery对象
                var $photoHtml = $(photoHtml);

                // 根据category确定照片墙项应该添加到哪个容器
                if (containers[newsItem.category]) {
                    $photoHtml.appendTo(containers[newsItem.category]);
                }
            });
        },
        error: function(xhr, status, error) {
            console.error('获取新闻列表失败:', error);
            var errorMessage = '无法加载新闻列表，请稍后再试。';
            $('#news-photo-wall').html('<p>' + errorMessage + '</p>');
            // 可以为其他容器也设置错误消息
        }
    });
});