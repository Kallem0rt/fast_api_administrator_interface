function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener("DOMContentLoaded", async function() {
  const token = getCookie('Auth');
  let htmlOutput = document.querySelector("#content");

  const response = await fetch("/secure-form", {
    method: "POST",
    contentType: "application/json",
    headers: {"Authorization": `bearer ${token}`}
  })

  if (!response.ok) {
    if (response.status === 401) {
      htmlOutput.textContent = "401 (Unauthorized)";
      window.open("/auth-form", "_self");
    }
  }

  const body = await response.text();
  $(htmlOutput).html(body);  //PoS!!!!
  //htmlOutput.innerHTML = body;
});
