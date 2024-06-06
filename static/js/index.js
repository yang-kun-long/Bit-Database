document.addEventListener('DOMContentLoaded', function() {
    fetchCategoryNews();
});

function fetchCategoryNews() {
    const apiURL = '/api/news/category-news'; // 根据实际的url_prefix调整URL

    fetch(apiURL)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data && data.success) {
            updateNewsCategory(data);
        } else {
            console.error('Failed to fetch news:', data.message);
        }
    })
    .catch(error => {
        console.error('Error fetching news:', error);
    });
}

function updateNewsCategory(newsData) {
    const noticeElement = document.querySelector('span[data-category="notice"]');
    const newsElement = document.querySelector('span[data-category="news"]');
    const activityElement = document.querySelector('span[data-category="activity"]');
    const noticeLink = document.getElementById('noticeLink');
    const newsLink = document.getElementById('newsLink');
    const activityLink = document.getElementById('activityLink');
    // 更新通知内容
    if (noticeElement && newsData.notice) {
        noticeElement.textContent = newsData.notice.title;
        noticeLink.href = newsData.notice.link || '/news_model?id=' + newsData.notice.id;
    }

    // 更新新闻内容
    if (newsElement && newsData.news) {
        newsElement.textContent = newsData.news.title; // 假设新闻的标题存储在 title 字段
        newsLink.href = newsData.news.link || '/news_model?id=' + newsData.news.id;
    }

    // 更新活动内容
    if (activityElement && newsData.activity) {
        activityElement.textContent = newsData.activity.title; // 假设活动的标题存储在 title 字段
        activityLink.href = newsData.activity.link || '/news_model?id=' + newsData.activity.id;
    }
}