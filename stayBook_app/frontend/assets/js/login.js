import { setFlash } from "./script.js";

async function handleLoginSubmit() {
    const form = document.querySelector(".needs-validation");
    if (!form) return;

    const submitBtn = form.querySelector("button[type='submit']");

    // listen to form:valid instead of submit
    form.addEventListener("form:valid", async (event) => {
        event.preventDefault();

        // prevent multiple clicks
        submitBtn.disabled = true;
        submitBtn.textContent = "Logging in...";

        const formData = new FormData(form);
        const payload = Object.fromEntries(formData.entries());

        try {
            const response = await fetch("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                setFlash("Invalid email or password", "danger");
                submitBtn.disabled = false;
                submitBtn.textContent = "Login";
                return;
            }

            const data = await response.json();

            localStorage.setItem("access_token", data.access_token);

            setFlash("Welcome back! Logged in successfully.", "success");
            window.location.href = "/";

        } catch (error) {
            console.error(error);
            setFlash("Something went wrong. Try again.", "danger");
            submitBtn.disabled = false;
            submitBtn.textContent = "Login";
        }
    });
}

handleLoginSubmit();
