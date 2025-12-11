async function editListingPage() {
    const form = document.querySelector("form");
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (!form) {
        console.error("Form element not found after layout load.");
        return;
    }
    if (!id) {
        alert("No listing ID found");
        return;
    }

    // fetch current data and pre-fill form
    try {
        const response = await fetch(`/listings/${id}`);
        if (!response.ok) throw new Error("Listing not found");

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
        alert("Error loading listing data");
    }

    // handle edit submit
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(`/listings/${id}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                alert("Error updating listing");
                return;
            }

            alert("Listing updated successfully!");
            window.location.href = `/listing.html?id=${id}`; // Go back to details page
        }
        catch (error) {
            console.error(error);
            alert("Something went wrong");
        }
    });
}

editListingPage();