export async function loadLayout(pageContentId) {
    const layoutContainer = document.getElementById("layout");

    if (!layoutContainer) {
        console.error("Layout container not found");
        return;
    }

    const res = await fetch("/templates/layout.html");
    layoutContainer.innerHTML = await res.text();

    const contentSlot = document.querySelector("#content");
    const pageContent = document.getElementById(pageContentId);

    if (contentSlot && pageContent) {
        contentSlot.appendChild(pageContent);
        pageContent.style.display = "block";
    }

    renderAuthNav();
}

// ==================================================
// AUTH NAV RENDER
// ==================================================
async function renderAuthNav() {
    const authNav = document.getElementById("auth-nav");
    if (!authNav) return;

    const token = localStorage.getItem("access_token");

    authNav.innerHTML = "";

    if (!token) {
        authNav.innerHTML = `
            <a class="nav-link" href="/signup.html">Sign Up</a>
            <a class="nav-link" href="/login.html">Login</a>
        `;
        return;
    }

    try {
        const response = await fetch("/auth/me", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error("Auth failed");

        const user = await response.json();

        authNav.innerHTML = `
            <span class="nav-link fw-semibold">
                <i class="fa-solid fa-user"></i> ${user.username}
            </span>
            <button class="btn btn-sm btn-outline-dark ms-2" id="logout-btn">
                Logout
            </button>
        `;

        document.getElementById("logout-btn").addEventListener("click", () => {
            localStorage.removeItem("access_token");
            window.location.href = "/";
        });

    } catch (error) {
        console.error("Auth nav error:", error);
        localStorage.removeItem("access_token");

        authNav.innerHTML = `
            <a class="nav-link" href="/login.html">Login</a>
        `;
    }
}
