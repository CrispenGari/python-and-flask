const users = document.querySelector(".app__users");

(async () =>
  await fetch("http://localhost:5000/users", {
    method: "GET",
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      console.log(data);
      const all_users = data
        ?.map(
          (u) =>
            `<div class="app__user">
              <p><strong>@${u.username}: </strong>${u.message}</p>
            </div>`
        )
        .join("");
      users.innerHTML = all_users;
    }))();

document.getElementById("btn").addEventListener("click", (e) => {
  e.preventDefault();
  const id = document.getElementById("id").value;
  const username = document.getElementById("username").value;
  const message = document.getElementById("message").value;
  const user = {
    username: username,
    id: id,
    message: message,
  };
  (async () => {
    fetch(`http://localhost:5000/user`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(user),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json",
      }),
    })
      .then((res) => console.log(res))
      .catch((err) => {
        console.log(err);
      });
  })();
});
