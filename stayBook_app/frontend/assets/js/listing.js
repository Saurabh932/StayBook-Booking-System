// ==================================================
// Autherization
// ==================================================
function getAuthHeader() {
    const token = localStorage.getItem("access_token");
    return token ? { "Authorization": `Bearer ${token}` } : {};
}



// ==================================================
// Listing Details + Reviews Loader
// ==================================================
async function listing_details(){
    const params = new URLSearchParams(window.location.search)
    const id = params.get("id")

    if (!id){
        console.error("Id not found")
        return;
    }

    try{
        const response = await fetch(`/listings/${id}`)

        
        if (!response.ok){
            throw new Error("Listing not found")
        }
        
        const details = await response.json()

        const h1 = document.getElementById("title")
        h1.textContent = details.title || "No title";

        const list_details = document.getElementById("list_details")
        list_details.innerHTML = `
                                <div class="col-6 offset-3 show-card">
                                    <div class="card listing-card">
                                        <img src="${details.image ?? ""}" class="card-img-top show-image" alt="listing_image">
                                        <div class="card-body">
                                            <br>
                                            ${details.description ?? "N/A"}
                                            <br>
                                            ${details.price ?? "N/A"}
                                            <br>
                                            ${details.location ?? "N/A"}
                                            <br>
                                            ${details.country ?? "N/A"}
                                            <br>
                                        </div>
                                    </div>
                                </div>
                            `;

        // ===============================
        // Render Reviews
        // ===============================
        renderReviews(details.reviews)

    }
    catch(error){
        console.error(error)
    }
}

listing_details()


// ===============================
// Render Reviews
// ===============================
function renderReviews(reviews){
    const reviewsDiv = document.getElementById("reviews")
    reviewsDiv.innerHTML = ""

    if (!reviews || reviews.length === 0){
        reviewsDiv.innerHTML = "<p>No reviews yet.</p>"
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement("div")
        reviewCard.className = "col-md-6 mb-3"

        reviewCard.innerHTML = `
                                <div class="card h-100">
                                    <div class="card-body">
                                        <small class="text-muted position-absolute top-0 end-0 m-2" style="font-size: 0.75rem;">
                                            ${new Date(review.created_at).toLocaleString()}
                                        </small>
                                        <h5 class="card-title"><b>UserName</b></h5>
                                        <p class="card-text mt-2">${review.comment}</p>
                                        <p class="card-text mt-2"><b>Rating:</b> ${review.rating} stars</p>
                                        <form>
                                            <button type="button" class="btn btn-sm btn-dark del-review-btn"data-review-id="${review.uid}">
                                                Delete
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            `

        reviewsDiv.appendChild(reviewCard)
    })
}


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
        const response = await fetch(`http://127.0.0.1:8000/listings/${id}`, {method:"DELETE",
                                                                            headers: {"Content-Type": "application/json",...getAuthHeader()}})
        
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


// ==================================================
// Review Form
// ==================================================
async function handleReviewForm(){
    const form = document.querySelector("form")
    if (!form) return;

    const param = new URLSearchParams(window.location.search)
    const id = param.get("id");

    if (!id) {
        console.error("Listing ID missing in URL");
        return;
    }

    form.addEventListener("submit", async (event) =>{
        event.preventDefault();

        const rating = document.getElementById("rating").value;
        const comment = document.getElementById("comment").value;

        const payload = {rating, comment}
        
        const response = await fetch(
                                    `/listings/${id}/reviews`,
                                    {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                            ...getAuthHeader()
                                        },
                                        body: JSON.stringify(payload)
                                    }
                                );


        
        if (!response.ok) {
            alert("Error Submitting review")
            return;
        }

        alert("Review submitted successfully")
        form.reset();

        await listing_details();
    });
}

handleReviewForm();


// ==================================================
// Review Delete button
// ==================================================
document.addEventListener("click", async (event)=>{
    if (!event.target.classList.contains("del-review-btn")) return;

    const reviewId = event.target.dataset.reviewId;
    const param = new URLSearchParams(window.location.search);
    const listingId = param.get("id");

    if (!reviewId || !listingId){
        console.log("Missing IDs.");
        return;
    }

    const confirmDelete = confirm("Delete this review?");
    if(!confirmDelete) return;

    const response = await fetch(`http://127.0.0.1:8000/listings/${listingId}/reviews/${reviewId}`, {method:"DELETE"});

    if(!response.ok){
        alert("Failed to delete review.");
        return;
    }

    alert("Review deleted");
    await listing_details()
})
