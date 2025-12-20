const token = localStorage.getItem("access_token");

if (!token) {
    alert("Please login first");
    window.location.href = "/login.html";
}


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
                alert("Error creating listing");
                return;
            }

            alert("Listing created");
            window.location.href = "/";
        }
        catch (error) {
            console.error(error);
            alert("Something went wrong");
        }
    });
}

handleNewListingSubmit();
