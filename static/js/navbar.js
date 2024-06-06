$(document).ready(function () {
function toggleDropdown() {
    var dropdown = document.getElementById('dropdown');
    if (dropdown.style.display === 'block') {
        dropdown.style.display = 'none';
    } else {
        dropdown.style.display = 'block';
    }
}
// 函数：获取并更新头像
function fetchAndUpdateAvatar() {
    // 发送GET请求到获取头像的API
    $.ajax({
        url: '/api/users/avatar', // 使用GET方法的API端点
        type: 'GET',
        success: function(response) {
            // API成功响应，获取头像路径
            var avatarPath = response.avatar;
            
            if (avatarPath) {
                // 如果头像路径存在，更新页面上的头像<img>标签的src属性
                var avatarImg = document.getElementById('avatar-img'); // 确保这个ID与您的头像<img>标签的ID匹配
                if (avatarImg) {
                    // 拼接完整的头像URL路径
                    
                    avatarImg.src = avatarPath;
                } else {
                    console.error('头像<img>标签未找到');
                }
            } else {
                console.log('没有头像路径返回');
            }
        },
        error: function(xhr) {
            // 请求出错处理
            console.error('获取头像失败:', xhr.status, xhr.statusText);
        }
    });
}

// 调用函数
fetchAndUpdateAvatar();
});