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
            alert("Invalid credentials");
            return;
        }

        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        window.location.href = "/";
    });
}

handleLoginSubmit();
