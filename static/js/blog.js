document.addEventListener('DOMContentLoaded', () => {
    const articlesList = document.getElementById('articles-list');
    const articleContents = document.querySelectorAll('.article-content');
    const readBtns = document.querySelectorAll('.read-article-btn');
    const backBtns = document.querySelectorAll('.back-to-list');

    readBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.article-card');
            const articleId = card.dataset.article;

            articlesList.style.display = 'none';

            document.getElementById(articleId).style.display = 'block';

            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });

    backBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            articleContents.forEach(article => {
                article.style.display = 'none';
            });

            articlesList.style.display = 'block';

            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
});
