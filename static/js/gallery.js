document.addEventListener('DOMContentLoaded', () => {
    Fancybox.bind("[data-fancybox='gallery']", {});

    const makeFilter = document.getElementById('make-filter');
    const modelFilter = document.getElementById('model-filter');
    const workFilter = document.getElementById('work-filter');
    const beforeAfterToggle = document.getElementById('before-after-toggle');
    
    const galleryItems = document.querySelectorAll('.gallery-list-item');

    makeFilter.addEventListener('change', () => {
        const selectedMake = makeFilter.value;
        modelFilter.innerHTML = '<option value="all">Все модели</option>'; // Сброс

        if (selectedMake && carData[selectedMake]) {
            carData[selectedMake].forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model.charAt(0).toUpperCase() + model.slice(1);
                modelFilter.appendChild(option);
            });
            modelFilter.disabled = false;
        } else {
            modelFilter.disabled = true;
        }
        filterGallery();
    });

    modelFilter.addEventListener('change', filterGallery);
    workFilter.addEventListener('change', filterGallery);
    beforeAfterToggle.addEventListener('change', filterGallery);

    function filterGallery() {
        const selectedMake = makeFilter.value;
        const selectedModel = modelFilter.value;
        const selectedWork = workFilter.value;
        const showBeforeAfterOnly = beforeAfterToggle.checked;

        galleryItems.forEach(item => {
            const itemMake = item.dataset.make || 'all';
            const itemModel = item.dataset.model || 'all';
            const itemWork = item.dataset.work || 'all';
            const isBeforeAfter = item.dataset.beforeAfter === 'true';

            const makeMatch = selectedMake === 'all' || itemMake === selectedMake;
            const modelMatch = selectedModel === 'all' || itemModel === selectedModel;
            const workMatch = selectedWork === 'all' || itemWork === selectedWork;
            const beforeAfterMatch = !showBeforeAfterOnly || isBeforeAfter;

            if (makeMatch && modelMatch && workMatch && beforeAfterMatch) {
                item.style.display = 'grid';
            } else {
                item.style.display = 'none';
            }
        });
    }
});