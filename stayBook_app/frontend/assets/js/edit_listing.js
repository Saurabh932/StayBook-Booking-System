import { setFlash } from "./script.js";


// ==================================================
// Auth Guard
// ==================================================
const token = localStorage.getItem("access_token");

if (!token) {
    setFlash("Please login first", "danger");
    window.location.href = "/login.html";
}


// ==================================================
// Edit Listing Page
// ==================================================
async function editListingPage() {
    const form = document.querySelector(".needs-validation");
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (!form || !id) {
        setFlash("Invalid page", "danger");
        return;
    }

    // ----------------------------------------------
    // Load existing listing
    // ----------------------------------------------
    try {
        const response = await fetch(`/listings/${id}`);

        if (response.status === 403) {
            setFlash("You don’t own this listing", "danger");
            window.location.href = "/";
            return;
        }

        const listing = await response.json();

        form.elements["title"].value = listing.title ?? "";
        form.elements["description"].value = listing.description ?? "";
        form.elements["image"].value = listing.image ?? "";
        form.elements["price"].value = listing.price ?? "";
        form.elements["location"].value = listing.location ?? "";
        form.elements["country"].value = listing.country ?? "";
    }
    catch (error) {
        console.error(error);
        setFlash("Error loading listing", "danger");
    }

    // ----------------------------------------------
    // Submit update
    // ----------------------------------------------
    form.addEventListener("form:valid", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(`/listings/${id}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                if (response.status === 403) {
                    setFlash("You are not allowed to edit this listing", "danger");
                } else {
                    setFlash("Error updating listing", "danger");
                }
                return;
            }

            setFlash("Listing updated successfully", "success");
            window.location.href = `/listing.html?id=${id}`;
        }
        catch (error) {
            console.error(error);
            setFlash("Something went wrong", "danger");
        }
    });
}

editListingPage();
