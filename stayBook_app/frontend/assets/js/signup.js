import { setFlash } from "./script.js";

async function handleSignupForm() {
  const form = document.querySelector(".needs-validation");
  if (!form) return;

  form.addEventListener("form:valid", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
      const response = await fetch("/auth/signup", {method: "POST", headers: { "Content-Type": "application/json" }, 
                                                    body: JSON.stringify(payload)});

      if (!response.ok) {
        const error = await response.json();
        setFlash(error?.error?.message || "Signup failed", "danger");
        return;
      }

      setFlash("Signup successful! You can now login.", "success");
      window.location.href = "/login.html";

      
    } catch (err) {
      console.error(err);
      setFlash("Something went wrong", "danger");
    }
  });
}

handleSignupForm();
