const token = localStorage.getItem("access_token");

if (!token) {
    setFlash("Please login first.", "warning");
    window.location.href = "/login.html";
    return;
}


import { setFlash } from "./script.js";

async function handleNewListingSubmit() {
    const form = document.querySelector(".needs-validation");
    if (!form) return;

    form.addEventListener("form:valid", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch("/listings/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                setFlash("Failed to create listing.", "danger");
                return;
            }

            setFlash("Listing created successfully!", "success");
            window.location.href = "/";
        }
        catch (error) {
            console.error(error);
            setFlash("Something went wrong", "danger");
        }
    });
}

handleNewListingSubmit();
