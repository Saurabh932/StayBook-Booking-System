async function listing_details(){
    const params = new URLSearchParams(window.location.search)
    const id = params.get("id")

    if (!id){
        console.error("Id not found")
        return;
    }

    try{
        const response = await fetch(`http://127.0.0.1:8000/listings/${id}`)
        
        if (!response.ok){
            throw new Error("Lising not found")
        }
        
        const details = await response.json()

        const h1 = document.getElementById("title")
        h1.textContent = details.title || "No title";

        
        const list_details = document.getElementById("list_details")
        list_details.innerHTML = `
                                <ul>
                                <li> <strong>Description: <strong> ${details.description ?? "N/A"}</li>
                                <li> <strong>Image: <strong> ${details.image ?? "N/A"}</li>
                                <li> <strong>Price: <strong> ${details.price ?? "N/A"}</li>
                                <li> <strong>Location:<strong> ${details.location ?? "N/A"}</li>
                                <li> <strong>Country: <strong> ${details.country ?? "N/A"}</li>
                                </ul>
                                `;
    }
    catch{

    }
}

listing_details()


// ==================================================
// Edit button
// ==================================================
async function editListing(){
    const btn = document.getElementById("edit-btn");
    const param = new URLSearchParams(window.location.search);
    const id = param.get("id")

    btn.addEventListener("click", () => {
        if (!id){
            console.error("No ID present in URL");
            return;
        }
        window.location.href = `/edit_listing.html?id=${id}`;
    });
};

editListing();


// ==================================================
// Delete button
// ==================================================
async function deleteListing(){
    const btn = document.getElementById("del-btn");
    const param = new URLSearchParams(window.location.search);
    const id = param.get("id");

    btn.addEventListener("click", async () => {
        if (!id){
            console.error("No ID present in URL");
            return
        }
        const response = await fetch(`http://127.0.0.1:8000/listings/${id}`, {method:"DELETE"})
        
        if (!response.ok){
            console.log("Error while deleting the listing")
            alert("Error while deleting.");
            return;
        };

        alert("Listing Deleted!!")
        window.location.href = "/";
    });
};

deleteListing();