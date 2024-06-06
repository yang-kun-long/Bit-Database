$(document).ready(function () {
    // 监听还书按钮的点击事件以发起还书申请
    $('.return-book-btn').on('click', function () {
        var loanId = $(this).data('loan-id'); // 获取借阅记录的ID
        $('#returnModal').data('loan-id', loanId); // 将loanId存储在模态框的数据属性中
        $('#returnModal').modal('show'); // 显示模态框
    });

    // 提交还书申请
    $('#submitReturnButton').on('click', function () {
        var loanId = $('#returnModal').data('loan-id'); // 获取存储的loanId
        var returnReason = $('#returnReason').val(); // 获取还书申请理由
        $('#returnModal').modal('hide'); // 隐藏模态框

        // 发送 AJAX 请求提交还书申请
        $.ajax({
            url: `/api/books_loans/request_return/${loanId}`, // 还书申请的API端点
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ reason: returnReason }), // 发送的数据
            success: function (response) {
                alert('还书申请已提交');
                // 更新页面上的按钮状态或内容
            },
            error: function (xhr) {
                var errorText = JSON.parse(xhr.responseText).error;
                alert('还书申请失败: ' + errorText);
            }
        });
    });
    // 绑定点击事件，处理修改信息按钮的点击
    $('.edit-btn').on('click', function () {
        var field = $(this).data('field'); // 获取要修改的字段
        var currentValue = null;
        var newValue = null;
        // 如果field为空，则不再执行下方代码
        if (!field) {
            return;
        }
        if (field === 'photo_path') {
            uploadNewAvatar()
                .then(result => {
                    newValue = result.newAvatarPath;
                    updateUserInfo(field, currentValue, newValue)
                })
                .catch(error => {
                    console.error('头像更新失败:', error);
                });
        }
        else {
            currentValue = $(this).prev().text().trim(); // 获取当前的值
            newValue = prompt('请输入新的' + field, currentValue); // 弹出输入框
            if (newValue && newValue !== currentValue) {
                updateUserInfo(field, currentValue, newValue)
            }
        }
        
    });
    // 通过id绑定点击事件，处理更换头像按钮的点击

    function updateUserInfo(field, currentValue, newValue) {
        // 检查新值是否与当前值不同
        if (newValue !== currentValue) {
            // 发送AJAX请求到服务器更新信息
            $.ajax({
                url: '/api/users/update', // 服务器端点
                type: 'PUT', // 请求类型
                contentType: 'application/json', // 发送JSON数据
                data: JSON.stringify({ // 发送的数据
                    field: field,
                    value: newValue
                }),
                success: function(response) {
                    // 更新成功后的操作
                    alert('信息更新成功');
                    window.location.reload();
                  
                },
                error: function(xhr) {
                    var errorText = JSON.parse(xhr.responseText).error;
                    alert('信息更新失败: ' + errorText);
                }
            });
            console.log('更新' + field + '为: ' + newValue);
        } else {
            // 如果新值与当前值相同，则不进行更新
            alert('新值与当前值相同，不进行更新。');
        }
    }
    // 计算并显示剩余归还天数
    function calculateDaysLeft(loan) {
        var today = new Date();
        var dueDate = new Date(loan.loan_date);
        dueDate.setMonth(dueDate.getMonth() + loan.days);
        var daysLeft = (dueDate - today) / (1000 * 60 * 60 * 24);
        return Math.ceil(daysLeft);
    }

    $('.loan-item').each(function () {
        var loanId = $(this).data('loan-id');
        var loan = getLoanData(loanId); // 假设这是一个获取贷款数据的函数
        $('#daysLeft-' + loanId).text(calculateDaysLeft(loan));
    });
    async function uploadNewAvatar() {
        return new Promise((resolve, reject) => {
            // 触发文件选择对话框
            document.getElementById('avatar-file-input').click();

            // 监听文件输入框的变化
            document.getElementById('avatar-file-input').addEventListener('change', function (event) {
                var file = event.target.files[0]; // 获取选择的文件
                var formData = new FormData(); // 创建FormData对象

                if (file) {
                    // 将文件添加到FormData对象中
                    formData.append('image', file);

                    // 使用jQuery的ajax方法上传文件
                    $.ajax({
                        url: '/api/users/avatar', // 设置API端点
                        type: 'POST',
                        data: formData,
                        contentType: false, // 不设置内容类型
                        processData: false, // 不处理数据
                        success: function (response) {
                            // 上传成功，获取返回的新头像路径
                            if (response.success) {
                                var newAvatarPath = response.filepath; // 从响应中获取新路径
                                console.log('新头像路径:', newAvatarPath);

                                // 更新页面上的头像显示
                                var avatarImg = document.getElementById('avatar-img1');
                                avatarImg.src = newAvatarPath; // 设置新头像的URL

                                // 解析Promise并返回新路径
                                resolve({ newAvatarPath: newAvatarPath });
                            } else {
                                // 如果API响应不成功，拒绝Promise
                                reject(new Error(response.error));
                            }
                        },
                        error: function (xhr) {
                            // 请求出错处理
                            var errorText = xhr.responseText || xhr.statusText || 'Unknown error';
                            console.error('上传出错:', errorText);
                            reject(new Error(errorText));
                        }
                    });
                } else {
                    reject(new Error('请选择一个文件。'));
                }
            });
        });
    }
});