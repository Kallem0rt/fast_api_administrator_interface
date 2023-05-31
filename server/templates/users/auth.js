function recordForm (formdata) {

    let isAuthorised = false;
    var obj;
    var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
    };

    fetch("/auth", requestOptions)
    .then(response => {
        console.log(response.status);
        if (response.status === 200) {
            isAuthorised = true;
        } else {
            console.log(response)
        }
        return response.text();
    })
    .then((text) => {
        if (isAuthorised) {
            console.log("redir");
            window.open("/secure", "_self");
        } else {
            alert(JSON.parse(text).detail)
        }
    })
    .catch(error => console.log('error', error));
}

$(document).ready(function () {
    $('body').on("submit", "#auth", function(e){
        e.preventDefault(); // avoid to execute the actual submit of the form.
        var form = $(this);
        var formdata = new FormData();
        formdata.append("username", $("#username").val());
        formdata.append("password", $("#password").val());
        console.log(form)
        status = recordForm (formdata)
    });

});


