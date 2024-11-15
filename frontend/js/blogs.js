const API_BASE_URL = 'https://api.devbutlazy.xyz'; 

async function fetchBlogs() {
    try {
        const response = await fetch(`${API_BASE_URL}/get_blogs`);
        const data = await response.json();
        return data.blogs;
    } catch (error) {
        console.error('Error fetching blogs:', error);
        return []; // Return an empty array if there's an error
    }
}

function createBlogSection(blog) {
    const sanitizedContent = DOMPurify.sanitize(blog.content, {
        ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'ul', 'li', 'ol', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'img', 'br'],
        ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'style', 'width', 'height']
    });

    let imageSection = '';
    if (blog.image_uri && blog.image_uri !== 'skip') {
        imageSection = `
        <div class="text-center" style="margin-top: 20px;">
            <img src="${blog.image_uri}" alt="Blog Image" class="img-fluid rounded" style="border-radius: 5px;">
        </div>`;
    }

    return `
    <section id="blog${blog.id}" class="shadow-blue white-bg padding">
        <h3 class="section-title" id="dark">${blog.title}</h3>
        <div class="spacer" data-height="40"></div>
        <div class="row">
            <div class="col-md-9">
                <h2 id="dark" class="mt-4 mt-md-0 mb-4"></h2>
                <p class="mb-0" style="white-space: pre-wrap;">${sanitizedContent}</p>
                <p class="text-muted" style="margin-top: 10px;">${blog.created_at}</p>
                ${imageSection}
            </div>
        </div>
    </section>
    `;
}

function createNoPostsSection(date) {
    return `
    <section class="shadow-blue white-bg padding">
        <h3 class="section-title" id="dark">No Posts Found</h3>
        <br>
        <p class="text-muted">As of ${date}</p>
    </section>
    `;
}

async function displayBlogs() {
    const blogs = await fetchBlogs();
    const blogContainer = document.getElementById('blog-container');

    if (blogs.length === 0) {
        const currentDate = new Date().toLocaleString(); // Get the current date and time
        const noPostsSection = createNoPostsSection(currentDate);
        blogContainer.innerHTML = noPostsSection;
    } else {
        blogs.reverse();
        blogs.forEach(blog => {
            const blogSection = createBlogSection(blog);
            blogContainer.innerHTML += blogSection;
        });
    }
}

displayBlogs().then(() => {
    console.log('Blogs displayed successfully');
});
