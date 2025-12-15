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

        // const h1 = document.getElementById("title")
        // h1.textContent = details.title || "No title";

        
        const list_details = document.getElementById("list_details")
        list_details.innerHTML = `
                            <div class="col-6 offset-3 show-card">
                                <div class="card">
                                    <img src="${details.image ?? ""}"  class="card-img-top show-image" alt="listing_image">
                                    <div class="card-body">
                                        <p class="card-text">
                                        <b>${details.title ?? "N/A"}</b>
                                        <br>
                                        ${details.description ?? "N/A"}
                                        <br>
                                        ${details.price ?? "N/A"}
                                        <br>
                                        ${details.location ?? "N/A"}
                                        <br>
                                        ${details.country ?? "N/A"}
                                        <br>
                                        </p>
                                    </div>
                                </div>
                            </div>
                                 
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