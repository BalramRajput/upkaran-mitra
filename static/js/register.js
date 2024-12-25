function updateStates() {
    const countryId = document.getElementById('country').value;
    const stateSelect = document.getElementById('state');
    const options = stateSelect.querySelectorAll('option');
    options.forEach(option => {
        option.style.display = option.getAttribute('data-country') === countryId ? 'block' : 'none';
    });
    stateSelect.value = '';
    updateDistricts();
}

function updateDistricts() {
    const stateId = document.getElementById('state').value;
    const districtSelect = document.getElementById('district');
    const options = districtSelect.querySelectorAll('option');
    options.forEach(option => {
        option.style.display = option.getAttribute('data-state') === stateId ? 'block' : 'none';
    });
    districtSelect.value = '';
    updateSubDistricts();
}

function updateSubDistricts() {
    const districtId = document.getElementById('district').value;
    const subDistrictSelect = document.getElementById('subdistrict');
    const options = subDistrictSelect.querySelectorAll('option');
    options.forEach(option => {
        option.style.display = option.getAttribute('data-district') === districtId ? 'block' : 'none';
    });
    subDistrictSelect.value = '';
}

async function updateVillages() {
    const subDistrictId = document.getElementById('subdistrict').value;
    const villageSelect = document.getElementById('village');
    
    // Clear existing options
    villageSelect.innerHTML = '<option value="">Select Village</option>';

    if (subDistrictId) {
        try {
            const response = await fetch(`/villages/${subDistrictId}`);
            const villages = await response.json();

            villages.forEach(village => {
                const option = document.createElement('option');
                option.value = village.village_id;
                option.textContent = village.village_name;
                villageSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching villages:', error);
        }
    }
    villageSelect.value = '';
}