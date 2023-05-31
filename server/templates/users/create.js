function recordForm (formData) {
    token = getCookie('Auth')
    fetch('/sign-up', {
        method: "POST",
        body: formData,
        headers: {'Authorization': `bearer ${token}`}
    })
    .then(res => res.json())
    .then(data => {obj = data;})
    .then(() => {window.location.reload();});
}


$(document).ready(function () {
    $('body').on("submit", "#create_event", function(e){
        e.preventDefault(); // avoid to execute the actual submit of the form.
        let formData = new FormData();
        formData.append("name", $("#name").val());
        formData.append("email", $("#email").val());
        formData.append("password", $("#password").val());
        recordForm (formData)
    });

});

