function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function printUsers(data) {
  div = document.getElementById("for_cr");
  h1 = document.createElement("h1");
  h1.textContent = `Приветствую, ${data.name}!`;
  div.appendChild(h1);
}

function del_cookie() {
    document.cookie = "Auth="
    window.open("/auth-form","_self")
}

token = getCookie('Auth')

function get_all_users() {
    $.ajax({
      url: '/get-all-users',
      type: 'post',
      contentType: 'application/json',
      headers: {'Authorization': `bearer ${token}`},
      success: function (result) {
        render_users(result)
      },
      error: function (error) {}
    })
}

function render_users(data) {
    users_div = document.getElementById('add_users')

    table = document.createElement("table");
    table.setAttribute("id", "users_list");
    th_name = document.createElement("th");
    th_mail = document.createElement("th");
    th_button = document.createElement("th");
    user_name = th_name.appendChild(document.createElement('td'));
    mail = th_mail.appendChild(document.createElement('td'));
    button = th_button.appendChild(document.createElement('td'));
    user_name.innerHTML = 'Имя';
    mail.innerHTML = 'Mail';
    button.innerHTML = 'Кнопка';
    table.appendChild(th_name);
    table.appendChild(th_mail);
    table.appendChild(th_button);
    for ( row of data ) {
          tr = document.createElement("tr");
          user_name = tr.appendChild(document.createElement('td'));
          user_mail = tr.appendChild(document.createElement('td'));
          user_button = tr.appendChild(document.createElement('td'));
          user_name.innerHTML = row.name;
          user_mail.innerHTML = row.email;
          user_button.innerHTML = `<button onClick='del_users(${row.id})'>Удалить</button>`;
          table.appendChild(tr);
    }
    users_div.appendChild(table)
}

function del_users(ids) {
    let formData = new FormData();
    formData.append("user_id", ids);
    fetch("/delete-user", {
    method: "POST",
    body: formData,
    headers: {'Authorization': `bearer ${token}`}
      })
      .then((response) => response.text())
      .then((text) => {
            alert(text);
      })
      .then(() => {window.location.reload();});

}

$('body').on('click', '#create_button', function (e) {
    e.preventDefault();
    $.ajax({
      url: '/create-users',
      type: 'get',
      contentType: 'application/json',
      headers: {'Authorization': `bearer ${token}`},
      success: function (result) {
        $("#user_form").html(result)
      },
      error: function (error) {}
    })
})

$( document ).ready(function() {
    printUsers({{user}});
    {% if user.superuser == 1 %}
        get_all_users();
    {% endif %}
});
