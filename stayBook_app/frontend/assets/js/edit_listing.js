// ==================================================
// Auth Guard
// ==================================================
const token = localStorage.getItem("access_token");

if (!token) {
    alert("Please login first");
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
        alert("Invalid page");
        return;
    }

    // ----------------------------------------------
    // Load existing listing
    // ----------------------------------------------
    try {
        const response = await fetch(`/listings/${id}`);

        if (!response.ok) {
            alert("Listing not found");
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
        alert("Error loading listing");
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
                    alert("You are not allowed to edit this listing");
                } else {
                    alert("Error updating listing");
                }
                return;
            }

            alert("Listing updated successfully");
            window.location.href = `/listing.html?id=${id}`;
        }
        catch (error) {
            console.error(error);
            alert("Something went wrong");
        }
    });
}

editListingPage();
