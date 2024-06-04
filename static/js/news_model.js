$(document).ready(function () {
    // 假设新闻详情数据通过URL参数传递，例如：news_model.html?id=123
    var newsId = window.location.search.split('=')[1]; // 获取URL中的新闻ID参数
    if (newsId) {
        // 调用API获取新闻详情数据
        $.ajax({
            url: '/api/news/' + newsId, // 假设API根据ID提供新闻详情
            type: 'GET',
            dataType: 'json',
            success: function (newsData) {
                // 动态填充新闻详情
                $('.news-title').text(newsData.title);
                $('.news-author').text('作者：' + newsData.author);
                $('.news-time').text('发布时间：' + newsData.create_time);

                // 处理content内容，清理并转换为段落
                var contentHtml = newsData.content;
                // 将<div>标签替换为<p>标签
                contentHtml = contentHtml.replace(/<div>/g, '<p>');
                contentHtml = contentHtml.replace(/<\/div>/g, '</p>');
                // 插入内容到新闻内容区域
                $('.news-content').html(contentHtml);
                //清楚图片的style属性
                $('.news-content img').removeAttr('style');

                // 处理附件
                if (newsData.attachments.length > 0) {
                    // 创建一个空的有序列表
                    var attachmentsList = $('<ol></ol>');
                    newsData.attachments.forEach(function (attachment, index) {
                        // 对每个附件，生成有序的附件名称，如“附件一”、“附件二”等
                        var attachmentName = '附件' + (index + 1);
                        // 为每个附件生成链接，并添加到列表中
                        var listItem = $('<li></li>').append(
                            $('<a></a>').attr('href', attachment).attr('class', 'attachment-link').attr('target', '_blank').text(attachment)
                        );
                        attachmentsList.append(listItem);
                    });
                    // 将生成的附件列表添加到附件容器中
                    $('.attachments-container').append(attachmentsList);
                }
            },
            error: function (xhr, status, error) {
                console.error('获取新闻详情失败:', error);
                // 显示错误信息
                $('.news-detail').html('<p>无法加载新闻详情，请稍后再试。</p>');
            }
        });
    }
});