import { setFlash } from "./script.js";


// ==================================================
// Authorization
// ==================================================
function getAuthHeader() {
    const token = localStorage.getItem("access_token");
    return token ? { "Authorization": `Bearer ${token}` } : {};
}


// ==================================================
// Current User Helper 
// ==================================================
function getCurrentUserId() {
    const token = localStorage.getItem("access_token");
    if (!token) return null;

    try {
        const base64 = token.split(".")[1];
        const payload = JSON.parse(atob(base64));
        return payload.sub || null;
    } catch {
        return null;
    }
}


const currentUserId = getCurrentUserId();


// ==================================================
// Listing Details + Reviews Loader
// ==================================================
async function listing_details() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (!id) {
        // console.error("Id not found");
        return;
    }

    try {
        const response = await fetch(`/listings/${id}`);

        if (!response.ok) {
            throw new Error("Listing not found");
        }

        const details = await response.json();

        const h1 = document.getElementById("title");
        h1.textContent = details.title || "No title";

        const list_details = document.getElementById("list_details");
        list_details.innerHTML = `
            <div class="col-6 offset-3 show-card">
                <div class="card listing-card">
                    <img src="${details.image ?? ""}" class="card-img-top show-image" alt="listing_image">
                    <div class="card-body">
                        <br>
                        <b>${details.description ?? "N/A"}<br>
                        Rs. ${details.price ?? "N/A"}<br></b>
                        ${details.location ?? "N/A"}<br>
                        ${details.country ?? "N/A"}<br>
                    </div>
                </div>
            </div>
        `;

        // ==================================================
        // Ownership Enforcement (Listing) ✅ NEW
        // ==================================================
        if (details.owner_id !== currentUserId) {
            const editBtn = document.getElementById("edit-btn");
            const delBtn = document.getElementById("del-btn");

            if (editBtn) editBtn.style.display = "none";
            if (delBtn) delBtn.style.display = "none";
        }

        renderReviews(details.reviews);

    } catch (error) {
        console.error(error);
    }
}

listing_details();


// ==================================================
// Star Renderer
// ==================================================
function renderStars(rating) {
    let stars = "";
    for (let i = 1; i <= 5; i++) {
        stars += i <= rating
            ? `<i class="bi bi-star-fill text-warning"></i>`
            : `<i class="bi bi-star text-warning"></i>`;
    }
    return stars;
}


// ==================================================
// Render Reviews
// ==================================================
function renderReviews(reviews) {
    const reviewsDiv = document.getElementById("reviews");
    reviewsDiv.innerHTML = "";

    if (!reviews || reviews.length === 0) {
        reviewsDiv.innerHTML = "<p>No reviews yet.</p>";
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement("div");
        reviewCard.className = "col-md-6 mb-3";

        reviewCard.innerHTML = `
            <div class="card h-100 review-card">
                <div class="card-body position-relative">
                    <small class="text-muted position-absolute top-0 end-0 m-2" style="font-size: 0.75rem;">
                        ${new Date(review.created_at).toLocaleString()}
                    </small>

                    <h5 class="card-title review-user"><b>User</b></h5>
                    <p class="card-text review-comment mt-2">${review.comment}</p>
                    <div class="mb-2 review-stars">${renderStars(review.rating)}</div>

                    ${
                        review.user_id === currentUserId
                            ? `<button
                                    type="button"
                                    class="btn btn-sm btn-dark del-review-btn"
                                    data-review-id="${review.uid}">
                                    Delete
                               </button>`
                            : ""
                    }
                </div>
            </div>
        `;

        reviewsDiv.appendChild(reviewCard);
    });
}


// ==================================================
// Edit Button
// ==================================================
function editListing() {
    const btn = document.getElementById("edit-btn");
    const param = new URLSearchParams(window.location.search);
    const id = param.get("id");

    btn.addEventListener("click", () => {
        if (!id) return;
        window.location.href = `/edit_listing.html?id=${id}`;
    });
}

editListing();


// ==================================================
// Delete Listing
// ==================================================
function deleteListing() {
    const btn = document.getElementById("del-btn");
    const param = new URLSearchParams(window.location.search);
    const id = param.get("id");

    btn.addEventListener("click", async () => {

    // ✅ AUTH GUARD
    if (!localStorage.getItem("access_token")) {
        setFlash("Please log in to delete listings.", "warning");
        window.location.href = "/login.html";
        return;
    }

    if (!id) return;

    const response = await fetch(`/listings/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            ...getAuthHeader()
        }
    });

    if (!response.ok) {
        setFlash("Error while deleting listing.", "danger");
        return;
    }

    setFlash("Listing deleted successfully.", "success");
    window.location.href = "/";
    });

}

deleteListing();


// ==================================================
// Review Form
// ==================================================
function handleReviewForm() {
    const form = document.getElementById("review-form");
    if (!form) return;

    const param = new URLSearchParams(window.location.search);
    const id = param.get("id");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // ✅ AUTH GUARD
        if (!localStorage.getItem("access_token")) {
            setFlash("Please log in to submit a review.", "warning");
            window.location.href = `/login.html?next=${encodeURIComponent(window.location.pathname + window.location.search)}`;
            return;
        }

        const payload = {
            rating: Number(document.getElementById("rating").value),
            comment: document.getElementById("comment").value
        };

        const response = await fetch(`/listings/${id}/reviews`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeader()
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            setFlash("Error submitting review.", "danger");
            return;
        }

        setFlash("Review submitted successfully.", "success");
        form.reset();
        await listing_details();
    });
}

handleReviewForm();



// ==================================================
// Review Delete Button
// ==================================================
document.addEventListener("click", async (event) => {
    if (!event.target.classList.contains("del-review-btn")) return;

    // ✅ AUTH GUARD
    if (!localStorage.getItem("access_token")) {
        setFlash("Please log in to manage reviews.", "warning");
        window.location.href = "/login.html";
        return;
    }

    const reviewId = event.target.dataset.reviewId;
    const param = new URLSearchParams(window.location.search);
    const listingId = param.get("id");

    if (!confirm("Delete this review?")) return;

    const response = await fetch(
        `/listings/${listingId}/reviews/${reviewId}`,
        {
            method: "DELETE",
            headers: {
                ...getAuthHeader()
            }
        }
    );

    if (!response.ok) {
        setFlash("Failed to delete review.", "danger");
        return;
    }

    setFlash("Review deleted.", "success");
    await listing_details();
});
