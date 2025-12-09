async function handleNewListingSubmit(){
    const form = document.querySelector("form")

    if (!form) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Collecting form data using FormData API
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Sending the data as JSON Post  requresing using fetch
        try{
            const response = await fetch("/listings/", {method: "POST", headers:{"Content-Type":"application/json"},
                                                        body: JSON.stringify(data)});
             if (!response.ok){
                alert("Error crating listing ");
                return;
             }

             console.log("Listing Created!!");
             alert("Listing Created!!");

            //  Then returning back to index
            window.location.href = "/";
        }
        catch (error){
            console.log("Error: ", error);
            alert("Some error while creating the listing.");
        }
    })
}

handleNewListingSubmit()