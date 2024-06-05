$(document).ready(function () {
    let activeIntroductionId = null; // 用于记录当前激活的简介ID

    // 初始化函数，用于加载简介列表
    function initialize() {
        loadIntroductions();
    }

    // 加载简介列表
    function loadIntroductions() {
        $.ajax({
            url: `/api/introduction_update/`,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                response.sort((a, b) => {
                    return b.is_active - a.is_active; // 已激活的简介排在前面
                });
                renderIntroductionsTable(response);
            },
            error: function (xhr) {
                console.error('获取简介列表失败:', xhr.status, xhr.statusText);
            }
        });
    }

    // 渲染简介列表到表格中
    function renderIntroductionsTable(introductions) {
        const table = document.querySelector('#introductionsTable');
        let rows = '';

        // 根据激活状态对简介进行排序
        introductions.sort((a, b) => {
            return b.is_active - a.is_active;
        });

        introductions.forEach(introduction => {
            // 根据激活状态设置按钮文本和样式
            const actionText = introduction.is_active ? '停用' : '启用';
            const actionClass = introduction.is_active ? 'btn btn-danger' : 'btn btn-success';
            const actionDisabled = introduction.is_active && activeIntroductionId === introduction.id ? ' disabled' : '';

            // 创建行并添加到表格
            rows += `
                <tr>
                    <td>${introduction.id}</td>
                    <td>${introduction.name}</td>
                    <td>${introduction.short_name}</td>
                    <td>${introduction.introduction}</td>
                    <td>${introduction.address}</td>
                    <td>${introduction.phone}</td>
                    <td>${introduction.fax}</td>
                    <td>${introduction.email}</td>
                    <td>${introduction.website}</td>
                    <td>
                        <img src="${introduction.logo_path}" alt="Logo" class="logo-preview">
                    </td>
                    <td>${introduction.created_at}</td>
                    <td>${introduction.is_active ? '是' : '否'}</td>
                    <td>${introduction.operator_name}</td>
                    <td>
                        <button class="${actionClass} ${actionDisabled}" data-id="${introduction.id}" onclick="toggleIntroductionActiveStatus(this)">${actionText}</button>
                    </td>
                </tr>
            `;
        });

        table.innerHTML = rows;
    }


    function toggleIntroductionActiveStatus(event) {
        // event.target 是触发事件的元素
        const button = event.target;
        const introductionId = button.dataset.id;
        let isActive = button.textContent.trim() === '启用'; // 检查当前按钮文本是启用

        // 如果简介已激活且再次点击，不执行任何操作
        if (introductionId === activeIntroductionId && !isActive) {

            return;
        }
        if (!isActive) {
            console.log('停用简介');
            // 发送请求停用当前激活的简介
            disableActiveIntroduction(introductionId);

        } else {

            // 如果尝试启用简介时已有其他简介被激活
            if (activeIntroductionId !== null && activeIntroductionId !== introductionId) {
                // 警告用户只能有一个激活的简介
                const userConfirmed = confirm('已有简介被激活。启用新的简介将停用当前激活的简介。是否继续？');
                if (!userConfirmed) {
                    return; // 如果用户取消，则不执行任何操作
                }

                // 发送请求停用当前激活的简介
                disableActiveIntroduction(activeIntroductionId);
            }
            console.log('启用简介');
            // 发送请求启用当前选择的简介
            activateIntroduction(introductionId);
            activeIntroductionId = introductionId; // 更新当前激活的简介ID
        }
        //刷新页面
        
    }

    function activateIntroduction(introductionId) {
        $.ajax({
            url: `/api/introduction_update/${introductionId}`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ is_active: true }),
            success: function (response) {
                if (response.success) {
                    // 如果成功启用，更新按钮状态
                    updateButtonState(introductionId, true);
                    activeIntroductionId = introductionId; // 更新当前激活的简介ID
                } else {
                    alert('启用简介失败，请稍后重试。');
                }
            },
            error: function (xhr) {
                console.error('启用简介失败:', xhr.responseText);
                alert('启用简介失败，请稍后重试。');
            }
        });
    }

    // 停用简介的函数
    function disableActiveIntroduction(introductionId) {
        $.ajax({
            url: `/api/introduction_update/${introductionId}`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ is_active: false }),
            success: function (response) {
                if (response.success) {
                    // 如果成功停用，更新按钮状态
                    updateButtonState(introductionId, false);
                } else {
                    alert('停用简介失败，请稍后重试。');
                }
            },
            error: function (xhr) {
                console.error('停用简介失败:', xhr.responseText);
                alert('停用简介失败，请稍后重试。');
            }
        });
    }
    function updateButtonState(introductionId, isActive) {
        const button = document.querySelector(`[data-id="${introductionId}"]`);
        button.textContent = isActive ? '停用' : '启用';
        button.classList.add(isActive ? 'btn-danger' : 'btn-success');
        button.classList.remove(isActive ? 'btn-success' : 'btn-danger');
    }
    // 创建简介
    $('#saveIntroduction').on('click', function (event) {
        event.preventDefault();
        const form = $('#addIntroductionForm');
        const formData = new FormData(form[0]);

        // 检查是否有文件被选择
        if (form.find('.custom-file-input')[0].files.length === 0) {
            alert('请上传LOGO图片。');
            return;
        }

        // 上传图片
        $.ajax({
            url: `/api/news/upload-image`,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.success) {
                    // 图片上传成功，获取图片路径
                    const logoPath = response.filepath;

                    // 从表单中获取其他数据
                    const introductionData = {
                        name: form.find('#name').val(),
                        short_name: form.find('#shortName').val(),
                        introduction: form.find('#introduction').val(),
                        address: form.find('#address').val(),
                        phone: form.find('#phone').val(),
                        fax: form.find('#fax').val(),
                        email: form.find('#email').val(),
                        website: form.find('#website').val(),
                        logo_path: logoPath,
                        is_active: false, // 默认创建时不激活
                        operator_id: form.find('#operatorId').val()
                    };

                    // 创建简介
                    createIntroduction(introductionData);
                } else {
                    alert('图片上传失败: ' + response.error);
                }
            },
            error: function (xhr) {
                console.error('图片上传失败:', xhr.responseText);
                alert('图片上传失败，请稍后重试。');
            }
        });
    });

    // 创建简介的函数
    function createIntroduction(introductionData) {
        $.ajax({
            url: `/api/introduction_update/`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(introductionData),
            success: function (response) {
                if (response.success) {
                    // 刷新简介列表
                    loadIntroductions();
                    $('#addIntroductionModal').modal('hide'); // 关闭模态框
                    $('#addIntroductionForm')[0].reset(); // 重置表单
                } else {
                    alert('创建简介失败，请稍后重试。');
                }
            },
            error: function (xhr) {
                console.error('创建简介失败:', xhr.responseText);
                alert('创建简介失败，请稍后重试。');
            }
        });
    }
    // 点击启用或停用按钮时，切换简介的激活状态

    $(document).on('click', '.btn-success, .btn-danger', function (event) {
        event.preventDefault();
        // 确保传递事件对象给 toggleIntroductionActiveStatus 函数
        toggleIntroductionActiveStatus(event);
    });

    initialize();
});