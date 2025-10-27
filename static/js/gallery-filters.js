document.addEventListener('DOMContentLoaded', () => {
    const makeFilter = document.getElementById('make-filter');
    const modelFilter = document.getElementById('model-filter');
    const workFilter = document.getElementById('work-filter');
    const beforeAfterToggle = document.getElementById('before-after-toggle');
    const galleryItems = document.querySelectorAll('.gallery-item');

    const makeOptions = ['all', ...MAKES.map(m => m.trim().toLowerCase())];
    makeFilter.innerHTML = '<option value="all">Все марки</option>';
    makeOptions.forEach(make => {
        if (make === 'all') return;
        const opt = document.createElement('option');
        opt.value = make;
        opt.textContent = make.charAt(0).toUpperCase() + make.slice(1);
        makeFilter.appendChild(opt);
    });

    makeFilter.addEventListener('change', () => {
        const selectedMake = makeFilter.value;
        modelFilter.innerHTML = '<option value="all">Все модели</option>';

        if (selectedMake && selectedMake !== 'all' && MODELS_BY_MAKE[selectedMake]) {
            modelFilter.disabled = false;
            MODELS_BY_MAKE[selectedMake].forEach(model => {
                const opt = document.createElement('option');
                opt.value = model;
                opt.textContent = model;

                modelFilter.appendChild(opt);
            });
        } else {
            modelFilter.disabled = true;
        }

        applyFilters();
    });

    const workOptions = ['all', ...WORK_TYPES];
    workFilter.innerHTML = '<option value="all">Все работы</option>';
    workOptions.forEach(type => {
        if (type === 'all') return;
        const opt = document.createElement('option');
        opt.value = type;
        if (type.toLowerCase() === "interior" ) {
                    opt.textContent = "Внутренний уход";
                } else if (type.toLowerCase() === "exterior") {
                    opt.textContent = "Внешний детейлинг"
                } else {
                    opt.textContent = "Индивидуальное решение"
                }
        workFilter.appendChild(opt);
    });

    function applyFilters() {
        const selectedMake = makeFilter.value;
        const selectedModel = modelFilter.value;
        const selectedWork = workFilter.value;
        const showOnlyBeforeAfter = beforeAfterToggle.checked;

        galleryItems.forEach(item => {
            const make = item.dataset.make?.toLowerCase() || '';
            const model = item.dataset.model || '';
            const workType = item.dataset.workType || '';
            const isBeforeAfter = item.dataset.beforeAfter === 'true';

            let show = true;

            if (selectedMake !== 'all' && make !== selectedMake) show = false;
            if (selectedModel !== 'all' && model !== selectedModel) show = false;
            if (selectedWork !== 'all' && workType !== selectedWork) show = false;
            if (showOnlyBeforeAfter && !isBeforeAfter) show = false;

            item.style.display = show ? 'block' : 'none';
        });
    }

    modelFilter.addEventListener('change', applyFilters);
    workFilter.addEventListener('change', applyFilters);
    beforeAfterToggle.addEventListener('change', applyFilters);

    applyFilters();
});