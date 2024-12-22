function searchEquipments() {
    const categoryId = document.getElementById('category').value;
    fetch(`/equipments/${categoryId}`)
        .then(response => response.json())
        .then(equipments => {

            const equipmentsDiv = document.getElementById('equipmentsDiv');
            const equipmentsTableBody = document.getElementById('equipmentsTableBody');
            const noEquipmentDiv = document.getElementById('noEquipmentsDiv');

            if(equipmentsTableBody !== null){
                equipmentsTableBody.innerHTML = ''; // Clear the table body
            }
            if (equipments.length > 0) {
                noEquipmentDiv.classList.add('hidden'); // Hide the no equipment message
                equipmentsDiv.classList.remove('hidden'); // Show the table
                equipments.forEach(equipment => {
                    const row = document.createElement('tr');

                    const imageCell = document.createElement('td');
                    const img = document.createElement('img');
                    img.src = `data:image/jpeg;base64,${equipment.image}`;
                    img.alt = equipment.name;
                    img.width = 100; // Set a width for the image
                    imageCell.appendChild(img);

                    const nameCell = document.createElement('td');
                    nameCell.textContent = equipment.name;

                    const rateCell = document.createElement('td');
                    rateCell.textContent = equipment.rate;

                    const unitCell = document.createElement('td');
                    unitCell.textContent = equipment.unit;

                    const specificationCell = document.createElement('td');
                    specificationCell.textContent = equipment.specification;

                    const ownerCell = document.createElement('td');
                    ownerCell.textContent = equipment.owner_name;

                    const villageCell = document.createElement('td');
                    villageCell.textContent = equipment.village;

                    const actionCell = document.createElement('td');
                    const bookButton = document.createElement('button');
                    bookButton.className = 'btn btn-primary';
                    bookButton.textContent = 'Book';
                    bookButton.dataset.equipment = JSON.stringify(equipment);

                    bookButton.onclick = () => {
                        const equipment = JSON.parse(bookButton.dataset.equipment);
                        document.getElementById('equipmentName').value = equipment.name;
                        document.getElementById('equipmentRate').value = equipment.rate;
                        document.getElementById('equipmentUnit').value = equipment.unit;
                        document.getElementById('equipmentSpecification').value = equipment.specification;
                        document.getElementById('ownerName').value = equipment.owner_name;
                        document.getElementById('equipmentVillage').value = equipment.village;
                        document.getElementById('ownerContact').value = equipment.owner_contact;
                        document.getElementById('rentalDuration').value = 1;
                        document.getElementById('totalAmount').textContent = `Total Amount: ${equipment.rate}`;

                        $('#bookingModal').modal('show');

                        document.getElementById('rentalDuration').oninput = () => {
                            const duration = document.getElementById('rentalDuration').value;
                            document.getElementById('totalAmount').textContent = `Total Amount: ${equipment.rate * duration}`;
                        };

                        document.getElementById('submitBooking').onclick = () => {
                            const duration = document.getElementById('rentalDuration').value;
                            const totalAmount = equipment.rate * duration;

                            fetch('/bookEquipment', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded'
                                },
                                body: `equipment_id=${equipment.id}&amount=${totalAmount}&duration=${duration}`
                            })
                            .then(response => response.text())
                            .then(data => {
                                window.location.href = '/myBookings';
                            })
                            .catch(error => console.error('Error:', error));
                        };
                    };
                    actionCell.appendChild(bookButton);
                    row.appendChild(nameCell);
                    row.appendChild(rateCell);
                    row.appendChild(unitCell);
                    row.appendChild(specificationCell);
                    row.appendChild(ownerCell);
                    row.appendChild(villageCell);
                    row.appendChild(imageCell);
                    row.appendChild(actionCell);

                    equipmentsTableBody.appendChild(row);
                });
            } else {
                equipmentsDiv.classList.add('hidden'); // Hide the table if no results
                noEquipmentDiv.classList.remove('hidden'); // Show the no equipment message
            }
        });
}