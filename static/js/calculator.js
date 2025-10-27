document.addEventListener('DOMContentLoaded', () => {
    const vehicleSelect = document.getElementById('vehicle-type');
    const partsContainer = document.getElementById('parts-container');
    const addPartBtn = document.getElementById('add-part');
    const totalEl = document.getElementById('total');
    const submitBtn = document.getElementById('submit-btn');

    function addPartRow() {
        const row = document.createElement('div');
        row.className = 'part-row';

        const select = document.createElement('select');
        select.className = 'custom-select part-select';
        select.innerHTML = '<option value="">-- Выберите часть кузова --</option>';

        for (const [zone, parts] of Object.entries(GROUPED_PARTS)) {
            const optgroup = document.createElement('optgroup');
            optgroup.label = zone;
            parts.forEach(name => {
                const opt = document.createElement('option');
                opt.value = name;
                opt.textContent = name;
                optgroup.appendChild(opt);
            });
            select.appendChild(optgroup);
        }

        const priceSpan = document.createElement('span');
        priceSpan.className = 'part-price';
        priceSpan.textContent = '0 ₽';

        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-part-btn';
        removeBtn.innerHTML = '&ndash;';
        removeBtn.addEventListener('click', () => {
            row.remove();
            calculate();
        });

        select.addEventListener('change', calculate);

        row.append(select, priceSpan, removeBtn);
        partsContainer.appendChild(row);
        calculate();
    }

    function calculate() {
        const vehicleOption = vehicleSelect.selectedOptions[0];
        const vehicleMult = vehicleOption ? parseFloat(vehicleOption.dataset.multiplier) : 1;

        const filmOption = document.querySelector('input[name="film"]:checked');
        const rawMult = filmOption ? filmOption.dataset.multiplier : '';
        const filmMult = rawMult ? parseFloat(rawMult.replace(',', '.')) || 1 : 1;

        let subtotal = 0;
        const rows = partsContainer.querySelectorAll('.part-row');

        rows.forEach(row => {
            const select = row.querySelector('.part-select');
            const priceSpan = row.querySelector('.part-price');
            const partName = select.value;

            if (partName && BASE_PRICES[partName] !== undefined) {
                const price = BASE_PRICES[partName] * vehicleMult;
                subtotal += price;
                priceSpan.textContent = Math.round(price).toLocaleString('ru-RU') + ' ₽';
            } else {
                priceSpan.textContent = '—';
            }
        });

        let total = subtotal * filmMult;

        document.querySelectorAll('.options-list input:checked').forEach(cb => {
            const parseNumber = (str) => {
                if (str == null || str === '' || str === 'null') return NaN;
                const normalized = str.toString().replace(',', '.');
                return parseFloat(normalized);
            };

            let fixed = parseNumber(cb.dataset.fixed);
            let percent = parseNumber(cb.dataset.percent);

            if (!isNaN(fixed)) {
                total += fixed;
            }
            else if (!isNaN(percent) && percent > 0) {
                total += total * percent;
            }
        });

        let discount = 0;
        for (const tier of DISCOUNT_TIERS) {
            if (total >= tier.min_amount && (tier.max_amount === null || total < tier.max_amount)) {
                discount = tier.discount_percent;
                break;
            }
        }
        total *= (1 - discount / 100);

        totalEl.textContent = Math.round(total).toLocaleString('ru-RU');
        submitBtn.disabled = rows.length === 0;
    }

    vehicleSelect.addEventListener('change', () => {
        if (vehicleSelect.value !== '') {
            addPartBtn.disabled = false;
        } else {
            addPartBtn.disabled = true;
        }
        calculate();
    });

    addPartBtn.addEventListener('click', addPartRow);

    document.querySelectorAll('input[name="film"]').forEach(r => r.addEventListener('change', calculate));
    document.querySelectorAll('.options-list input').forEach(cb => cb.addEventListener('change', calculate));


    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function showStep(stepId) {
        document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));
        document.getElementById(stepId).classList.add('active');
    }

    document.getElementById('submit-btn')?.addEventListener('click', (e) => {
        e.preventDefault();
        showStep('booking-form-step');
    });

    document.getElementById('back-to-calculator')?.addEventListener('click', () => {
        showStep('calculator-step');
    });

    document.getElementById('booking-form')?.addEventListener('submit', async (e) => {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        const vehicleId = document.getElementById('vehicle-type').value;
        const filmId = document.querySelector('input[name="film"]:checked')?.value;
        const total = parseFloat(document.getElementById('total').textContent.replace(/\s/g, '')) || 0;

        const selectedParts = [];
        document.querySelectorAll('.part-select').forEach(sel => {
            if (sel.value) selectedParts.push(sel.value);
        });

        const selectedOptions = [];
        document.querySelectorAll('.options-list input:checked').forEach(cb => {
            selectedOptions.push(cb.value);
        });

        const payload = {
            name: formData.get('name'),
            phone: formData.get('phone'),
            email: formData.get('email') || '',
            appointment_datetime: formData.get('appointment_datetime'),
            comment: formData.get('comment') || '',
            vehicle_type_id: vehicleId,
            film_type_id: filmId,
            selected_parts: selectedParts,
            selected_options: selectedOptions,
            total_price: total,
            discount_applied: 0,
            captcha_0: formData.get('captcha_0'),
            captcha_1: formData.get('captcha_1'),
        };

        try {
            const response = await fetch(SUBMIT_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorText = await response.text();
                if ('captcha' in errorText) {
                    alert('Капча введена не верно');
                } else {
                    alert('Ошибка сервера: ' + errorText);
                }
                return;
            }

            const result = await response.json();
            if (result.success) {
                showStep('success-step');
            } else {
                alert('Ошибка: ' + (result.error || 'Неизвестная ошибка'));
            }
        } catch (err) {
            alert('Не удалось отправить заявку. Проверьте соединение.');
        }
    });
});