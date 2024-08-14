document.addEventListener('DOMContentLoaded', (event) => {
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const passwordHelpBlock = document.getElementById('passwordHelpBlock');
    const passwordMatchBlock = document.getElementById('passwordMatchBlock');

    if (password1 && password2) {
        password1.addEventListener('input', function () {
            let message = 'Ваш пароль должен содержать не менее 8 символов, включать буквы и цифры.';
            const value = password1.value;

            if (value.length < 8) {
                message = 'Пароль слишком короткий. Минимум 8 символов.';
            } else if (!/[a-zA-Z]/.test(value)) {
                message = 'Пароль должен содержать хотя бы одну букву.';
            } else if (!/[0-9]/.test(value)) {
                message = 'Пароль должен содержать хотя бы одну цифру.';
            } else {
                message = 'Пароль выглядит хорошо.';
            }

            passwordHelpBlock.textContent = message;
        });

        password2.addEventListener('input', function () {
            if (password1.value !== password2.value) {
                passwordMatchBlock.textContent = 'Пароли не совпадают.';
                passwordMatchBlock.style.color = 'red';
            } else {
                passwordMatchBlock.textContent = 'Пароли совпадают.';
                passwordMatchBlock.style.color = 'green';
            }
        });
    } else {
        console.error('One or more elements were not found in the DOM.');
    }
});

document.querySelector('.input-group-text').addEventListener('click', function() {
        const query = document.querySelector('.form-control').value;

        fetch(/search/?query=${encodeURIComponent(query)})
            .then(response => response.json())
            .then(data => {
                const userList = document.querySelector('.chat-list');
                userList.innerHTML = '';

                if (data.users.length > 0) {
                    data.users.forEach(user => {
                        const userItem = document.createElement('li');
                        userItem.className = 'clearfix';
                        userItem.innerHTML = `
                            <img src="${user.avatar || 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'}" alt="avatar">
                            <div class="about">
                                <div class="name">${user.username}</div>
                                <div class="status"> <i class="fa fa-circle online"></i> online </div>
                            </div>
                            <a href="javascript:void(0);" onclick="showProfileModal('${user.id}', '${user.username}', '${user.avatar || 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'}')">
                                <i class="fa fa-question" style="font-size: 20px;"></i>
                            </a>
                        `;
                        userList.appendChild(userItem);
                    });
                } else {
                    userList.innerHTML = '<li class="clearfix">No users found.</li>';
                }
            })
            .catch(error => console.error('Error during search:', error));
    });
document.querySelector('.input-group-text').addEventListener('click', function() {
        const query = document.querySelector('.form-control').value;

        fetch(/search/?query=${encodeURIComponent(query)})
            .then(response => response.json())
            .then(data => {
                const userList = document.querySelector('.chat-list');
                userList.innerHTML = '';

                if (data.users.length > 0) {
                    data.users.forEach(user => {
                        const userItem = document.createElement('li');
                        userItem.className = 'clearfix';
                        userItem.innerHTML = `
                            <img src="${user.avatar || 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'}" alt="avatar">
                            <div class="about">
                                <div class="name">${user.username}</div>
                                <div class="status"> <i class="fa fa-circle online"></i> online </div>
                            </div>
                            <a href="javascript:void(0);" onclick="showProfileModal('${user.id}', '${user.username}', '${user.avatar || 'https://abrakadabra.fun/uploads/posts/2021-12/1640528661_1-abrakadabra-fun-p-serii-chelovek-na-avu-1.png'}')">
                                <i class="fa fa-question" style="font-size: 20px;"></i>
                            </a>
                        `;
                        userList.appendChild(userItem);
                    });
                } else {
                    userList.innerHTML = '<li class="clearfix">No users found.</li>';
                }
            })
            .catch(error => console.error('Error during search:', error));
    });