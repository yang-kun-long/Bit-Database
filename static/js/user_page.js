$(document).ready(function() {
     // 监听还书按钮的点击事件以发起还书申请
    $('.return-book-btn').on('click', function() {
        var loanId = $(this).data('loan-id'); // 获取借阅记录的ID
        $('#returnModal').data('loan-id', loanId); // 将loanId存储在模态框的数据属性中
        $('#returnModal').modal('show'); // 显示模态框
    });

    // 提交还书申请
    $('#submitReturnButton').on('click', function() {
        var loanId = $('#returnModal').data('loan-id'); // 获取存储的loanId
        var returnReason = $('#returnReason').val(); // 获取还书申请理由
        $('#returnModal').modal('hide'); // 隐藏模态框

        // 发送 AJAX 请求提交还书申请
        $.ajax({
            url: `/api/books_loans/request_return/${loanId}`, // 还书申请的API端点
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ reason: returnReason }), // 发送的数据
            success: function(response) {
                alert('还书申请已提交');
                // 更新页面上的按钮状态或内容
            },
            error: function(xhr) {
                var errorText = JSON.parse(xhr.responseText).error;
                alert('还书申请失败: ' + errorText);
            }
        });
    });
    // 绑定点击事件，处理修改信息按钮的点击
    $('.edit-btn').on('click', function() {
        var field = $(this).data('field'); // 获取要修改的字段
        var currentValue = $(this).prev().text().trim(); // 获取当前的值
        var newValue = prompt('请输入新的' + field, currentValue); // 弹出输入框

        if (newValue && newValue !== currentValue) {
            $.ajax({
                url: '/api/users/update', // 服务器端点，根据实际情况进行修改
                type: 'PUT', // 请求类型
                contentType: 'application/json', // 发送 JSON 数据
                data: JSON.stringify({ // 发送的数据
                    field: field,
                    value: newValue
                }),
                success: function(response) {
                    // 更新成功后的操作
                    alert('信息更新成功');
                    // 更新页面上显示的值
                    $(this).prev().text(newValue);
                },
                error: function(xhr) {
                    var errorText = JSON.parse(xhr.responseText).error;
                    alert('信息更新失败:'+ errorText);
                }
            });
            console.log('更新' + field + '为: ' + newValue);
        }
    });

    // 计算并显示剩余归还天数
    function calculateDaysLeft(loan) {
        var today = new Date();
        var dueDate = new Date(loan.loan_date);
        dueDate.setMonth(dueDate.getMonth() + loan.days);
        var daysLeft = (dueDate - today) / (1000 * 60 * 60 * 24);
        return Math.ceil(daysLeft);
    }

    $('.loan-item').each(function() {
        var loanId = $(this).data('loan-id');
        var loan = getLoanData(loanId); // 假设这是一个获取贷款数据的函数
        $('#daysLeft-' + loanId).text(calculateDaysLeft(loan));
    });
});