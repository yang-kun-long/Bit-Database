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
        displayInstitutionDetails(data);
    })
    .catch(error => {
        document.getElementById('message').textContent = 'Error fetching data: ' + error.message;
    });
}

function displayInstitutionDetails(institution) {
    // 设置Logo图像
    const logoContainer = document.getElementById('logoContainer');
    logoContainer.innerHTML = ''; // 清空容器内容
    const logoImg = document.createElement('img');
    logoImg.src = institution.logo_path;
    logoImg.alt = 'Institution Logo';
    logoImg.style.width = '200px'; // 设置图像宽度，按需调整
    logoImg.style.height = 'auto'; // 保持图像的宽高比
    logoContainer.appendChild(logoImg);

    // 填充其他详情
    document.getElementById('institutionId').textContent = institution.id;
    document.getElementById('institutionName').textContent = institution.name;
    document.getElementById('institutionShortName').textContent = institution.short_name;
    document.getElementById('institutionIntroduction').textContent = institution.introduction;
    document.getElementById('institutionAddress').textContent = institution.address;
    document.getElementById('institutionPhone').textContent = institution.phone;
    document.getElementById('institutionFax').textContent = institution.fax;
    document.getElementById('institutionEmail').textContent = institution.email;
    const websiteLink = document.getElementById('institutionWebsite');
    websiteLink.href = institution.website;
    websiteLink.textContent = institution.website;
    document.getElementById('institutionCreatedAt').textContent = institution.created_at;
    document.getElementById('institutionIsActive').textContent = institution.is_active ? 'Yes' : 'No';
    document.getElementById('institutionOperatorId').textContent = institution.operator_id;
    document.getElementById('institutionOperatorName').textContent = institution.operator_name;
}