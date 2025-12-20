import { setFlash } from "./script.js";

async function handleLoginSubmit() {
    const form = document.querySelector("form");
    if (!form) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const payload = Object.fromEntries(formData.entries());

        const response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            setFlash("Invalid credentials", "danger");
            return;
        }

        const data = await response.json();

        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("username", payload.email.split("@")[0]);

        setFlash("Welcome back! Logged in successfully.", "success");
        window.location.href = "/";
    });
}

handleLoginSubmit();