async function fetchBlogs() {
    try {
        const response = await fetch('http://127.0.0.1:8000/get_blogs');
        const data = await response.json();
        return data.blogs;
    } catch (error) {
        console.error('Error fetching blogs:', error);
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
            <img src="${blog.image_uri}" alt="Blog Image" class="img-fluid rounded" style="border-radius: 10px;">
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



async function displayBlogs() {
    const blogs = await fetchBlogs();
    const blogContainer = document.getElementById('blog-container');

    blogs.reverse();

    blogs.forEach(blog => {
        const blogSection = createBlogSection(blog);
        blogContainer.innerHTML += blogSection;
    });
}

async function fetchReactions(blog_id) {
    const like_button = document.getElementById(`like-button-${blog_id}`);
    const views = document.getElementById(`views-${blog_id}`);

    try {
        const response = await fetch('http://127.0.0.1:8000/get_reactions', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ blog_id })
        });
        const data = await response.json();

        like_button.innerText = `👍: ${data.likes}`;
        views.innerText = `👁️: ${data.views}`;

    } catch (error) {
        console.error('Error fetching reactions:', error);
    }
}

async function incrementViews(blog_id) {
    const views = document.getElementById(`views-${blog_id}`);
    const views_count = views.innerText.split(':')[1].trim();

    try {
        const response = await fetch('http://127.0.0.1:8000/increment_views', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ blog_id })
        });
        const data = await response.json();
        console.log(data);
        updateReactions(data, blog_id);
    } catch (error) {
        console.error(error);
    }
}

displayBlogs();