import { setFlash } from "./script.js";

/* ==================================================
   Auth Helpers
================================================== */
function getToken() {
    return localStorage.getItem("access_token");
}

function requireAuth() {
    const token = getToken();
    if (!token) {
        setFlash("Please log in to create a listing.", "warning");
        window.location.href =
            `/login.html?next=${encodeURIComponent(window.location.pathname)}`;
        return null;
    }
    return token;
}

/* ==================================================
   New Listing Page
================================================== */
async function handleNewListingSubmit() {

    // ✅ AUTH GUARD (early and explicit)
    const token = requireAuth();
    if (!token) return;

    const form = document.querySelector(".needs-validation");
    if (!form) return;

    form.addEventListener("form:valid", async (event) => {
        event.preventDefault();

        const data = Object.fromEntries(
            new FormData(form).entries()
        );

        try {
            const response = await fetch("/listings/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                setFlash("Failed to create listing.", "danger");
                return;
            }

            setFlash("Listing created successfully!", "success");
            window.location.href = "/";

        } catch (error) {
            console.error(error);
            setFlash("Something went wrong.", "danger");
        }
    });
}

handleNewListingSubmit();
