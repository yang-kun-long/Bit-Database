document.addEventListener('DOMContentLoaded', function() {
    fetchActiveInstitutionDetails();
});

function fetchActiveInstitutionDetails() {
    const apiUrl = '/api/introduction_update/active'; // 根据Blueprint的url_prefix和路由定义调整URL

    fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) { // 检查是否有success属性且为true
            displayInstitutionDetails(data);
        } else {
            showError(data.message || 'No active introduction available!');
        }
    })
    .catch(error => {
        showError('Error fetching data: ' + error.message);
    });
}

function displayInstitutionDetails(institution) {
    // 填充机构信息，检查元素是否存在
    const elementsWithText = ['name', 'introduction', 'address', 'phone', 'fax', 'email', 'operator_name'];
    const elementsWithHref = ['website']; // 需要设置href的元素

    elementsWithText.forEach(field => {
        const element = document.getElementById(`institution${capitalize(field)}`);
        if (element) {
            element.textContent = institution[field] || 'N/A'; // 如果数据不存在，显示'N/A'
        }
    });

    elementsWithHref.forEach(field => {
        const element = document.getElementById(`institution${capitalize(field)}`);
        if (element) {
            element.setAttribute('href', institution[field] || '#'); // 如果没有网站，设置为无操作
            element.textContent = institution[field] || 'No website'; // 如果没有网站，显示'No website'
        }
    });

    // Logo处理
    const logoImg = document.getElementById('institutionLogo');
    if (logoImg) {
        logoImg.src = institution.logo_path || 'default-logo.png'; // 如果没有logo_path，使用默认logo
        logoImg.alt = 'Institution Logo';
        if (!institution.logo_path) {
            logoImg.style.display = 'none'; // 如果没有logo，隐藏图片标签
        }
    }

    // 激活状态处理
    const isActiveElement = document.getElementById('institutionIsActive');
    if (isActiveElement) {
        isActiveElement.textContent = institution.is_active ? 'Yes' : 'No';
    }

    // 操作员ID处理
    const operatorIdElement = document.getElementById('institutionOperatorId');
    if (operatorIdElement) {
        operatorIdElement.textContent = institution.operator_id || 'N/A';
    }
}

function capitalize(word) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

function showError(message) {
    const messageElement = document.getElementById('message');
    if (messageElement) {
        messageElement.textContent = message;
        messageElement.classList.remove('d-none');
    }
}