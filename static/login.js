document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginform");
  const errorMsg = document.getElementById("errormssg");

  form.addEventListener("submit", async (e) => {
    e.preventDefault(); 

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;


    if (!email || !password) {
      errorMsg.textContent = "Please fill in all fields";
      errorMsg.style.color = "red";
      return;
    }

    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const data = await response.json();

      if (!response.ok) {
      
        errorMsg.textContent = data.message || "Login failed";
        errorMsg.style.color = "red";
      } else {
      
        window.location.href = "/dashboard";
      }

    } catch (error) {
      errorMsg.textContent = "Server error. Try again later.";
      errorMsg.style.color = "red";
      console.error(error);
    }
  });
});
